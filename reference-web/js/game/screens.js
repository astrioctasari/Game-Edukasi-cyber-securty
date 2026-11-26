// Layar utama: halaman awal, materi sebelum kasus, dan daftar kasus.

// Logo perisai (SVG)
const SHIELD =
  '<svg class="sh" viewBox="0 0 60 70" aria-hidden="true"><path d="M30 4L54 12V34C54 52 42 62 30 67C18 62 6 52 6 34V12Z" fill="#fff" stroke="#111" stroke-width="5"/><path d="M30 4V67C18 62 6 52 6 34V12Z" fill="#111"/></svg>';

// Halaman awal
function landing() {
  show(
    '<div class="lnd"><span class="bdg">🎮 GAME EDUKASI • KEAMANAN SIBER</span>' +
      SHIELD +
      '<h1 class="big">DETEKTIF <mark>SIBER</mark></h1><p class="lead">Selidiki kejahatan digital lewat kasus seru, tanpa koding dan tanpa risiko nyata.</p><div class="feat">' +
      [
        [
          "🎯",
          "Kenali modus kejahatan",
          "Pelajari phishing, tebak sandi, dan kebocoran data lewat kasus nyata.",
        ],
        [
          "🕵️",
          "Selidiki seperti detektif",
          "Periksa tabel, browser, CCTV, dan papan bukti untuk menemukan pelaku.",
        ],
        [
          "🏆",
          "Dapatkan EXP dan naik level",
          "Setiap bukti yang tepat memberi EXP. Makin teliti, makin tinggi levelmu.",
        ],
      ]
        .map((f) => "<div><i>" + f[0] + "</i><span><b>" + f[1] + "</b>" + f[2] + "</span></div>")
        .join("") +
      '</div><small class="cap">CARA BERMAIN</small><div class="flow">' +
      [
        ["📁", "Pilih Kasus"],
        ["🎓", "Belajar"],
        ["🔎", "Selidiki"],
        ["🏆", "Tuntaskan"],
      ]
        .map((f, i) => (i ? "<em>→</em>" : "") + "<div><i>" + f[0] + "</i>" + f[1] + "</div>")
        .join("") +
      '</div><div class="nb gr rules"><b>Tata cara bermain</b><p>1. Di meja detektif, buka folder <b>Kasus</b> lalu pilih level.</p><p>2. Baca materi edukasi singkat sebelum kasus dimulai.</p><p>3. Selidiki lewat Tabel, Browser, CCTV, dan Foto, lalu klik bukti yang kamu temukan.</p><p>4. Tiap bukti yang tepat memberi EXP. Kasus tuntas membuka level berikutnya.</p></div><button class="nbtn big2" id="st">🕵️ BUKA MEJA DETEKTIF</button><small class="ft">Semua skenario fiktif: belajar aman tanpa risiko nyata</small></div>',
    "🕵️ DetektifSiber.exe"
  );
  $("#st").onclick = () => {
    S.seen = 1;
    save();
    home();
  };
}

// Layar materi sebelum kasus dimulai, satu bab per halaman
function learn(i, j) {
  const l = LV[i],
    ks = l.ed,
    k = ks[j],
    v = ED[k],
    em = v[0].split(" ")[0],
    last = j == ks.length - 1;
  if (!read[k]) {
    read[k] = 1;
    xp += 10;
    save();
    toast("+10 XP: materi dibaca");
  }
  show(
    '<div class="hd c"><h2>📖 Fase Belajar</h2><p>Level ' +
      (i + 1) +
      " • " +
      l.t +
      '. Baca materi singkat ini sebelum menyelidiki.</p><div class="dots">' +
      ks.map((_, x) => '<b class="' + (x == j ? "on" : "") + '"></b>').join("") +
      "<small>Materi " +
      (j + 1) +
      "/" +
      ks.length +
      '</small></div></div><div class="sl"><div class="ic2">' +
      em +
      "</div><h3>" +
      v[0].slice(em.length + 1) +
      '</h3><div class="nb">' +
      v[1] +
      '</div><div class="nb cr"><i>💡 ' +
      v[2] +
      "</i></div>" +
      (last
        ? '<div class="nb gr"><p><b>📨 Pesan masuk</b></p><p>' +
          l.story[0][0] +
          ": " +
          l.story[0][1] +
          "</p></div>"
        : "") +
      '</div><div class="nav"><button class="nbtn w" id="pv">◂ ' +
      (j ? "Sebelumnya" : "Kembali") +
      "</button>" +
      (done[i] && !last ? '<button class="nbtn w" id="sk">Lewati ▸▸</button>' : "") +
      '<button class="nbtn" id="nx2">' +
      (last ? "🔎 Mulai Penyelidikan ▸" : "Selanjutnya ▸") +
      "</button></div>",
    "📖 FaseBelajar.exe"
  );
  $("#pv").onclick = () => (j ? learn(i, j - 1) : home());
  const sk = $("#sk");
  if (sk) sk.onclick = () => enter(i);
  $("#nx2").onclick = () => (last ? enter(i) : learn(i, j + 1));
}

// Meja utama: daftar kasus, Buku Panduan, Profil, dan Pengaturan
function home() {
  cancelAnimationFrame(raf);
  $("#scr").innerHTML = '<div class="desk" id="desk"></div>';
  desk = $("#desk");
  document.title = "Detektif Siber";
  desk.className = "desk";
  const AC = ["#38bdf8", "#ffb08a", "#a9b3ff"];
  desk.innerHTML =
    WALL +
    '<div class="icons" id="ics"></div><div class="wp">DETEKTIF SIBER<small>DIVISI KEJAHATAN DIGITAL</small></div><div class="bar"><span><button class="btn g" id="bk0">← Layar Awal</button> Kasus selesai: ' +
    done.filter(Boolean).length +
    "/" +
    LV.length +
    '</span><span id="tbw" class="tbw"></span><span><b id="xp">' +
    xp +
    '</b> XP · <span id="rk">' +
    rank() +
    "</span></span></div>";
  mk(
    {
      halo: [
        "🕵️",
        "Selamat Datang",
        96,
        40,
        340,
        '<p style="margin:0 0 8px"><b>Detektif Siber</b>: selidiki kejahatan digital tanpa koding.</p><p style="margin:0">1. Buka ikon <b>📁 Kasus</b> (di kiri, atau di bawah pada HP).<br>2. Pilih level dan baca edukasinya.<br>3. Cari bukti di Tabel dan Browser.</p>',
      ],
      kasus: [
        "📁",
        "Kasus",
        110,
        90,
        520,
        '<div class="lvs">' +
          LV.map((l, i) => {
            const lk = i > 0 && !done[i - 1];
            return (
              '<button class="lvi" style="--a:' +
              AC[l.lv == "Mudah" ? 0 : l.lv == "Sedang" ? 1 : 2] +
              '" data-i="' +
              i +
              '"' +
              (lk ? " disabled" : "") +
              "><i>" +
              (lk ? "🔒" : done[i] ? "✔" : i + 1) +
              "</i><b>Level " +
              (i + 1) +
              "</b><small>" +
              l.t +
              "<br><b>" +
              l.lv +
              "</b></small></button>"
            );
          }).join("") +
          "</div>",
      ],
      edu: ["📖", "Buku Panduan", 160, 260, 460, bookHTML(Object.keys(ED))],
      profil: ["👤", "Profil", 140, 50, 520, profilHTML()],
      set: ["⚙️", "Pengaturan", 190, 70, 470, setHTML()],
    },
    ["halo"]
  );
  $("#w-kasus").addEventListener("click", (e) => {
    const b = e.target.closest(".lvi");
    if (b && !b.disabled) learn(+b.dataset.i, 0);
  });
  wireEdu();
  wireProf();
  wireSet();
  $("#bk0").onclick = landing;
  if (S.lg == "en") tr(document.body, "en");
}
