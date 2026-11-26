// Level 4: Link WA dari Teman (Mudah)
// Teman tiba-tiba kirim link kuota gratis.
// Materi Buku Panduan: mfa, phish
const LEVEL_04 = {
  t: "Link WA dari Teman",
  lv: "Mudah",
  tz: "Teman tiba-tiba kirim link kuota gratis.",
  ed: ["mfa", "phish"],
  vals: ["Perangkat Baru", "HP Dinda", "Dinda"],
  story: [
    ["Dinda (teman)", "Gaes klik link ini, kuota 50GB gratis! kuota-gratis-wa.xyz/dapat"],
    ["Kamu", "Kok tumben Dinda kirim begini jam 2 pagi?"],
    ["Dinda (telepon)", "Aku nggak kirim apa-apa! HP-ku mungkin dibobol."],
  ],
  db: {
    "Riwayat Grup WA": T(
      ["No", "Pengirim", "Pesan", "Waktu", "Perangkat"],
      [
        [1, "Dinda", "Besok kumpul jam 10 ya", "2026-10-21 18:30", "HP Dinda"],
        [2, "Rani", "Oke siap", "2026-10-21 18:32", "HP Rani"],
        [3, "Dinda", "Makasih ya semua", "2026-10-21 20:05", "HP Dinda"],
        [
          4,
          "Dinda",
          "Gaes klik, kuota 50GB gratis! kuota-gratis-wa.xyz/dapat",
          "2026-10-22 02:14",
          "Perangkat Baru",
        ],
        [5, "Dinda", "Cepet klik sebelum habis", "2026-10-22 02:15", "Perangkat Baru"],
      ]
    ),
  },
  tk: [
    [
      "Cari",
      "Link tadi dikirim dari perangkat apa? Klik nama perangkatnya.",
      /^Perangkat Baru$/i,
      "Di Tabel saring: Pengirim sama dengan Dinda, lalu Perangkat bukan HP Dinda.",
    ],
    [
      "Selidiki",
      "Buka link itu di Browser. Apa yang diminta halaman itu? Klik permintaannya.",
      /^kode verifikasi 6 digit$/i,
      "Di Browser cari: kuota gratis wa.",
    ],
    [
      "Pulihkan",
      "Dinda ingin akunnya kembali. Cari panduannya di Browser, lalu klik langkah yang benar.",
      /^daftar ulang WhatsApp dengan nomor sendiri$/i,
      "Di Browser cari: panduan akun whatsapp diretas.",
    ],
  ],
  web: [
    [
      "kuota-gratis-wa.xyz",
      "Klaim Kuota 50GB Gratis",
      "kuota gratis wa klaim 50gb link",
      "<h3>Klaim Kuota 50GB</h3><p>Masukkan nomor WA dan <u data-v='kode verifikasi 6 digit'>kode verifikasi 6 digit</u> yang dikirim ke SMS-mu.</p>",
    ],
    [
      "help.wa-info.id/akun-diretas",
      "Panduan: Akun WhatsApp Diambil Alih",
      "panduan akun whatsapp diretas diambil alih wa",
      "<h3>Akun WA Diambil Alih</h3><ol><li><u data-v='daftar ulang WhatsApp dengan nomor sendiri'>daftar ulang WhatsApp dengan nomor sendiri</u></li><li><u data-v='tunggu sampai penyerang bosan'>tunggu sampai penyerang bosan</u></li><li><u data-v='kirim kode verifikasi ke teman'>kirim kode verifikasi ke teman</u></li></ol><p>Lalu aktifkan verifikasi dua langkah.</p>",
    ],
  ],
  cul: ["PEMBAJAK AKUN", "Pembajak WhatsApp", "#8f9bff", "gc"],
  end: "Akun Dinda diambil alih lewat kode verifikasi yang dipancing. Kalau teman tiba-tiba mengirim link aneh, konfirmasi lewat telepon sebelum klik.",
};
