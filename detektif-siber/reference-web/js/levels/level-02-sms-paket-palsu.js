// Level 2: SMS Paket Palsu (Mudah)
// SMS minta biaya untuk paket yang tidak kamu pesan.
// Materi Buku Panduan: phish, dom
const LEVEL_02 = {
  t: "SMS Paket Palsu",
  lv: "Mudah",
  tz: "SMS minta biaya untuk paket yang tidak kamu pesan.",
  ed: ["phish", "dom"],
  vals: ["Dikirim", "Selesai"],
  story: [
    [
      "JNE-Info",
      "Paket Anda tertahan di gudang. Bayar biaya <u data-v='Rp 15.000'>Rp 15.000</u> di: <u data-v='jne-cek-paket.xyz/bayar'>jne-cek-paket.xyz/bayar</u>",
    ],
    ["Kamu", "Aku nggak merasa belanja apa-apa belakangan ini."],
    ["Adik", "Kak, jangan langsung klik. Cek dulu ya."],
  ],
  db: {
    "Pesanan Saya": T(
      ["No", "Toko", "Barang", "Kurir", "Status"],
      [
        [1, "Toko Buku Maju", "Novel", "JNE", "Selesai"],
        [2, "Gadget Ria", "Kabel", "JNT", "Selesai"],
        [3, "Kedai Kopi", "Biji kopi", "Ambil sendiri", "Selesai"],
      ]
    ),
  },
  tk: [
    [
      "Cari",
      "Baca SMS di jendela Pesan. Klik alamat tautan yang janggal.",
      /^jne-cek-paket\.xyz\/bayar$/i,
      "Cari alamat web di SMS. Kurir resmi memakai alamat seperti jne.co.id.",
    ],
    [
      "Selidiki",
      "Periksa domain itu di Browser. Kapan didaftarkan? Klik tanggalnya.",
      /^2026-10-19$/,
      "Di Browser cari: cek domain jne cek paket.",
    ],
    [
      "Hitung",
      "Adakah pesanan berstatus Dikirim di Pesanan Saya?",
      /^0$/,
      "Di Tabel: Status sama dengan Dikirim. Jumlah 0 berarti tidak ada paket yang sedang dikirim.",
    ],
  ],
  web: [
    [
      "cekdomain.id/jne-cek-paket.xyz",
      "Cek Domain: jne-cek-paket.xyz",
      "cek domain jne cek paket xyz whois terdaftar",
      "<h3>jne-cek-paket.xyz</h3><p>Terdaftar: <u data-v='2026-10-19'>19 Oktober 2026</u> (3 hari lalu)</p><p>Pemilik: disembunyikan</p><p>Catatan: meniru nama kurir, banyak dilaporkan sebagai penipuan.</p>",
    ],
    [
      "jne.co.id",
      "JNE (situs resmi)",
      "jne resmi kurir situs",
      "<h3>jne.co.id</h3><p>Situs resmi, terdaftar sejak 1990.</p>",
    ],
    [
      "promo.toko.id",
      "Promo Akhir Pekan",
      "promo diskon toko",
      "<h3>Diskon 50%</h3><p>Khusus akhir pekan.</p>",
    ],
  ],
  cul: ["PENIPU", "Pengirim SMS", "#ff7a6b", "c"],
  end: "SMS itu penipuan: tautannya palsu dan kamu memang tidak punya paket yang sedang dikirim. Jangan klik, hapus saja, dan cek resi hanya lewat aplikasi resmi.",
};
