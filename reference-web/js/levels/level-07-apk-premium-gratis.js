// Level 7: APK Premium Gratis (Sedang)
// Aplikasi musik premium gratis dari grup chat.
// Materi Buku Panduan: apk, mfa
const LEVEL_07 = {
  t: "APK Premium Gratis",
  lv: "Sedang",
  tz: "Aplikasi musik premium gratis dari grup chat.",
  ed: ["apk", "mfa"],
  vals: ["MusikPro", "PemutarResmi", "Tidak", "Ya", "Akses SMS"],
  story: [
    ["Grup Telegram", "Unduh MusikPro Premium GRATIS (APK): musikpro-apk.xyz"],
    ["Kamu", "Wah mau coba. Tapi ini bukan dari toko aplikasi ya?"],
    ["Sistem", "Aplikasi tidak dikenal meminta banyak izin."],
  ],
  db: {
    "Izin Aplikasi": T(
      ["Aplikasi", "Izin", "Wajar"],
      [
        ["MusikPro", "Akses SMS", "Tidak"],
        ["MusikPro", "Baca Kontak", "Tidak"],
        ["MusikPro", "Aksesibilitas", "Tidak"],
        ["MusikPro", "Tampil di atas aplikasi lain", "Tidak"],
        ["MusikPro", "Mikrofon", "Tidak"],
        ["MusikPro", "Penyimpanan", "Ya"],
        ["MusikPro", "Internet", "Ya"],
        ["PemutarResmi", "Penyimpanan", "Ya"],
        ["PemutarResmi", "Internet", "Ya"],
      ]
    ),
  },
  tk: [
    [
      "Hitung",
      "Berapa izin MusikPro yang tidak wajar untuk pemutar musik?",
      /^5$/,
      "SELECT * FROM Izin Aplikasi WHERE Aplikasi = 'MusikPro' AND Wajar = 'Tidak'",
    ],
    [
      "Cari",
      "Izin mana yang bisa membaca kode OTP di SMS-mu? Klik izinnya.",
      /^Akses SMS$/i,
      "Cari izin yang berhubungan dengan SMS.",
    ],
    [
      "Selidiki",
      "Cari di Browser: dari mana aplikasi sebaiknya diunduh? Klik jawabannya.",
      /^toko aplikasi resmi$/i,
      "Di Browser cari: keamanan aplikasi apk.",
    ],
  ],
  web: [
    [
      "info.aman.id/apk",
      "Keamanan Aplikasi (APK)",
      "keamanan aplikasi apk unduh",
      "<h3>Keamanan Aplikasi</h3><p>Unduh hanya dari <u data-v='toko aplikasi resmi'>toko aplikasi resmi</u>. Hindari file APK dari tautan atau grup.</p>",
    ],
  ],
  cul: ["PENIPU", "Pembuat APK", "#38bdf8", "b"],
  end: "APK premium gratis adalah aplikasi jebakan: meminta akses SMS dan aksesibilitas untuk mencuri OTP dan mengendalikan HP. Unduh hanya dari toko resmi.",
};
