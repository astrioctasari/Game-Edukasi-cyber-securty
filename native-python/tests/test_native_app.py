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
from PySide6.QtWidgets import QApplication

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
    # Isolate local save_path and disable background network writes during UI tests
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


def test_auth_validation_and_recovery_parsing():
    client = SupabaseClient.from_app_root(ROOT)

    with pytest.raises(SupabaseAuthError):
        client.sign_up("", "user@example.com", "123456")

    with pytest.raises(SupabaseAuthError):
        client.sign_up("detektif_uji", "bukan-email", "123456")

    with pytest.raises(SupabaseAuthError):
        client.sign_up("detektif_uji", "user@example.com", "123")

    tok = client.verify_recovery_input(
        "user@example.com",
        "http://localhost:3000/#access_token=jwt_recovery_abc&type=recovery",
    )
    assert tok == "jwt_recovery_abc"


def test_callback_listener_roundtrip():
    client = SupabaseClient.from_app_root(ROOT)
    if not client.callback_listener.start():
        pytest.skip("Port 3000 is already bound by another process")
    try:
        page = urllib.request.urlopen("http://127.0.0.1:3000/", timeout=3).read().decode("utf-8")
        assert "DETEKTIF" in page
        req = urllib.request.Request(
            "http://127.0.0.1:3000/__capture",
            data=json.dumps({"access_token": "tok_xyz", "type": "recovery"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=3).read()
        captured = client.callback_listener.poll()
        assert captured is not None
        assert captured["access_token"] == "tok_xyz"
    finally:
        client.callback_listener.stop()


def test_auth_screens_render_cleanly(game, qapp):
    # 1. Login screen
    game.show_login("detektif@kampus.ac.id")
    qapp.processEvents()
    assert game.shell.desk is not None
    assert game.shell.desk.screen_win is not None
    assert game.shell.desk.screen_win.screen_key == "login"

    # 2. Sign Up screen
    game.show_signup()
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "signup"

    # 3. Account Created Alert screen
    game.show_account_created("detektif@kampus.ac.id", "detektif_satu", True)
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "alert"

    # 4. Reset Password (request & confirm modes)
    game.show_reset_password("detektif@kampus.ac.id", "request")
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "reset"

    game.show_reset_password("detektif@kampus.ac.id", "confirm", recovery_token="tok_123")
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "reset"


def test_gameplay_flow_and_language_switch(game, qapp):
    game.state["username"] = "detektif_tester"
    game.state["email"] = "tester@kampus.ac.id"

    # Landing -> Home desktop
    game.landing()
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "landing"

    game.open_desk()
    qapp.processEvents()
    desk = game.shell.desk
    assert desk.mode == "desk"
    assert set(desk.windows.keys()) == {"halo", "kasus", "edu", "profil", "set"}

    # Study phase -> Start Level 1
    game.learn(0, 0)
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "learning"

    game.start_case(0)
    qapp.processEvents()
    assert game.in_case is True
    assert game.step == 0

    # Submit correct evidence for step 1 of Level 1
    game.set_evidence("2026-10-26 21:47", "Login Kasir")
    game.submit_evidence()
    qapp.processEvents()
    assert game.step == 1
    assert game.state["xp"] >= 100

    # Switch language mid-case without losing progress
    game.set_language("en")
    qapp.processEvents()
    assert game.state["language"] == "en"
    assert game.step == 1
    game.set_language("id")
    qapp.processEvents()
    assert game.state["language"] == "id"

    # Start Level 9 (includes Terminal, CCTV, and Crime Scene Photo)
    game.start_case(8)
    qapp.processEvents()
    case_windows = set(game.shell.desk.windows.keys())
    assert {"kasus", "pesan", "tabel", "term", "cctv", "rek", "papan", "web"}.issubset(case_windows)

    # Logout returns to Login screen
    game.logout()
    qapp.processEvents()
    assert game.shell.desk.screen_win.screen_key == "login"
