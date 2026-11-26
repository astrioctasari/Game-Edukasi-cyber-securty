// Peta emoji -> file ikon di img/icons/.
// Untuk mengganti ikon: timpa file-nya (SVG/PNG) dengan nama yang sama,
// atau ubah nama file di peta ini. Kalau file tidak ditemukan, emoji dipakai sebagai cadangan.
const ICON_DIR = "img/icons/";
const ICON_FILES = {
  "🕵️": "selamat-datang.svg",
  "📁": "kasus.svg",
  "📖": "buku-panduan.svg",
  "👤": "profil.svg",
  "⚙️": "pengaturan.svg",
  "🗂️": "berkas.svg",
  "📨": "pesan.svg",
  "📊": "tabel.svg",
  "⌨️": "terminal.svg",
  "🎥": "cctv.svg",
  "📌": "papan-bukti.svg",
  "🖼️": "foto-tkp.svg",
  "🌐": "browser.svg",
};
const ico = (e) =>
  ICON_FILES[e]
    ? '<img class="ico" src="' +
      ICON_DIR +
      ICON_FILES[e] +
      '" alt="" draggable="false" onerror="this.outerHTML=\'' +
      e +
      "'\">"
    : e;
