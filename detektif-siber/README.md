# Detektif Siber

Versi desktop utama proyek ini adalah aplikasi Python native. `reference-web/`
dipertahankan sebagai referensi versi web dan sumber gambar.

## Struktur

```text
detektif-siber/
├── reference-web/          # Versi web: HTML, CSS, JavaScript, dan gambar
├── native-python/          # Aplikasi desktop Python native dan data kasus
├── design-reference/       # Screenshot UI/UX sebelum dan sesudah revisi
├── .vscode/                # Pengaturan tampilan Explorer workspace
└── requirements-desktop.txt
```

### Versi web referensi

`reference-web/` berisi `index.html`, `css/`, `js/`, dan `img/`. Untuk menjalankan
versi web referensi, buka `reference-web/index.html` di browser.

### Full Python native

`native-python/` berisi `native_app.py` dan data kasus di `data/`. Gambar ikon
dipakai langsung dari `reference-web/img/`, sehingga tidak perlu ada salinan
asset yang mudah berbeda. Jalankan `python native_app.py` dari folder tersebut.
Untuk membuat build Windows, jalankan `.\build_native_windows.ps1`.
Installer Full Python Native disimpan terpisah di
`dist\Full Python Native\DetektifSiber-Full-Python-Native-Setup.exe`.
Musik latar dan efek suara dibuat langsung oleh aplikasi (tanpa unduhan) dan
bisa diaktifkan atau dimatikan melalui menu Pengaturan.

#### Mode lokal tanpa database

Edisi native saat ini tidak memerlukan database, server, email, atau akun
online. Masukkan nama detektif untuk mulai bermain. Progres disimpan sebagai
`progress.json` di `%APPDATA%\Detektif Siber\Detektif Siber` dan tetap ada
setelah aplikasi ditutup. Progres tidak disinkronkan ke perangkat lain; salin
file tersebut jika ingin membuat cadangan atau memindahkannya secara manual.
Satu profil lokal digunakan pada satu perangkat; mengganti nama detektif akan
memulai progres baru agar progres profil sebelumnya tidak tercampur.

### Dependensi desktop

Di root proyek, jalankan `python -m pip install -r requirements-desktop.txt`.
Build installer membutuhkan Inno Setup. Skrip build menyimpan file aplikasi di
folder edisi masing-masing.

## Data kasus native

`native-python/tools/export_reference_data.js` membuat ulang
`native-python/data/game_data.json` dari data level dan materi di `reference-web/js/`.
Jalankan dari folder mana pun dengan:

```powershell
node .\native-python\tools\export_reference_data.js
```

Untuk menambah level, tambahkan file ke `reference-web/js/levels/`, daftarkan di
`reference-web/js/levels/index.js`, lalu jalankan skrip ekspor di atas agar data
native ikut diperbarui.

## Referensi UI/UX

Screenshot desain ada di `design-reference/uiux-correct/` dan
`design-reference/uiux-before/`.
