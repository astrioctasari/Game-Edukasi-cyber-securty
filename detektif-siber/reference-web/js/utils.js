// Fungsi kecil yang dipakai di banyak tempat.

// $ = ambil elemen, T = ubah baris data menjadi objek berdasarkan nama kolom
const $ = (s) => document.querySelector(s),
  T = (h, r) => r.map((x) => Object.fromEntries(h.map((k, i) => [k, x[i]])));

// Amankan teks sebelum dimasukkan ke HTML
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
