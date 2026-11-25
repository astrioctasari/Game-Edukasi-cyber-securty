// Materi Buku Panduan. Kuncinya dipakai oleh `ed` di tiap level.

// Daftar bab: kunci -> [judul, isi, tips]
const ED = {
  otp: [
    "🔢 OTP: Kode Rahasiamu",
    "OTP adalah kode sekali pakai untuk membuktikan bahwa itu benar-benar kamu. Penipu menelepon pura-pura dari bank lalu memintanya.",
    "Aturan emas: bank dan marketplace tidak pernah meminta OTP. Jangan berikan ke siapa pun.",
  ],
  sql: [
    "🔎 Bertanya ke Data (SQL)",
    "SQL adalah bahasa untuk bertanya ke data. Ada tiga bagian: SELECT (apa yang ditampilkan), FROM (dari tabel mana), WHERE (syaratnya). Di Terminal kamu tinggal menyusun bubble, tanpa mengetik.",
    "Contoh: SELECT * FROM Log Telepon WHERE Catatan = 'Mengaku dari bank' artinya tampilkan semua panggilan yang dicatat mengaku dari bank.",
  ],
  sql2: [
    "🧮 SQL Lanjutan",
    "AND menggabungkan dua syarat. LIKE mencari pola ('Kopi%' berarti diawali Kopi). COUNT(*) menghitung jumlah baris.",
    "Tips: mulai dari pertanyaan sederhana, lalu persempit dengan syarat tambahan.",
  ],
  wifi: [
    "📶 Waspada WiFi Publik",
    "WiFi terbuka tanpa sandi bisa dibuat penipu dengan nama mirip kafe. Datamu bisa disadap.",
    "Tips: tanyakan nama dan sandi WiFi ke petugas, hindari login bank di WiFi publik, atau pakai data seluler.",
  ],
  apk: [
    "📦 Aplikasi di Luar Toko Resmi",
    "File APK dari tautan atau grup sering disusupi. Tandanya: meminta izin berlebihan, misalnya membaca SMS.",
    "Tips: unduh hanya dari toko aplikasi resmi dan periksa izin sebelum memasang.",
  ],
  toko: [
    "🛒 Toko Online Palsu",
    "Harga terlalu murah, ulasan sempurna yang muncul bersamaan, dan rekening pribadi adalah tanda toko palsu.",
    "Tips: cek umur domain, baca ulasan bintang rendah, dan bayar lewat platform resmi.",
  ],
  qris: [
    "🔳 QRIS Palsu",
    "Penipu menempel stiker QRIS sendiri menimpa yang asli, sehingga uang masuk ke rekening mereka.",
    "Tips: periksa nama merchant yang muncul di layar sebelum membayar.",
  ],
  brute: [
    "🔑 Tebak Sandi (Brute Force)",
    "Penyerang mencoba banyak kata sandi satu per satu sampai ada yang cocok. Tandanya: banyak GAGAL beruntun, lalu satu BERHASIL.",
    "Cegah: sandi panjang, batasi percobaan login, aktifkan verifikasi dua langkah.",
  ],
  ip: [
    "🌐 Alamat IP",
    "Alamat IP mirip plat nomor perangkat di jaringan. Dari situ perangkat dan lokasinya bisa dilacak.",
    "Catatan: IP bisa disamarkan (misalnya VPN), jadi cocokkan dengan bukti lain.",
  ],
  log: [
    "📜 Catatan Aktivitas (Log)",
    "Sistem mencatat siapa melakukan apa, kapan, dan dari mana. Cari pola janggal: jam tak wajar, banyak gagal, perubahan besar.",
    "Tips: simpan salinan log di tempat terpisah agar tak bisa dihapus pelaku.",
  ],
  phish: [
    "🎣 Waspada Phishing",
    "Pesan palsu yang menyamar jadi bank, kampus, atau atasan agar kamu menyerahkan sandi. Tandanya: mendesak, pengirim mirip tapi beda, tautan aneh.",
    "Tips: jangan klik tautan dari pesan yang menekan. Buka situs resmi lewat pencarian sendiri.",
  ],
  dom: [
    "🔍 Cek Nama Domain",
    "Perhatikan bagian setelah @. 'kampus.ac.id' asli, sedangkan 'kampus-verif.xyz' hanya meniru.",
    "Tips: tahan kursor pada tautan untuk melihat alamat aslinya sebelum diklik.",
  ],
  mfa: [
    "📲 Verifikasi Dua Langkah",
    "Selain sandi, kamu perlu kode dari HP. Walau sandi bocor, penyerang tetap tertahan.",
    "Tips: aktifkan untuk email, bank, dan akun kerja.",
  ],
  share: [
    "🤝 Jangan Pinjamkan Akun",
    "Akun yang dipakai bersama membuat jejak jadi kabur: log menunjuk pemilik, padahal pelakunya orang lain.",
    "Tips: tiap orang punya akun sendiri, dan keluar (logout) saat selesai.",
  ],
  min: [
    "🔐 Akses Secukupnya",
    "Karyawan hanya perlu akses ke data yang dipakai kerjanya. Data pelanggan sebaiknya dibatasi dan unduhan besar dipantau.",
    "Tips: beri peringatan otomatis untuk unduhan besar di luar jam kerja.",
  ],
};

// Bab tentang sandi (dipakai Level 1)
ED.sandi = [
  "🗒️ Sandi Jangan Ditempel",
  "Menulis sandi di sticky note yang menempel di monitor sama saja membukakan pintu untuk siapa saja yang lewat. Bahkan kamera CCTV bisa ikut merekamnya.",
  "Tips: jangan pakai sandi gampang seperti nama+123, simpan sandi di pengelola sandi (password manager), dan aktifkan verifikasi dua langkah.",
];
