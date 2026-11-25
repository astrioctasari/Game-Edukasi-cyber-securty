// Level 3: Telepon CS Palsu (Mudah)
// Penelepon mengaku dari bank dan minta kode OTP.
// Materi Buku Panduan: otp
const LEVEL_03 = {
  t: "Telepon CS Palsu",
  lv: "Mudah",
  tz: "Penelepon mengaku dari bank dan minta kode OTP.",
  ed: ["otp"],
  vals: ["Mengaku dari bank", "Kontak tersimpan", "+62 811-0000-123", "BankKu"],
  story: [
    [
      "+62 811-0000-123",
      "Halo, kami CS bank. Ada transaksi mencurigakan. Mohon sebutkan kode OTP yang baru dikirim.",
    ],
    ["Kamu", "OTP? Aku memang baru dapat kode di SMS tadi."],
    ["Ibu", "Nak, jangan kasih kode itu ke siapa pun ya!"],
  ],
  db: {
    "Log Telepon": T(
      ["No", "Nomor", "Waktu", "Durasi", "Catatan"],
      [
        [1, "Ibu", "2026-10-20 08:00", 3, "Kontak tersimpan"],
        [2, "+62 811-0000-123", "2026-10-20 09:10", 2, "Mengaku dari bank"],
        [3, "Ojek Pak Dani", "2026-10-20 09:25", 1, "Kontak tersimpan"],
        [4, "+62 811-0000-123", "2026-10-20 09:31", 6, "Mengaku dari bank"],
        [5, "+62 811-0000-123", "2026-10-20 09:45", 4, "Mengaku dari bank"],
      ]
    ),
    "SMS Masuk": T(
      ["No", "Pengirim", "Isi", "Waktu"],
      [
        [1, "BankKu", "Kode OTP 482913. JANGAN BERIKAN KE SIAPA PUN.", "2026-10-20 09:32"],
        [2, "Operator", "Pulsa Anda tersisa Rp 12.000", "2026-10-20 08:10"],
      ]
    ),
  },
  tk: [
    [
      "Cari",
      "Penelepon yang mengaku dari bank itu nomornya berapa? Klik nomornya.",
      /^\+62 811-0000-123$/,
      "Di Tabel pilih Log Telepon, saring Catatan sama dengan Mengaku dari bank.",
    ],
    [
      "Hitung",
      "Berapa kali nomor itu menelepon?",
      /^3$/,
      "Saring Log Telepon: Nomor sama dengan nomor tadi. Lihat jumlahnya, lalu klik 📌 Pakai jumlah ini.",
    ],
    [
      "Selidiki",
      "Cari di Browser: apa aturan bank soal OTP? Klik jawabannya.",
      /^TIDAK PERNAH$/i,
      "Di Browser cari: aturan bank OTP.",
    ],
  ],
  web: [
    [
      "bankku.co.id/keamanan",
      "Keamanan Nasabah BankKu",
      "bank otp aturan keamanan nasabah telepon pin",
      "<h3>Keamanan Nasabah</h3><p>Pihak bank <u data-v='TIDAK PERNAH'>TIDAK PERNAH</u> meminta OTP, PIN, atau password lewat telepon, SMS, atau chat.</p><p>Hubungi call center resmi di nomor kartu.</p>",
    ],
    ["berita.kampus.id", "Berita Kampus", "berita kampus wisuda", "<h3>Wisuda Oktober</h3>"],
  ],
  cul: ["PENIPU", "Penelepon palsu", "#ff7a6b", "g"],
  end: "Penelepon itu penipu rekayasa sosial: menelepon 3 kali dan menekan agar kamu menyebut OTP. OTP tidak boleh diberikan ke siapa pun, termasuk yang mengaku dari bank.",
};
