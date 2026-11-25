// Level 1: Sticky Note Sandi (Mudah)
// Akun kasir dipakai orang saat toko sudah tutup.
// Materi Buku Panduan: sandi
const LEVEL_01 = {
  t: "Sticky Note Sandi",
  lv: "Mudah",
  tz: "Akun kasir dipakai orang saat toko sudah tutup.",
  ed: ["sandi"],
  story: [
    [
      "Mbak Sari",
      "Akun kasir toko dipakai orang pas toko sudah tutup. Padahal sandinya cuma aku yang tahu!",
    ],
    ["Kamu", "Sandinya disimpan di mana, Mbak?"],
    [
      "Mbak Sari",
      "Hmm... di <u data-v='Sticky note'>sticky note kuning</u> yang nempel di monitor. Hehe.",
    ],
  ],
  db: {
    "Login Kasir": T(
      ["No", "Akun", "Waktu", "Hasil"],
      [
        [1, "kasir_sari", "2026-10-26 07:58", "BERHASIL"],
        [2, "kasir_sari", "2026-10-26 12:10", "BERHASIL"],
        [3, "kasir_sari", "2026-10-26 16:30", "BERHASIL"],
        [4, "kasir_sari", "2026-10-26 21:47", "BERHASIL"],
      ]
    ),
  },
  tk: [
    [
      "Cari",
      "Toko tutup jam 21:00. Kapan akun kasir dipakai setelah toko tutup? Klik waktunya.",
      /^2026-10-26 21:47$/,
      "Buka Tabel dan lihat kolom Waktu. Hanya satu login yang lewat dari jam 21:00.",
    ],
    [
      "Selidiki",
      "Menurut cerita Mbak Sari, di mana sandi itu disimpan? Klik jawabannya.",
      /^Sticky note$/i,
      "Baca lagi pesan Mbak Sari di jendela Pesan. Klik teks yang bergaris bawah.",
    ],
    [
      "Telusuri",
      "Cari tahu di Browser: bagaimana cara menyimpan sandi yang lebih aman? Klik jawabannya.",
      /^Pengelola sandi$/i,
      "Di Browser cari: simpan sandi aman.",
    ],
  ],
  web: [
    [
      "sandi.id/aman",
      "Cara Menyimpan Sandi dengan Aman",
      "simpan sandi aman cara kata password",
      "<h3>Simpan Sandi dengan Aman</h3><p>Cara berisiko: <u data-v='Kertas tempel'>menempel sandi di meja atau monitor</u>.</p><p>Cara yang disarankan: <u data-v='Pengelola sandi'>pakai pengelola sandi (password manager)</u>.</p>",
    ],
    [
      "warung.id/menu",
      "Menu Warung Mbak Sari",
      "menu warung makan nasi",
      "<h3>Menu</h3><p>Nasi goreng, es teh, dan gorengan.</p>",
    ],
  ],
  cul: ["PELAKU", "Orang iseng", "#ff7a6b", "gb"],
  end: "Orang iseng membaca sandi dari sticky note di monitor lalu login setelah toko tutup. Jangan tempel sandi di tempat yang bisa dilihat orang, ya!",
};
