// Status game dan penyimpanan progres di browser.

// Semua status yang berubah selama bermain: XP, kasus selesai, langkah, bukti, dan pengaturan (S)
let replay = false,
  xp = 0,
  done = [],
  cur = 0,
  DB,
  TK,
  ti,
  hint,
  pin,
  got = [],
  tb,
  rules,
  sk,
  sd,
  cnt,
  read = {},
  z = 5,
  prog = [],
  qruns = 0,
  S = { n: "", r: 0, av: 0, an: 0, th: "light", mu: 0, sf: 1, nt: 1, lg: "id", seen: 0 };

// Meja kerja (area jendela) yang sedang tampil
let desk;

// Nama kunci penyimpanan di localStorage
const SKEY = "ds-v2";

// Baca progres yang tersimpan
function load() {
  try {
    const j = JSON.parse(localStorage.getItem(SKEY) || "null");
    if (j) {
      Object.assign(S, j.S || {});
      xp = j.xp || 0;
      done = j.done || [];
      read = j.read || {};
      prog = j.prog || [];
      qruns = j.q || 0;
      if (j.v != 2) {
        done.unshift(null);
        prog.unshift(0);
      }
    }
  } catch (e) {}
}

// Simpan progres
function save() {
  try {
    localStorage.setItem(SKEY, JSON.stringify({ S, xp, done, read, prog, q: qruns, v: 2 }));
  } catch (e) {}
}

// Gelar detektif berdasarkan XP
const rank = () => (xp >= 2500 ? "Detektif Senior" : xp >= 1000 ? "Detektif" : "Magang");
