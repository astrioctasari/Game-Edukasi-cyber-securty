// Level 5: WiFi Kafe Palsu (Sedang)
// WiFi gratis dengan nama mirip kafe.
// Materi Buku Panduan: sql, wifi, sql2
const LEVEL_05 = {
  t: "WiFi Kafe Palsu",
  lv: "Sedang",
  tz: "WiFi gratis dengan nama mirip kafe.",
  ed: ["sql", "wifi", "sql2"],
  vals: ["Terbuka", "WPA2", "KopiSenja%", "Luar Negeri", "Indonesia"],
  story: [
    ["Kamu", "Ada 3 WiFi di kafe: KopiSenja, KopiSenja_FREE, KopiSenja-Guest. Pilih yang mana ya?"],
    ["Barista", "WiFi kami KopiSenja, sandinya ada di struk."],
    ["Sistem", "Peringatan: ada jaringan di sekitar tanpa enkripsi."],
  ],
  db: {
    "Daftar WiFi": T(
      ["Nama", "Keamanan", "Sinyal", "Sandi"],
      [
        ["KopiSenja", "WPA2", 70, "Ya"],
        ["KopiSenja_FREE", "Terbuka", 95, "Tidak"],
        ["KopiSenja-Guest", "WPA2", 40, "Ya"],
        ["Warung Sebelah", "WPA2", 30, "Ya"],
        ["Free WiFi", "Terbuka", 88, "Tidak"],
      ]
    ),
    "Login Akun": T(
      ["No", "Akun", "Waktu", "Lokasi"],
      [
        [1, "ig_kamu", "2026-10-22 14:55", "Indonesia"],
        [2, "ig_kamu", "2026-10-22 15:20", "Luar Negeri"],
        [3, "email_kamu", "2026-10-22 15:22", "Luar Negeri"],
      ]
    ),
  },
  tk: [
    [
      "Hitung",
      "Ada berapa WiFi yang Keamanannya Terbuka?",
      /^2$/,
      "SELECT * FROM Daftar WiFi WHERE Keamanan = 'Terbuka'",
    ],
    [
      "Cari",
      "Dari WiFi terbuka itu, mana yang meniru nama kafe? Klik namanya.",
      /^KopiSenja_FREE$/i,
      "SELECT * FROM Daftar WiFi WHERE Keamanan = 'Terbuka' AND Nama LIKE 'KopiSenja%'",
    ],
    [
      "Telusuri",
      "Setelah itu akunmu dimasuki dari luar negeri? Klik akun yang kena paling dulu.",
      /^ig_kamu$/i,
      "SELECT * FROM Login Akun WHERE Lokasi <> 'Indonesia'. Lihat waktu paling awal.",
    ],
  ],
  web: [
    [
      "info.aman.id/wifi-publik",
      "Risiko WiFi Publik",
      "risiko wifi publik terbuka kafe",
      "<h3>Risiko WiFi Publik</h3><p>WiFi terbuka dapat dibuat penipu dengan nama mirip kafe. Datamu bisa disadap.</p>",
    ],
  ],
  cul: ["PENIPU", "Pemilik WiFi palsu", "#ffd95a", "g"],
  end: "KopiSenja_FREE adalah WiFi kembaran: terbuka, sinyal kuat, nama mirip. Setelah tersambung, akun Instagram dan emailmu dimasuki dari luar negeri.",
};
