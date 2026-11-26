"""Lightweight Supabase Auth & PostgREST client for Detektif Siber (stdlib only)."""

from __future__ import annotations

import http.server
import json
import logging
import os
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_LOG = logging.getLogger(__name__)
_TIMEOUT = 8.0
_CALLBACK_PORT = 3000
_REDIRECT_URL = f"http://localhost:{_CALLBACK_PORT}"


class SupabaseAuthError(Exception):
    """Human-friendly authentication error returned by Supabase Auth."""

    def __init__(self, message: str, code: str = "", status: int = 0):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status


def _friendly_auth_error(status: int, payload: dict | None, fallback: str) -> SupabaseAuthError:
    payload = payload or {}
    code = str(payload.get("error_code") or payload.get("error") or "").strip()
    raw_msg = str(
        payload.get("msg")
        or payload.get("error_description")
        or payload.get("message")
        or fallback
    ).strip()
    low = f"{code} {raw_msg}".lower()

    if "invalid_credentials" in low or "invalid login credentials" in low:
        msg = "Email atau password salah."
    elif "email_not_confirmed" in low or "email not confirmed" in low:
        msg = "Email belum diverifikasi. Silakan klik tautan verifikasi di emailmu terlebih dahulu."
    elif "user_already_exists" in low or "already registered" in low:
        msg = "Email ini sudah terdaftar. Silakan masuk atau gunakan fitur Lupa Password."
    elif "weak_password" in low or "at least 6 characters" in low:
        msg = "Password minimal 6 karakter."
    elif "same_password" in low or "different from the old password" in low:
        msg = "Password baru harus berbeda dari password lama."
    elif status == 429 or "rate_limit" in low or "security purposes" in low:
        msg = "Terlalu banyak permintaan email. Tunggu sekitar 1 menit lalu coba lagi."
    elif "otp_expired" in low or "expired" in low or "invalid" in low and "token" in low:
        msg = "Kode atau tautan pemulihan tidak valid atau sudah kedaluwarsa."
    elif "validation_failed" in low or "unable to validate email" in low:
        msg = "Format alamat email tidak valid."
    else:
        msg = raw_msg or fallback
    return SupabaseAuthError(msg, code=code, status=status)


_CALLBACK_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Detektif Siber — Verifikasi Akun</title>
<style>
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:#171a3a; font-family:'Segoe UI',Arial,sans-serif; color:#111; padding:16px; }
  .win { background:#f3f3f3; border:3px solid #111; box-shadow:6px 6px 0 #111;
         max-width:460px; width:100%; }
  .bar { background:#6cc4ff; border-bottom:3px solid #111; padding:7px 12px;
         font-weight:800; font-size:14px; }
  .body { padding:26px 24px 28px; text-align:center; }
  .brand { font-size:30px; font-weight:800; margin:8px 0 12px; }
  .brand span { background:#6cc4ff; padding:0 8px; }
  .card { background:#e4f2ff; border:3px solid #111; box-shadow:4px 4px 0 #111;
          padding:14px; margin-top:14px; font-size:14px; line-height:1.45; }
  .err { background:#ffe0dc; }
</style>
</head>
<body>
  <div class="win">
    <div class="bar">🕵️ DetektifSiber.exe — Autentikasi</div>
    <div class="body">
      <div class="brand">DETEKTIF <span>SIBER</span></div>
      <div id="status" class="card">Memproses verifikasi dari email...</div>
    </div>
  </div>
<script>
(function() {
  var hash = window.location.hash ? window.location.hash.substring(1) : "";
  var search = window.location.search ? window.location.search.substring(1) : "";
  var hp = new URLSearchParams(hash);
  var sp = new URLSearchParams(search);
  var data = {
    access_token: hp.get("access_token") || sp.get("access_token") || "",
    refresh_token: hp.get("refresh_token") || sp.get("refresh_token") || "",
    type: hp.get("type") || sp.get("type") || "",
    token_hash: sp.get("token_hash") || hp.get("token_hash") || "",
    token: sp.get("token") || hp.get("token") || "",
    error: hp.get("error") || sp.get("error") || "",
    error_description: hp.get("error_description") || sp.get("error_description") || ""
  };
  var box = document.getElementById("status");
  fetch("/__capture", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  }).then(function() {
    if (data.error || data.error_description) {
      box.className = "card err";
      box.innerHTML = "<b>⛔ Verifikasi Gagal</b><br>" + (data.error_description || data.error);
    } else if (data.type === "recovery") {
      box.innerHTML = "<b>✅ Tautan Reset Password Terverifikasi!</b><br>Silakan kembali ke jendela aplikasi <b>Detektif Siber</b> untuk menyimpan password barumu. Tab browser ini boleh ditutup.";
    } else {
      box.innerHTML = "<b>✅ Email Berhasil Diverifikasi!</b><br>Akun detektifmu sudah aktif. Silakan kembali ke aplikasi <b>Detektif Siber</b> untuk masuk.";
    }
  }).catch(function() {
    box.innerHTML = "Verifikasi selesai. Silakan kembali ke aplikasi Detektif Siber.";
  });
})();
</script>
</body>
</html>
"""


class AuthCallbackListener:
    """Temporary 127.0.0.1:3000 HTTP listener to capture Supabase email redirects."""

    def __init__(self, port: int = _CALLBACK_PORT):
        self.port = port
        self._server: http.server.ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._captured: dict | None = None
        self.available = False

    def start(self) -> bool:
        self.stop()
        with self._lock:
            self._captured = None
        parent = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format: str, *args) -> None:  # noqa: A002
                return

            def do_GET(self) -> None:  # noqa: N802
                body = _CALLBACK_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self) -> None:  # noqa: N802
                if self.path != "/__capture":
                    self.send_response(404)
                    self.end_headers()
                    return
                length = int(self.headers.get("Content-Length", "0") or 0)
                raw = self.rfile.read(min(length, 32768)).decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, dict):
                        with parent._lock:
                            parent._captured = parsed
                except ValueError:
                    pass
                out = b'{"ok":true}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)

        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", self.port), Handler)
            server.daemon_threads = True
            self._server = server
            self._thread = threading.Thread(target=server.serve_forever, daemon=True)
            self._thread.start()
            self.available = True
            return True
        except OSError as err:
            _LOG.info("Local callback port %s busy (%s); manual token input available.", self.port, err)
            self._server = None
            self._thread = None
            self.available = False
            return False

    def poll(self) -> dict | None:
        with self._lock:
            data = self._captured
            self._captured = None
            return data

    def stop(self) -> None:
        server = self._server
        self._server = None
        self.available = False
        if server is not None:
            threading.Thread(target=server.shutdown, daemon=True).start()
            try:
                server.server_close()
            except OSError:
                pass


class SupabaseClient:
    """Connects to Supabase Auth & PostgREST API with local-fallback safety."""

    def __init__(self, url: str = "", key: str = ""):
        self.url = url.rstrip("/")
        self.key = key
        self.access_token: str = ""
        self.refresh_token: str = ""
        self.user_id: str = ""
        self.user_email: str = ""
        self._lock = threading.Lock()
        self.callback_listener = AuthCallbackListener()

    @classmethod
    def from_app_root(cls, root: Path) -> "SupabaseClient":
        env_url = os.environ.get("SUPABASE_URL", "").strip()
        env_key = os.environ.get("SUPABASE_KEY", "").strip()
        if env_url and env_key:
            return cls(env_url, env_key)

        cfg_path = root / "data" / "supabase_config.json"
        if cfg_path.exists():
            try:
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
                return cls(
                    str(cfg.get("url", "")).strip(),
                    str(cfg.get("publishable_key", cfg.get("key", ""))).strip(),
                )
            except (OSError, ValueError) as err:
                _LOG.warning("Could not read supabase_config.json: %s", err)
        return cls()

    @property
    def enabled(self) -> bool:
        return bool(self.url and self.key)

    @property
    def redirect_url(self) -> str:
        return _REDIRECT_URL

    def set_session(self, access_token: str = "", refresh_token: str = "",
                    user_id: str = "", email: str = "") -> None:
        self.access_token = access_token or ""
        self.refresh_token = refresh_token or ""
        if user_id:
            self.user_id = user_id
        if email:
            self.user_email = email

    def clear_session(self) -> None:
        self.access_token = ""
        self.refresh_token = ""
        self.user_id = ""
        self.user_email = ""

    def _raw_request(
        self,
        method: str,
        path: str,
        payload: dict | list | None = None,
        bearer: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ):
        if not self.enabled:
            return None
        token = bearer if bearer is not None else (self.access_token or self.key)
        headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        body: bytes | None = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        if extra_headers:
            headers.update(extra_headers)
        req = urllib.request.Request(
            f"{self.url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw.strip() else None

    def _request(
        self,
        method: str,
        path: str,
        payload: dict | list | None = None,
        extra_headers: dict[str, str] | None = None,
    ):
        try:
            return self._raw_request(method, path, payload, None, extra_headers)
        except urllib.error.HTTPError as err:
            if err.code == 401 and self.access_token and self.refresh_token:
                if self.refresh_auth_session():
                    return self._raw_request(method, path, payload, None, extra_headers)
                # Fall back to publishable key for public tables
                return self._raw_request(method, path, payload, self.key, extra_headers)
            raise

    def _auth_request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        bearer: str | None = None,
        fallback_error: str = "Gagal menghubungi layanan autentikasi.",
    ) -> dict:
        if not self.enabled:
            raise SupabaseAuthError("Konfigurasi Supabase belum tersedia.")
        try:
            res = self._raw_request(method, path, payload, bearer=bearer or self.key)
            return res if isinstance(res, dict) else {}
        except urllib.error.HTTPError as err:
            err_payload = None
            try:
                raw = err.read().decode("utf-8", errors="replace")
                err_payload = json.loads(raw) if raw.strip() else None
            except ValueError:
                err_payload = None
            raise _friendly_auth_error(err.code, err_payload, fallback_error) from err
        except (urllib.error.URLError, TimeoutError) as err:
            raise SupabaseAuthError(
                "Tidak dapat terhubung ke server Supabase. Periksa koneksi internetmu."
            ) from err

    # -- Auth API -----------------------------------------------------------
    def username_exists(self, username: str) -> bool:
        clean = username.strip()
        if not self.enabled or not clean:
            return False
        try:
            encoded = urllib.parse.quote(clean.casefold(), safe="")
            rows = self._raw_request(
                "GET",
                f"/rest/v1/player_profiles?select=username&username_lower=eq.{encoded}&limit=1",
                bearer=self.key,
            )
            return isinstance(rows, list) and len(rows) > 0
        except (urllib.error.URLError, TimeoutError, ValueError):
            return False

    def sign_up(self, username: str, email: str, password: str) -> dict:
        clean_user = username.strip()
        clean_email = email.strip().lower()
        if not clean_user:
            raise SupabaseAuthError("Isi username terlebih dahulu.")
        if not clean_email or "@" not in clean_email or "." not in clean_email.split("@")[-1]:
            raise SupabaseAuthError("Isi alamat email yang valid.")
        if len(password) < 6:
            raise SupabaseAuthError("Password minimal 6 karakter.")

        if self.username_exists(clean_user):
            raise SupabaseAuthError("Username sudah digunakan detektif lain. Pilih username berbeda.")

        redirect_q = urllib.parse.quote(self.redirect_url, safe="")
        res = self._auth_request(
            "POST",
            f"/auth/v1/signup?redirect_to={redirect_q}",
            payload={
                "email": clean_email,
                "password": password,
                "data": {"username": clean_user},
            },
            fallback_error="Pendaftaran akun gagal.",
        )

        user_obj = res.get("user") if isinstance(res.get("user"), dict) else res
        identities = user_obj.get("identities") if isinstance(user_obj, dict) else None
        if isinstance(identities, list) and len(identities) == 0:
            raise SupabaseAuthError(
                "Email ini sudah terdaftar. Silakan masuk atau gunakan Lupa Password.",
                code="user_already_exists",
                status=400,
            )

        access_token = str(res.get("access_token") or "")
        refresh_token = str(res.get("refresh_token") or "")
        uid = str(user_obj.get("id") or "") if isinstance(user_obj, dict) else ""
        if access_token:
            self.set_session(access_token, refresh_token, uid, clean_email)

        # Initialize the detective's profile row in player_profiles
        self.save_profile({
            "username": clean_user,
            "xp": 0,
            "avatar": 0,
            "language": "id",
            "music": True,
            "sound": True,
            "seen": False,
            "query_runs": 0,
            "done": [],
            "progress": [],
            "read": {},
            "got": {},
        })

        return {
            "username": clean_user,
            "email": clean_email,
            "user_id": uid,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "needs_confirmation": not bool(access_token),
        }

    def sign_in(self, email: str, password: str) -> dict:
        clean_email = email.strip().lower()
        if not clean_email or "@" not in clean_email:
            raise SupabaseAuthError("Masukkan alamat email akunmu yang valid.")
        if not password:
            raise SupabaseAuthError("Masukkan password terlebih dahulu.")

        res = self._auth_request(
            "POST",
            "/auth/v1/token?grant_type=password",
            payload={"email": clean_email, "password": password},
            fallback_error="Gagal masuk ke akun.",
        )
        access_token = str(res.get("access_token") or "")
        refresh_token = str(res.get("refresh_token") or "")
        raw_user = res.get("user")
        user_obj: dict = raw_user if isinstance(raw_user, dict) else {}
        uid = str(user_obj.get("id") or "")
        raw_meta = user_obj.get("user_metadata")
        meta: dict = raw_meta if isinstance(raw_meta, dict) else {}
        username = str(meta.get("username") or "").strip()
        if not username:
            username = clean_email.split("@")[0][:24]

        self.set_session(access_token, refresh_token, uid, clean_email)
        profile = self.load_profile(username)
        return {
            "username": profile["username"] if profile else username,
            "email": clean_email,
            "user_id": uid,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "profile": profile,
        }

    def resend_confirmation(self, email: str) -> None:
        clean_email = email.strip().lower()
        if not clean_email or "@" not in clean_email:
            raise SupabaseAuthError("Masukkan alamat email yang valid.")
        self._auth_request(
            "POST",
            "/auth/v1/resend",
            payload={
                "type": "signup",
                "email": clean_email,
                "options": {"emailRedirectTo": self.redirect_url},
            },
            fallback_error="Gagal mengirim ulang email verifikasi.",
        )

    def request_password_reset(self, email: str) -> None:
        clean_email = email.strip().lower()
        if not clean_email or "@" not in clean_email or "." not in clean_email.split("@")[-1]:
            raise SupabaseAuthError("Masukkan alamat email yang valid.")
        redirect_q = urllib.parse.quote(self.redirect_url, safe="")
        self._auth_request(
            "POST",
            f"/auth/v1/recover?redirect_to={redirect_q}",
            payload={"email": clean_email},
            fallback_error="Gagal mengirim email reset password.",
        )

    def verify_recovery_input(self, email: str, raw_input: str) -> str:
        """Turn an OTP code, token_hash, or pasted recovery URL into an access_token."""
        text = raw_input.strip()
        clean_email = email.strip().lower()
        if not text:
            raise SupabaseAuthError(
                "Klik tautan di email terlebih dahulu, atau tempel kode OTP / tautan dari email."
            )

        # Case 1: Full URL or fragment pasted from email / browser
        if "://" in text or "access_token=" in text or "token=" in text or "token_hash=" in text:
            parsed = urllib.parse.urlparse(text)
            frag = urllib.parse.parse_qs(parsed.fragment)
            qs = urllib.parse.parse_qs(parsed.query)
            if "access_token" in frag and frag["access_token"]:
                return frag["access_token"][0]
            if "access_token" in qs and qs["access_token"]:
                return qs["access_token"][0]
            token_hash = (qs.get("token_hash") or frag.get("token_hash") or [""])[0]
            token = (qs.get("token") or frag.get("token") or [""])[0]
            candidate = token_hash or token
            if candidate:
                return self._verify_token_hash_or_otp(clean_email, candidate)

        # Case 2: Raw OTP code (e.g. 6-8 digits) or raw token_hash
        return self._verify_token_hash_or_otp(clean_email, text)

    def _verify_token_hash_or_otp(self, email: str, token_value: str) -> str:
        # Short numeric/code -> try OTP with email first, else token_hash first
        attempts: list[dict] = []
        if len(token_value) <= 10 and email:
            attempts.append({"type": "recovery", "email": email, "token": token_value})
            attempts.append({"type": "recovery", "token_hash": token_value})
        else:
            attempts.append({"type": "recovery", "token_hash": token_value})
            if email:
                attempts.append({"type": "recovery", "email": email, "token": token_value})

        last_err: SupabaseAuthError | None = None
        for body in attempts:
            try:
                res = self._auth_request(
                    "POST",
                    "/auth/v1/verify",
                    payload=body,
                    fallback_error="Kode atau tautan pemulihan tidak valid.",
                )
                access = str(res.get("access_token") or "")
                if access:
                    return access
            except SupabaseAuthError as err:
                last_err = err
        raise last_err or SupabaseAuthError("Kode atau tautan pemulihan tidak valid.")

    def update_password(self, access_token: str, new_password: str) -> None:
        if len(new_password) < 6:
            raise SupabaseAuthError("Password baru minimal 6 karakter.")
        if not access_token:
            raise SupabaseAuthError("Sesi pemulihan belum terverifikasi.")
        self._auth_request(
            "PUT",
            "/auth/v1/user",
            payload={"password": new_password},
            bearer=access_token,
            fallback_error="Gagal memperbarui password.",
        )

    def refresh_auth_session(self) -> bool:
        if not self.enabled or not self.refresh_token:
            return False
        try:
            res = self._raw_request(
                "POST",
                "/auth/v1/token?grant_type=refresh_token",
                payload={"refresh_token": self.refresh_token},
                bearer=self.key,
            )
            if isinstance(res, dict) and res.get("access_token"):
                self.access_token = str(res["access_token"])
                if res.get("refresh_token"):
                    self.refresh_token = str(res["refresh_token"])
                return True
        except (urllib.error.URLError, TimeoutError, ValueError):
            pass
        return False

    def sign_out(self) -> None:
        token = self.access_token
        self.clear_session()
        if not self.enabled or not token:
            return
        try:
            self._raw_request("POST", "/auth/v1/logout", bearer=token)
        except (urllib.error.URLError, TimeoutError, ValueError):
            pass

    # -- Game Content & Profile Data API ------------------------------------
    def fetch_game_data(self) -> dict | None:
        """Fetch lessons, levels, and wallpaper from Supabase."""
        if not self.enabled:
            return None
        try:
            lessons_rows = self._request(
                "GET",
                "/rest/v1/game_lessons?select=key,title,body,tip&order=sort_order.asc",
            )
            levels_rows = self._request(
                "GET",
                "/rest/v1/game_levels?select=*&order=level_index.asc",
            )
            config_rows = self._request(
                "GET",
                "/rest/v1/game_config?select=key,value&key=eq.wallpaper&limit=1",
            )
            if not isinstance(lessons_rows, list) or not isinstance(levels_rows, list):
                return None
            if not levels_rows or not lessons_rows:
                return None

            lessons = {
                row["key"]: [row.get("title", ""), row.get("body", ""), row.get("tip", "")]
                for row in lessons_rows
            }
            levels = []
            for row in levels_rows:
                lv = {
                    "t": row.get("title", ""),
                    "lv": row.get("difficulty", ""),
                    "tz": row.get("teaser", ""),
                    "ed": row.get("lesson_keys") or [],
                    "vals": row.get("terminal_vals") or [],
                    "story": row.get("story") or [],
                    "db": row.get("db_tables") or {},
                    "tk": row.get("tasks") or [],
                    "web": row.get("web_pages") or [],
                    "cul": row.get("culprit") or [],
                    "end": row.get("ending_text", ""),
                }
                if row.get("scene_data") is not None:
                    lv["sc"] = row["scene_data"]
                if row.get("cctv_data") is not None:
                    lv["cc"] = row["cctv_data"]
                levels.append(lv)

            wallpaper = ""
            if isinstance(config_rows, list) and config_rows:
                wallpaper = str(config_rows[0].get("value", ""))

            return {"levels": levels, "lessons": lessons, "wallpaper": wallpaper}
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as err:
            _LOG.warning("Falling back to local game_data.json: %s", err)
            return None

    def load_profile(self, username: str) -> dict | None:
        """Load a player profile by case-insensitive username."""
        clean = username.strip()
        if not self.enabled or not clean:
            return None
        try:
            encoded = urllib.parse.quote(clean.casefold(), safe="")
            rows = self._request(
                "GET",
                f"/rest/v1/player_profiles?username_lower=eq.{encoded}&limit=1",
            )
            if isinstance(rows, list) and rows:
                row = rows[0]
                return {
                    "username": row.get("username", clean),
                    "xp": int(row.get("xp", 0)),
                    "avatar": int(row.get("avatar", 0)),
                    "language": row.get("language", "id"),
                    "music": bool(row.get("music", True)),
                    "sound": bool(row.get("sound", True)),
                    "seen": bool(row.get("seen", False)),
                    "query_runs": int(row.get("query_runs", 0)),
                    "done": row.get("done") or [],
                    "progress": row.get("progress") or [],
                    "read": row.get("read_lessons") or {},
                    "got": row.get("got_evidence") or {},
                }
        except (urllib.error.URLError, TimeoutError, ValueError, TypeError) as err:
            _LOG.warning("Could not load profile from Supabase: %s", err)
        return None

    def save_profile(self, state: dict) -> bool:
        """Upsert the player's profile and progress into Supabase."""
        username = str(state.get("username", "")).strip()
        if not self.enabled or not username:
            return False
        payload = {
            "username": username,
            "xp": max(0, int(state.get("xp", 0))),
            "avatar": int(state.get("avatar", 0)),
            "language": "en" if state.get("language") == "en" else "id",
            "music": bool(state.get("music", True)),
            "sound": bool(state.get("sound", True)),
            "seen": bool(state.get("seen", False)),
            "query_runs": max(0, int(state.get("query_runs", 0))),
            "done": list(state.get("done") or []),
            "progress": list(state.get("progress") or []),
            "read_lessons": dict(state.get("read") or {}),
            "got_evidence": dict(state.get("got") or {}),
        }
        try:
            with self._lock:
                self._request(
                    "POST",
                    "/rest/v1/player_profiles?on_conflict=username_lower",
                    payload=payload,
                    extra_headers={
                        "Prefer": "resolution=merge-duplicates,return=minimal",
                    },
                )
            return True
        except (urllib.error.URLError, TimeoutError, ValueError, TypeError) as err:
            _LOG.warning("Could not sync profile to Supabase: %s", err)
            return False

    def save_profile_async(self, state: dict) -> None:
        """Sync profile in the background so UI interactions stay responsive."""
        snapshot = {
            "username": state.get("username", ""),
            "xp": state.get("xp", 0),
            "avatar": state.get("avatar", 0),
            "language": state.get("language", "id"),
            "music": state.get("music", True),
            "sound": state.get("sound", True),
            "seen": state.get("seen", False),
            "query_runs": state.get("query_runs", 0),
            "done": list(state.get("done") or []),
            "progress": list(state.get("progress") or []),
            "read": dict(state.get("read") or {}),
            "got": dict(state.get("got") or {}),
        }
        thread = threading.Thread(
            target=self.save_profile,
            args=(snapshot,),
            daemon=True,
        )
        thread.start()
