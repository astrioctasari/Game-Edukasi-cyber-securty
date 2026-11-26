// Level 6: QRIS Kedai Kopi (Sedang)
// Uang pelanggan masuk ke merchant yang tidak dikenal.
// Materi Buku Panduan: qris, sql2
const LEVEL_06 = {
  t: "QRIS Kedai Kopi",
  lv: "Sedang",
  tz: "Uang pelanggan masuk ke merchant yang tidak dikenal.",
  ed: ["qris", "sql2"],
  vals: ["Kedai Kopi Senja", "TOKO ABC99", "Meja 3"],
  story: [
    ["Mbak Sari (pemilik)", "Uang masuk ke rekening kok kurang ya? Padahal kedai ramai."],
    ["Kasir", "Ada stiker QRIS di meja 3, kayaknya baru ditempel."],
    ["Sistem", "Peringatan: beberapa transaksi masuk ke merchant tak dikenal."],
  ],
  db: {
    "Transaksi QRIS": T(
      ["No", "Meja", "Nominal", "Merchant", "Waktu"],
      [
        [1, "Meja 1", 25000, "Kedai Kopi Senja", "2026-10-22 10:05"],
        [2, "Meja 3", 40000, "TOKO ABC99", "2026-10-22 10:20"],
        [3, "Meja 2", 18000, "Kedai Kopi Senja", "2026-10-22 10:31"],
        [4, "Meja 3", 32000, "TOKO ABC99", "2026-10-22 11:02"],
        [5, "Meja 4", 27000, "Kedai Kopi Senja", "2026-10-22 11:15"],
        [6, "Meja 3", 55000, "TOKO ABC99", "2026-10-22 12:40"],
        [7, "Meja 5", 21000, "Kedai Kopi Senja", "2026-10-22 12:55"],
        [8, "Meja 3", 47000, "TOKO ABC99", "2026-10-22 13:20"],
      ]
    ),
  },
  tk: [
    [
      "Hitung",
      "Berapa transaksi yang masuk ke merchant selain Kedai Kopi Senja?",
      /^4$/,
      "SELECT COUNT(*) FROM Transaksi QRIS WHERE Merchant <> 'Kedai Kopi Senja'",
    ],
    [
      "Lacak",
      "Transaksi ke merchant asing berasal dari meja mana? Klik mejanya.",
      /^Meja 3$/i,
      "SELECT * FROM Transaksi QRIS WHERE Merchant = 'TOKO ABC99'. Lihat kolom Meja.",
    ],
    [
      "Selidiki",
      "Cari di Browser: apa yang diperiksa sebelum membayar QRIS? Klik jawabannya.",
      /^nama merchant$/i,
      "Di Browser cari: cara cek qris asli.",
    ],
  ],
  web: [
    [
      "info.aman.id/cek-qris",
      "Cara Cek QRIS Asli",
      "cek qris asli merchant bayar",
      "<h3>Cek QRIS Asli</h3><p>Sebelum bayar, periksa <u data-v='nama merchant'>nama merchant</u> yang muncul di layar. Jika berbeda dari kedai, jangan bayar.</p>",
    ],
  ],
  cul: ["PENIPU", "Penempel stiker", "#a9b3ff", "c"],
  end: "Ada stiker QRIS palsu yang ditempel di Meja 3. Empat pembayaran masuk ke rekening penipu. Periksa stiker QRIS secara berkala dan biasakan membaca nama merchant.",
};
