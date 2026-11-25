// Alur satu kasus: membuka meja kerja, memilih bukti, dan mengerjakan tugas.

// Buka meja kerja untuk level ke-i
function enter(i) {
  $("#scr").innerHTML = '<div class="desk" id="desk"></div>';
  desk = $("#desk");
  replay = !!done[i];
  cur = i;
  QT = [];
  const L = LV[i];
  DB = L.db;
  TK = L.tk;
  ti = 0;
  got = [];
  hint = false;
  pin = null;
  tb = Object.keys(DB)[0];
  rules = [{ c: 0, o: "=", v: "" }];
  sk = null;
  desk.className = "desk";
  document.title = "Level " + (i + 1) + ": " + L.t;
  const W = {
    kasus: [
      "🗂️",
      "Berkas",
      92,
      14,
      350,
      '<div id="tks"></div><div class="pin" id="pn">📌 Belum ada bukti. Klik sel di tabel.</div><div class="row"><button class="btn" id="go">Serahkan bukti</button><button class="btn g" id="hb">Petunjuk (−20 XP)</button></div><div class="msg" id="msg" role="status"></div>',
    ],
    pesan: [
      "📨",
      "Pesan",
      470,
      40,
      320,
      L.story.map((s) => '<div class="bub"><small>' + s[0] + "</small>" + s[1] + "</div>").join(""),
    ],
    tabel: [
      "📊",
      "Tabel",
      90,
      30,
      450,
      '<div class="row" style="margin:0 0 6px">' +
        Object.keys(DB)
          .map((k) => '<button class="btn g tt" data-t="' + k + '">' + k + "</button>")
          .join("") +
        '</div><b>Saring data</b> (kosongkan nilai untuk menampilkan semua)<div id="rl"></div><div class="row"><button class="btn g" id="ar">+ Syarat</button><button class="btn g" id="rs">Reset</button><span>Ditemukan <b id="cn"></b> baris</span><button class="btn" id="pc">📌 Pakai jumlah ini</button></div><div id="tv"></div>',
    ],
    term: ["⌨️", "Terminal", 100, 50, 500, TERMHTML],
    cctv: [
      "🎥",
      "CCTV",
      120,
      60,
      490,
      '<div class="cvw"><svg id="cv" class="scn cv" viewBox="0 0 600 340"></svg></div><div class="row"><button class="btn" id="cp">▶ Putar</button><input type="range" id="cs" min="0" max="' +
        (L.cc ? L.cc.dur : 0) +
        '" step="0.1" value="0" aria-label="Linimasa rekaman" style="flex:1;min-width:100px"><button class="btn g" id="cr">↺</button></div><div class="sclog" id="cl"></div>',
    ],
    papan: [
      "📌",
      "Papan Bukti",
      70,
      40,
      520,
      '<svg id="pb" class="scn" viewBox="0 0 600 340"></svg>',
    ],
    rek: [
      "🖼️",
      "Foto TKP",
      150,
      90,
      480,
      '<svg id="sv" class="scn" viewBox="0 0 600 340"></svg><div class="sclog" id="sl"></div>',
    ],
    web: [
      "🌐",
      "Browser",
      130,
      50,
      470,
      '<div class="row" style="margin:0"><input type="text" id="bq" placeholder="Cari di internet..."><button class="btn" id="bs">Cari</button><button class="btn g" id="bh">Beranda</button></div><div class="url" id="bu"></div><div class="bpg" id="bp"></div>',
    ],
    edu: ["📖", "Buku Panduan", 330, 90, 460, bookHTML(L.ed)],
    profil: ["👤", "Profil", 140, 50, 520, profilHTML()],
    set: ["⚙️", "Pengaturan", 190, 70, 470, setHTML()],
  };
  if (!L.cc) {
    delete W.cctv;
    delete W.rek;
  }
  if (i < 4) delete W.term;
  desk.className = "desk";
  desk.innerHTML =
    WALL +
    '<div class="icons" id="ics"></div><div class="icons2" id="ics2"></div><div class="bar"><span><button class="btn g" id="bk">← Desktop</button> <span id="st"></span></span><span id="tbw" class="tbw"></span><span><b id="xp"></b> XP · <span id="rk"></span></span></div>';
  mk(W, ["kasus", "pesan"]);
  $("#bk").onclick = home;
  const w = $("#w-tabel");
  w.addEventListener("input", (e) => {
    if (e.target.dataset.f == "v") {
      rules[+e.target.parentNode.dataset.i].v = e.target.value;
      view();
    }
  });
  w.addEventListener("change", (e) => {
    const f = e.target.dataset.f;
    if (f && f != "v") {
      const r = rules[+e.target.parentNode.dataset.i];
      r[f] = e.target.value;
      if (f == "c") r.v = "";
      ui();
    }
  });
  w.addEventListener("click", (e) => {
    const t = e.target;
    if (t.classList.contains("tt")) {
      tb = t.dataset.t;
      rules = [{ c: 0, o: "=", v: "" }];
      sk = null;
      ui();
    } else if (t.id == "ar") {
      if (rules.length < 3) {
        rules.push({ c: 0, o: "=", v: "" });
        ui();
      }
    } else if (t.id == "rs") {
      rules = [{ c: 0, o: "=", v: "" }];
      sk = null;
      ui();
    } else if (t.id == "pc") setPin(String(cnt), "jumlah baris");
    else if (t.tagName == "TD") setPin(t.dataset.v, tb);
    else if (t.tagName == "TH") {
      sd = sk == t.dataset.k ? -sd : 1;
      sk = t.dataset.k;
      view();
    }
  });
  wireEdu();
  wireProf();
  wireSet();
  wireWeb();
  if (i >= 4) wireTerm();
  $("#w-pesan").addEventListener("click", (e) => {
    const u = e.target.closest("[data-v]");
    if (u) setPin(u.dataset.v, "Pesan");
  });
  if (L.cc) {
    wireScene();
    wireCctv();
  }
  $("#go").onclick = () => {
    if (ti >= TK.length) return;
    if (pin === null)
      return errBox(
        "Belum ada bukti yang dipilih. Klik sel di Tabel, teks bergaris bawah di Browser, atau sosok di gambar."
      );
    if (TK[ti][2].test(pin)) {
      const nw = ti >= (prog[cur] || 0),
        l0 = lvl();
      if (nw) {
        xp += hint ? 80 : 100;
        prog[cur] = ti + 1;
      }
      got[ti] = pin;
      ti++;
      hint = false;
      pin = null;
      $("#pn").textContent = "Belum ada bukti. Klik sel di tabel.";
      if (ti >= TK.length) done[cur] = true;
      save();
      beep(780);
      tk();
      say("good", ti < TK.length ? "Tepat! Langkah berikutnya terbuka." : "Kasus selesai!");
      if (nw) toast("Bukti diterima. Total XP: " + xp);
      if (lvl() > l0) toast("Naik ke Level " + lvl() + "!");
    } else {
      beep(180);
      errBox(wrongMsg());
    }
  };
  $("#hb").onclick = () => {
    if (ti < TK.length) {
      hint = true;
      say("hint", TK[ti][3]);
    }
  };
  ui();
  tk();
}

// Asal bukti yang dipilih (Tabel, Browser, CCTV, dan lain-lain)
let psrc = "";

// Pesan yang menjelaskan kenapa bukti belum tepat
function wrongMsg() {
  const t = TK[ti],
    c = t[0] == "Hitung" || /^Berapa|Adakah/.test(t[1]),
    n = /^\d+$/.test(pin),
    p = '"' + pin + '"';
  if (c && !n)
    return (
      "Langkah ini meminta ANGKA jumlah, tapi yang kamu pilih " +
      p +
      " (dari " +
      psrc +
      ") bukan angka. Saring datanya dulu, lalu klik 📌 Pakai jumlah ini."
    );
  if (c)
    return (
      "Angka " +
      p +
      " belum tepat. Periksa lagi syarat saringannya (kolom, operator, nilai), lihat baris yang cocok, lalu hitung ulang."
    );
  if (n)
    return (
      "Langkah ini bukan meminta angka, tapi kamu memilih " +
      p +
      ". Klik nama, tulisan, atau sosok yang diminta di tugas."
    );
  return (
    "Belum tepat. Yang kamu pilih: " +
    p +
    " (dari " +
    psrc +
    "). Baca lagi tugas di Berkas, cek tabel, halaman, atau sosok yang disebut, atau tekan Petunjuk."
  );
}

// Pilih bukti
function setPin(v, s) {
  pin = v;
  psrc = s;
  $("#pn").innerHTML = "📌 Bukti dipilih: <b>" + esc(v) + "</b> <small>(" + esc(s) + ")</small>";
}

// Tampilkan pesan status di jendela Berkas
const say = (c, t) => {
  const m = $("#msg");
  m.className = "msg " + c;
  m.textContent = t;
};

// Gambar ulang jendela Berkas: langkah, progres, dan tombol lanjut
function tk() {
  $("#xp").textContent = xp;
  $("#rk").textContent = rank();
  $("#st").textContent =
    ti < TK.length ? "Langkah " + (ti + 1) + " dari " + TK.length : "Kasus selesai";
  $("#tks").innerHTML =
    "<b>Level " +
    (cur + 1) +
    ": " +
    LV[cur].t +
    "</b>" +
    TK.map(
      (t, i) =>
        '<div class="tk ' +
        (i < ti ? "ok" : i == ti ? "cur" : "") +
        '"><span class="tg">' +
        t[0] +
        "</span>" +
        (i <= ti ? t[1] : "Terkunci") +
        "</div>"
    ).join("") +
    (ti >= TK.length
      ? '<div class="tk ok"><b>' +
        LV[cur].end +
        '</b> Baca folder Edukasi untuk cara mencegahnya.</div><div class="row"><button class="btn g" id="bk2">← Desktop</button>' +
        (cur < LV.length - 1
          ? '<button class="btn" id="nl">Lanjut ke Level ' + (cur + 2) + " ▶</button>"
          : "") +
        "</div>"
      : "");
  const b = $("#bk2");
  if (b) b.onclick = home;
  const nl = $("#nl");
  if (nl) nl.onclick = () => learn(cur + 1, 0);
  const fin = ti >= TK.length;
  ["pn", "msg"].forEach((id) => {
    const e = $("#" + id);
    if (e) e.style.display = fin ? "none" : "";
  });
  const g = $("#go");
  if (g) g.parentNode.style.display = fin ? "none" : "";
  board();
}
