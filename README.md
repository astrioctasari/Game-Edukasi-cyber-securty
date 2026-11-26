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

#### Integrasi Database & Autentikasi Supabase

Edisi native terhubung ke **Supabase** (`https://dgpnfsdvypvgfnddpfel.supabase.co`) melalui `native-python/supabase_client.py` dan konfigurasi di `native-python/data/supabase_config.json` (dapat di-override dengan environment variable `SUPABASE_URL` dan `SUPABASE_KEY`):

- **Autentikasi Akun (Supabase Auth — OTP & Password)**: Dilengkapi layar **Login** (`Login.exe`, dengan **Login OTP** sebagai metode utama dan tab **Password** sebagai opsi alternatif), **Sign Up** (`SignUp.exe`), **Konfirmasi Pembuatan Akun** (`Alert.exe`), serta **Reset Password** (`ResetPassword.exe` maupun langsung dari jendela **Profil**). Mendukung deteksi tautan verifikasi/OTP email otomatis via listener lokal `localhost:3000` maupun input kode OTP 6 digit (`{{ .Token }}` pada template email Magic Link Supabase).
- **Edit Profil & Simpanan Game (Export / Import)**: Di dalam jendela **Profil** pemain dapat mengubah *Username*, *Nama Tampilan*, *Bio/Motto*, dan *Karakter*, mengubah/mereset *Password*, serta melakukan **Export Save** dan **Import Save** berformat `.json` (tersedia juga di jendela **Pengaturan**) yang langsung tersinkron ke Supabase.
- **Konten Game & Progres Cloud**: Materi panduan (`game_lessons`), 11 level kasus (`game_levels`), dan wallpaper (`game_config`) dimuat dari Supabase dengan fallback otomatis ke `native-python/data/game_data.json` bila offline. Progres pemain tersimpan di tabel `player_profiles` sekaligus di-cache lokal pada `%APPDATA%\Detektif Siber\Detektif Siber\progress.json`.
- **Migrasi Skema**: Definisi lengkap tabel dan kebijakan RLS tersedia di folder `supabase/migrations/`.

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
