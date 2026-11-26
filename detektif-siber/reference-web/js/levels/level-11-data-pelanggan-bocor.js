// Level 11: Data Pelanggan Bocor (Ahli)
// Ada unduhan besar tengah malam.
// Materi Buku Panduan: share, min, mfa
const LEVEL_11 = {
  t: "Data Pelanggan Bocor",
  lv: "Ahli",
  tz: "Ada unduhan besar tengah malam.",
  ed: ["share", "min", "mfa"],
  vals: ["tono.k", "Dewi Anggraini", "Tono Kurniawan", 500],
  story: [
    ["Direktur", "Data pelanggan kita muncul di forum gelap. Cari tahu siapa yang mengambilnya."],
    ["Sistem", "PERINGATAN 22:15: unduhan sangat besar dari server data."],
    ["Tono", "Saya pulang jam 5 sore. Sungguh bukan saya!"],
  ],
  db: {
    "Akses File": T(
      ["No", "Akun", "File", "Waktu", "Unduh (MB)"],
      [
        [1, "maya.l", "Daftar Cuti", "2026-10-02 10:00", 2],
        [2, "budi.s", "Materi Promo", "2026-10-02 13:20", 45],
        [3, "tono.k", "Laporan Bulanan", "2026-10-02 15:00", 12],
        [4, "tono.k", "Data Pelanggan Lengkap", "2026-10-02 22:15", 820],
      ]
    ),
    "Absensi Gedung": T(
      ["Nama", "Masuk", "Keluar"],
      [
        ["Tono Kurniawan", "2026-10-02 08:00", "2026-10-02 17:30"],
        ["Budi Santoso", "2026-10-02 09:00", "2026-10-02 17:00"],
        ["Maya Lestari", "2026-10-02 08:30", "2026-10-02 16:45"],
        ["Dewi Anggraini", "2026-10-02 21:30", "2026-10-02 23:10"],
      ]
    ),
  },
  tk: [
    [
      "Cari",
      "Akun mana yang mengunduh data amat besar? Klik nama akunnya di tabel.",
      /^tono\.k$/i,
      "Di Akses File, saring: Unduh (MB) lebih dari 500.",
    ],
    [
      "Lacak",
      "Siapa pemilik akun itu? Cari di Browser (direktori karyawan), lalu klik namanya.",
      /^Tono Kurniawan$/i,
      "Di Browser cari: direktori karyawan.",
    ],
    [
      "Tangkap",
      "Buka CCTV kantor dan putar sampai unduhan 22:15. Sosok mana yang duduk di meja Tono? Klik sosoknya.",
      /^Sosok A$/i,
      "Putar CCTV dan lihat siapa yang masuk lalu duduk di meja Tono.",
    ],
    [
      "Cocokkan",
      "Lihat ciri sosoknya di Foto TKP, lalu cocokkan dengan foto karyawan. Siapa dia? Klik namanya.",
      /^Dewi Anggraini$/i,
      "Cari di Browser: foto karyawan. Bandingkan warna baju, kacamata, dan topi. Absensi Gedung juga membantu.",
    ],
    [
      "Bukti akhir",
      "Data itu dijual di internet. Di Browser, cari siapa username penjualnya dan klik username itu.",
      /^dw_anggi$/i,
      "Di Browser cari: forum jual data pelanggan.",
    ],
  ],
  web: [
    [
      "hr.kantor.id/direktori",
      "Direktori Karyawan",
      "direktori karyawan akun nama pemilik divisi",
      "<h3>Direktori Karyawan</h3><ul><li>tono.k : <u data-v='Tono Kurniawan'>Tono Kurniawan</u> (Keuangan)</li><li>dewi.a : <u data-v='Dewi Anggraini'>Dewi Anggraini</u> (Magang IT)</li><li>budi.s : <u data-v='Budi Santoso'>Budi Santoso</u> (Pemasaran)</li><li>maya.l : <u data-v='Maya Lestari'>Maya Lestari</u> (HRD)</li></ul>",
    ],
    [
      "hr.kantor.id/foto",
      "Foto Karyawan",
      "foto karyawan wajah ciri orang pegawai",
      "<h3>Foto Karyawan</h3><p>Perhatikan pakaian dan atributnya.</p>" +
        GAL([
          ["Tono Kurniawan", "#38bdf8", "b"],
          ["Dewi Anggraini", "#ff7a6b", "gc"],
          ["Budi Santoso", "#ff7a6b", "g"],
          ["Maya Lestari", "#8f9bff", "c"],
        ]),
    ],
    [
      "forumgelap.net/jual-data",
      "Forum: Jual Data Pelanggan",
      "forum jual data pelanggan dijual bocor",
      "<h3>Dijual: data pelanggan</h3><p>Penjual: <u data-v='dw_anggi'>dw_anggi</u></p><p>Isi: 5.000 pelanggan lengkap. Bayar kripto.</p>",
    ],
    [
      "sosmed.id/dw_anggi",
      "Profil @dw_anggi",
      "profil dw_anggi dewi anggraini sosial media",
      "<h3>@dw_anggi</h3><p>Dewi Anggraini · Magang IT · suka kopi dan kucing.</p>",
    ],
    [
      "berita.kantor.id",
      "Berita Internal",
      "berita internal kantor acara",
      "<h3>Berita</h3><p>Gathering kantor bulan depan.</p>",
    ],
  ],
  sc: {
    t0: "22:14:50",
    dur: 22,
    bg:
      '<rect width="600" height="340" fill="#dfe8ff"/><rect width="600" height="110" fill="#c3d2fb"/><rect y="255" width="600" height="85" fill="#e9d9b8"/><text x="12" y="22" font-size="12" fill="#3d4bb8">TKP · Kantor Keuangan · malam</text><rect width="8" height="120" y="130" fill="#8f9bff"/><rect x="510" y="130" width="86" height="60" fill="#3d4bb8" stroke="#0d0f24" stroke-width="2"/><text x="553" y="165" text-anchor="middle" font-size="11" fill="#fff">POS SATPAM</text>' +
      PC(130, "Meja Budi", false) +
      PC(240, "Meja Maya", false) +
      PC(350, "Meja Tono", true),
    cap: "Kantor Keuangan · pukul 22:15. Komputer di meja Tono menyala.",
    ch: [
      ["Sosok A", "#ff7a6b", [350, 207], "gc"],
      ["Sosok B", "#ffd95a", [553, 215], "c"],
    ],
    ev: [
      [0, "Kamera aktif. Kantor tampak sepi."],
      [10, "22:15:00 komputer Tono menyala."],
      [14, "Unduhan data pelanggan dimulai."],
    ],
    bub: [
      ["Sosok A", "Mengunduh..."],
      ["Sosok B", "Ronda dulu ah."],
    ],
  },
  cc: {
    t0: "22:14:50",
    dur: 22,
    ch: [
      [
        "Sosok A",
        "#ff7a6b",
        [
          [0, -30, 235],
          [4, -30, 235],
          [9, 270, 235],
          [11, 350, 207],
          [22, 350, 207],
        ],
        "gc",
      ],
      [
        "Sosok B",
        "#ffd95a",
        [
          [0, 553, 215],
          [12, 553, 215],
          [17, 470, 300],
          [22, 300, 305],
        ],
        "c",
      ],
    ],
    ev: [
      [0, "Kamera aktif. Kantor tampak sepi."],
      [10, "22:15:00 komputer Tono menyala."],
      [14, "Unduhan data pelanggan dimulai."],
    ],
    bub: [
      [3, 9, "Sosok B", "Ronda dulu ah."],
      [11, 15, "Sosok A", "Sepi, aman..."],
      [15, 22, "Sosok A", "Mengunduh..."],
    ],
  },
  cul: ["PELAKU", "Dewi Anggraini", "#ff7a6b", "gc"],
  end: "Dewi memakai akun Tono untuk mengunduh data saat Tono sudah pulang, lalu menjualnya di forum dengan username dw_anggi.",
};
