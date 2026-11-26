"""Automated test suite for Detektif Siber native desktop app & Supabase client."""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

import native_app
from supabase_client import SupabaseAuthError, SupabaseClient


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        app.setStyle("Fusion")
    return app


@pytest.fixture()
def game(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr(
        native_app.QStandardPaths,
        "writableLocation",
        lambda *_args, **_kwargs: str(tmp_path),
    )
    win = native_app.NativeGame()
    monkeypatch.setattr(win.supabase, "save_profile_async", lambda _state: None)
    win.resize(1120, 760)
    win.show()
    qapp.processEvents()
    yield win
    win.close()
    qapp.processEvents()


def _widget_texts(root) -> list[str]:
    texts: list[str] = []
    for lab in root.findChildren(QLabel):
        if lab.text():
            texts.append(lab.text())
    for btn in root.findChildren(QPushButton):
        if btn.text():
            texts.append(btn.text())
    return texts


def test_supabase_config_and_live_game_data():
    client = SupabaseClient.from_app_root(ROOT)
    assert client.enabled is True
    data = client.fetch_game_data()
    assert data is not None
    assert len(data["levels"]) == 11
    assert len(data["lessons"]) == 16
    assert "<svg" in data["wallpaper"]


def test_supabase_local_fallback_when_disabled():
    offline_client = SupabaseClient("", "")
    assert offline_client.enabled is False
    data = native_app.read_data(offline_client)
    assert len(data["levels"]) == 11
    assert len(data["lessons"]) == 16


def test_auth_and_otp_validation():
    client = SupabaseClient.from_app_root(ROOT)

    with pytest.raises(SupabaseAuthError):
        client.sign_up("", "user@example.com", "123456")
    with pytest.raises(SupabaseAuthError):
        client.sign_up("detektif_uji", "bukan-email", "123456")
    with pytest.raises(SupabaseAuthError):
        client.sign_up("detektif_uji", "user@example.com", "123")
    with pytest.raises(SupabaseAuthError):
        client.request_login_otp("email-salah")
    with pytest.raises(SupabaseAuthError):
        client.verify_login_otp("user@example.com", "")

    tok = client.verify_recovery_input(
        "user@example.com",
        "http://localhost:3000/#access_token=jwt_recovery_abc&type=recovery",
    )
    assert tok == "jwt_recovery_abc"


def test_login_otp_main_and_password_option(game, qapp):
    # Default show_login() MUST open in OTP mode as the main login method
    game.show_login("fathfahlevi@gmail.com")
    qapp.processEvents()
    scr = game.shell.desk.screen_win
    assert scr is not None and scr.screen_key == "login"
    texts_otp_step1 = " | ".join(_widget_texts(scr))
    assert "Kirim Kode OTP" in texts_otp_step1
    assert "Masuk dengan OTP" in texts_otp_step1

    # OTP Step 2 (code input screen)
    game.show_login("fathfahlevi@gmail.com", mode="otp", otp_sent=True)
    qapp.processEvents()
    scr2 = game.shell.desk.screen_win
    texts_otp_step2 = " | ".join(_widget_texts(scr2))
    assert "Verifikasi Kode OTP" in texts_otp_step2
    assert "Kirim Ulang OTP" in texts_otp_step2

    # Alternative Password mode
    game.show_login("fathfahlevi@gmail.com", mode="password")
    qapp.processEvents()
    scr_pw = game.shell.desk.screen_win
    texts_pw = " | ".join(_widget_texts(scr_pw))
    assert "Lupa password?" in texts_pw


def test_callback_listener_roundtrip():
    client = SupabaseClient.from_app_root(ROOT)
    if not client.callback_listener.start():
        pytest.skip("Port 3000 is already bound by another process")
    try:
        page = urllib.request.urlopen("http://127.0.0.1:3000/", timeout=3).read().decode("utf-8")
        assert "DETEKTIF" in page
        req = urllib.request.Request(
            "http://127.0.0.1:3000/__capture",
            data=json.dumps({"access_token": "tok_xyz", "type": "magiclink"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=3).read()
        captured = client.callback_listener.poll()
        assert captured is not None
        assert captured["access_token"] == "tok_xyz"
    finally:
        client.callback_listener.stop()


def test_profile_edit_and_in_profile_password_reset(game, qapp, monkeypatch):
    game.state["username"] = "agen_awal"
    game.state["email"] = "agen@kampus.ac.id"
    game.state["display_name"] = "Agen Awal"
    game.state["bio"] = "Selalu waspada di dunia siber."
    game.supabase.set_session("dummy_access_token", "dummy_refresh_token", "uid-1", "agen@kampus.ac.id")

    # Overview tab shows display_name, bio, Edit Profil, Reset Password, Export/Import Save
    overview = game.profile_panel("overview")
    qapp.processEvents()
    ov_texts = " | ".join(_widget_texts(overview))
    assert "Agen Awal" in ov_texts
    assert "Selalu waspada di dunia siber." in ov_texts
    assert "Edit Profil" in ov_texts
    assert "Reset Password" in ov_texts
    assert "Export Save" in ov_texts
    assert "Import Save" in ov_texts

    # Edit Profile tab & update_profile_details logic
    edit_view = game.profile_panel("edit")
    qapp.processEvents()
    ed_texts = " | ".join(_widget_texts(edit_view))
    assert "Edit Profil Detektif" in ed_texts
    assert "Simpan Profil" in ed_texts

    offline_sb = SupabaseClient("", "")
    updated = offline_sb.update_profile_details(
        old_username="agen_awal",
        new_username="agen_baru",
        display_name="Detektif Baru",
        bio="Jejak digital tak pernah bohong.",
        avatar=3,
        state=game.state,
    )
    assert updated == {
        "username": "agen_baru",
        "display_name": "Detektif Baru",
        "bio": "Jejak digital tak pernah bohong.",
        "avatar": 3,
    }

    # In-profile Password Reset / Change tab
    pw_view = game.profile_panel("password")
    qapp.processEvents()
    pw_texts = " | ".join(_widget_texts(pw_view))
    assert "Reset / Ubah Password" in pw_texts
    assert "Simpan Password Baru" in pw_texts
    assert "Kirim Reset ke Email" in pw_texts

    called = {}

    def fake_update_pw(token: str, new_pw: str) -> None:
        called["token"] = token
        called["new_pw"] = new_pw

    monkeypatch.setattr(game.supabase, "update_password", fake_update_pw)
    game.supabase.change_password_authenticated("sandiBaruAman99")
    assert called == {"token": "dummy_access_token", "new_pw": "sandiBaruAman99"}


def test_export_and_import_save_game(game, qapp, tmp_path):
    game.state["username"] = "detektif_save"
    game.state["email"] = "save@kampus.ac.id"
    game.state["display_name"] = "Sang Penyelidik"
    game.state["bio"] = "Bukti adalah segalanya."
    game.state["xp"] = 680
    game.state["avatar"] = 2
    game.state["query_runs"] = 7
    game.state["done"] = [True, True, False] + [False] * 8
    game.state["progress"] = [3, 3, 1] + [0] * 8
    game.state["read"] = {"sandi": 1, "phish": 1, "otp": 1}
    game.state["got"] = {"0": {"0": "2026-10-26 21:47", "1": "Sticky note", "2": "Pengelola sandi"}}

    game.open_desk()
    qapp.processEvents()

    save_file = tmp_path / "backup_detektif.json"
    assert game.export_save_game(save_file) is True
    assert save_file.exists()

    exported = json.loads(save_file.read_text(encoding="utf-8"))
    assert exported["app"] == "Detektif Siber"
    assert exported["profile"]["xp"] == 680

    # Wipe progress, verify reset, then import save file back
    game.reset_progress()
    assert game.state["xp"] == 0
    assert game.done_count() == 0

    assert game.import_save_game(save_file) is True
    qapp.processEvents()
    assert game.state["xp"] == 680
    assert game.state["avatar"] == 2
    assert game.state["query_runs"] == 7
    assert game.done_count() == 2
    assert game.state["progress"][2] == 1
    assert game.state["read"]["otp"] == 1
    assert game.state["got"]["0"]["1"] == "Sticky note"
    assert game.state["username"] == "detektif_save"

    # Reject corrupted / invalid JSON gracefully
    bad_file = tmp_path / "corrupt.json"
    bad_file.write_text('{"hello": "world"}', encoding="utf-8")
    assert game.import_save_game(bad_file) is False


def test_gameplay_flow_and_language_switch(game, qapp):
    game.state["username"] = "detektif_tester"
    game.state["email"] = "tester@kampus.ac.id"

    game.landing()
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "landing"

    game.open_desk()
    qapp.processEvents()
    desk = game.shell.desk
    assert desk.mode == "desk"
    assert set(desk.windows.keys()) == {"halo", "kasus", "edu", "profil", "set"}

    game.learn(0, 0)
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "learning"

    game.start_case(0)
    qapp.processEvents()
    assert game.in_case is True
    assert game.step == 0

    game.set_evidence("2026-10-26 21:47", "Login Kasir")
    game.submit_evidence()
    qapp.processEvents()
    assert game.step == 1
    assert game.state["xp"] >= 100

    game.set_language("en")
    qapp.processEvents()
    assert game.state["language"] == "en"
    assert game.step == 1
    game.set_language("id")
    qapp.processEvents()
    assert game.state["language"] == "id"

    game.start_case(8)
    qapp.processEvents()
    case_windows = set(game.shell.desk.windows.keys())
    assert {"kasus", "pesan", "tabel", "term", "cctv", "rek", "papan", "web"}.issubset(case_windows)

    game.logout()
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "login"
