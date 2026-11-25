// Profil pemain, avatar, dan pengaturan.

// XP per level pemain, rumus level, dan ikon kategori kasus
const STEP = 300,
  lvl = () => 1 + Math.floor(xp / STEP),
  IC = ["📝", "🎣", "🗄️"];

// Pilihan avatar, daftar pangkat, dan ikon lencana tiap level
const AVS = [
    ["#ff7a6b", "gc"],
    ["#8f9bff", "c"],
    ["#38bdf8", "g"],
    ["#ffd95a", "gb"],
  ],
  RANKS = ["Detective Trainee", "Junior Analyst", "Analyst", "Senior Analyst", "Chief Detective"],
  BIC = ["🗒️", "📦", "📞", "💬", "📶", "🔳", "📱", "🛒", "🎣", "📝", "🗄️"];

// Gambar avatar pemain
const avc = (i, z2, an) =>
  '<span class="avw an' +
  (an == null ? S.an || 0 : an) +
  '" style="width:' +
  z2 +
  "px;height:" +
  z2 +
  'px"><svg viewBox="-20 -34 40 40" aria-hidden="true"><rect x="-20" y="-34" width="40" height="40" fill="#20244a"/>' +
  BODY(AVS[i][0], AVS[i][1]) +
  "</svg></span>";

// Isi jendela Profil
function profilHTML() {
  const dn = done.filter(Boolean).length,
    pr = xp % STEP,
    r = RANKS[Math.min(4, Math.floor(dn / 2.5))];
  return (
    '<div class="prf"><div><div class="prh">' +
    avc(S.av || 0, 84) +
    "<div><h3>" +
    esc(S.n || "Detektif") +
    "</h3><span>" +
    r +
    "</span><br><b>Level " +
    lvl() +
    '</b></div></div><div class="pbar"><i style="width:' +
    (pr / STEP) * 100 +
    '%"></i></div><small class="mut">' +
    pr +
    " / " +
    STEP +
    " XP menuju level berikutnya</small><h4>Karakter</h4><div>" +
    AVS.map(
      (a, i) =>
        '<button class="pk' +
        ((S.av || 0) == i ? " on" : "") +
        '" data-av="' +
        i +
        '" aria-label="Karakter ' +
        (i + 1) +
        '">' +
        avc(i, 46, 3) +
        "</button>"
    ).join("") +
    "</div><h4>Lencana</h4><div>" +
    LV.map(
      (l, i) =>
        '<span class="bdgc' +
        (done[i] ? "" : " off") +
        '" title="' +
        esc(l.t) +
        '">' +
        BIC[i] +
        "</span>"
    ).join("") +
    '</div></div><div><div class="txp"><small>Total XP</small><div>★ ' +
    xp +
    '</div></div><p class="qt">Langkah kecil adalah bagian dari solusi besar.</p></div></div>'
  );
}

// Pasang aksi klik di jendela Profil
function wireProf() {
  const w = $("#w-profil");
  if (!w) return;
  w.addEventListener("click", (e) => {
    const a = e.target.closest("[data-av]"),
      b = e.target.closest("[data-an]");
    if (a) S.av = +a.dataset.av;
    else if (b) S.an = +b.dataset.an;
    else return;
    save();
    w.querySelector(".bd").innerHTML = profilHTML();
    if (S.lg == "en") tr(w, "en");
  });
}

// Tombol saklar untuk pengaturan
const sw = (k) =>
  '<button class="sw' +
  (S[k] ? " on" : "") +
  '" data-k="' +
  k +
  '" role="switch" aria-checked="' +
  (S[k] ? "true" : "false") +
  '" aria-label="' +
  k +
  '"></button>';

// Isi jendela Pengaturan
function setHTML() {
  return (
    '<p class="mut" style="margin:0 0 6px">Sesuaikan pengalaman bermain sesuai keinginanmu.</p><div class="stg"><span>Musik latar</span>' +
    sw("mu") +
    '</div><div class="stg"><span>Efek Suara</span>' +
    sw("sf") +
    '</div><div class="stg"><span>Notifikasi</span>' +
    sw("nt") +
    '</div><div class="stg"><span>Bahasa</span><span><button class="btn' +
    (S.lg != "en" ? "" : " g") +
    '" data-lg="id">Bahasa Indonesia</button> <button class="btn' +
    (S.lg == "en" ? "" : " g") +
    '" data-lg="en">English</button></span></div>' +
    (S.lg == "en"
      ? '<p class="mut sm">Antarmuka diterjemahkan. Isi kasus tetap berbahasa Indonesia.</p>'
      : "") +
    '<div class="row"><button class="btn g" id="rsp">Reset Progres</button><button class="btn g" id="out">Keluar</button></div>'
  );
}

// Pasang aksi di jendela Pengaturan
function wireSet() {
  const w = $("#w-set");
  if (!w) return;
  const re = () => {
    w.querySelector(".bd").innerHTML = setHTML();
    if (S.lg == "en") tr(w, "en");
  };
  w.addEventListener("click", (e) => {
    const t = e.target,
      k = t.closest("[data-k]"),
      lg = t.closest("[data-lg]");
    if (k) {
      S[k.dataset.k] = +!S[k.dataset.k];
      save();
      if (k.dataset.k == "mu") ambient();
      re();
    } else if (lg) {
      const was = S.lg;
      S.lg = lg.dataset.lg;
      save();
      re();
      if (S.lg != was) tr(document.body, S.lg);
    } else if (t.id == "rsp") {
      if (t.dataset.c) {
        xp = 0;
        done = [];
        read = {};
        prog = [];
        qruns = 0;
        save();
        const x = $("#xp"),
          r = $("#rk");
        if (x) x.textContent = 0;
        if (r) r.textContent = rank();
        const pw = $("#w-profil");
        if (pw) pw.querySelector(".bd").innerHTML = profilHTML();
        re();
        toast("Progres direset.", 1);
      } else {
        t.dataset.c = 1;
        t.textContent = "Yakin? Klik lagi";
        if (S.lg == "en") tr(t, "en");
        setTimeout(() => {
          if (t.isConnected) {
            delete t.dataset.c;
            t.textContent = "Reset Progres";
            if (S.lg == "en") tr(t, "en");
          }
        }, 3500);
      }
    } else if (t.id == "out") {
      S.r = 0;
      save();
      ambient();
      loginScreen();
    }
  });
}
