// Terjemahan antarmuka Indonesia dan Inggris.

// Terjemahan kata dan kalimat pendek
const EXD = {
  "Selamat Datang": "Welcome",
  Kasus: "Cases",
  "Buku Panduan": "Guide Book",
  Profil: "Profile",
  Pengaturan: "Settings",
  Berkas: "Files",
  Pesan: "Messages",
  Tabel: "Tables",
  Browser: "Browser",
  "Foto TKP": "Crime Scene Photo",
  "Papan Bukti": "Evidence Board",
  Masuk: "Sign In",
  Daftar: "Sign Up",
  "Ingat saya": "Remember me",
  Kembali: "Back",
  Cari: "Search",
  Beranda: "Home",
  Reset: "Reset",
  Perintah: "Commands",
  Kolom: "Columns",
  Operator: "Operators",
  Nilai: "Values",
  Hapus: "Delete",
  Bersihkan: "Clear",
  Jalankan: "Run",
  Selesai: "Done",
  Terkunci: "Locked",
  Karakter: "Character",
  Animasi: "Animation",
  Hidup: "Lively",
  Melayang: "Floating",
  Bercahaya: "Glowing",
  Diam: "Still",
  Lencana: "Badges",
  Gelap: "Dark",
  Terang: "Light",
  Bahasa: "Language",
  Notifikasi: "Notifications",
  Keluar: "Log Out",
  Lewati: "Skip",
  Mudah: "Easy",
  Sedang: "Medium",
  Sulit: "Hard",
  Ahli: "Expert",
  Belajar: "Learn",
  Selidiki: "Investigate",
  Tuntaskan: "Complete",
  Putar: "Play",
  Jeda: "Pause",
  "Pilih Kasus": "Choose Case",
  "Efek Suara": "Sound Effects",
  "Musik latar": "Background music",
  "Mode Gelap": "Dark Mode",
  "Reset Progres": "Reset Progress",
  "Progres Level": "Level Progress",
  "Fase Belajar": "Study Phase",
  "Saring data": "Filter data",
  Ditemukan: "Found",
  baris: "rows",
  bukan: "not",
  mengandung: "contains",
  "sama dengan": "equals",
  Tampilkan: "Show",
  "Total XP": "Total XP",
  "Yakin? Klik lagi": "Sure? Click again",
  "Pakai jumlah ini": "Use this count",
  "Serahkan bukti": "Submit evidence",
  "+ Syarat": "+ Condition",
  "Kasus selesai": "Case solved",
  "Kasus selesai!": "Case solved!",
};

// Pola kalimat dinamis dan terjemahannya
const RXD = [
    [/^Langkah (\d+) dari (\d+)$/, "Step $1 of $2"],
    [/^Kasus selesai: (\d+)\/(\d+)$/, "Cases done: $1/$2"],
    [/^Materi (\d+)\/(\d+)$/, "Lesson $1/$2"],
    [/^(\d+) \/ (\d+) XP menuju level berikutnya$/, "$1 / $2 XP to the next level"],
  ],
  RXR = [
    [/^Step (\d+) of (\d+)$/, "Langkah $1 dari $2"],
    [/^Cases done: (\d+)\/(\d+)$/, "Kasus selesai: $1/$2"],
    [/^Lesson (\d+)\/(\d+)$/, "Materi $1/$2"],
    [/^(\d+) \/ (\d+) XP to the next level$/, "$1 / $2 XP menuju level berikutnya"],
  ];

// Terjemahan kalimat panjang
const PHD = {
  "SELAMAT DATANG!": "WELCOME!",
  "SELAMAT KAMU BERHASIL MEMBUAT AKUN": "YOU HAVE SUCCESSFULLY CREATED AN ACCOUNT",
  "Mengalihkan ke halaman masuk...": "Redirecting to sign in...",
  "Buat akun detektifmu untuk memulai penyelidikan.":
    "Create your detective account to start investigating.",
  "Isi email yang valid.": "Enter a valid email.",
  "Password minimal 4 karakter.": "Password must be at least 4 characters.",
  "Akun dibuat. Silakan masuk.": "Account created. Please sign in.",
  "GAME EDUKASI • KEAMANAN SIBER": "EDUCATIONAL GAME • CYBER SECURITY",
  "Selidiki kejahatan digital lewat kasus seru, tanpa koding dan tanpa risiko nyata.":
    "Investigate digital crimes through exciting cases, with no coding and no real risk.",
  "Kenali modus kejahatan": "Recognize criminal tactics",
  "Pelajari phishing, tebak sandi, dan kebocoran data lewat kasus nyata.":
    "Learn about phishing, password guessing, and data leaks through realistic cases.",
  "Selidiki seperti detektif": "Investigate like a detective",
  "Periksa tabel, browser, CCTV, dan papan bukti untuk menemukan pelaku.":
    "Check tables, browser, CCTV, and the evidence board to find the culprit.",
  "Dapatkan EXP dan naik level": "Earn XP and level up",
  "Setiap bukti yang tepat memberi EXP. Makin teliti, makin tinggi levelmu.":
    "Every correct piece of evidence earns XP. The more careful you are, the higher your level.",
  "CARA BERMAIN": "HOW TO PLAY",
  "Tata cara bermain": "How to play",
  "Di meja detektif, buka folder": "At the detective desk, open the folder",
  "lalu pilih level.": "then choose a level.",
  "Baca materi edukasi singkat sebelum kasus dimulai.":
    "Read a short lesson before the case starts.",
  "Selidiki lewat Tabel, Browser, CCTV, dan Foto, lalu klik bukti yang kamu temukan.":
    "Investigate with Tables, Browser, CCTV, and Photos, then click the evidence you find.",
  "Tiap bukti yang tepat memberi EXP. Kasus tuntas membuka level berikutnya.":
    "Each correct piece of evidence earns XP. Completing a case unlocks the next level.",
  "BUKA MEJA DETEKTIF": "OPEN DETECTIVE DESK",
  "Semua skenario fiktif: belajar aman tanpa risiko nyata":
    "All scenarios are fictional: learn safely with no real risk",
  "Baca materi singkat ini sebelum menyelidiki.": "Read this short lesson before investigating.",
  "Pesan masuk": "Incoming message",
  "Mulai Penyelidikan": "Start Investigation",
  Sebelumnya: "Previous",
  Selanjutnya: "Next",
  "Kembali ke Desktop": "Back to Desktop",
  "Layar Awal": "Start Screen",
  "Petunjuk (−20 XP)": "Hint (−20 XP)",
  "Belum ada bukti. Klik sel di tabel.": "No evidence yet. Click a cell in a table.",
  "Bukti dipilih:": "Selected evidence:",
  "(kosongkan nilai untuk menampilkan semua)": "(leave the value empty to show everything)",
  "lebih dari / sesudah": "greater than / after",
  "kurang dari / sebelum": "less than / before",
  "Susun bubble di bawah menjadi sebuah perintah.": "Arrange the bubbles below into a command.",
  "Klik angka hasilnya untuk dijadikan bukti.": "Click the result number to use it as evidence.",
  "Tidak ada data yang cocok.": "No matching data.",
  "Tepat! Langkah berikutnya terbuka.": "Correct! The next step is unlocked.",
  "Bukti ditolak: belum cocok dengan petunjuk. Periksa lagi datanya.":
    "Evidence rejected: it does not match the clues. Check the data again.",
  "Sesuaikan pengalaman bermain sesuai keinginanmu.": "Customize your play experience.",
  "Antarmuka diterjemahkan. Isi kasus tetap berbahasa Indonesia.":
    "The interface is translated. Case content stays in Indonesian.",
  "Langkah kecil adalah bagian dari solusi besar.": "Small steps are part of a big solution.",
  "Masuk untuk melanjutkan penyelidikan": "Sign in to continue investigating",
  "Buat akun detektifmu": "Create your detective account",
  "Belum punya akun?": "No account yet?",
  "Sudah punya akun?": "Already have an account?",
  "Demo: nama dan sandi bebas. Progres tersimpan di perangkat ini.":
    "Demo: any name and password works. Progress is saved on this device.",
  "Isi username terlebih dahulu.": "Enter a username first.",
  "Progres direset.": "Progress reset.",
  "1. Buka ikon ": "1. Open the ",
  "2. Pilih level dan baca edukasinya.": "2. Choose a level and read its lesson.",
  "3. Cari bukti di Tabel dan Browser.": "3. Find evidence in Tables and Browser.",
  ": selidiki kejahatan digital tanpa koding.": ": investigate digital crimes without coding.",
  "Menu Kantin Hari Ini": "Menu",
};

// Membalik kamus untuk terjemahan arah sebaliknya
const inv = (o) => Object.fromEntries(Object.entries(o).map(([a, b]) => [b, a]));

// Terjemahkan seluruh teks di dalam sebuah elemen
function tr(root, to) {
  if (!root) return;
  const M = to == "en" ? EXD : inv(EXD),
    P = to == "en" ? PHD : inv(PHD),
    R = to == "en" ? RXD : RXR,
    ks = Object.keys(P).sort((a, b) => b.length - a.length),
    w = root.nodeType == 3 ? [root] : [],
    tw = root.nodeType == 3 ? null : document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  while (tw && tw.nextNode()) w.push(tw.currentNode);
  w.forEach((n) => {
    if (n.parentNode && /^(SCRIPT|STYLE|TEXTAREA)$/.test(n.parentNode.nodeName)) return;
    const m = n.data.match(/^([^A-Za-z]*)(.*?)(\s*)$/s);
    if (!m || !m[2]) return;
    let c = m[2],
      o = c;
    if (M[c]) c = M[c];
    else {
      R.forEach(([r, t]) => {
        if (r.test(c)) c = c.replace(r, t);
      });
      if (c == o)
        ks.forEach((k) => {
          if (c.includes(k)) c = c.split(k).join(P[k]);
        });
    }
    if (c != o) n.data = m[1] + c + m[3];
  });
}

// Terjemahkan otomatis elemen baru yang muncul saat bahasa Inggris aktif
new MutationObserver((ms) => {
  if (S.lg != "en") return;
  ms.forEach((m) => m.addedNodes.forEach((n) => tr(n, "en")));
}).observe(document.body, { childList: true, subtree: true });
