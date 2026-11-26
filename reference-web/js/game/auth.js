// Layar masuk dan buat akun.

// Layar masuk
function loginScreen(reg) {
  document.title = "Masuk";
  show(
    '<div class="lgb">' +
      SHIELD +
      '<h1 class="lgt">DETEKTIF <mark>SIBER</mark></h1><p class="lead">' +
      (reg ? "Buat akun detektifmu" : "Masuk untuk melanjutkan penyelidikan") +
      '</p><div class="fl2"><label class="in"><span>👤</span><input id="un" placeholder="Username" autocomplete="username" maxlength="24" value="' +
      (reg ? "" : esc(S.n || "")) +
      '"></label><label class="in"><span>🔑</span><input id="pw" type="password" placeholder="Password" autocomplete="current-password"><button class="eye" id="ey" type="button" aria-label="Tampilkan sandi">👁</button></label><button class="nbtn big2" id="lgo">' +
      (reg ? "Daftar" : "Masuk") +
      '</button><p class="ft">' +
      (reg ? "Sudah punya akun? " : "Belum punya akun? ") +
      '<a href="#" id="alt">' +
      (reg ? "Masuk" : "Daftar") +
      '</a></p><small class="ft">Demo: nama dan sandi bebas. Progres tersimpan di perangkat ini.</small></div></div>',
    "🔐 Login.exe"
  );
  const go = () => {
    const n = $("#un").value.trim();
    if (!n) return toast("Isi username terlebih dahulu.", 1);
    if (S.n && n != S.n) {
      xp = 0;
      done = [];
      read = {};
      prog = [];
      qruns = 0;
      S.seen = 0;
    }
    S.n = n;
    S.r = 0;
    save();
    beep(660);
    ambient();
    toast("Selamat datang, " + n + ".");
    landing();
  };
  $("#lgo").onclick = go;
  $("#un").onkeydown = $("#pw").onkeydown = (e) => {
    if (e.key == "Enter") go();
  };
  $("#ey").onclick = () => {
    const p = $("#pw");
    p.type = p.type == "password" ? "text" : "password";
  };
  $("#alt").onclick = (e) => {
    e.preventDefault();
    signUpScreen();
  };
  if (S.lg == "en") tr(document.body, "en");
  $("#un").focus();
}

// Layar buat akun
function signUpScreen() {
  document.title = "Daftar";
  show(
    '<div class="sgn"><div class="wl"><h2>SELAMAT DATANG!</h2>' +
      SHIELD +
      '<h1 class="lgt">DETEKTIF <mark>SIBER</mark></h1><p class="lead">Buat akun detektifmu untuk memulai penyelidikan.</p></div><div class="fl2"><label class="in"><span>👤</span><input id="su" placeholder="Username" autocomplete="username" maxlength="24"></label><label class="in"><span>✉️</span><input id="se" type="email" placeholder="Email" autocomplete="email" maxlength="60"></label><label class="in"><span>🔑</span><input id="sp" type="password" placeholder="Password" autocomplete="new-password"><button class="eye" id="sey" type="button" aria-label="Tampilkan sandi">👁</button></label><button class="nbtn big2" id="sgo">Daftar</button><p class="ft">Sudah punya akun? <a href="#" id="sal">Masuk</a></p></div></div>',
    "📝 SignUp.exe"
  );
  const go = () => {
    const n = $("#su").value.trim(),
      m = $("#se").value.trim(),
      p = $("#sp").value;
    if (!n) return toast("Isi username terlebih dahulu.", 1);
    if (!/^\S+@\S+\.\S+$/.test(m)) return toast("Isi email yang valid.", 1);
    if (p.length < 4) return toast("Password minimal 4 karakter.", 1);
    if (S.n && n != S.n) {
      xp = 0;
      done = [];
      read = {};
      prog = [];
      qruns = 0;
      S.seen = 0;
    }
    S.n = n;
    S.r = 0;
    save();
    try {
      localStorage.setItem("ds-acc", JSON.stringify({ u: n, e: m }));
    } catch (e) {}
    beep(660);
    accountOK();
  };
  $("#sgo").onclick = go;
  $("#su").onkeydown =
    $("#se").onkeydown =
    $("#sp").onkeydown =
      (e) => {
        if (e.key == "Enter") go();
      };
  $("#sey").onclick = () => {
    const p = $("#sp");
    p.type = p.type == "password" ? "text" : "password";
  };
  $("#sal").onclick = (e) => {
    e.preventDefault();
    loginScreen();
  };
  if (S.lg == "en") tr(document.body, "en");
  $("#su").focus();
}

// Layar konfirmasi setelah akun dibuat
function accountOK() {
  document.title = "Akun dibuat";
  show(
    '<div class="al"><h2>SELAMAT KAMU BERHASIL MEMBUAT AKUN</h2>' +
      SHIELD +
      '<h1 class="lgt">DETEKTIF <mark>SIBER</mark></h1><p class="lead">Mengalihkan ke halaman masuk...</p></div>',
    "✅ Alert.exe"
  );
  if (S.lg == "en") tr(document.body, "en");
  setTimeout(() => {
    if (document.title == "Akun dibuat") {
      loginScreen();
      toast("Akun dibuat. Silakan masuk.");
    }
  }, 2600);
}
