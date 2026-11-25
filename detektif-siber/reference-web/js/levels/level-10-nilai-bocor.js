// Level 10: Nilai Bocor (Sulit)
// Nilai mahasiswa berubah tengah malam.
// Materi Buku Panduan: brute, ip, log
const LEVEL_10 = {
  t: "Nilai Bocor",
  lv: "Sulit",
  tz: "Nilai mahasiswa berubah tengah malam.",
  ed: ["brute", "ip", "log"],
  vals: ["10.4.7.23", "GAGAL", "BERHASIL", "Lab Komputer 3", "Dimas", 80, 85],
  story: [
    [
      "Kaprodi",
      "Nilai beberapa mahasiswa berubah tengah malam. Tidak ada dosen yang mengaku. Tolong selidiki.",
    ],
    ["Sistem", "PERINGATAN 23:35: akun dosen_wati aktif di luar jam kerja."],
    ["Bu Wati", "Saya tidur jam 9 malam. Itu bukan saya!"],
  ],
  db: {
    "Perubahan Nilai": T(
      ["No", "Mahasiswa", "Mata Kuliah", "Nilai Lama", "Nilai Baru", "Waktu", "Alamat IP"],
      [
        [1, "Andi", "Algoritma", 55, 90, "2026-09-29 23:41", "10.4.7.23"],
        [2, "Andi", "Matdis", 48, 85, "2026-09-29 23:44", "10.4.7.23"],
        [3, "Rina", "Alpro", 70, 72, "2026-09-28 10:15", "10.4.2.5"],
        [4, "Budi", "OOP", 60, 65, "2026-09-27 09:30", "10.4.2.5"],
        [5, "Dimas", "Kalkulus", 40, 88, "2026-09-29 23:52", "10.4.7.23"],
        [6, "Sari", "Basis Data", 75, 78, "2026-09-29 20:05", "10.4.2.5"],
      ]
    ),
    "Catatan Login": T(
      ["No", "Akun", "Alamat IP", "Waktu", "Hasil"],
      [
        [1, "dosen_wati", "10.4.2.5", "2026-09-29 08:02", "BERHASIL"],
        [2, "andi", "10.4.5.9", "2026-09-29 09:10", "BERHASIL"],
        [3, "rina", "10.4.2.8", "2026-09-29 14:00", "GAGAL"],
        [4, "rina", "10.4.2.8", "2026-09-29 14:01", "BERHASIL"],
        [5, "budi", "10.4.5.11", "2026-09-29 18:45", "BERHASIL"],
        [6, "dosen_wati", "10.4.7.23", "2026-09-29 23:20", "GAGAL"],
        [7, "dosen_wati", "10.4.7.23", "2026-09-29 23:22", "GAGAL"],
        [8, "dosen_wati", "10.4.7.23", "2026-09-29 23:24", "GAGAL"],
        [9, "dosen_wati", "10.4.7.23", "2026-09-29 23:26", "GAGAL"],
        [10, "dosen_wati", "10.4.7.23", "2026-09-29 23:29", "GAGAL"],
        [11, "dosen_wati", "10.4.7.23", "2026-09-29 23:31", "GAGAL"],
        [12, "dosen_wati", "10.4.7.23", "2026-09-29 23:35", "BERHASIL"],
      ]
    ),
    "Absensi Lab": T(
      ["Nama", "Lokasi", "Masuk", "Keluar"],
      [
        ["Fajar", "Lab Komputer 3", "2026-09-29 22:50", "2026-09-30 00:10"],
        ["Maya", "Lab Komputer 3", "2026-09-29 13:00", "2026-09-29 15:00"],
        ["Tono", "Lab Komputer 1", "2026-09-29 23:00", "2026-09-30 00:30"],
        ["Lina", "Lab Komputer 3", "2026-09-29 20:00", "2026-09-29 22:30"],
      ]
    ),
  },
  tk: [
    [
      "Cari",
      "Dari Alamat IP mana nilai itu diubah? Klik IP-nya di tabel.",
      /^10\.4\.7\.23$/,
      "Di Perubahan Nilai, saring: Nilai Baru lebih dari 80. Perhatikan IP yang berulang.",
    ],
    [
      "Hitung",
      "Berapa kali IP itu gagal login sebelum berhasil? Pakai tombol 📌 jumlah.",
      /^6$/,
      "Di Catatan Login: Alamat IP sama dengan 10.4.7.23, dan Hasil sama dengan GAGAL. Tekan 📌 Pakai jumlah ini.",
    ],
    [
      "Lacak",
      "Buka Browser dan cari tahu: IP itu berada di lokasi mana? Klik lokasi yang bergaris bawah.",
      /^Lab Komputer 3$/i,
      "Di Browser cari: denah jaringan kampus. Cocokkan 10.4.7.x dengan lokasinya.",
    ],
    [
      "Tangkap",
      "Buka CCTV Lab Komputer 3 dan putar rekamannya. Sosok mana yang masuk lalu mengetik di PC-23 sekitar pukul 23:41? Klik sosoknya.",
      /^Sosok B$/i,
      "Putar CCTV dan lihat siapa yang masuk, lalu duduk di PC-23.",
    ],
    [
      "Cocokkan",
      "Lihat ciri sosok itu lebih jelas di Foto TKP (baju, kacamata, tas), lalu cocokkan dengan foto di internet. Siapa dia? Klik namanya di bawah foto.",
      /^Fajar$/i,
      "Cari di Browser: galeri praktikum lab. Hati-hati, beberapa orang bajunya sama. Cek kacamata dan tas.",
    ],
  ],
  web: [
    [
      "wiki.kampus.id/jaringan",
      "Denah Jaringan Kampus",
      "ip alamat jaringan denah lokasi perangkat komputer",
      "<h3>Denah Jaringan Kampus</h3><p>Alamat IP dibagi menurut lokasi:</p><ul><li>10.4.2.x : <u data-v='Ruang Dosen'>Ruang Dosen</u></li><li>10.4.5.x : <u data-v='Perpustakaan'>Perpustakaan</u></li><li>10.4.7.x : <u data-v='Lab Komputer 3'>Lab Komputer 3</u></li></ul>",
    ],
    [
      "lab.kampus.id/galeri",
      "Galeri Praktikum Lab 3",
      "galeri foto praktikum lab mahasiswa wajah ciri orang",
      "<h3>Galeri Praktikum Lab Komputer 3</h3><p>Perhatikan pakaian dan atributnya.</p>" +
        GAL([
          ["Fajar", "#ff7a6b", "gb"],
          ["Maya", "#ff7a6b", "b"],
          ["Dimas", "#ff7a6b", "g"],
          ["Lina", "#ffd95a", "c"],
          ["Tono", "#38bdf8", ""],
        ]),
    ],
    [
      "kantin.kampus.id",
      "Menu Kantin Hari Ini",
      "kantin makan menu nasi",
      "<h3>Menu Kantin</h3><p>Nasi goreng, soto ayam, es teh.</p>",
    ],
    [
      "berita.kampus.id",
      "Berita: Wisuda Oktober",
      "berita wisuda kampus mahasiswa",
      "<h3>Wisuda Oktober</h3><p>Wisuda dilaksanakan 12 Oktober di aula utama.</p>",
    ],
  ],
  sc: {
    t0: "23:40:40",
    dur: 24,
    bg:
      '<rect width="600" height="340" fill="#dfe8ff"/><rect width="600" height="110" fill="#c3d2fb"/><rect y="255" width="600" height="85" fill="#e9d9b8"/><text x="300" y="322" text-anchor="middle" font-size="11" fill="#5b5f8f">KORIDOR LUAR</text><rect width="8" height="120" y="130" fill="#8f9bff"/><text x="12" y="22" font-size="12" fill="#3d4bb8">TKP · Lab Komputer 3</text>' +
      [200, 280, 360, 440, 520].map((x, i) => PC(x, "PC-" + (21 + i), i == 2)).join(""),
    cap: "Lab Komputer 3 · pukul 23:41. Komputer PC-23 sedang dipakai.",
    ch: [
      ["Sosok A", "#ffd95a", [200, 205], "c"],
      ["Sosok B", "#ff7a6b", [360, 207], "gb"],
      ["Sosok C", "#38bdf8", [470, 300], ""],
    ],
    ev: [
      [0, "Kamera lab aktif."],
      [14, "PC-23 menyala."],
      [20, "23:41:00 PC-23 login sebagai dosen_wati. Nilai mulai diubah."],
    ],
    bub: [
      ["Sosok A", "Lanjut tugas..."],
      ["Sosok B", "Ketik ketik..."],
      ["Sosok C", "Lab 1 di mana ya?"],
    ],
  },
  cc: {
    t0: "23:40:40",
    dur: 24,
    ch: [
      [
        "Sosok A",
        "#ffd95a",
        [
          [0, 200, 205],
          [3, 200, 205],
          [7, 40, 225],
          [9, -30, 235],
        ],
        "c",
      ],
      [
        "Sosok B",
        "#ff7a6b",
        [
          [0, -30, 235],
          [7, -30, 235],
          [10, 300, 235],
          [12, 360, 207],
          [24, 360, 207],
        ],
        "gb",
      ],
      [
        "Sosok C",
        "#38bdf8",
        [
          [0, -30, 300],
          [6, -30, 300],
          [22, 640, 300],
        ],
        "",
      ],
    ],
    ev: [
      [0, "Kamera lab aktif."],
      [14, "PC-23 menyala."],
      [20, "23:41:00 PC-23 login sebagai dosen_wati."],
    ],
    bub: [
      [3, 6, "Sosok A", "Aku pulang dulu."],
      [13, 24, "Sosok B", "Ketik ketik..."],
      [10, 14, "Sosok C", "Lab 1 di mana ya?"],
    ],
  },
  cul: ["PELAKU", "Fajar", "#ff7a6b", "gb"],
  end: "Pelakunya Fajar. Ia menebak sandi Bu Wati berkali-kali dari Lab Komputer 3, lalu mengubah nilai.",
};
