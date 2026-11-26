// Level 8: Toko Online Palsu (Sulit)
// HP flagship cuma Rp 499.000, ulasannya bagus semua.
// Materi Buku Panduan: toko, dom
const LEVEL_08 = {
  t: "Toko Online Palsu",
  lv: "Sulit",
  tz: "HP flagship cuma Rp 499.000, ulasannya bagus semua.",
  ed: ["toko", "dom"],
  vals: ["0812-5521-0001", "0877-1111-9090", 5, 1, 0],
  story: [
    ["Iklan", "HP flagship cuma Rp 499.000! Stok terbatas, transfer ke rekening toko sekarang."],
    ["Kamu", "Murah banget, ulasannya bagus semua lagi."],
    ["Sistem", "Peringatan: banyak laporan penipuan dari toko ini."],
  ],
  db: {
    "Ulasan Toko": T(
      ["No", "Pengulas", "Bintang", "Umur Akun", "Waktu"],
      [
        [1, "user_a1", 5, 0, "2026-10-21 10:01"],
        [2, "user_a2", 5, 0, "2026-10-21 10:01"],
        [3, "user_a3", 5, 0, "2026-10-21 10:02"],
        [4, "user_a4", 5, 0, "2026-10-21 10:02"],
        [5, "user_a5", 5, 0, "2026-10-21 10:02"],
        [6, "user_a6", 5, 0, "2026-10-21 10:03"],
        [7, "user_a7", 5, 0, "2026-10-21 10:03"],
        [8, "user_a8", 5, 0, "2026-10-21 10:03"],
        [9, "sari_m", 1, 420, "2026-10-22 09:15"],
        [10, "joko_w", 1, 380, "2026-10-22 11:40"],
      ]
    ),
    "Laporan Korban": T(
      ["No", "Platform", "Kerugian", "Rekening"],
      [
        [1, "WhatsApp", 499000, "0812-5521-0001"],
        [2, "Instagram", 499000, "0812-5521-0001"],
        [3, "Facebook", 998000, "0812-5521-0001"],
        [4, "WhatsApp", 499000, "0812-5521-0001"],
        [5, "Telegram", 499000, "0812-5521-0001"],
        [6, "WhatsApp", 250000, "0877-1111-9090"],
      ]
    ),
  },
  tk: [
    [
      "Hitung",
      "Berapa ulasan bintang 5 dari akun yang baru dibuat (umur 0 hari)?",
      /^8$/,
      "SELECT COUNT(*) FROM Ulasan Toko WHERE Bintang = 5 AND Umur Akun = 0",
    ],
    [
      "Selidiki",
      "Cek toko itu di Browser. Rekening tujuan atas nama siapa? Klik namanya.",
      /^Budi Prasetyo$/i,
      "Di Browser cari: hp murah gila.",
    ],
    [
      "Telusuri",
      "Berapa laporan korban yang memakai rekening 0812-5521-0001?",
      /^5$/,
      "SELECT * FROM Laporan Korban WHERE Rekening = '0812-5521-0001'",
    ],
  ],
  web: [
    [
      "hp-murah-gila.shop",
      "HP Murah Gila Shop",
      "hp murah gila shop toko diskon rekening",
      "<h3>hp-murah-gila.shop</h3><p>Terdaftar: 5 hari lalu</p><p>Pembayaran hanya ke rekening pribadi 0812-5521-0001 a.n. <u data-v='Budi Prasetyo'>Budi Prasetyo</u></p><p>Garansi: <u data-v='Garansi seumur hidup'>Garansi seumur hidup</u></p>",
    ],
  ],
  cul: ["PENIPU", "Pemilik toko palsu", "#ff7a6b", "gb"],
  end: "Toko palsu: ulasan bintang 5 muncul serentak dari akun baru, pembayaran ke rekening pribadi, dan 5 korban lain memakai rekening yang sama. Jangan transfer ke rekening pribadi dan cek umur domain.",
};
