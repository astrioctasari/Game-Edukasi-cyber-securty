// Daftar semua level, diurutkan dari yang paling mudah.
// Untuk menambah level baru: buat file baru di folder ini, lalu masukkan ke daftar LV
// dan ke index.html.
//
// Isi satu level:
//   t     judul kasus
//   lv    tingkat kesulitan (Mudah / Sedang / Sulit / Ahli)
//   tz    ringkasan singkat
//   ed    bab Buku Panduan yang dibaca sebelum kasus (kunci dari ED)
//   vals  nilai-nilai yang muncul sebagai bubble di Terminal
//   story percakapan pembuka: [pembicara, teks]
//   db    tabel data kasus
//   tk    langkah tugas: [label, perintah, pola jawaban (regex), petunjuk]
//   web   halaman Browser: [alamat, judul, kata kunci, isi HTML]
//   sc    Foto TKP (opsional)
//   cc    rekaman CCTV (opsional)
//   cul   kartu pelaku di Papan Bukti
//   end   teks penutup kasus
const LV = [
  LEVEL_01, // Sticky Note Sandi
  LEVEL_02, // SMS Paket Palsu
  LEVEL_03, // Telepon CS Palsu
  LEVEL_04, // Link WA dari Teman
  LEVEL_05, // WiFi Kafe Palsu
  LEVEL_06, // QRIS Kedai Kopi
  LEVEL_07, // APK Premium Gratis
  LEVEL_08, // Toko Online Palsu
  LEVEL_09, // Email Palsu
  LEVEL_10, // Nilai Bocor
  LEVEL_11, // Data Pelanggan Bocor
];
