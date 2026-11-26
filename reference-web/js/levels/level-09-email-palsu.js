// Level 9: Email Palsu (Sulit)
// Pegawai dikirimi email 'gaji ditahan'.
// Materi Buku Panduan: phish, dom, mfa
const LEVEL_09 = {
  t: "Email Palsu",
  lv: "Sulit",
  tz: "Pegawai dikirimi email 'gaji ditahan'.",
  ed: ["phish", "dom", "mfa"],
  vals: ["kampus-verif.xyz", "kampus.ac.id", "Rusia", "Indonesia", "bu_ratna"],
  story: [
    [
      "Admin IT",
      "Beberapa pegawai melapor menerima email 'SEGERA verifikasi akun'. Ada yang sudah mengeklik.",
    ],
    ["Bu Ratna", "Akun saya tiba-tiba minta login ulang. Aneh sekali."],
    ["Sistem", "PERINGATAN 09:40: login berhasil dari luar negeri."],
  ],
  db: {
    "Email Masuk": T(
      ["No", "Pengirim", "Domain Pengirim", "Subjek", "Waktu"],
      [
        [1, "Biro Keuangan", "kampus.ac.id", "Slip honor Agustus", "2026-10-01 08:10"],
        [2, "Admin IT", "kampus.ac.id", "Jadwal pemeliharaan server", "2026-10-01 08:40"],
        [
          3,
          "Layanan Kampus",
          "kampus-verif.xyz",
          "SEGERA verifikasi akun atau diblokir",
          "2026-10-01 09:02",
        ],
        [4, "Perpustakaan", "kampus.ac.id", "Buku jatuh tempo", "2026-10-01 09:15"],
        [5, "Layanan Kampus", "kampus-verif.xyz", "SEGERA: gaji akan ditahan", "2026-10-01 09:20"],
      ]
    ),
    "Catatan Klik": T(
      ["No", "Akun", "Waktu", "Tujuan Tautan"],
      [
        [1, "bu_ratna", "2026-10-01 09:05", "kampus-verif.xyz"],
        [2, "pak_anto", "2026-10-01 09:07", "kampus-verif.xyz"],
        [3, "andi", "2026-10-01 09:12", "kampus.ac.id"],
        [4, "siti_admin", "2026-10-01 09:25", "kampus-verif.xyz"],
        [5, "dewi_it", "2026-10-01 09:30", "kampus-verif.xyz"],
        [6, "budi", "2026-10-01 09:40", "kampus.ac.id"],
      ]
    ),
    "Login Baru": T(
      ["No", "Akun", "Waktu", "Negara", "Hasil"],
      [
        [1, "andi", "2026-10-01 08:50", "Indonesia", "BERHASIL"],
        [2, "pak_anto", "2026-10-01 09:50", "Indonesia", "BERHASIL"],
        [3, "bu_ratna", "2026-10-01 09:40", "Rusia", "BERHASIL"],
        [4, "siti_admin", "2026-10-01 10:05", "Indonesia", "BERHASIL"],
        [5, "dewi_it", "2026-10-01 10:10", "Indonesia", "BERHASIL"],
      ]
    ),
  },
  tk: [
    [
      "Cari",
      "Email palsu itu dikirim dari domain apa? Klik domainnya di tabel.",
      /^kampus-verif\.xyz$/i,
      "Di Email Masuk, saring: Domain Pengirim bukan kampus.ac.id.",
    ],
    [
      "Selidiki",
      "Buka Browser dan periksa domain palsu itu. Kapan domain itu didaftarkan? Klik tanggalnya.",
      /^2026-09-29$/,
      "Di Browser cari: cek domain kampus-verif.xyz.",
    ],
    [
      "Hitung",
      "Berapa orang mengeklik tautan ke domain palsu itu? Pakai 📌 jumlah.",
      /^4$/,
      "Di Catatan Klik, saring: Tujuan Tautan sama dengan kampus-verif.xyz.",
    ],
    [
      "Tangkap",
      "Akun mana yang dibobol dari luar negeri? Klik nama akunnya.",
      /^bu_ratna$/i,
      "Di Login Baru, saring: Negara bukan Indonesia.",
    ],
    [
      "Saksi",
      "Buka CCTV Ruang Admin. Sosok mana yang curiga lalu berjalan melapor ke Admin IT? Klik sosoknya.",
      /^Sosok D$/i,
      "Putar CCTV dan perhatikan siapa yang berdiri lalu berjalan ke meja Admin IT.",
    ],
    [
      "Cocokkan",
      "Lihat ciri sosoknya di Foto TKP, lalu cocokkan dengan foto staf. Akun siapa dia? Klik namanya.",
      /^andi$/i,
      "Cari di Browser: foto staf. Bandingkan warna baju dan kacamata.",
    ],
  ],
  web: [
    [
      "cekdomain.id/kampus-verif.xyz",
      "Cek Domain: kampus-verif.xyz",
      "cek domain kampus-verif whois pemilik terdaftar xyz",
      "<h3>kampus-verif.xyz</h3><p>Terdaftar: <u data-v='2026-09-29'>29 September 2026</u> (2 hari lalu)</p><p>Pemilik: disembunyikan</p><p>Server: luar negeri</p><p>Catatan: domain baru yang meniru situs resmi sering dipakai untuk phishing.</p>",
    ],
    [
      "hr.kampus.id/foto-staf",
      "Foto Staf",
      "foto staf pegawai wajah ciri orang akun",
      "<h3>Foto Staf</h3><p>Nama akun di bawah tiap foto.</p>" +
        GAL([
          ["bu_ratna", "#ff7a6b", "g"],
          ["pak_anto", "#8f9bff", "c"],
          ["siti_admin", "#ffd95a", "b"],
          ["andi", "#38bdf8", "g"],
          ["dewi_it", "#ff7a6b", "c"],
        ]),
    ],
    [
      "kampus.ac.id",
      "Situs Resmi Kampus",
      "kampus resmi domain ac.id",
      "<h3>kampus.ac.id</h3><p>Situs resmi, terdaftar sejak 2005.</p>",
    ],
    [
      "promo.toko.id",
      "Promo Belanja Akhir Pekan",
      "promo diskon belanja toko",
      "<h3>Diskon 50%</h3><p>Khusus akhir pekan.</p>",
    ],
  ],
  sc: {
    t0: "09:02:00",
    dur: 18,
    bg:
      '<rect width="600" height="340" fill="#dfe8ff"/><rect width="600" height="110" fill="#c3d2fb"/><rect y="255" width="600" height="85" fill="#e9d9b8"/><text x="12" y="22" font-size="12" fill="#3d4bb8">TKP · Ruang Admin</text><rect x="500" y="118" width="90" height="56" rx="4" fill="#3d4bb8" stroke="#0d0f24" stroke-width="2"/><text x="545" y="150" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">ADMIN IT</text>' +
      [100, 215, 330, 445].map((x) => PC(x, "", true)).join(""),
    cap: 'Ruang Admin · pukul 09:05. Email "SEGERA verifikasi akun" baru saja masuk.',
    ch: [
      ["Sosok A", "#ff7a6b", [100, 208], "g"],
      ["Sosok B", "#8f9bff", [215, 208], "c"],
      ["Sosok C", "#ffd95a", [330, 208], "b"],
      ["Sosok D", "#38bdf8", [520, 208], "g"],
    ],
    ev: [
      [0, 'Email "SEGERA verifikasi akun" masuk ke 4 pengguna.'],
      [10, "Admin IT menerima laporan langsung dari seorang pengguna."],
    ],
    bub: [
      ["Sosok A", "Verifikasi? Klik ah."],
      ["Sosok B", "Gaji ditahan?! Klik!"],
      ["Sosok C", "Cepat diverifikasi..."],
      ["Sosok D", "Domainnya aneh..."],
    ],
  },
  cc: {
    t0: "09:02:00",
    dur: 18,
    ch: [
      [
        "Sosok A",
        "#ff7a6b",
        [
          [0, 100, 208],
          [18, 100, 208],
        ],
        "g",
      ],
      [
        "Sosok B",
        "#8f9bff",
        [
          [0, 215, 208],
          [18, 215, 208],
        ],
        "c",
      ],
      [
        "Sosok C",
        "#ffd95a",
        [
          [0, 330, 208],
          [18, 330, 208],
        ],
        "b",
      ],
      [
        "Sosok D",
        "#38bdf8",
        [
          [0, 445, 208],
          [5, 445, 208],
          [7, 445, 226],
          [10, 520, 208],
          [18, 520, 208],
        ],
        "g",
      ],
    ],
    ev: [
      [0, 'Email "SEGERA verifikasi akun" masuk ke 4 pengguna.'],
      [10, "Admin IT menerima laporan langsung dari seorang pengguna."],
    ],
    bub: [
      [3, 7, "Sosok A", "Verifikasi? Klik ah."],
      [3, 8, "Sosok B", "Gaji ditahan?! Klik!"],
      [4, 9, "Sosok C", "Cepat diverifikasi..."],
      [5, 9, "Sosok D", "Domainnya aneh..."],
      [11, 18, "Sosok D", "Ada email palsu!"],
    ],
  },
  cul: ["SAKSI KUNCI", "andi", "#38bdf8", "g"],
  end: "Email palsu dari kampus-verif.xyz menjebak 4 orang. Akun bu_ratna dipakai penyerang dari luar negeri.",
};
