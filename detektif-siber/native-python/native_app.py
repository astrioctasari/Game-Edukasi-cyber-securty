#!/usr/bin/env python3
"""Native Python edition of Detektif Siber (PySide6).

This is a widget-for-widget port of the browser edition's desktop UI: the
painted wallpaper, draggable in-desktop windows, taskbar, notebook cards,
level tiles, the guide book, and all investigation tools.  No web view is
used; every screen is built from Qt widgets and painted SVG.
"""

from __future__ import annotations

import html
import json
import logging
import math
import re
import struct
import sys
import wave
from pathlib import Path
from typing import Callable, NoReturn

from PySide6.QtCore import (
    QEvent,
    QPoint,
    QPointF,
    QRect,
    QRectF,
    QSize,
    Qt,
    QStandardPaths,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QComboBox,
    QCompleter,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
APP_TITLE = "Detektif Siber"
TASKBAR_H = 40
INK = "#111"
DEEP = "#0d0f24"
BLUE = "#6cc4ff"
CYAN = "#3dc6ff"
PAPER = "#f3f3f3"
PANEL = "#f3f4ff"
YELLOW = "#fff1c1"
GREEN = "#e4f2ff"
RED = "#d9483a"
MUTED = "#666"
PURPLE = "#3d4bb8"

COL = ["#ff7a6b", "#6cc4ff", "#3dc6ff", "#ffd95a", "#a9b3ff"]
AVS = [("#ff7a6b", "gc"), ("#8f9bff", "c"), ("#38bdf8", "g"), ("#ffd95a", "gb")]
RANKS = [
    "Detective Trainee",
    "Junior Analyst",
    "Analyst",
    "Senior Analyst",
    "Chief Detective",
]
BIC = ["🗒️", "📦", "📞", "💬", "📶", "🔳", "📱", "🛒", "🎣", "📝", "🗄️"]
BANNER_COLORS = ["#ff7a6b", "#6cc4ff", "#3dc6ff", "#ffd95a", "#a9b3ff"]
DIFFICULTY = {"Mudah": "#38bdf8", "Sedang": "#ffb08a", "Sulit": "#a9b3ff", "Ahli": "#a9b3ff"}

ICON_FILES = {
    "halo": "penyelidik",
    "kasus": "kasus",
    "edu": "buku-panduan",
    "profil": "profil",
    "set": "pengaturan",
    "berkas": "berkas",
    "pesan": "pesan",
    "tabel": "tabel",
    "term": "terminal",
    "cctv": "cctv",
    "papan": "papan-bukti",
    "rek": "foto-tkp",
    "web": "browser",
}

# English translations for the interface and game content.
EN = {
    "Berkas": "Case File",
    "Tabel": "Table",
    "Terminal": "Terminal",
    "Papan Bukti": "Evidence Board",
    "Foto TKP": "Crime Scene",
    "Browser": "Browser",
    "Buku Panduan": "Guide Book",
    "Profil": "Profile",
    "Pengaturan": "Settings",
    "Selamat Datang": "Welcome",
    "Kasus": "Cases",
    "Musik latar": "Background music",
    "Efek Suara": "Sound effects",
    "Bahasa": "Language",
    "Reset Progres": "Reset progress",
    "Ganti Nama": "Change name",
    "Serahkan bukti": "Submit evidence",
    "Petunjuk (−20 XP)": "Hint (−20 XP)",
    "Belum ada bukti dipilih": "No evidence selected",
    "Terkunci": "Locked",
    "Kasus selesai": "Case closed",
    "Kembali": "Back",
    "Sebelumnya": "Previous",
    "Selanjutnya ▸": "Next ▸",
    "Lewati": "Skip",
    "Lewati ▸▸": "Skip ▸▸",
    "Mulai Penyelidikan": "Start investigating",
    "Layar Awal": "Start screen",
    "Desktop": "Desktop",
    "Ditemukan": "Found",
    "Reset": "Reset",
    "Beranda": "Home",
    "Jalankan": "Run",
    "Hapus": "Undo",
    "Bersihkan": "Clear",
    "Detektif Siber": "Cyber Detective",
    "DETEKTIF": "CYBER",
    "SIBER": "DETECTIVE",
    "Error": "Incorrect answer",
    "Langkah": "Step",
    "Nama detektif untuk progres lokal": "Detective name for local progress",
    "Mulai bermain": "Start playing",
    "Progres hanya tersimpan di perangkat ini.": "Progress is saved on this device only.",
    "Isi nama detektif terlebih dahulu.": "Enter a detective name first.",
    "Sesuaikan pengalaman bermain sesuai keinginanmu.": "Customize your play experience.",
    "Level": "Level",
    "Mudah": "Easy",
    "Sedang": "Medium",
    "Sulit": "Hard",
    "Ahli": "Expert",
    "Karakter": "Character",
    "Lencana": "Badges",
    "Total XP": "Total XP",
    "XP menuju level berikutnya": "XP to the next level",
    "Langkah kecil adalah bagian dari solusi besar.":
        "Small steps are part of a big solution.",
    "Selamat datang,": "Welcome,",
    "Tiap bab yang dibaca memberi +10 EXP.": "Each chapter you read gives +10 XP.",
    "Pilih bab di sisi kanan": "Choose a chapter on the right",
    "BUKU PANDUAN": "GUIDE BOOK",
    "BAB": "CHAPTER",
    "Materi": "Lesson",
    "Baca materi singkat ini sebelum menyelidiki.": "Read this short lesson before investigating.",
    "Selanjutnya": "Next",
    "Pesan masuk": "Incoming message",
    "Bukti dipilih:": "Selected evidence:",
    "Tampilkan": "Show",
    "semua kolom": "all columns",
    "dari tabel": "from table",
    "yang": "where",
    "dan": "and",
    "mirip pola": "matches pattern",
    "lebih dari": "greater than",
    "kurang dari": "less than",
    "urutkan menurut": "sort by",
    "dari terbesar": "descending",
    "Perintah": "Command",
    "Kolom": "Columns",
    "Operator": "Operator",
    "Nilai": "Values",
    "Kembali ke hasil": "Back to results",
    "Ketik nama pengguna": "Enter a username",
    "Ketik kata sandi": "Enter a password",
    "salah": "incorrect",
    "jawaban": "answer",

    "Sticky Note Sandi": "The Sticky Note Password",
    "Akun kasir dipakai orang saat toko sudah tutup.":
        "Someone used the cashier account after the shop had closed.",
    "Akun kasir toko dipakai orang pas toko sudah tutup. Padahal sandinya cuma aku yang tahu!":
        "Someone used the shop's cashier account after closing. I thought I was the only one who knew the password!",
    "Sandinya disimpan di mana, Mbak?": "Where did you keep the password?",
    "Hmm... di <u data-v='Sticky note'>sticky note kuning</u> yang nempel di monitor. Hehe.":
        "Hmm... on the yellow <u data-v='Sticky note'>sticky note</u> stuck to the monitor.",
    "Toko tutup jam 21:00. Kapan akun kasir dipakai setelah toko tutup? Klik waktunya.":
        "The shop closes at 9:00 PM. When was the cashier account used afterward? Select the time.",
    "Menurut cerita Mbak Sari, di mana sandi itu disimpan? Klik jawabannya.":
        "According to Sari, where was the password kept? Select the answer.",
    "Cari tahu di Browser: bagaimana cara menyimpan sandi yang lebih aman? Klik jawabannya.":
        "Search the Browser: what is a safer way to store passwords?",
    "Buka Tabel dan lihat kolom Waktu. Hanya satu login yang lewat dari jam 21:00.":
        "Open Tables and check the Time column. Only one login was after 9:00 PM.",
    "Di Browser cari: simpan sandi aman.": "Search the Browser for: store passwords safely.",
    "Orang iseng membaca sandi dari sticky note di monitor lalu login setelah toko tutup. Jangan tempel sandi di tempat yang bisa dilihat orang, ya!":
        "Someone read the password from the sticky note and logged in after closing. Never leave passwords where others can see them.",
    "SMS Paket Palsu": "The Fake Parcel SMS",
    "SMS minta biaya untuk paket yang tidak kamu pesan.":
        "A text asks you to pay a fee for a package you never ordered.",
    "Aku nggak merasa belanja apa-apa belakangan ini.": "I haven't ordered anything lately.",
    "Kak, jangan langsung klik. Cek dulu ya.": "Don't click it right away. Check it first.",
    "Baca SMS di jendela Pesan. Klik alamat tautan yang janggal.":
        "Read the text in Messages and select the suspicious link.",
    "Periksa domain itu di Browser. Kapan didaftarkan? Klik tanggalnya.":
        "Check the domain in the Browser. When was it registered?",
    "Adakah pesanan berstatus Dikirim di Pesanan Saya?":
        "Are any orders in My Orders marked as Shipped?",
    "Cari alamat web di SMS. Kurir resmi memakai alamat seperti jne.co.id.":
        "Check the web address in the text. The official courier uses jne.co.id.",
    "Di Browser cari: cek domain jne cek paket.": "Search the Browser for: check the JNE parcel domain.",
    "Di Tabel: Status sama dengan Dikirim. Jumlah 0 berarti tidak ada paket yang sedang dikirim.":
        "In Tables, filter Status to Shipped. A count of 0 means no package is being delivered.",
    "SMS itu penipuan: tautannya palsu dan kamu memang tidak punya paket yang sedang dikirim. Jangan klik, hapus saja, dan cek resi hanya lewat aplikasi resmi.":
        "The text is a scam: the link is fake, and you have no package on the way. Delete it and check tracking only in the official app.",
    "Telepon CS Palsu": "The Fake Bank Support Call",
    "Penelepon mengaku dari bank dan minta kode OTP.":
        "A caller claims to be from the bank and asks for your one-time code.",
    "Halo, kami CS bank. Ada transaksi mencurigakan. Mohon sebutkan kode OTP yang baru dikirim.":
        "Hello, this is bank support. We found a suspicious transaction. Please tell us the one-time code we just sent.",
    "OTP? Aku memang baru dapat kode di SMS tadi.": "A one-time code? I just received one by text.",
    "Nak, jangan kasih kode itu ke siapa pun ya!": "Never give that code to anyone!",
    "Penelepon yang mengaku dari bank itu nomornya berapa? Klik nomornya.":
        "Which number called claiming to be from the bank?",
    "Berapa kali nomor itu menelepon?": "How many times did that number call?",
    "Cari di Browser: apa aturan bank soal OTP? Klik jawabannya.":
        "Search the Browser: what is the bank's rule about one-time codes?",
    "Di Tabel pilih Log Telepon, saring Catatan sama dengan Mengaku dari bank.":
        "In Tables, open Call Log and filter Notes to 'Claimed to be from the bank'.",
    "Saring Log Telepon: Nomor sama dengan nomor tadi. Lihat jumlahnya, lalu klik 📌 Pakai jumlah ini.":
        "Filter Call Log by the number you found, then select the count.",
    "Di Browser cari: aturan bank OTP.": "Search the Browser for: bank OTP rules.",
    "Penelepon itu penipu rekayasa sosial: menelepon 3 kali dan menekan agar kamu menyebut OTP. OTP tidak boleh diberikan ke siapa pun, termasuk yang mengaku dari bank.":
        "The caller used social engineering, calling three times and pressuring you to reveal a one-time code. Never share it, even with someone claiming to be from your bank.",
    "Link WA dari Teman": "A WhatsApp Link from a Friend",
    "Teman tiba-tiba kirim link kuota gratis.":
        "A friend suddenly sends a link promising free mobile data.",
    "Gaes klik link ini, kuota 50GB gratis! kuota-gratis-wa.xyz/dapat":
        "Hey, click this link for 50 GB of free data! kuota-gratis-wa.xyz/dapat",
    "Kok tumben Dinda kirim begini jam 2 pagi?": "Why is Dinda sending this at 2 AM?",
    "Aku nggak kirim apa-apa! HP-ku mungkin dibobol.": "I didn't send anything! My phone may be compromised.",
    "Link tadi dikirim dari perangkat apa? Klik nama perangkatnya.":
        "Which device sent that link? Select its name.",
    "Buka link itu di Browser. Apa yang diminta halaman itu? Klik permintaannya.":
        "Open the link in the Browser. What does the page ask for?",
    "Dinda ingin akunnya kembali. Cari panduannya di Browser, lalu klik langkah yang benar.":
        "Dinda wants her account back. Find the guide in the Browser and select the right step.",
    "Di Tabel saring: Pengirim sama dengan Dinda, lalu Perangkat bukan HP Dinda.":
        "In Tables, filter Sender to Dinda and Device to anything other than Dinda's phone.",
    "Di Browser cari: kuota gratis wa.": "Search the Browser for: free WhatsApp data.",
    "Di Browser cari: panduan akun whatsapp diretas.": "Search the Browser for: recover a hacked WhatsApp account.",
    "Akun Dinda diambil alih lewat kode verifikasi yang dipancing. Kalau teman tiba-tiba mengirim link aneh, konfirmasi lewat telepon sebelum klik.":
        "Dinda's account was taken over using a trick to steal her verification code. Call a friend to confirm before opening an unexpected link.",
    "WiFi Kafe Palsu": "The Fake Cafe Wi-Fi",
    "WiFi gratis dengan nama mirip kafe.": "Free Wi-Fi with a name similar to the cafe's.",
    "Ada 3 WiFi di kafe: KopiSenja, KopiSenja_FREE, KopiSenja-Guest. Pilih yang mana ya?":
        "There are three networks: KopiSenja, KopiSenja_FREE, and KopiSenja-Guest. Which one should I use?",
    "WiFi kami KopiSenja, sandinya ada di struk.": "Our Wi-Fi is KopiSenja. The password is on the receipt.",
    "Peringatan: ada jaringan di sekitar tanpa enkripsi.":
        "Warning: an unencrypted network is nearby.",
    "Ada berapa WiFi yang Keamanannya Terbuka?": "How many Wi-Fi networks have Open security?",
    "KopiSenja_FREE adalah WiFi kembaran: terbuka, sinyal kuat, nama mirip. Setelah tersambung, akun Instagram dan emailmu dimasuki dari luar negeri.":
        "KopiSenja_FREE is a fake hotspot: open, strong signal, and a similar name. After connecting, your Instagram and email accounts were accessed from abroad.",
    "Dari WiFi terbuka itu, mana yang meniru nama kafe? Klik namanya.":
        "Which open network is imitating the cafe's name?",
    "Setelah itu akunmu dimasuki dari luar negeri? Klik akun yang kena paling dulu.":
        "Which account was first accessed from abroad?",
    "SELECT * FROM Daftar WiFi WHERE Keamanan = 'Terbuka'":
        "SELECT * FROM Wi-Fi Networks WHERE Security = 'Open'",
    "SELECT * FROM Daftar WiFi WHERE Keamanan = 'Terbuka' AND Nama LIKE 'KopiSenja%'":
        "SELECT * FROM Wi-Fi Networks WHERE Security = 'Open' AND Name LIKE 'KopiSenja%'",
    "SELECT * FROM Login Akun WHERE Lokasi <> 'Indonesia'. Lihat waktu paling awal.":
        "SELECT * FROM Account Sign-ins WHERE Location <> 'Indonesia'. Find the earliest time.",
    "QRIS Kedai Kopi": "The Coffee Shop QR Code Scam",
    "Uang pelanggan masuk ke merchant yang tidak dikenal.":
        "Customer payments are going to an unknown merchant.",
    "Uang masuk ke rekening kok kurang ya? Padahal kedai ramai.":
        "Why are our payments short even though the cafe is busy?",
    "Ada stiker QRIS di meja 3, kayaknya baru ditempel.":
        "There's a QR code sticker on table 3. It looks new.",
    "Peringatan: beberapa transaksi masuk ke merchant tak dikenal.":
        "Warning: some payments went to an unknown merchant.",
    "Berapa transaksi yang masuk ke merchant selain Kedai Kopi Senja?":
        "How many transactions went to a merchant other than Kopi Senja Cafe?",
    "SELECT COUNT(*) FROM Transaksi QRIS WHERE Merchant <> 'Kedai Kopi Senja'":
        "SELECT COUNT(*) FROM QR Code Transactions WHERE Merchant <> 'Kopi Senja Cafe'",
    "SELECT * FROM Transaksi QRIS WHERE Merchant = 'TOKO ABC99'. Lihat kolom Meja.":
        "SELECT * FROM QR Code Transactions WHERE Merchant = 'TOKO ABC99'. Check the Table column.",
    "Transaksi ke merchant asing berasal dari meja mana? Klik mejanya.":
        "Which table did the payments to the unknown merchant come from?",
    "Cari di Browser: apa yang diperiksa sebelum membayar QRIS? Klik jawabannya.":
        "Search the Browser: what should you check before paying with a QR code?",
    "Ada stiker QRIS palsu yang ditempel di Meja 3. Empat pembayaran masuk ke rekening penipu. Periksa stiker QRIS secara berkala dan biasakan membaca nama merchant.":
        "A fake QR code sticker was placed on table 3. Four payments went to the scammer. Check QR code stickers regularly and verify the merchant name before paying.",
    "APK Premium Gratis": "The Free Premium APK",
    "Aplikasi musik premium gratis dari grup chat.":
        "A group chat offers a free premium music app.",
    "Wah mau coba. Tapi ini bukan dari toko aplikasi ya?": "I'd like to try it, but it's not from an app store, right?",
    "Aplikasi tidak dikenal meminta banyak izin.": "An unknown app is requesting many permissions.",
    "Berapa izin MusikPro yang tidak wajar untuk pemutar musik?":
        "How many MusikPro permissions are unusual for a music player?",
    "Izin mana yang bisa membaca kode OTP di SMS-mu? Klik izinnya.":
        "Which permission could read one-time codes in your texts?",
    "Cari di Browser: dari mana aplikasi sebaiknya diunduh? Klik jawabannya.":
        "Search the Browser: where should you download apps from?",
    "Di Browser cari: keamanan aplikasi apk.": "Search the Browser for: APK app safety.",
    "Unduh MusikPro Premium GRATIS (APK): musikpro-apk.xyz":
        "Download MusikPro Premium FREE (APK): musikpro-apk.xyz",
    "Cari izin yang berhubungan dengan SMS.": "Look for the permission related to text messages.",
    "SELECT * FROM Izin Aplikasi WHERE Aplikasi = 'MusikPro' AND Wajar = 'Tidak'":
        "SELECT * FROM App Permissions WHERE App = 'MusikPro' AND Expected = 'No'",
    "APK premium gratis adalah aplikasi jebakan: meminta akses SMS dan aksesibilitas untuk mencuri OTP dan mengendalikan HP. Unduh hanya dari toko resmi.":
        "The free premium APK is a trap: it requests text-message and accessibility access to steal codes and control the phone. Download apps only from official stores.",
    "Toko Online Palsu": "The Fake Online Store",
    "HP flagship cuma Rp 499.000, ulasannya bagus semua.":
        "A flagship phone for only Rp 499,000, with nothing but perfect reviews.",
    "HP flagship cuma Rp 499.000! Stok terbatas, transfer ke rekening toko sekarang.":
        "Flagship phones for only Rp 499,000! Limited stock. Transfer to the store now.",
    "Murah banget, ulasannya bagus semua lagi.": "That's so cheap, and all the reviews are great.",
    "Peringatan: banyak laporan penipuan dari toko ini.":
        "Warning: many scam reports have been filed about this store.",
    "Berapa ulasan bintang 5 dari akun yang baru dibuat (umur 0 hari)?":
        "How many five-star reviews came from newly created accounts (zero days old)?",
    "Cek toko itu di Browser. Rekening tujuan atas nama siapa? Klik namanya.":
        "Check the store in the Browser. Whose name is on the payment account?",
    "Berapa laporan korban yang memakai rekening 0812-5521-0001?":
        "How many victim reports mention account 0812-5521-0001?",
    "SELECT COUNT(*) FROM Ulasan Toko WHERE Bintang = 5 AND Umur Akun = 0":
        "SELECT COUNT(*) FROM Store Reviews WHERE Stars = 5 AND Account Age = 0",
    "SELECT * FROM Laporan Korban WHERE Rekening = '0812-5521-0001'":
        "SELECT * FROM Victim Reports WHERE Account = '0812-5521-0001'",
    "Toko palsu: ulasan bintang 5 muncul serentak dari akun baru, pembayaran ke rekening pribadi, dan 5 korban lain memakai rekening yang sama. Jangan transfer ke rekening pribadi dan cek umur domain.":
        "This store is fake: new accounts posted five-star reviews at the same time, payments go to a personal account, and five other victims used the same account. Avoid personal-account transfers and check the domain's age.",
    "Email Palsu": "The Fake Email",
    "Pegawai dikirimi email 'gaji ditahan'.": "Employees receive an email claiming their salary is being withheld.",
    "Beberapa pegawai melapor menerima email 'SEGERA verifikasi akun'. Ada yang sudah mengeklik.":
        "Several employees reported an email saying 'VERIFY YOUR ACCOUNT NOW.' Some have already clicked.",
    "Akun saya tiba-tiba minta login ulang. Aneh sekali.": "My account suddenly asked me to sign in again. That's strange.",
    "PERINGATAN 09:40: login berhasil dari luar negeri.":
        "ALERT 09:40: a successful sign-in came from abroad.",
    "Email palsu itu dikirim dari domain apa? Klik domainnya di tabel.":
        "Which domain sent the fake email?",
    "Buka Browser dan periksa domain palsu itu. Kapan domain itu didaftarkan? Klik tanggalnya.":
        "Check the fake domain in the Browser. When was it registered?",
    "Berapa orang mengeklik tautan ke domain palsu itu? Pakai 📌 jumlah.":
        "How many people clicked the link to the fake domain?",
    "Akun mana yang dibobol dari luar negeri? Klik nama akunnya.":
        "Which account was compromised from abroad?",
    "Buka CCTV Ruang Admin. Sosok mana yang curiga lalu berjalan melapor ke Admin IT? Klik sosoknya.":
        "Open the Admin Room CCTV. Who looks suspicious and walks over to report it to IT?",
    "Lihat ciri sosoknya di Foto TKP, lalu cocokkan dengan foto staf. Akun siapa dia? Klik namanya.":
        "Compare the person's features in the scene photo with the staff photos. Which account is theirs?",
    "Di Email Masuk, saring: Domain Pengirim bukan kampus.ac.id.":
        "In Incoming Email, filter Sender Domain to anything other than kampus.ac.id.",
    "Di Browser cari: cek domain kampus-verif.xyz.": "Search the Browser for: check kampus-verif.xyz domain.",
    "Di Catatan Klik, saring: Tujuan Tautan sama dengan kampus-verif.xyz.":
        "In Click Log, filter Link Destination to kampus-verif.xyz.",
    "Di Login Baru, saring: Negara bukan Indonesia.": "In New Sign-ins, filter Country to anything other than Indonesia.",
    "Putar CCTV dan perhatikan siapa yang berdiri lalu berjalan ke meja Admin IT.":
        "Play the CCTV and watch who stands up and walks to the IT desk.",
    "Cari di Browser: foto staf. Bandingkan warna baju dan kacamata.":
        "Search the Browser for: staff photos. Compare clothing and glasses.",
    "Email palsu dari kampus-verif.xyz menjebak 4 orang. Akun bu_ratna dipakai penyerang dari luar negeri.":
        "The fake kampus-verif.xyz email tricked four people. An attacker abroad used the bu_ratna account.",
    "Nilai Bocor": "The Leaked Grades",
    "Nilai mahasiswa berubah tengah malam.": "Student grades were changed at midnight.",
    "Saya tidur jam 9 malam. Itu bukan saya!": "I was asleep at 9 PM. That wasn't me!",
    "Dari Alamat IP mana nilai itu diubah? Klik IP-nya di tabel.":
        "Which IP address changed the grades?",
    "Berapa kali IP itu gagal login sebelum berhasil? Pakai tombol 📌 jumlah.":
        "How many failed sign-ins came from that IP before the successful one?",
    "Buka Browser dan cari tahu: IP itu berada di lokasi mana? Klik lokasi yang bergaris bawah.":
        "Find where that IP address is located in the Browser.",
    "Buka CCTV Lab Komputer 3 dan putar rekamannya. Sosok mana yang masuk lalu mengetik di PC-23 sekitar pukul 23:41? Klik sosoknya.":
        "Play the Computer Lab 3 CCTV. Who entered and used PC-23 around 11:41 PM?",
    "Lihat ciri sosok itu lebih jelas di Foto TKP (baju, kacamata, tas), lalu cocokkan dengan foto di internet. Siapa dia? Klik namanya di bawah foto.":
        "Compare the person's clothes, glasses, and bag with the online photos. Who is it?",
    "Di Perubahan Nilai, saring: Nilai Baru lebih dari 80. Perhatikan IP yang berulang.":
        "In Grade Changes, filter New Grade to greater than 80 and look for the repeated IP.",
    "Di Catatan Login: Alamat IP sama dengan 10.4.7.23, dan Hasil sama dengan GAGAL. Tekan 📌 Pakai jumlah ini.":
        "In Sign-in Log, filter IP Address to 10.4.7.23 and Result to Failed, then select the count.",
    "Di Browser cari: denah jaringan kampus. Cocokkan 10.4.7.x dengan lokasinya.":
        "Search the Browser for: campus network map. Match 10.4.7.x to its location.",
    "Putar CCTV dan lihat siapa yang masuk, lalu duduk di PC-23.":
        "Play the CCTV and watch who enters and sits at PC-23.",
    "Cari di Browser: galeri praktikum lab. Hati-hati, beberapa orang bajunya sama. Cek kacamata dan tas.":
        "Search the Browser for: lab class gallery. Some people wear similar clothes, so check the glasses and bag.",
    "Pelakunya Fajar. Ia menebak sandi Bu Wati berkali-kali dari Lab Komputer 3, lalu mengubah nilai.":
        "Fajar was responsible. He repeatedly guessed Bu Wati's password from Computer Lab 3, then changed the grades.",
    "Nilai beberapa mahasiswa berubah tengah malam. Tidak ada dosen yang mengaku. Tolong selidiki.":
        "Several students' grades changed around midnight. No instructor admits to it. Please investigate.",
    "PERINGATAN 23:35: akun dosen_wati aktif di luar jam kerja.":
        "ALERT 23:35: the dosen_wati account was active after hours.",
    "Data Pelanggan Bocor": "The Customer Data Leak",
    "Ada unduhan besar tengah malam.": "A large download happened after hours.",
    "Data pelanggan kita muncul di forum gelap. Cari tahu siapa yang mengambilnya.":
        "Our customer data appeared on a dark web forum. Find out who took it.",
    "PERINGATAN 22:15: unduhan sangat besar dari server data.":
        "ALERT 22:15: an unusually large download came from the data server.",
    "Saya pulang jam 5 sore. Sungguh bukan saya!": "I went home at 5 PM. It wasn't me!",
    "Akun mana yang mengunduh data amat besar? Klik nama akunnya di tabel.":
        "Which account downloaded an unusually large amount of data?",
    "Siapa pemilik akun itu? Cari di Browser (direktori karyawan), lalu klik namanya.":
        "Who owns that account? Find the employee directory in the Browser.",
    "Buka CCTV kantor dan putar sampai unduhan 22:15. Sosok mana yang duduk di meja Tono? Klik sosoknya.":
        "Play the office CCTV around 10:15 PM. Who sits at Tono's desk?",
    "Lihat ciri sosoknya di Foto TKP, lalu cocokkan dengan foto karyawan. Siapa dia? Klik namanya.":
        "Compare the person's features in the scene photo with employee photos. Who is it?",
    "Data itu dijual di internet. Di Browser, cari siapa username penjualnya dan klik username itu.":
        "The data is being sold online. Find the seller's username in the Browser.",
    "Di Akses File, saring: Unduh (MB) lebih dari 500.":
        "In File Access, filter Download (MB) to greater than 500.",
    "Di Browser cari: direktori karyawan.": "Search the Browser for: employee directory.",
    "Putar CCTV dan lihat siapa yang masuk lalu duduk di meja Tono.":
        "Play the CCTV and watch who enters and sits at Tono's desk.",
    "Cari di Browser: foto karyawan. Bandingkan warna baju, kacamata, dan topi. Absensi Gedung juga membantu.":
        "Search the Browser for: employee photos. Compare clothing, glasses, and hat. Building attendance may also help.",
    "Di Browser cari: forum jual data pelanggan.": "Search the Browser for: customer data sale forum.",
    "Dewi memakai akun Tono untuk mengunduh data saat Tono sudah pulang, lalu menjualnya di forum dengan username dw_anggi.":
        "Dewi used Tono's account to download the data after he had left, then sold it on a forum as dw_anggi.",
    "SELAMAT DATANG!": "WELCOME!",
    "Tata cara bermain": "How to play",
    "Akun dibuat": "Account created",
    "Tidak ada bukti dipilih": "No evidence selected",
    "Bukti diterima. Total XP: ": "Evidence accepted. Total XP: ",
    "Bukti diterima. Total XP:": "Evidence accepted. Total XP:",
    "KopiSenja_FREE": "KopiSenja_FREE",
    "SARING DATA": "FILTER DATA",
    "Toko tutup jam 21:00.": "The shop closes at 9:00 PM.",
    "Situs resmi": "Official site",
    "Paket Anda tertahan di gudang. Bayar biaya":
        "Your package is being held at the depot. Pay a fee",
    "Ada 3 WiFi di kafe:": "There are three Wi-Fi networks:",
    "Pilih yang mana ya?": "Which one should I use?",
    "Hmm...": "Hmm...",
    "TIDAK PERNAH": "NEVER",
    "Jangan klik, hapus saja": "Delete it without clicking",
    "Cek resi hanya lewat aplikasi resmi.": "Check tracking only in the official app.",
    "banyak dilaporkan sebagai penipuan.": "widely reported as a scam.",
    "CCTV Ruang Admin": "Admin Room CCTV",
    "CCTV Lab Komputer 3": "Computer Lab 3 CCTV",
    "Cari di internet...": "Search the internet...",
    "Tekan Petunjuk.": "Use a hint.",
    "Tepat! Langkah berikutnya terbuka.": "Correct! The next step is unlocked.",
    "Kasus selesai!": "Case solved!",
    "Saring datanya dulu, lalu klik 📌 Pakai jumlah ini.":
        "Filter the data, then select 📌 Use this count.",
    "Belum tepat.": "Not quite.",
    "Baca lagi pesan Mbak Sari di jendela Pesan. Klik teks yang bergaris bawah.":
        "Read Sari's message again and click the underlined text.",
    "Server: luar negeri": "Server: abroad",
    "Catatan: domain baru yang meniru situs resmi sering dipakai untuk phishing.":
        "Note: new domains imitating official sites are often used for phishing.",
    "Data itu dijual di internet.": "The data is being sold online.",
    "Penjual: dw_anggi": "Seller: dw_anggi",
    "Dewi Anggraini · Magang IT · suka kopi dan kucing.":
        "Dewi Anggraini · IT intern · likes coffee and cats.",

    "🔢 OTP: Kode Rahasiamu": "🔢 OTP: Your Secret Code",
    "OTP adalah kode sekali pakai untuk membuktikan bahwa itu benar-benar kamu. Penipu menelepon pura-pura dari bank lalu memintanya.":
        "A one-time password (OTP) proves it's really you. Scammers may pretend to be your bank and ask for it.",
    "Aturan emas: bank dan marketplace tidak pernah meminta OTP. Jangan berikan ke siapa pun.":
        "Golden rule: banks and marketplaces never ask for your OTP. Never share it.",
    "🔎 Bertanya ke Data (SQL)": "🔎 Asking Questions of Data (SQL)",
    "SQL adalah bahasa untuk bertanya ke data. Ada tiga bagian: SELECT (apa yang ditampilkan), FROM (dari tabel mana), WHERE (syaratnya). Di Terminal kamu tinggal menyusun bubble, tanpa mengetik.":
        "SQL is a language for querying data. SELECT chooses what to show, FROM chooses the table, and WHERE sets conditions. In the Terminal, arrange the bubbles without typing.",
    "Contoh: SELECT * FROM Log Telepon WHERE Catatan = 'Mengaku dari bank' artinya tampilkan semua panggilan yang dicatat mengaku dari bank.":
        "Example: SELECT * FROM Call Log WHERE Notes = 'Claimed to be from the bank' shows all calls with that note.",
    "🧮 SQL Lanjutan": "🧮 More SQL",
    "AND menggabungkan dua syarat. LIKE mencari pola ('Kopi%' berarti diawali Kopi). COUNT(*) menghitung jumlah baris.":
        "AND combines two conditions. LIKE searches for a pattern ('Kopi%' means it starts with Kopi). COUNT(*) counts rows.",
    "Tips: mulai dari pertanyaan sederhana, lalu persempit dengan syarat tambahan.":
        "Tip: start with a simple query, then narrow it with more conditions.",
    "📶 Waspada WiFi Publik": "📶 Beware of Public Wi-Fi",
    "WiFi terbuka tanpa sandi bisa dibuat penipu dengan nama mirip kafe. Datamu bisa disadap.":
        "Scammers can create password-free Wi-Fi networks with names similar to a cafe's and intercept your data.",
    "Tips: tanyakan nama dan sandi WiFi ke petugas, hindari login bank di WiFi publik, atau pakai data seluler.":
        "Tip: ask staff for the correct network and password, avoid banking on public Wi-Fi, or use mobile data.",
    "📦 Aplikasi di Luar Toko Resmi": "📦 Apps from Outside Official Stores",
    "File APK dari tautan atau grup sering disusupi. Tandanya: meminta izin berlebihan, misalnya membaca SMS.":
        "APK files from links or chat groups may be tampered with. Watch for excessive permissions, such as reading texts.",
    "Tips: unduh hanya dari toko aplikasi resmi dan periksa izin sebelum memasang.":
        "Tip: download only from official app stores and review permissions before installing.",
    "🛒 Toko Online Palsu": "🛒 Fake Online Stores",
    "Harga terlalu murah, ulasan sempurna yang muncul bersamaan, dan rekening pribadi adalah tanda toko palsu.":
        "Prices that are too low, perfect reviews posted together, and personal bank accounts are signs of a fake store.",
    "Tips: cek umur domain, baca ulasan bintang rendah, dan bayar lewat platform resmi.":
        "Tip: check the domain's age, read low-rated reviews, and pay through an official platform.",
    "🔳 QRIS Palsu": "🔳 Fake QR Codes",
    "Penipu menempel stiker QRIS sendiri menimpa yang asli, sehingga uang masuk ke rekening mereka.":
        "Scammers may cover the real payment code with their own sticker, sending money to their account.",
    "Tips: periksa nama merchant yang muncul di layar sebelum membayar.":
        "Tip: check the merchant name on screen before paying.",
    "🔑 Tebak Sandi (Brute Force)": "🔑 Password Guessing (Brute Force)",
    "Penyerang mencoba banyak kata sandi satu per satu sampai ada yang cocok. Tandanya: banyak GAGAL beruntun, lalu satu BERHASIL.":
        "An attacker tries many passwords until one works. A pattern of repeated failures followed by a success is a warning sign.",
    "Cegah: sandi panjang, batasi percobaan login, aktifkan verifikasi dua langkah.":
        "Protect yourself with long passwords, sign-in attempt limits, and two-step verification.",
    "🌐 Alamat IP": "🌐 IP Addresses",
    "Alamat IP mirip plat nomor perangkat di jaringan. Dari situ perangkat dan lokasinya bisa dilacak.":
        "An IP address is like a device's license plate on a network. It can help identify a device and its location.",
    "Catatan: IP bisa disamarkan (misalnya VPN), jadi cocokkan dengan bukti lain.":
        "Note: IP addresses can be masked (for example, by a VPN), so corroborate with other evidence.",
    "📜 Catatan Aktivitas (Log)": "📜 Activity Logs",
    "Sistem mencatat siapa melakukan apa, kapan, dan dari mana. Cari pola janggal: jam tak wajar, banyak gagal, perubahan besar.":
        "Systems record who did what, when, and from where. Look for unusual times, repeated failures, and major changes.",
    "Tips: simpan salinan log di tempat terpisah agar tak bisa dihapus pelaku.":
        "Tip: keep a separate copy of logs so an intruder cannot erase them.",
    "🎣 Waspada Phishing": "🎣 Beware of Phishing",
    "Pesan palsu yang menyamar jadi bank, kampus, atau atasan agar kamu menyerahkan sandi. Tandanya: mendesak, pengirim mirip tapi beda, tautan aneh.":
        "Fake messages impersonate a bank, school, or manager to steal passwords. Warning signs include urgency, lookalike senders, and odd links.",
    "Tips: jangan klik tautan dari pesan yang menekan. Buka situs resmi lewat pencarian sendiri.":
        "Tip: don't click links in urgent messages. Find the official site yourself.",
    "🔍 Cek Nama Domain": "🔍 Check the Domain Name",
    "Perhatikan bagian setelah @. 'kampus.ac.id' asli, sedangkan 'kampus-verif.xyz' hanya meniru.":
        "Check the part after @. 'kampus.ac.id' is genuine, while 'kampus-verif.xyz' is an imitation.",
    "Tips: tahan kursor pada tautan untuk melihat alamat aslinya sebelum diklik.":
        "Tip: hover over a link to inspect its real address before clicking.",
    "📲 Verifikasi Dua Langkah": "📲 Two-Step Verification",
    "Selain sandi, kamu perlu kode dari HP. Walau sandi bocor, penyerang tetap tertahan.":
        "In addition to a password, you need a code from your phone. A stolen password alone won't be enough.",
    "Tips: aktifkan untuk email, bank, dan akun kerja.":
        "Tip: enable it for email, banking, and work accounts.",
    "🤝 Jangan Pinjamkan Akun": "🤝 Don't Share Accounts",
    "Akun yang dipakai bersama membuat jejak jadi kabur: log menunjuk pemilik, padahal pelakunya orang lain.":
        "Shared accounts obscure the evidence: logs point to the owner even when someone else was responsible.",
    "Tips: tiap orang punya akun sendiri, dan keluar (logout) saat selesai.":
        "Tip: give everyone their own account and sign out when finished.",
    "🔐 Akses Secukupnya": "🔐 Limit Access",
    "Karyawan hanya perlu akses ke data yang dipakai kerjanya. Data pelanggan sebaiknya dibatasi dan unduhan besar dipantau.":
        "Employees should access only the data they need. Restrict customer data and monitor large downloads.",
    "Tips: beri peringatan otomatis untuk unduhan besar di luar jam kerja.":
        "Tip: set alerts for large downloads outside working hours.",
    "🗒️ Sandi Jangan Ditempel": "🗒️ Don't Put Passwords on Sticky Notes",
    "Menulis sandi di sticky note yang menempel di monitor sama saja membukakan pintu untuk siapa saja yang lewat. Bahkan kamera CCTV bisa ikut merekamnya.":
        "Writing a password on a sticky note on your monitor leaves it exposed to anyone passing by. A CCTV camera could record it too.",
    "Tips: jangan pakai sandi gampang seperti nama+123, simpan sandi di pengelola sandi (password manager), dan aktifkan verifikasi dua langkah.":
        "Tip: avoid easy passwords like a name plus 123. Use a password manager and enable two-step verification.",
    "Cari": "Search",
    "Selidiki": "Investigate",
    "Hitung": "Count",
    "Telusuri": "Explore",
    "Lacak": "Trace",
    "Pulihkan": "Recover",
    "Tangkap": "Catch",
    "Saksi": "Witness",
    "Cocokkan": "Match",
    "Bukti akhir": "Final evidence",
    "Kamu": "You",
    "Sistem": "System",
    "Ibu": "Mother",
    "Adik": "Sibling",
    "Barista": "Barista",
    "Kasir": "Cashier",
    "Direktur": "Director",
    "Kaprodi": "Department Chair",
    "No": "No.",
    "Akun": "Account",
    "Waktu": "Time",
    "Hasil": "Result",
    "Toko": "Store",
    "Barang": "Item",
    "Kurir": "Courier",
    "Nomor": "Number",
    "Durasi": "Duration",
    "Catatan": "Notes",
    "Pengirim": "Sender",
    "Pesan": "Message",
    "Perangkat": "Device",
    "Nama": "Name",
    "Keamanan": "Security",
    "Sinyal": "Signal",
    "Sandi": "Password",
    "Merchant": "Merchant",
    "Meja": "Table",
    "Nominal": "Amount",
    "Aplikasi": "App",
    "Izin": "Permission",
    "Wajar": "Expected",
    "Pengulas": "Reviewer",
    "Bintang": "Stars",
    "Umur Akun": "Account Age",
    "Domain Pengirim": "Sender Domain",
    "Subjek": "Subject",
    "Tujuan Tautan": "Link Destination",
    "Negara": "Country",
    "Mahasiswa": "Student",
    "Mata Kuliah": "Course",
    "Nilai Lama": "Previous Grade",
    "Nilai Baru": "New Grade",
    "Alamat IP": "IP Address",
    "File": "File",
    "Unduh (MB)": "Download (MB)",
    "Status": "Status",
    "Dikirim": "Shipped",
    "Selesai": "Completed",
    "BERHASIL": "SUCCESS",
    "GAGAL": "FAILED",
    "Mengaku dari bank": "Claimed to be from the bank",
    "Kontak tersimpan": "Saved contact",
    "Perangkat Baru": "New Device",
    "Terbuka": "Open",
    "Ya": "Yes",
    "Tidak": "No",
    "Luar Negeri": "Abroad",
    "Sticky note kuning": "yellow sticky note",
    "Cara Menyimpan Sandi dengan Aman": "How to Store Passwords Safely",
    "Simpan Sandi dengan Aman": "Store Passwords Safely",
    "Cara berisiko:": "Risky approach:",
    "menempel sandi di meja atau monitor": "leaving passwords on a desk or monitor",
    "Cara yang disarankan:": "Recommended approach:",
    "pakai pengelola sandi (password manager)": "use a password manager",
    "Cek Domain:": "Domain Check:",
    "Terdaftar:": "Registered:",
    "Pemilik: disembunyikan": "Owner: hidden",
    "Catatan: meniru nama kurir, banyak dilaporkan sebagai penipuan.":
        "Note: imitates a courier's name and has been widely reported as a scam.",
    "Situs resmi, terdaftar sejak 1990.": "Official site, registered since 1990.",
    "Pihak bank TIDAK PERNAH meminta OTP, PIN, atau password lewat telepon, SMS, atau chat.":
        "The bank will NEVER ask for your OTP, PIN, or password by phone, text, or chat.",
    "Hubungi call center resmi di nomor kartu.": "Call the official support number on your card.",
    "Masukkan nomor WA dan kode verifikasi 6 digit yang dikirim ke SMS-mu.":
        "Enter your WhatsApp number and the six-digit verification code sent by text.",
    "daftar ulang WhatsApp dengan nomor sendiri": "register WhatsApp again with your own number",
    "tunggu sampai penyerang bosan": "wait until the attacker gives up",
    "kirim kode verifikasi ke teman": "send a verification code to a friend",
    "Lalu aktifkan verifikasi dua langkah.": "Then enable two-step verification.",
    "Sebelum bayar, periksa nama merchant yang muncul di layar.":
        "Before paying, check the merchant name shown on screen.",
    "Sebelum bayar, periksa ": "Before paying, check ",
    "nama merchant": "merchant name",
    " yang muncul di layar.": " that appears on screen.",
    "Jika berbeda dari kedai, jangan bayar.": "If it doesn't match the cafe, don't pay.",
    "Unduh hanya dari toko aplikasi resmi. Hindari file APK dari tautan atau grup.":
        "Download only from official app stores. Avoid APK files from links or chat groups.",
    "Terdaftar: 5 hari lalu": "Registered: 5 days ago",
    "Pembayaran hanya ke rekening pribadi": "Payments only to a personal account",
    "Garansi: Garansi seumur hidup": "Warranty: Lifetime warranty",
    "Perhatikan pakaian dan atributnya.": "Look closely at clothing and accessories.",
    "Alamat IP dibagi menurut lokasi:": "IP addresses are assigned by location:",
    "Ruang Dosen": "Faculty Office",
    "Perpustakaan": "Library",
    "Lab Komputer 3": "Computer Lab 3",
    "Menu Kantin": "Cafeteria Menu",
    "Nasi goreng, soto ayam, es teh.": "Fried rice, chicken soup, and iced tea.",
    "Wisuda dilaksanakan 12 Oktober di aula utama.":
        "The graduation ceremony is on October 12 in the main hall.",
    "Forum: Jual Data Pelanggan": "Forum: Customer Data for Sale",
    "Dijual: data pelanggan": "For sale: customer data",
    "Penjual:": "Seller:",
    "Isi: 5.000 pelanggan lengkap. Bayar kripto.":
        "Contains details for 5,000 customers. Pay with cryptocurrency.",
    "Berita Internal:": "Internal News:",
    "Gathering kantor bulan depan.": "Office gathering next month.",
    "Situs resmi, terdaftar sejak 2005.": "Official site, registered since 2005.",
    "Khusus akhir pekan.": "This weekend only.",
    "Diskon 50%": "50% off",
    "Cek QRIS Asli": "Check the QR Code",
    "Cara Cek QRIS Asli": "How to Check a QR Code",
    "Keamanan Aplikasi": "App Safety",
    "Galeri Praktikum Lab Komputer 3": "Computer Lab 3 Class Gallery",
    "Direktori Karyawan": "Employee Directory",
    "Foto Karyawan": "Employee Photos",
    "Foto Staf": "Staff Photos",
    "Profil @dw_anggi": "Profile @dw_anggi",
    "Berita Kampus": "Campus News",
    "Wisuda Oktober": "October Graduation",
    "Menu": "Menu",
    "Baca folder Edukasi untuk cara mencegahnya.":
        "Read the Guide Book to learn how to prevent it.",
    "Langkah tidak tepat.": "Incorrect answer. Review the clue and try again.",
    "Belum ada bukti yang dipilih. Klik sel di Tabel, teks bergaris bawah di Browser, atau sosok di gambar.":
        "No evidence selected. Choose a table cell, underlined text in the Browser, or a person in the scene.",
    "Langkah ini meminta ANGKA jumlah, tapi yang kamu pilih":
        "This step needs a COUNT, but you selected",
    "Angka": "The number",
    "belum tepat. Periksa lagi syarat saringannya":
        "is not correct. Recheck the filter conditions",
    "Saring datanya dulu, lalu klik": "Filter the data, then select",
    "bukan angka.": "is not a number.",
    "Langkah ini bukan meminta angka, tapi kamu memilih":
        "This step does not ask for a number, but you selected",
    "Klik nama, tulisan, atau sosok yang diminta di tugas.":
        "Select the name, text, or person requested in the task.",
    "Belum tepat. Yang kamu pilih:": "Incorrect. You selected:",
    "Baca lagi tugas di Berkas, cek tabel, halaman, atau sosok yang disebut, atau tekan Petunjuk.":
        "Review the case file and check the table, web page, or person mentioned, or use a hint.",
    "Level 1": "Level 1",
    "Level 2": "Level 2",
    "Level 3": "Level 3",
    "Level 4": "Level 4",
    "Level 5": "Level 5",
    "Level 6": "Level 6",
    "Level 7": "Level 7",
    "Level 8": "Level 8",
    "Level 9": "Level 9",
    "Level 10": "Level 10",
    "Level 11": "Level 11",
}


def app_root() -> Path:
    bundle = getattr(sys, "_MEIPASS", None)
    return Path(bundle) if bundle else Path(__file__).resolve().parent


def image_root() -> Path:
    if getattr(sys, "_MEIPASS", None):
        return app_root() / "img"
    return app_root().parent / "reference-web" / "img"


def read_data() -> dict:
    path = app_root() / "data" / "game_data.json"
    return json.loads(path.read_text(encoding="utf-8"))


class GameAudio:
    """Generate and play the native edition's ambient music and sound effects."""

    sample_rate = 22050
    effects_notes = {
        180: (311.13, 233.08),
        660: (523.25, 659.25),
        780: (523.25, 659.25, 783.99),
    }

    def __init__(self, audio_dir: Path, parent: QWidget):
        audio_dir.mkdir(parents=True, exist_ok=True)
        self.sound_enabled = True
        self.music_enabled = False
        self.effects: dict[int, QSoundEffect] = {}
        for frequency, notes in self.effects_notes.items():
            source = audio_dir / f"tone-{frequency}.wav"
            self._write_effect(source, notes)
            effect = QSoundEffect(parent)
            effect.setSource(QUrl.fromLocalFile(str(source)))
            effect.setVolume(0.18)
            effect.statusChanged.connect(
                lambda e=effect, f=frequency: self._log_audio_error(e, f"tone {f}"))
            self.effects[frequency] = effect

        source = audio_dir / "ambient.wav"
        self._write_ambient(source)
        self.music_output = QAudioOutput(parent)
        self.music_output.setVolume(0.7)
        self.music_player = QMediaPlayer(parent)
        self.music_player.setAudioOutput(self.music_output)
        self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
        self.music_player.setSource(QUrl.fromLocalFile(str(source)))
        self.music_player.errorOccurred.connect(self._log_music_error)

    @classmethod
    def _write_ambient(cls, path: Path) -> None:
        duration = 16.0
        frame_count = int(cls.sample_rate * duration)
        chords = (
            (130.81, 164.81, 196.00),
            (110.00, 130.81, 164.81),
            (98.00, 116.54, 146.83),
            (87.31, 110.00, 130.81),
        )
        frames = bytearray(frame_count * 2)
        for index in range(frame_count):
            elapsed = index / cls.sample_rate
            chord_index = int(elapsed // 4.0) % len(chords)
            beat = elapsed % 0.75
            chord = chords[chord_index]
            pad = sum(
                math.sin(2 * math.pi * frequency * elapsed)
                + 0.18 * math.sin(4 * math.pi * frequency * elapsed)
                for frequency in chord
            ) * 0.055
            melody = chord[int(elapsed / 0.75) % len(chord)] * 2
            pluck = (math.sin(2 * math.pi * melody * elapsed)
                     * math.exp(-beat * 4.0) * 0.17)
            kick = (math.sin(2 * math.pi * 55 * beat)
                    * math.exp(-beat * 8.0) * 0.065)
            edge_fade = min(1.0, elapsed / 0.05, (duration - elapsed) / 0.05)
            sample = max(-0.75, min(0.75, (pad + pluck + kick) * edge_fade))
            struct.pack_into("<h", frames, index * 2, int(sample * 32767))

        with wave.open(str(path), "wb") as audio_file:
            audio_file.setnchannels(1)
            audio_file.setsampwidth(2)
            audio_file.setframerate(cls.sample_rate)
            audio_file.writeframes(frames)

    @classmethod
    def _write_effect(cls, path: Path, notes: tuple[float, ...]) -> None:
        note_duration = 0.14
        duration = note_duration * len(notes)
        frame_count = int(cls.sample_rate * duration)
        frames = bytearray(frame_count * 2)
        for index in range(frame_count):
            elapsed = index / cls.sample_rate
            note_index = min(int(elapsed / note_duration), len(notes) - 1)
            note_time = elapsed - note_index * note_duration
            envelope = min(1.0, note_time / 0.01) * (1 - note_time / note_duration)
            frequency = notes[note_index]
            sample = 0.22 * envelope * (
                math.sin(2 * math.pi * frequency * elapsed)
                + 0.16 * math.sin(4 * math.pi * frequency * elapsed)
            )
            struct.pack_into("<h", frames, index * 2, int(sample * 32767))

        with wave.open(str(path), "wb") as audio_file:
            audio_file.setnchannels(1)
            audio_file.setsampwidth(2)
            audio_file.setframerate(cls.sample_rate)
            audio_file.writeframes(frames)

    @staticmethod
    def _log_audio_error(effect: QSoundEffect, name: str) -> None:
        if effect.status() == QSoundEffect.Status.Error:
            logging.getLogger(__name__).warning("Could not load %s audio.", name)

    def play(self, frequency: int) -> None:
        effect = self.effects.get(frequency)
        if self.sound_enabled and effect is not None:
            effect.play()

    def set_sound_enabled(self, enabled: bool) -> None:
        self.sound_enabled = enabled

    def set_music_enabled(self, enabled: bool) -> None:
        self.music_enabled = enabled
        if enabled:
            if self.music_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
                self.music_player.play()
        else:
            self.music_player.pause()

    @staticmethod
    def _log_music_error(error: QMediaPlayer.Error, error_string: str) -> None:
        logging.getLogger(__name__).warning(
            "Could not play ambient music (%s): %s", error, error_string)


def esc(value) -> str:
    return html.escape(str(value), quote=False)


def strip_links(markup: str) -> str:
    text = re.sub(r"<u\s+data-v=(['\"])(.*?)\1\s*>(.*?)</u>", r"\3", markup, flags=re.I | re.S)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\s*>", "\n", text, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


# ---------------------------------------------------------------------------
# SVG graphics
# ---------------------------------------------------------------------------

def body_svg(color: str, marks: str = "") -> str:
    """Port of BODY() from js/data/graphics.js."""
    marks = marks or ""
    out = ""
    if "b" in marks:
        out += (
            f"<rect x='6' y='0' width='9' height='21' rx='3' fill='#1b6fd8' "
            "stroke='#0d0f24' stroke-width='1.5'/>"
        )
    out += (
        "<rect class='l1' x='-8' y='22' width='6' height='9' rx='2' fill='#2d3270'/>"
        "<rect class='l2' x='2' y='22' width='6' height='9' rx='2' fill='#2d3270'/>"
        f"<rect x='-9' y='-2' width='18' height='27' rx='8' fill='{color}' "
        "stroke='#0d0f24' stroke-width='1.5'/>"
        "<circle cy='-12' r='9' fill='#f6d9c0' stroke='#0d0f24' stroke-width='1.5'/>"
        "<path d='M-9 -13a9 9 0 0 1 18 0z' fill='#2d3270'/>"
    )
    if "c" in marks:
        out += (
            "<path d='M-10 -16Q0 -28 10 -16Z' fill='#fff' stroke='#0d0f24' stroke-width='1.5'/>"
            "<rect x='-3' y='-17' width='15' height='3' fill='#fff' stroke='#0d0f24' stroke-width='1.2'/>"
        )
    if "g" in marks:
        out += (
            "<rect x='-8' y='-14' width='7' height='5' rx='2' fill='#0d0f24'/>"
            "<rect x='1' y='-14' width='7' height='5' rx='2' fill='#0d0f24'/>"
        )
    return out


def body_svg_doc(color: str, marks: str = "", viewbox: str = "-20 -34 40 40") -> str:
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='{viewbox}'>"
        f"<rect x='-20' y='-34' width='40' height='40' fill='#20244a'/>"
        f"{body_svg(color, marks)}</svg>"
    )


_SVG_CACHE: dict[tuple[str, int], QPixmap] = {}


def icon_pixmap(key: str, size: int = 18) -> QPixmap:
    cache_key = (key, size)
    if cache_key in _SVG_CACHE:
        return _SVG_CACHE[cache_key]
    path = image_root() / "icons" / f"{key}.svg"
    pm = QPixmap(size * 2, size * 2)
    pm.setDevicePixelRatio(2)
    pm.fill(Qt.GlobalColor.transparent)
    if path.exists():
        renderer = QSvgRenderer(str(path))
        painter = QPainter(pm)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if renderer.isValid():
            renderer.render(painter, QRectF(0, 0, size, size))
        painter.end()
    _SVG_CACHE[cache_key] = pm
    return pm


def svg_pixmap(svg: str, width: int, height: int, dpr: float = 2.0) -> QPixmap:
    pm = QPixmap(max(1, int(width * dpr)), max(1, int(height * dpr)))
    pm.setDevicePixelRatio(dpr)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer = QSvgRenderer(svg.encode("utf-8"))
    if renderer.isValid():
        renderer.render(painter, QRectF(0, 0, width, height))
    painter.end()
    return pm


def avatar_pixmap(index: int, size: int = 84, dpr: float = 2.0) -> QPixmap:
    index = max(0, min(len(AVS) - 1, int(index)))
    color, marks = AVS[index]
    pm = QPixmap(int(size * dpr), int(size * dpr))
    pm.setDevicePixelRatio(dpr)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    rect = QRectF(1.5, 1.5, size - 3, size - 3)
    path = QPainterPath()
    path.addEllipse(rect)
    painter.setClipPath(path)
    painter.fillRect(QRectF(0, 0, size, size), QColor("#20244a"))
    renderer = QSvgRenderer(body_svg_doc(color, marks).encode("utf-8"))
    if renderer.isValid():
        renderer.render(painter, rect)
    painter.setClipping(False)
    painter.setPen(QPen(QColor(INK), 3))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawEllipse(rect)
    painter.end()
    return pm


def character_pixmap(color: str, marks: str) -> QPixmap:
    """Full-body sprite used by CCTV / crime-scene canvases."""
    doc = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='-20 -34 40 76'>"
        f"{body_svg(color, marks)}</svg>"
    )
    key = ("char", hash((color, marks)))
    cached = _SVG_CACHE.get(key)
    if cached is not None:
        return cached
    pm = svg_pixmap(doc, 40, 76, 2.0)
    _SVG_CACHE[key] = pm
    return pm


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def set_font(widget: QWidget, size: int = 14, bold: bool = False, italic: bool = False) -> None:
    font = widget.font()
    font.setFamilies(["Segoe UI", "Bricolage Grotesque", "Arial"])
    font.setPixelSize(size)
    font.setWeight(QFont.Weight.DemiBold if bold else QFont.Weight.Normal)
    font.setItalic(italic)
    widget.setFont(font)


def label(
    text: str = "",
    size: int = 14,
    bold: bool = False,
    color: str | None = None,
    wrap: bool = False,
    align=None,
    italic: bool = False,
    rich: bool = False,
) -> QLabel:
    lab = QLabel(text)
    set_font(lab, size, bold, italic)
    if color:
        lab.setStyleSheet(f"color:{color};background:transparent;")
    lab.setWordWrap(wrap)
    # Qt needs this policy hint to reserve enough vertical space for wrapped
    # copy when a screen is laid out inside a narrower scroll area.
    policy = lab.sizePolicy()
    policy.setHeightForWidth(wrap)
    if wrap:
        policy.setVerticalPolicy(QSizePolicy.Policy.Minimum)
    lab.setSizePolicy(policy)
    if align is not None:
        lab.setAlignment(align)
    if rich:
        lab.setTextFormat(Qt.TextFormat.RichText)
    return lab


def rich(text: str, size: int = 14, color: str | None = None, wrap: bool = True,
         align=None, bold: bool = False) -> QLabel:
    lab = label(text, size, bold, color, wrap, align, rich=True)
    lab.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    return lab


def hard_shadow(widget: QWidget, dx: int = 4, dy: int = 4, color: str = INK,
                alpha: int = 255) -> QGraphicsDropShadowEffect:
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(0)
    effect.setOffset(dx, dy)
    c = QColor(color)
    c.setAlpha(alpha)
    effect.setColor(c)
    widget.setGraphicsEffect(effect)
    return effect


def repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def button(
    text: str,
    callback=None,
    kind: str = "primary",
    size: int = 13,
    icon_key: str | None = None,
    shadow: bool = True,
    bold: bool = True,
) -> QPushButton:
    btn = QPushButton(text)
    btn.setProperty("kind", kind)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    set_font(btn, size, bold)
    if icon_key:
        btn.setIcon(QIcon(icon_pixmap(icon_key, 16)))
        btn.setIconSize(QSize(16, 16))
    if callback is not None:
        btn.clicked.connect(callback)
    if shadow and kind in ("primary", "white", "small", "big"):
        offset = 2 if kind in ("small", "big") else 1
        hard_shadow(btn, offset, offset, alpha=90)
    return btn


def icon_button(icon_key: str, callback=None, size: int = 34, tooltip: str = "") -> QToolButton:
    btn = QToolButton()
    btn.setIcon(QIcon(icon_pixmap(icon_key, size)))
    btn.setIconSize(QSize(size, size))
    btn.setAutoRaise(True)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setToolTip(tooltip)
    btn.setFixedSize(size + 8, size + 8)
    btn.setStyleSheet("QToolButton{background:transparent;border:0;}QToolButton:hover{background:#ffffff33;}")
    if callback is not None:
        btn.clicked.connect(callback)
    return btn


def line_edit(placeholder: str = "", text: str = "", password: bool = False) -> QLineEdit:
    edit = QLineEdit()
    edit.setPlaceholderText(placeholder)
    edit.setText(text)
    if password:
        edit.setEchoMode(QLineEdit.EchoMode.Password)
    set_font(edit, 14)
    return edit


def note_card(text: str, bg: str = "#fff", shadow: bool = True, pad: int = 14) -> QFrame:
    frame = QFrame()
    frame.setObjectName("noteCard")
    frame.setStyleSheet(f"QFrame#noteCard{{background:{bg};border:3px solid {INK};}}")
    if shadow:
        hard_shadow(frame, 6, 6)
    box = QVBoxLayout(frame)
    box.setContentsMargins(pad, pad - 3, pad, pad - 3)
    box.setSpacing(4)
    lab = rich(text, 14)
    box.addWidget(lab)
    return frame


def clear_layout(layout: QLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item is None:
            continue
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()
            continue
        child_layout = item.layout()
        if child_layout is not None:
            clear_layout(child_layout)


def content_height(content: QWidget, width: int) -> int:
    layout = content.layout()
    if layout is None:
        return content.sizeHint().height()
    if layout.hasHeightForWidth():
        height = layout.heightForWidth(max(120, width))
        if height > 0:
            return height
    return max(content.sizeHint().height(), content.minimumSizeHint().height())


def wrapped_height(sizes: list[QSize], width: int, hspacing: int = 2,
                   vspacing: int = 2) -> int:
    """Height taken by a flow of widgets at the given width."""
    x = 0
    line = 0
    y = 0
    for size in sizes:
        if x and x + size.width() > width:
            y += line + vspacing
            x = 0
            line = 0
        x += size.width() + hspacing
        line = max(line, size.height())
    return y + line


def hline() -> QFrame:
    frame = QFrame()
    frame.setFixedHeight(2)
    frame.setStyleSheet("background:#c9cbe0;border:0;")
    return frame


# ---------------------------------------------------------------------------
# Layouts and painted widgets
# ---------------------------------------------------------------------------

class FlowLayout(QLayout):
    """Simple wrapping layout used for level tiles and filter chips."""

    def __init__(self, parent=None, margin: int = 0, hspacing: int = 10, vspacing: int = 10):
        super().__init__(parent)
        self.items: list = []
        self.hspacing = hspacing
        self.vspacing = vspacing
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item) -> None:  # noqa: N802 - Qt API
        self.items.append(item)

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int):  # noqa: N802
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def takeAt(self, index: int):  # noqa: N802
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def expandingDirections(self):  # noqa: N802
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        return self._do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.minimumSize()

    def minimumSize(self) -> QSize:  # noqa: N802
        size = QSize()
        for item in self.items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        margins = self.contentsMargins()
        x = rect.x() + margins.left()
        y = rect.y() + margins.top()
        right = rect.right() - margins.right()
        line_height = 0
        for item in self.items:
            hint = item.sizeHint()
            if x + hint.width() > right and line_height > 0:
                x = rect.x() + margins.left()
                y += line_height + self.vspacing
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x += hint.width() + self.hspacing
            line_height = max(line_height, hint.height())
        return y + line_height + margins.bottom() - rect.y()


class SvgView(QWidget):
    """Paints an SVG while keeping the 600x340 stage ratio."""

    def __init__(self, svg: str = "", ratio: float = 600 / 340, parent=None):
        super().__init__(parent)
        self.ratio = ratio
        self.renderer = QSvgRenderer()
        policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setMinimumHeight(120)
        self.set_svg(svg)

    def set_svg(self, svg: str) -> None:
        self.renderer = QSvgRenderer(svg.encode("utf-8")) if svg else QSvgRenderer()
        self.update()

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        return max(90, int(width / self.ratio))

    def paintEvent(self, _) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        target = QRectF(self.rect()).adjusted(1.5, 1.5, -1.5, -1.5)
        painter.fillRect(target, QColor("#dfe8ff"))
        if self.renderer.isValid():
            self.renderer.render(painter, target)
        painter.setPen(QPen(QColor(DEEP), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(target, 6, 6)
        painter.end()


class AvatarView(QWidget):
    def __init__(self, avatar: int = 0, size: int = 84, parent=None):
        super().__init__(parent)
        self.avatar = avatar
        self._size = size
        self.setFixedSize(size, size)

    def set_avatar(self, avatar: int) -> None:
        self.avatar = avatar
        self.update()

    def paintEvent(self, _) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPixmap(0, 0, avatar_pixmap(self.avatar, self._size))
        painter.end()


class AvatarButton(QAbstractButton):
    def __init__(self, avatar: int, size: int = 54, parent=None):
        super().__init__(parent)
        self.avatar = avatar
        self._size = size
        self.setCheckable(True)
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Karakter {avatar + 1}")

    def paintEvent(self, _) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.isChecked():
            painter.setPen(QPen(QColor(BLUE), 3))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QRectF(1.5, 1.5, self._size - 3, self._size - 3))
        inner = self._size - 12
        painter.drawPixmap(6, 6, avatar_pixmap(self.avatar, inner))
        painter.end()


class Switch(QAbstractButton):
    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(checked)
        self.setFixedSize(46, 26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggled.connect(lambda _: self.update())

    def paintEvent(self, _) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(1.5, 1.5, 43, 23)
        painter.setPen(QPen(QColor(INK), 3))
        painter.setBrush(QColor(BLUE if self.isChecked() else "#d4d4d4"))
        painter.drawRoundedRect(rect, 12, 12)
        knob_x = 22 if self.isChecked() else 2
        painter.setBrush(QColor(INK))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(knob_x + 4, 5, 16, 16))
        painter.end()


class DesktopIcon(QFrame):
    clicked = Signal()

    def __init__(self, title: str, icon_key: str, parent=None):
        super().__init__(parent)
        self.setObjectName("deskIcon")
        self.setFixedSize(66, 70)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 3, 0, 2)
        box.setSpacing(2)
        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(icon_pixmap(icon_key, 32))
        icon.setStyleSheet("background:transparent;")
        box.addWidget(icon)
        text = label(title, 10, True, "#ffffff", True, Qt.AlignmentFlag.AlignHCenter)
        text.setFixedHeight(26)
        box.addWidget(text)
        self.setStyleSheet(
            "QFrame#deskIcon{background:transparent;border:1px solid transparent;}"
            "QFrame#deskIcon:hover{background:rgba(255,255,255,0.16);border:1px solid rgba(255,255,255,0.4);}"
        )

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.position().toPoint()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class LevelTile(QFrame):
    clicked = Signal(int)

    def __init__(self, index: int, level: dict, locked: bool, completed: bool,
                 difficulty: str | None = None, translated_title: str | None = None,
                 parent=None):
        super().__init__(parent)
        self.index = index
        self.locked = locked
        self.setObjectName("levelTile")
        self.setFixedWidth(104)
        self.setCursor(Qt.CursorShape.ForbiddenCursor if locked else Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            "QFrame#levelTile{background:transparent;border:0;}"
            "QFrame#levelTile:hover{background:transparent;}"
        )
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(3)
        color = DIFFICULTY.get(level.get("lv", ""), "#a9b3ff")
        badge = label("🔒" if locked else ("✔" if completed else str(index + 1)), 26, True,
                      INK, align=Qt.AlignmentFlag.AlignCenter)
        badge.setFixedSize(64, 74)
        badge.setStyleSheet(
            f"background:{color};border:3px solid {DEEP};"
            "border-radius:6px 18px 6px 6px;color:#111;"
        )
        wrapper = QHBoxLayout()
        wrapper.addStretch(1)
        wrapper.addWidget(badge)
        wrapper.addStretch(1)
        box.addLayout(wrapper)
        box.addWidget(label(f"Level {index + 1}", 12, True, INK, align=Qt.AlignmentFlag.AlignHCenter))
        title = label(
            translated_title if translated_title is not None else level.get("t", ""),
            10, False, INK, True, Qt.AlignmentFlag.AlignHCenter)
        title.setFixedHeight(26)
        box.addWidget(title)
        difficulty_text = level.get("lv", "") if difficulty is None else difficulty
        box.addWidget(label(difficulty_text, 10, True, PURPLE,
                            align=Qt.AlignmentFlag.AlignHCenter))
        if locked:
            from PySide6.QtWidgets import QGraphicsOpacityEffect

            effect = QGraphicsOpacityEffect(self)
            effect.setOpacity(0.55)
            self.setGraphicsEffect(effect)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if not self.locked and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
        super().mouseReleaseEvent(event)


# ---------------------------------------------------------------------------
# Window chrome
# ---------------------------------------------------------------------------

class TitleButton(QPushButton):
    def __init__(self, text: str, callback=None, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(22, 22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        set_font(self, 12, True)
        self.setStyleSheet(
            "QPushButton{background:#fff;color:#111;border:2px solid #111;"
            "border-radius:0;padding:0;font-weight:800;}"
            "QPushButton:hover{background:#fff1c1;}"
        )
        if callback is not None:
            self.clicked.connect(callback)


class TitleBar(QFrame):
    def __init__(self, window, title: str, icon_key: str | None = None, controls: bool = True):
        super().__init__(window)
        self.win = window
        self.setObjectName("titleBar")
        self.setFixedHeight(30)
        self.drag_origin: QPoint | None = None
        self.win_origin: QPoint | None = None
        row = QHBoxLayout(self)
        row.setContentsMargins(9, 2, 4, 2)
        row.setSpacing(5)
        if icon_key:
            icon = QLabel()
            icon.setPixmap(icon_pixmap(icon_key, 15))
            icon.setStyleSheet("background:transparent;")
            icon.setFixedSize(16, 16)
            row.addWidget(icon)
        self.title_label = label(title, 13, True, "#ffffff")
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        row.addWidget(self.title_label, 1)
        if controls:
            row.addWidget(TitleButton("–", window.minimize))
            row.addWidget(TitleButton("▢", window.toggle_max))
            row.addWidget(TitleButton("×", window.close_window))
        self.set_active(False)

    def set_active(self, active: bool, fixed_blue: bool = False) -> None:
        if active or fixed_blue:
            self.setStyleSheet(
                "QFrame#titleBar{background:#6cc4ff;border:0;border-bottom:3px solid #111;}"
            )
            self.title_label.setStyleSheet("color:#111;background:transparent;")
        else:
            self.setStyleSheet(
                "QFrame#titleBar{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
                "stop:0 #3d4bb8,stop:1 #8f9bff);border:0;border-bottom:3px solid #111;}"
            )
            self.title_label.setStyleSheet("color:#fff;background:transparent;")

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and hasattr(self.win, "toggle_max"):
            if not self.win.maximized:
                self.drag_origin = event.globalPosition().toPoint()
                self.win_origin = self.win.pos()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self.drag_origin is not None and self.win_origin is not None:
            desk = self.win.desk
            point = self.win_origin + (event.globalPosition().toPoint() - self.drag_origin)
            x = max(0, min(desk.width() - 60, point.x()))
            y = max(0, min(desk.height() - 70, point.y()))
            self.win.move(x, y)
            self.win.fit_height()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        self.drag_origin = None
        self.win_origin = None
        self.unsetCursor()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802
        if hasattr(self.win, "toggle_max"):
            self.win.toggle_max()
        super().mouseDoubleClickEvent(event)


class GameWindow(QFrame):
    """Frameless window living inside the desktop."""

    def __init__(self, desk: "Desk", key: str, icon_key: str, title: str,
                 content: QWidget, left: int, top: int, width: int):
        super().__init__(desk)
        self.desk = desk
        self.key = key
        self.icon_key = icon_key
        self.window_title = title
        self.content = content
        self.opened = False
        self.closed = False
        self.minimized = False
        self.maximized = False
        self.normal_geometry: QRect | None = None
        self.setObjectName("gameWindow")
        self.setStyleSheet(
            "QFrame#gameWindow{background:#f3f4ff;border:2px solid #252746;"
            "border-radius:10px;}"
        )
        self.setMinimumWidth(min(width, 300))
        self.resize(width, 110)
        self.titlebar = TitleBar(self, title, icon_key)
        self.content_scroll = QScrollArea(self)
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.content_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_scroll.setStyleSheet(
            "QScrollArea{background:transparent;border:0;}"
            "QScrollArea>QWidget>QWidget{background:transparent;}"
        )
        self.content_scroll.viewport().setAutoFillBackground(False)
        self.content_scroll.setWidget(content)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self.titlebar)
        outer.addWidget(self.content_scroll, 1)
        hard_shadow(self, 3, 3, alpha=110)
        self.move(max(0, left), max(0, top))
        self.fit_height()
        self.hide()

    def fit_height(self) -> None:
        if self.maximized:
            return
        max_height = max(140, self.desk.height() - TASKBAR_H - self.y() - 6)
        inner = max(100, self.width() - 32)
        height = content_height(self.content, inner) + self.titlebar.height() + 24
        self.resize(self.width(), max(110, min(height, max_height)))

    def set_active(self, active: bool) -> None:
        self.titlebar.set_active(active)

    def open(self) -> None:
        self.opened = True
        self.closed = False
        self.minimized = False
        self.show()
        self.desk.focus_window(self)
        QTimer.singleShot(0, self.fit_height)

    def minimize(self) -> None:
        self.minimized = True
        self.hide()
        self.set_active(False)
        self.desk.active = None
        self.desk.sync_taskbar()

    def close_window(self) -> None:
        self.opened = False
        self.closed = True
        self.minimized = False
        self.hide()
        if self.desk.active is self:
            self.desk.active = None
        self.desk.sync_taskbar()

    def toggle_max(self) -> None:
        if self.maximized:
            self.maximized = False
            if self.normal_geometry:
                self.setGeometry(self.normal_geometry)
            self.fit_height()
        else:
            self.normal_geometry = self.geometry()
            self.maximized = True
            self.setGeometry(0, 0, self.desk.width(), self.desk.height() - TASKBAR_H)
        self.desk.focus_window(self)

    def refresh_title(self, title: str) -> None:
        self.window_title = title
        self.titlebar.title_label.setText(title)


class ScreenWindow(QFrame):
    """Centered browser-style screen window (login, landing, learning)."""

    def __init__(self, desk: "Desk", title: str, content: QWidget, screen_key: str):
        super().__init__(desk)
        self.desk = desk
        self.content = content
        self.screen_key = screen_key
        self.setObjectName("screenWindow")
        self.setStyleSheet(
            "QFrame#screenWindow{background:#f3f3f3;border:3px solid #111;}"
        )
        self.titlebar = TitleBar(self, title, None, controls=True)
        self.titlebar.set_active(True, fixed_blue=True)
        self.content_scroll = QScrollArea(self)
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.content_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_scroll.setStyleSheet(
            "QScrollArea{background:transparent;border:0;}"
            "QScrollArea>QWidget>QWidget{background:transparent;}"
        )
        self.content_scroll.viewport().setAutoFillBackground(False)
        self.content_scroll.setWidget(content)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self.titlebar)
        outer.addWidget(self.content_scroll, 1)
        hard_shadow(self, 6, 6)
        self.fit_screen()

    def fit_screen(self) -> None:
        width = min(780, int(self.desk.width() * 0.94))
        self.setFixedWidth(width)
        # Measure wrapped labels at the actual page width. Measuring at the
        # layout's unconstrained sizeHint leaves long landing/lesson text with
        # too little height once the scroll area narrows it to fit the window.
        inner = max(120, width - 26)
        self.content.setMinimumWidth(inner)
        layout = self.content.layout()
        if layout is not None:
            layout.invalidate()
            layout.activate()
        page_height = content_height(self.content, inner)
        self.content.setMinimumHeight(page_height)
        wanted = page_height + self.titlebar.height() + 26
        height = min(int(self.desk.height() * 0.94), max(180, wanted))
        self.setFixedHeight(height)
        x = (self.desk.width() - width) // 2
        y = max(10, (self.desk.height() - height) // 2)
        self.move(x, y)

    def minimize(self) -> None:
        self.desk.window().showMinimized()

    def toggle_max(self) -> None:
        game = self.desk.window()
        if game.isMaximized():
            game.showNormal()
        else:
            game.showMaximized()

    def close_window(self) -> None:
        game = self.desk.window()
        if self.screen_key == "login":
            game.close()
        else:
            if not isinstance(game, NativeGame):
                raise RuntimeError("The screen window is not attached to the game.")
            game.show_login()


# ---------------------------------------------------------------------------
# Desktop
# ---------------------------------------------------------------------------

class Desk(QWidget):
    """Wallpaper surface holding icons, windows, watermark and taskbar."""

    def __init__(self, wallpaper: str, parent=None):
        super().__init__(parent)
        self.renderer = QSvgRenderer(wallpaper.encode("utf-8")) if wallpaper else QSvgRenderer()
        self.windows: dict[str, GameWindow] = {}
        self.icon_widgets: list[DesktopIcon] = []
        self.screen: ScreenWindow | None = None
        self.active: GameWindow | None = None
        self.mode = "desk"

        self.taskbar = QFrame(self)
        self.taskbar.setObjectName("taskbar")
        self.taskbar.setStyleSheet(
            "QFrame#taskbar{background:#111;border:0;}"
            "QLabel{color:#6cc4ff;background:transparent;}"
        )
        bar = QHBoxLayout(self.taskbar)
        bar.setContentsMargins(7, 4, 9, 4)
        bar.setSpacing(8)
        self.back_btn = button("← Layar Awal", self.close, "white", 12, shadow=False)
        self.back_btn.setStyleSheet(
            "QPushButton{background:#fff;color:#111;border:2px solid #343657;"
            "border-radius:7px;padding:2px 9px;font-weight:700;}"
            "QPushButton:hover{background:#fff1c1;border-color:#111;}"
        )
        bar.addWidget(self.back_btn, 0)
        self.status_label = label("", 12, True, BLUE)
        self.status_label.setMinimumWidth(0)
        self.status_label.setStyleSheet(
            "QLabel{color:#d9eaff;background:#252746;border-radius:7px;"
            "padding:4px 8px;}")
        bar.addWidget(self.status_label, 0)
        self.tb_buttons = QHBoxLayout()
        self.tb_buttons.setContentsMargins(0, 0, 0, 0)
        self.tb_buttons.setSpacing(5)
        self.tb_buttons.addStretch(1)
        bar.addLayout(self.tb_buttons, 1)
        self.xp_label = label("", 12, True, BLUE)
        self.xp_label.setMinimumWidth(0)
        bar.addWidget(self.xp_label, 0)

        self.watermark = QWidget(self)
        mark_box = QVBoxLayout(self.watermark)
        mark_box.setContentsMargins(0, 0, 0, 0)
        mark_box.setSpacing(0)
        big = label("DETEKTIF SIBER", 34, True, "#ffffff")
        small = label("DIVISI KEJAHATAN DIGITAL", 10, True, "#ffffff")
        small.setStyleSheet("color:#fff;background:transparent;letter-spacing:2px;")
        mark_box.addWidget(big)
        mark_box.addWidget(small)
        for child in (big, small):
            hard_shadow(child, 0, 4, DEEP)
        self.watermark.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.watermark.hide()

        self.taskbar.hide()

    # -- painting -----------------------------------------------------------
    def paintEvent(self, _) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()).adjusted(1.5, 1.5, -1.5, -1.5), 14, 14)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QColor("#1b1e3f"))
        if self.renderer.isValid():
            scale = max(self.width() / 1000.0, self.height() / 690.0)
            painter.save()
            painter.translate((self.width() - 1000 * scale) / 2, (self.height() - 690 * scale) / 2)
            painter.scale(scale, scale)
            self.renderer.render(painter, QRectF(0, 0, 1000, 690))
            painter.restore()
        painter.setClipping(False)
        painter.setPen(QPen(QColor(DEEP), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(self.rect()).adjusted(1.5, 1.5, -1.5, -1.5), 14, 14)
        painter.end()

    def resizeEvent(self, event) -> None:  # noqa: N802
        self.taskbar.setGeometry(3, self.height() - TASKBAR_H, self.width() - 6, TASKBAR_H)
        self.watermark.adjustSize()
        self.watermark.move(18, max(0, self.height() - TASKBAR_H - self.watermark.height() - 12))
        self.relayout_icons()
        for win in self.windows.values():
            if win.maximized:
                win.setGeometry(0, 0, self.width(), self.height() - TASKBAR_H)
            else:
                win.fit_height()
        if self.screen:
            self.screen.fit_screen()
        super().resizeEvent(event)

    # -- icons --------------------------------------------------------------
    def add_icon(self, title: str, icon_key: str, callback, column: int = 1) -> DesktopIcon:
        icon = DesktopIcon(title, icon_key, self)
        icon.clicked.connect(callback)
        icon.setProperty("column", column)
        icon.setProperty("index", len(self.icon_widgets))
        self.icon_widgets.append(icon)
        icon.show()
        self.relayout_icons()
        return icon

    def relayout_icons(self) -> None:
        counters = {1: 0, 2: 0}
        for icon in self.icon_widgets:
            column = int(icon.property("column") or 1)
            index = counters[column]
            counters[column] += 1
            x = 8 if column == 1 else 80
            y = 8 + index * 72
            icon.move(x, y)

    # -- windows ------------------------------------------------------------
    def add_window(self, key: str, icon_key: str, title: str, content: QWidget,
                   left: int, top: int, width: int) -> GameWindow:
        left = max(8, left)
        left = min(left, max(8, self.width() - width - 8))
        win = GameWindow(self, key, icon_key, title, content, left, top, width)
        self.windows[key] = win
        return win

    def open_window(self, key: str) -> None:
        win = self.windows.get(key)
        if win is not None:
            win.open()

    def focus_window(self, win: GameWindow) -> None:
        if win is self.active and win.isVisible() and not win.minimized:
            return
        for other in self.windows.values():
            other.set_active(False)
        self.active = win
        win.minimized = False
        win.set_active(True)
        win.show()
        win.raise_()
        self.sync_taskbar()

    def sync_taskbar(self) -> None:
        while self.tb_buttons.count() > 1:
            item = self.tb_buttons.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        position = 0
        for win in self.windows.values():
            if not win.opened:
                continue
            text = win.window_title
            metrics = QFontMetrics(QFont("Segoe UI", 8))
            if metrics.horizontalAdvance(text) > 92:
                text = metrics.elidedText(text, Qt.TextElideMode.ElideRight, 92)
            btn = QPushButton(text)
            btn.setProperty("kind", "task")
            btn.setProperty("active", "yes" if (self.active is win and not win.minimized) else "no")
            set_font(btn, 11, True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumWidth(54)
            btn.setMaximumWidth(132)
            btn.setIcon(QIcon(icon_pixmap(win.icon_key, 14)))
            btn.setIconSize(QSize(14, 14))
            btn.clicked.connect(lambda _, w=win: self.toggle_task(w))
            self.tb_buttons.insertWidget(position, btn)
            position += 1

    def toggle_task(self, win: GameWindow) -> None:
        if self.active is win and not win.minimized:
            win.minimize()
        else:
            win.open()

    def set_status(
        self, status: str, xp_text: str, back_text: str, back_callback,
        status_tooltip: str | None = None,
    ) -> None:
        self.status_label.setText(status)
        self.status_label.setToolTip(status_tooltip or status)
        self.xp_label.setText(xp_text)
        self.xp_label.setToolTip(xp_text)
        self.back_btn.setText(back_text)
        try:
            self.back_btn.clicked.disconnect()
        except (RuntimeError, TypeError):
            pass
        self.back_btn.clicked.connect(back_callback)

    # -- screen mode --------------------------------------------------------
    def set_screen(self, content: QWidget, title: str, screen_key: str) -> None:
        self.mode = "screen"
        self.taskbar.hide()
        self.watermark.hide()
        for icon in self.icon_widgets:
            icon.hide()
        if self.screen is not None:
            self.screen.setParent(None)
            self.screen.deleteLater()
        self.screen = ScreenWindow(self, title, content, screen_key)
        self.screen.show()
        self.screen.raise_()

    def close(self) -> None:  # noqa: A003 - used as a back-button callback
        pass


class Toast(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"background:#111;color:{BLUE};border:3px solid {BLUE};"
            "padding:8px 15px;font-weight:700;"
        )
        set_font(self, 13, True)
        hard_shadow(self, 4, 4, "#000")
        self.hide()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

    def flash(self, text: str, error: bool = False) -> None:
        if error:
            self.setStyleSheet(
                f"background:#3a1010;color:#fff;border:3px solid {RED};"
                "padding:8px 15px;font-weight:700;")
        else:
            self.setStyleSheet(
                f"background:#111;color:{BLUE};border:3px solid {BLUE};"
                "padding:8px 15px;font-weight:700;")
        self.setText(text)
        self.adjustSize()
        parent = self.parentWidget()
        if parent:
            self.move(max(8, (parent.width() - self.width()) // 2), max(8, parent.height() - 72))
        self.raise_()
        self.show()
        self.timer.start(2800)


class Shell(QWidget):
    """Page background that centers the 1000x690 desktop."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("shell")
        self.setStyleSheet("QWidget#shell{background:#f3f3f3;}")
        self.desk: Desk | None = None
        self.toast = Toast(self)

    def set_desk(self, desk: Desk) -> None:
        if self.desk is not None:
            self.desk.setParent(None)
            self.desk.deleteLater()
        self.desk = desk
        desk.setParent(self)
        desk.show()
        self.layout_desk()
        self.toast.raise_()

    def layout_desk(self) -> None:
        if self.desk is None:
            return
        width = min(1000, max(320, self.width() - 24))
        height = min(690, max(340, self.height() - 24))
        x = (self.width() - width) // 2
        y = (self.height() - height) // 2
        self.desk.setGeometry(x, y, width, height)
        if self.toast.isVisible():
            self.toast.move(max(8, (self.width() - self.toast.width()) // 2),
                            max(8, self.height() - 72))

    def resizeEvent(self, event) -> None:  # noqa: N802
        self.layout_desk()
        super().resizeEvent(event)

# ===========================================================================
# Global style and reusable chrome pieces
# ===========================================================================

GLOBAL_QSS = """
QWidget { color:#111; }
QMainWindow, QWidget#page { background:#f3f3f3; }
QPushButton[kind="primary"] { background:#6cc4ff; border:2px solid #343657;
    border-radius:8px; padding:6px 14px; }
QPushButton[kind="primary"]:hover { background:#8ed2ff; }
QPushButton[kind="primary"]:pressed { background:#3dc6ff; }
QPushButton[kind="white"] { background:#fff; border:2px solid #343657;
    border-radius:8px; padding:6px 14px; }
QPushButton[kind="white"]:hover { background:#fff1c1; }
QPushButton[kind="white"]:pressed { background:#ffe9a8; }
QPushButton[kind="small"] { background:#6cc4ff; border:2px solid #343657;
    border-radius:7px; padding:3px 9px; }
QPushButton[kind="small"]:hover { background:#8ed2ff; }
QPushButton[kind="big"] { background:#6cc4ff; border:2px solid #343657;
    border-radius:10px; padding:16px 32px; }
QPushButton[kind="big"]:hover { background:#8ed2ff; }
QPushButton[kind="big"]:pressed { background:#3dc6ff; }
QPushButton[kind="link"] { background:transparent; border:0; color:#3d4bb8; padding:0; }
QPushButton[kind="link"]:hover { color:#111; text-decoration:underline; }
QPushButton[kind="task"] { background:#fff; border:1px solid #596080;
    border-radius:7px; padding:3px 8px; }
QPushButton[kind="task"]:hover { background:#fff1c1; }
QPushButton[kind="task"][active="yes"] { background:#6cc4ff; }
QPushButton:disabled { background:#e4e4e4; color:#888; }
QLineEdit, QComboBox { background:#fff; border:2px solid #343657; padding:6px 8px;
    border-radius:7px; selection-background-color:#6cc4ff; }
QLineEdit:focus, QComboBox:focus { border-color:#ff7a6b; }
QLineEdit[flat="yes"] { border:0; background:transparent; padding:12px 0; }
QComboBox::drop-down { border:0; width:22px; }
QTextBrowser { background:#fff; border:2px solid #343657; border-radius:8px; padding:6px; }
QTableWidget { background:#fff; gridline-color:#c4c9e2; border:1px solid #596080;
    border-radius:7px;
    selection-background-color:#6cc4ff; selection-color:#111; }
QHeaderView::section { background:#d9eaff; border:1px solid #c4c9e2; padding:5px 8px;
    font-weight:800; }
QScrollArea { background:transparent; border:0; }
QScrollArea > QWidget > QWidget { background:transparent; }
QScrollBar:vertical { background:transparent; width:12px; margin:0; }
QScrollBar::handle:vertical { background:#b9bccc; border:2px solid #f3f4ff;
    border-radius:5px; min-height:24px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background:transparent; }
QScrollBar:horizontal { background:transparent; height:12px; margin:0; }
QScrollBar::handle:horizontal { background:#b9bccc; border:2px solid #f3f4ff;
    border-radius:5px; min-width:24px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width:0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background:transparent; }
QToolTip { background:#111; color:#6cc4ff; border:2px solid #6cc4ff; padding:4px; }
"""

EN.update({
    "Level": "Level",
    "Kasus selesai:": "Cases done:",
    "Baca materi singkat ini sebelum menyelidiki.":
        "Read this short lesson before investigating.",
    "Pilih bab di sisi kanan": "Pick a chapter on the right",
    "Tiap bab yang dibaca memberi +10 EXP.": "Each chapter you read gives +10 EXP.",
    "BUKU PANDUAN": "GUIDE BOOK",
    "BAB": "CHAPTER",
    "Karakter": "Character",
    "Lencana": "Badges",
    "Total XP": "Total XP",
    "Langkah kecil adalah bagian dari solusi besar.":
        "Small steps are part of a big solution.",
    "XP menuju level berikutnya": "XP to the next level",
    "Sesuaikan pengalaman bermain sesuai keinginanmu.": "Customize your play experience.",
    "Bahasa Indonesia": "Indonesian",
    "English": "English",
    "Yakin? Klik lagi": "Sure? Click again",
    "Progres direset.": "Progress reset.",
    "Selamat datang,": "Welcome,",
    "GAME EDUKASI • KEAMANAN SIBER": "EDUCATIONAL GAME • CYBER SECURITY",
    "Selidiki kejahatan digital lewat kasus seru, tanpa koding dan tanpa risiko nyata.":
        "Investigate digital crimes through exciting cases, with no coding and no real risk.",
    "CARA BERMAIN": "HOW TO PLAY",
    "Tata cara bermain": "How to play",
    "BUKA MEJA DETEKTIF": "OPEN DETECTIVE DESK",
    "Semua skenario fiktif: belajar aman tanpa risiko nyata":
        "All scenarios are fictional: learn safely with no real risk",
    "Fase Belajar": "Study Phase",
    "Materi": "Lesson",
    "Sebelumnya": "Previous",
    "Selanjutnya": "Next",
    "Kembali": "Back",
    "Mulai Penyelidikan": "Start Investigation",
    "Pesan masuk": "Incoming message",
    "Ketuk untuk melihat": "Click to open",
    "Kenali modus kejahatan": "Recognize criminal tactics",
    "Pelajari phishing, tebak sandi, dan kebocoran data lewat kasus nyata.":
        "Learn about phishing, password guessing, and data leaks through realistic cases.",
    "Selidiki seperti detektif": "Investigate like a detective",
    "Periksa tabel, browser, CCTV, dan papan bukti untuk menemukan pelaku.":
        "Check tables, browser, CCTV, and the evidence board to find the culprit.",
    "Dapatkan EXP dan naik level": "Earn XP and level up",
    "Setiap bukti yang tepat memberi EXP. Makin teliti, makin tinggi levelmu.":
        "Every correct piece of evidence earns XP. The more careful you are, the higher your level.",
    "Pilih Kasus": "Choose Case",
    "Belajar": "Learn",
    "Selidiki": "Investigate",
    "Tuntaskan": "Complete",
    "Detektif Siber": "Cyber Detective",
    "selidiki kejahatan digital tanpa koding.": "investigate digital crimes without coding.",
    "Buka ikon": "Open the",
    "Pilih level dan baca edukasinya.": "Choose a level and read its lesson.",
    "Cari bukti di Tabel dan Browser.": "Find evidence in Tables and Browser.",
    "Musik latar": "Background music",
    "Efek Suara": "Sound effects",
    "Reset Progres": "Reset progress",
    "Ganti Nama": "Change name",
    "Bahasa": "Language",
    "Bukti dipilih:": "Selected evidence:",
    "Lanjut ke Level": "Continue to Level",
    "Baca folder Edukasi untuk cara mencegahnya.":
        "Read the Education folder for how to prevent it.",
    "Kasus selesai!": "Case solved!",
    "Tepat! Langkah berikutnya terbuka.": "Correct! The next step is unlocked.",
    "sama dengan": "equals",
    "mengandung": "contains",
    "lebih dari / sesudah": "greater than / after",
    "kurang dari / sebelum": "less than / before",
    "bukan": "not",
    "pilih / isi nilai": "pick / enter a value",
    "Saring data": "Filter data",
    "(kosongkan nilai untuk menampilkan semua)":
        "(leave the value empty to show everything)",
    "+ Syarat": "+ Condition",
    "Pakai jumlah ini": "Use this count",
    "dari": "of",
    "baris": "rows",
    "jumlah baris": "row count",
    "Tidak ada data yang cocok.": "No matching data.",
    "Coba ubah atau kurangi syaratnya.": "Try changing or removing conditions.",
    "Cari di internet...": "Search the internet...",
    "Klik angka hasilnya untuk dijadikan bukti.":
        "Click the result number to use it as evidence.",
    "Susun bubble di bawah menjadi sebuah perintah.":
        "Arrange the bubbles below into a command.",
    "Mudah": "Easy",
    "Sedang": "Medium",
    "Sulit": "Hard",
    "Ahli": "Expert",
    "1. Di meja detektif, buka folder <b>Kasus</b> lalu pilih level.":
        "1. At the detective desk, open the <b>Cases</b> folder, then choose a level.",
    "2. Baca materi edukasi singkat sebelum kasus dimulai.":
        "2. Read a short educational lesson before the case starts.",
    "3. Selidiki lewat Tabel, Browser, CCTV, dan Foto, lalu klik bukti yang kamu temukan.":
        "3. Investigate with Tables, Browser, CCTV, and Photos, then click the evidence you find.",
    "4. Tiap bukti yang tepat memberi EXP. Kasus tuntas membuka level berikutnya.":
        "4. Each correct piece of evidence earns XP. Completing a case unlocks the next level.",
    "Tampilkan": "Show",
    "semua kolom": "all columns",
    "dari tabel": "from table",
    "yang": "where",
    "dan": "and",
    "mirip pola": "matches pattern",
    "lebih dari": "greater than",
    "kurang dari": "less than",
    "urutkan menurut": "sort by",
    "dari terbesar": "descending",
    "Perintah": "Command",
    "Kolom": "Columns",
    "Operator": "Operator",
    "Nilai": "Values",
    "Kembali ke hasil": "Back to results",
    "hasil untuk": "results for",
    "Tidak ada hasil untuk": "No results for",
    "Coba kata kunci lain.": "Try another search term.",
    "Cari petunjuk di internet. Coba kata kunci seperti nama, domain, atau topik kasus.":
        "Search for clues online. Try a name, domain, or case topic.",
    "Detektif Senior": "Senior Detective",
    "Detektif": "Detective",
    "Magang": "Trainee",
    "Jawaban salah": "Incorrect answer",
    "Peringatan": "Warning",
    "Belum terungkap": "Unsolved",
    "Error": "Incorrect answer",
    "Bukti diterima. Total XP:": "Evidence accepted. Total XP:",
    "Naik ke Level": "Promoted to Level",
    "+10 XP: materi dibaca": "+10 XP: lesson read",
    "Login Kasir": "Cashier Log",
    "Pesanan Saya": "My Orders",
    "Log Telepon": "Call Log",
    "SMS Masuk": "Incoming Texts",
    "Riwayat Grup WA": "WhatsApp Group History",
    "Daftar WiFi": "Wi-Fi Networks",
    "Login Akun": "Account Sign-ins",
    "Transaksi QRIS": "QR Code Transactions",
    "Izin Aplikasi": "App Permissions",
    "Ulasan Toko": "Store Reviews",
    "Laporan Korban": "Victim Reports",
    "Email Masuk": "Incoming Email",
    "Catatan Klik": "Click Log",
    "Login Baru": "New Sign-ins",
    "Perubahan Nilai": "Grade Changes",
    "Catatan Login": "Sign-in Log",
    "Absensi Lab": "Lab Attendance",
    "Akses File": "File Access",
    "Absensi Gedung": "Building Attendance",
    "Sticky note": "Sticky note",
    "Pengelola sandi": "Password manager",
    "Kertas tempel": "Sticky note",
    "jne-cek-paket.xyz": "jne-cek-paket.xyz",
    "Perangkat Baru": "New Device",
    "Terbuka": "Open",
    "Tidak": "No",
    "Ya": "Yes",
    "Dikirim": "Shipped",
    "Selesai": "Completed",
    "Mengaku dari bank": "Claimed to be from the bank",
    "Kontak tersimpan": "Saved contact",
    "CCTV": "CCTV",
    "Mbak Sari": "Sari",
    "JNE-Info": "JNE Info",
    "Dinda (teman)": "Dinda (friend)",
    "Dinda (telepon)": "Dinda (phone)",
    "Mbak Sari (pemilik)": "Sari (owner)",
    "Admin IT": "IT Admin",
    "Bu Ratna": "Ms. Ratna",
    "Kamu": "You",
    "Sistem": "System",
    "Adik": "Sibling",
    "Barista": "Barista",
    "Kasir": "Cashier",
    "Ibu": "Mother",
    "Kaprodi": "Department Chair",
    "Direktur": "Director",
    "Penipu": "Scammer",
    "Pengirim SMS": "Text Sender",
    "Orang iseng": "Prankster",
    "Data Pelanggan Bocor": "The Customer Data Leak",
    "Menu Warung Mbak Sari": "Sari's Shop Menu",
    "JNE (situs resmi)": "JNE (official site)",
    "Promo Akhir Pekan": "Weekend Promotion",
    "Keamanan Nasabah BankKu": "BankKu Customer Security",
    "Klaim Kuota 50GB Gratis": "Claim 50 GB of Free Data",
    "Panduan: Akun WhatsApp Diambil Alih": "Guide: Recover a Hijacked WhatsApp Account",
    "Risiko WiFi Publik": "Public Wi-Fi Risks",
    "Keamanan Aplikasi (APK)": "App Safety (APK)",
    "HP Murah Gila Shop": "Crazy Cheap Phone Shop",
    "Cek Domain: kampus-verif.xyz": "Domain Check: kampus-verif.xyz",
    "Foto Staf": "Staff Photos",
    "Situs Resmi Kampus": "Official Campus Site",
    "Promo Belanja Akhir Pekan": "Weekend Shopping Promotion",
    "Denah Jaringan Kampus": "Campus Network Map",
    "Galeri Praktikum Lab 3": "Lab 3 Class Gallery",
    "Menu Kantin Hari Ini": "Today's Cafeteria Menu",
    "Berita: Wisuda Oktober": "News: October Graduation",
    "Berita Internal": "Internal News",
    "Paket Anda tertahan di gudang. Bayar biaya <u data-v='Rp 15.000'>Rp 15.000</u> di: <u data-v='jne-cek-paket.xyz/bayar'>jne-cek-paket.xyz/bayar</u>":
        "Your package is being held at the depot. Pay a <u data-v='Rp 15.000'>Rp 15,000</u> fee at: <u data-v='jne-cek-paket.xyz/bayar'>jne-cek-paket.xyz/bayar</u>",
    "Terdaftar: 19 Oktober 2026": "Registered: October 19, 2026",
    "Terdaftar: 29 September 2026": "Registered: September 29, 2026",
    "Terdaftar: 5 hari lalu": "Registered: 5 days ago",
    "Terdaftar sejak 1990.": "Registered since 1990.",
    "Terdaftar sejak 2005.": "Registered since 2005.",
    "Klaim Kuota 50GB": "Claim 50 GB of Data",
    "Masukkan nomor WA dan kode verifikasi 6 digit yang dikirim ke SMS-mu.":
        "Enter your WhatsApp number and the six-digit verification code sent by text.",
    "Akun WA Diambil Alih": "Hijacked WhatsApp Account",
    "daftar ulang WhatsApp dengan nomor sendiri":
        "register WhatsApp again with your own number",
    "tunggu sampai penyerang bosan": "wait until the attacker gives up",
    "kirim kode verifikasi ke teman": "send a verification code to a friend",
    "WiFi terbuka dapat dibuat penipu dengan nama mirip kafe. Datamu bisa disadap.":
        "Scammers can create open Wi-Fi with a name similar to a cafe's and intercept your data.",
    "Terdaftar:": "Registered:",
    "Pemilik: disembunyikan": "Owner: hidden",
    "Server: luar negeri": "Server: abroad",
    "Catatan: domain baru yang meniru situs resmi sering dipakai untuk phishing.":
        "Note: new domains imitating official sites are often used for phishing.",
    "Foto StafNama akun di bawah tiap foto.":
        "Staff PhotosThe account name appears below each photo.",
    "Nama akun di bawah tiap foto.": "The account name appears below each photo.",
    "Alamat IP dibagi menurut lokasi:": "IP addresses are assigned by location:",
    "10.4.2.x : Ruang Dosen": "10.4.2.x: Faculty Office",
    "10.4.5.x : Perpustakaan": "10.4.5.x: Library",
    "10.4.7.x : Lab Komputer 3": "10.4.7.x: Computer Lab 3",
    "Perhatikan pakaian dan atributnya.": "Look closely at clothing and accessories.",
    "Galeri Praktikum Lab Komputer 3": "Computer Lab 3 Class Gallery",
    "Nasi goreng, soto ayam, es teh.": "Fried rice, chicken soup, and iced tea.",
    "Wisuda dilaksanakan 12 Oktober di aula utama.":
        "The graduation ceremony is on October 12 in the main hall.",
    "Direktori Karyawan": "Employee Directory",
    "tono.k : Tono Kurniawan (Keuangan)": "tono.k: Tono Kurniawan (Finance)",
    "dewi.a : Dewi Anggraini (Magang IT)": "dewi.a: Dewi Anggraini (IT Intern)",
    "budi.s : Budi Santoso (Pemasaran)": "budi.s: Budi Santoso (Marketing)",
    "maya.l : Maya Lestari (HRD)": "maya.l: Maya Lestari (Human Resources)",
    "Tono Kurniawan": "Tono Kurniawan",
    "Dewi Anggraini": "Dewi Anggraini",
    "Budi Santoso": "Budi Santoso",
    "Maya Lestari": "Maya Lestari",
    "Dijual: data pelanggan": "For sale: customer data",
    "Isi: 5.000 pelanggan lengkap. Bayar kripto.":
        "Contains details for 5,000 customers. Pay with cryptocurrency.",
    "BeritaGathering kantor bulan depan.": "NewsOffice gathering next month.",
    "Gathering kantor bulan depan.": "Office gathering next month.",
    "Grup Telegram": "Telegram Group",
    "Iklan": "Advertisement",
    "Bu Wati": "Ms. Wati",
    "Tono": "Tono",
    "cara cek qris asli": "how to check an authentic QR code",
    "Di Browser cari: cara cek qris asli.":
        "Search the Browser for: how to check an authentic QR code.",
    "Di Browser cari: hp murah gila.":
        "Search the Browser for: Crazy Cheap Phone Shop.",
    "Cari alamat web di SMS. Kurir resmi memakai alamat seperti jne.co.id.":
        "Check the web address in the text. The official courier uses jne.co.id.",
    "Paket Anda tertahan di gudang.": "Your package is being held at the depot.",
    "Bayar biaya": "Pay a fee",
    "di:": "at:",
    "Cek Domain:": "Domain Check:",
    "Situs resmi, terdaftar sejak 1990.": "Official site, registered since 1990.",
    "Situs resmi, terdaftar sejak 2005.": "Official site, registered since 2005.",
    "Diskon 50%": "50% off",
    "Khusus akhir pekan.": "This weekend only.",
    "Khusus akhir pekan": "This weekend only",
    "Simpan Sandi dengan Aman": "Store Passwords Safely",
    "Nasi goreng, es teh, dan gorengan.": "Fried rice, iced tea, and fritters.",
    "Tampilan salah": "Incorrect display",
    "sandi": "password",
    "Pemberitahuan": "Notice",
    "OTP": "OTP",
    "Putar": "Play",
    "Jeda": "Pause",
})

SHIELD_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 70'>"
    "<path d='M30 4L54 12V34C54 52 42 62 30 67C18 62 6 52 6 34V12Z' fill='#fff' "
    "stroke='#111' stroke-width='5'/>"
    "<path d='M30 4V67C18 62 6 52 6 34V12Z' fill='#111'/></svg>"
)


def shield_label(width: int = 58) -> QLabel:
    lab = QLabel()
    lab.setPixmap(svg_pixmap(SHIELD_SVG, width, int(width * 70 / 60), 2.0))
    lab.setFixedSize(width, int(width * 70 / 60))
    lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lab.setStyleSheet("background:transparent;")
    return lab


def brand_title(
    size: int = 46, mark: str = "SIBER", title: str = "DETEKTIF"
) -> QLabel:
    lab = rich(
        f"<span style='font-size:{size}px;font-weight:800;line-height:1;'>{title} "
        f"<span style='background-color:{BLUE};padding:0 10px;'>{mark}</span></span>",
        14,
        INK,
        align=Qt.AlignmentFlag.AlignCenter,
    )
    lab.setWordWrap(False)
    lab.setStyleSheet("background:transparent;")
    return lab


def big_headline(text: str, size: int = 34) -> QLabel:
    lab = rich(f"<span style='font-size:{size}px;font-weight:800;'>{esc(text)}</span>",
               14, INK, align=Qt.AlignmentFlag.AlignCenter)
    lab.setWordWrap(False)
    lab.setStyleSheet("background:transparent;")
    return lab


def spacer(height: int = 8) -> QWidget:
    widget = QWidget()
    widget.setFixedHeight(height)
    widget.setStyleSheet("background:transparent;")
    return widget


def badge(text: str, bg: str = CYAN) -> QFrame:
    frame = QFrame()
    frame.setStyleSheet(f"QFrame{{background:{bg};border:3px solid #111;}}")
    hard_shadow(frame, 4, 4)
    box = QHBoxLayout(frame)
    box.setContentsMargins(12, 3, 12, 3)
    box.addWidget(label(text, 13, True, INK))
    return frame


def field_row(icon: str, edit: QLineEdit, eye: bool = False) -> QFrame:
    frame = QFrame()
    frame.setStyleSheet("QFrame#inp{background:#fff;border:3px solid #111;}")
    frame.setObjectName("inp")
    hard_shadow(frame, 3, 3)
    row = QHBoxLayout(frame)
    row.setContentsMargins(11, 0, 8, 0)
    row.setSpacing(9)
    glyph = label(icon, 16, False, INK)
    glyph.setFixedWidth(22)
    row.addWidget(glyph)
    edit.setProperty("flat", "yes")
    edit.setStyleSheet(
        "QLineEdit{background:transparent;border:0;padding:12px 0;color:#111;}"
        "QLineEdit:focus{border:0;}"
    )
    row.addWidget(edit, 1)
    if eye:
        btn = QPushButton("👁")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedWidth(30)
        set_font(btn, 16, False)
        btn.setStyleSheet(
            "QPushButton{background:transparent;border:0;padding:0;}"
            "QPushButton:hover{background:#fff1c1;}"
        )

        def toggle() -> None:
            if edit.echoMode() == QLineEdit.EchoMode.Password:
                edit.setEchoMode(QLineEdit.EchoMode.Normal)
            else:
                edit.setEchoMode(QLineEdit.EchoMode.Password)

        btn.clicked.connect(toggle)
        row.addWidget(btn)
    return frame


def screen_page() -> tuple[QWidget, QVBoxLayout]:
    page = QWidget()
    page.setObjectName("page")
    page.setStyleSheet("QWidget#page{background:#f3f3f3;}")
    box = QVBoxLayout(page)
    box.setContentsMargins(10, 14, 14, 18)
    box.setSpacing(10)
    return page, box


def feature_row(glyph: str, title: str, desc: str) -> QWidget:
    wrap = QWidget()
    wrap.setStyleSheet("background:transparent;")
    row = QHBoxLayout(wrap)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(14)
    ic = label(glyph, 26)
    ic.setFixedWidth(34)
    ic.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
    row.addWidget(ic)
    text = QVBoxLayout()
    text.setContentsMargins(0, 0, 0, 0)
    text.setSpacing(1)
    text.addWidget(label(title, 15, True, INK))
    body = label(desc, 13, False, "#666", True)
    body.setSizePolicy(
        QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    text.addWidget(body)
    row.addLayout(text, 1)
    wrap.setMinimumHeight(max(ic.sizeHint().height(), text.sizeHint().height()))
    return wrap


def flow_step(glyph: str, text: str) -> QWidget:
    wrap = QWidget()
    wrap.setStyleSheet("background:transparent;")
    col = QVBoxLayout(wrap)
    col.setContentsMargins(0, 0, 0, 0)
    col.setSpacing(0)
    ic = label(glyph, 24, align=Qt.AlignmentFlag.AlignCenter)
    col.addWidget(ic)
    col.addWidget(label(text, 13, True, INK, align=Qt.AlignmentFlag.AlignCenter))
    return wrap


def dots_row(total: int, current: int, caption: str) -> QWidget:
    wrap = QWidget()
    wrap.setStyleSheet("background:transparent;")
    row = QHBoxLayout(wrap)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(8)
    row.addStretch(1)
    for i in range(total):
        dot = QFrame()
        dot.setFixedSize(26, 14)
        dot.setStyleSheet(
            "background:%s;border:3px solid #111;" % (CYAN if i == current else "#fff")
        )
        row.addWidget(dot)
    row.addWidget(label(caption, 12, False, "#666"))
    row.addStretch(1)
    return wrap


# ===========================================================================
# Main application state and screens
# ===========================================================================

class NativeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = read_data()
        self.levels: list[dict] = self.data["levels"]
        self.lessons: dict = self.data["lessons"]
        self.wallpaper: str = self.data.get("wallpaper", "")

        storage = Path(QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation))
        storage.mkdir(parents=True, exist_ok=True)
        self.save_path = storage / "progress.json"

        self.state = {
            "username": "",
            "xp": 0,
            "done": [],
            "read": {},
            "progress": [],
            "query_runs": 0,
            "avatar": 0,
            "music": True,
            "sound": True,
            "language": "id",
            "seen": False,
            "got": {},
        }
        self.active_level = 0
        self.step = 0
        self.hint_used = False
        self.selected_evidence: str | None = None
        self.evidence_source = ""
        self.learning_page = 0
        self.learning_target = 0
        self.load_progress()
        self.audio = GameAudio(storage / "audio", self)
        self.audio.set_sound_enabled(bool(self.state.get("sound", True)))
        self.audio.set_music_enabled(bool(self.state.get("music", True)))
        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

        self.setWindowTitle(self.t(APP_TITLE))
        self.resize(1280, 840)
        self.setMinimumSize(960, 640)
        self.setStyleSheet(GLOBAL_QSS)

        self.shell = Shell(self)
        self.setCentralWidget(self.shell)
        self.show_login()

    # -- persistence --------------------------------------------------------
    def load_progress(self) -> None:
        try:
            saved = json.loads(self.save_path.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                for key in self.state:
                    if key in saved:
                        self.state[key] = saved[key]
        except (OSError, ValueError):
            pass
        n = len(self.levels)
        done = self.state.get("done") or []
        if not isinstance(done, list):
            done = []
        self.state["done"] = (done + [False] * n)[:n]
        prog = self.state.get("progress") or []
        if not isinstance(prog, list):
            prog = []
        self.state["progress"] = (prog + [0] * n)[:n]
        if not isinstance(self.state.get("read"), dict):
            self.state["read"] = {}
        if not isinstance(self.state.get("got"), dict):
            self.state["got"] = {}
        try:
            self.state["query_runs"] = max(0, int(self.state.get("query_runs", 0)))
        except (TypeError, ValueError):
            self.state["query_runs"] = 0
        if not isinstance(self.state.get("username"), str):
            self.state["username"] = ""

    def save(self) -> None:
        try:
            self.save_path.write_text(
                json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as error:
            logging.getLogger(__name__).exception("Could not save local progress: %s", error)

    # -- small helpers ------------------------------------------------------
    def t(self, text: str) -> str:
        if self.state.get("language") != "en":
            return text
        if text in EN:
            return EN[text]
        out = text
        for source in sorted(EN, key=len, reverse=True):
            if source and source[0].isalnum() and source[-1].isalnum():
                pattern = rf"(?<!\w){re.escape(source)}(?!\w)"
                out = re.sub(pattern, lambda _: EN[source], out)
            elif source in out:
                out = out.replace(source, EN[source])
        return out

    def source_text(self, text: str) -> str:
        if self.state.get("language") != "en":
            return text
        return next(
            (source for source, translated in EN.items() if translated == text),
            text,
        )

    def translate_markup(self, markup: str) -> str:
        if self.state.get("language") != "en" or markup in EN:
            return self.t(markup)
        values: list[str] = []

        def protect(match: re.Match) -> str:
            values.append(match.group(3))
            return f"{match.group(1)}{match.group(2)}__DATA_VALUE_{len(values) - 1}__{match.group(2)}"

        translated = re.sub(
            r"(data-v\s*=\s*)(['\"])(.*?)\2", protect, markup, flags=re.I | re.S)
        translated = self.t(translated)
        for index, value in enumerate(values):
            translated = translated.replace(f"__DATA_VALUE_{index}__", value)
        return translated

    def toast(self, text: str, error: bool = False) -> None:
        self.shell.toast.flash(self.t(text), error)

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if (event.type() == QEvent.Type.MouseButtonRelease
                and isinstance(watched, QAbstractButton)
                and watched.isEnabled()):
            self.audio.play(660)
        return super().eventFilter(watched, event)

    def add_xp(self, value: int) -> None:
        self.state["xp"] = max(0, int(self.state.get("xp", 0)) + int(value))
        self.save()

    def rank(self) -> str:
        xp = int(self.state.get("xp", 0))
        rank = "Detektif Senior" if xp >= 2500 else "Detektif" if xp >= 1000 else "Magang"
        return self.t(rank)

    def done_count(self) -> int:
        return sum(1 for value in self.state.get("done", []) if value)

    def is_done(self, index: int) -> bool:
        done = self.state.get("done", [])
        return bool(done[index]) if 0 <= index < len(done) else False

    def unlocked(self, index: int) -> bool:
        return index == 0 or self.is_done(index - 1)

    def reset_progress(self) -> None:
        self.state["xp"] = 0
        self.state["done"] = [False] * len(self.levels)
        self.state["read"] = {}
        self.state["progress"] = [0] * len(self.levels)
        self.state["got"] = {}
        self.state["query_runs"] = 0
        self.state["seen"] = False
        self.save()

    def add_read(self, key: str) -> bool:
        read = self.state.setdefault("read", {})
        if not read.get(key):
            read[key] = 1
            self.state["xp"] = int(self.state.get("xp", 0)) + 10
            self.save()
            return True
        return False

    # -- desk / screen management ------------------------------------------
    def fresh_desk(self) -> Desk:
        desk = Desk(self.wallpaper)
        desk.back_btn.setText(f"← {self.t('Layar Awal')}")
        self.shell.set_desk(desk)
        return desk

    def show_screen(self, content: QWidget, title: str, screen_key: str) -> Desk:
        desk = self.fresh_desk()
        desk.set_screen(content, self.t(title), screen_key)
        QTimer.singleShot(0, lambda d=desk: d.screen and d.screen.fit_screen())
        return desk

    def back_to_landing(self) -> None:
        self.landing()

    # -- local profile ------------------------------------------------------
    def show_login(self) -> None:
        self.setWindowTitle(self.t("Mulai bermain"))
        page, box = screen_page()
        card = QWidget()
        card.setFixedWidth(380)
        col = QVBoxLayout(card)
        col.setContentsMargins(0, 4, 0, 8)
        col.setSpacing(10)
        col.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(shield_label(58), 0, Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(brand_title(44, self.t("SIBER"), self.t("DETEKTIF")),
                      0, Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(label(self.t("Nama detektif untuk progres lokal"), 14, False,
                            "#666", True, Qt.AlignmentFlag.AlignHCenter))
        username = line_edit("Nama detektif", self.state.get("username", ""))
        username.setMaxLength(24)
        col.addWidget(field_row("👤", username))
        start = button(self.t("Mulai bermain"), None, "big", 22)
        start.setStyleSheet(
            "QPushButton{background:#6cc4ff;color:#111;border:3px solid #111;"
            "border-radius:0;padding:18px 34px;font-weight:800;}"
            "QPushButton:hover{background:#8ed2ff;}"
            "QPushButton:pressed{background:#3dc6ff;}")
        hard_shadow(start, 4, 4)
        col.addWidget(start)
        col.addWidget(label(self.t("Progres hanya tersimpan di perangkat ini."),
                            12, False, "#888", True, Qt.AlignmentFlag.AlignHCenter))

        def submit() -> None:
            name = username.text().strip()
            if not name:
                self.toast("Isi nama detektif terlebih dahulu.", True)
                username.setFocus()
                return
            old_name = self.state.get("username", "")
            if old_name and name.casefold() != old_name.casefold():
                self.reset_progress()
            self.state["username"] = name
            self.state["seen"] = False
            self.save()
            self.audio.set_music_enabled(bool(self.state.get("music", True)))
            self.toast(f"Selamat datang, {name}.")
            self.landing()

        start.clicked.connect(submit)
        username.returnPressed.connect(submit)
        wrap = QHBoxLayout()
        wrap.addStretch(1)
        wrap.addWidget(card)
        wrap.addStretch(1)
        box.addStretch(1)
        box.addLayout(wrap)
        box.addStretch(1)
        self.show_screen(page, "👤 Profil Lokal.exe", "login")
        QTimer.singleShot(50, username.setFocus)

    # -- landing ------------------------------------------------------------
    def landing(self) -> None:
        self.setWindowTitle(self.t(APP_TITLE))
        page, box = screen_page()
        col = QVBoxLayout()
        col.setContentsMargins(0, 6, 0, 18)
        col.setSpacing(13)
        col.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        col.addWidget(badge(self.t("GAME EDUKASI • KEAMANAN SIBER"), CYAN), 0,
                      Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(shield_label(58), 0, Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(brand_title(52, self.t("SIBER"), self.t("DETEKTIF")),
                      0, Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(label(
            self.t("Selidiki kejahatan digital lewat kasus seru, tanpa koding dan tanpa risiko nyata."),
            14, False, "#666", True, Qt.AlignmentFlag.AlignHCenter))

        features = QWidget()
        features.setMaximumWidth(480)
        fbox = QVBoxLayout(features)
        fbox.setContentsMargins(0, 0, 0, 0)
        fbox.setSpacing(13)
        fbox.addWidget(feature_row(
            "🎯", self.t("Kenali modus kejahatan"),
            self.t("Pelajari phishing, tebak sandi, dan kebocoran data lewat kasus nyata.")))
        fbox.addWidget(feature_row(
            "🕵️", self.t("Selidiki seperti detektif"),
            self.t("Periksa tabel, browser, CCTV, dan papan bukti untuk menemukan pelaku.")))
        fbox.addWidget(feature_row(
            "🏆", self.t("Dapatkan EXP dan naik level"),
            self.t("Setiap bukti yang tepat memberi EXP. Makin teliti, makin tinggi levelmu.")))
        col.addWidget(features, 0, Qt.AlignmentFlag.AlignHCenter)

        cap = label(self.t("CARA BERMAIN"), 11, True, "#666")
        col.addWidget(cap, 0, Qt.AlignmentFlag.AlignHCenter)
        flow = QHBoxLayout()
        flow.setSpacing(12)
        flow.addStretch(1)
        steps = [("📁", "Pilih Kasus"), ("🎓", "Belajar"),
                 ("🔎", "Selidiki"), ("🏆", "Tuntaskan")]
        for index, (glyph, text) in enumerate(steps):
            if index:
                arrow = label("→", 16, False, "#888")
                flow.addWidget(arrow, 0, Qt.AlignmentFlag.AlignVCenter)
            flow.addWidget(flow_step(glyph, self.t(text)))
        flow.addStretch(1)
        col.addLayout(flow)

        rules = QWidget()
        rules.setObjectName("landingInstructions")
        rules.setStyleSheet(
            "QWidget#landingInstructions{background:#e4f2ff;border:3px solid #111;}")
        rules.setFixedWidth(520)
        hard_shadow(rules, 4, 4, alpha=150)
        rbox = QVBoxLayout(rules)
        rbox.setContentsMargins(15, 12, 15, 12)
        rbox.setSpacing(3)
        rbox.addWidget(label(self.t("Tata cara bermain"), 15, True, INK))
        rules_text = [
            ("1. Di meja detektif, buka folder <b>Kasus</b> lalu pilih level.",),
            ("2. Baca materi edukasi singkat sebelum kasus dimulai.",),
            ("3. Selidiki lewat Tabel, Browser, CCTV, dan Foto, lalu klik bukti yang kamu temukan.",),
            ("4. Tiap bukti yang tepat memberi EXP. Kasus tuntas membuka level berikutnya.",),
        ]
        for (line,) in rules_text:
            instruction = rich(self.t(line), 14)
            instruction.setMinimumHeight(
                instruction.heightForWidth(rules.width() - 30) + 8)
            rbox.addWidget(instruction)
        col.addWidget(rules, 0, Qt.AlignmentFlag.AlignHCenter)

        start = button(f"🕵️ {self.t('BUKA MEJA DETEKTIF')}", None, "big", 21)
        start.setStyleSheet(
            "QPushButton{background:#6cc4ff;color:#111;border:3px solid #111;"
            "border-radius:0;padding:16px 32px;font-weight:800;}"
            "QPushButton:hover{background:#8ed2ff;}"
            "QPushButton:pressed{background:#3dc6ff;}")
        hard_shadow(start, 4, 4)
        start.clicked.connect(self.open_desk)
        col.addWidget(start, 0, Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(label(
            self.t("Semua skenario fiktif: belajar aman tanpa risiko nyata"),
            12, False, "#888", True, Qt.AlignmentFlag.AlignHCenter))

        box.addLayout(col)
        self.show_screen(page, "🕵️ DetektifSiber.exe", "landing")

    def open_desk(self) -> None:
        self.state["seen"] = True
        self.save()
        self.home()

    # -- learning -----------------------------------------------------------
    def learn(self, level_index: int, page_index: int = 0) -> None:
        level = self.levels[level_index]
        keys = level.get("ed", [])
        if not keys:
            self.start_case(level_index)
            return
        page_index = max(0, min(len(keys) - 1, page_index))
        key = keys[page_index]
        lesson = self.lessons.get(key, ["📖 Materi", "", ""])
        title = self.t(lesson[0] if lesson else "📖 Materi")
        glyph, _, title_text = title.partition(" ")
        last = page_index == len(keys) - 1

        self.learning_target = level_index
        self.learning_page = page_index
        self.setWindowTitle(self.t("Fase Belajar"))

        if self.add_read(key):
            self.toast("+10 XP: materi dibaca")

        page, box = screen_page()
        head = QVBoxLayout()
        head.setContentsMargins(0, 0, 0, 4)
        head.setSpacing(4)
        head.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        head.addWidget(big_headline(f"📖 {self.t('Fase Belajar')}", 28), 0,
                       Qt.AlignmentFlag.AlignHCenter)
        sub = label(
            f"{self.t('Level')} {level_index + 1} • "
            f"{self.t(str(level.get('t', '')))}. "
            + self.t("Baca materi singkat ini sebelum menyelidiki."),
            14, False, "#666", True, Qt.AlignmentFlag.AlignHCenter)
        sub.setMinimumHeight(sub.sizeHint().height())
        head.addWidget(sub)
        head.addWidget(dots_row(
            len(keys), page_index,
            f"{self.t('Materi')} {page_index + 1}/{len(keys)}"), 0,
            Qt.AlignmentFlag.AlignHCenter)
        box.addLayout(head)

        body = QWidget()
        body.setMaximumWidth(760)
        body.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        bl = QVBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(8)
        icon = label(glyph or "📖", 42)
        bl.addWidget(icon)
        bl.addWidget(label(title_text, 24, True, INK))
        lesson_box = QFrame()
        lesson_box.setObjectName("lessonContentCard")
        lesson_box.setStyleSheet(
            "QFrame#lessonContentCard{background:#fff;border:3px solid #111;}")
        hard_shadow(lesson_box, 4, 4, alpha=150)
        lesson_content = QVBoxLayout(lesson_box)
        lesson_content.setContentsMargins(16, 14, 16, 14)
        lesson_content.setSpacing(8)
        lesson_content.addWidget(
            rich(self.t(lesson[1] if len(lesson) > 1 else ""), 14))

        if len(lesson) > 2 and lesson[2]:
            lesson_content.addWidget(rich(f"<i>💡 {self.t(lesson[2])}</i>", 14))

        if last:
            story = level.get("story") or []
            if story:
                lesson_content.addWidget(rich(
                    "<b>📨 " + self.t("Pesan masuk") + "</b><br>"
                    f"{esc(self.t(story[0][0]))}: {self.t(story[0][1])}", 14))
        bl.addWidget(lesson_box)
        box.addWidget(body)

        nav = QHBoxLayout()
        nav.setSpacing(10)
        prev_btn = button(
            f"◂ {self.t('Sebelumnya' if page_index else 'Kembali')}", None, "white", 14)
        prev_btn.setStyleSheet(
            "QPushButton{background:#fff;color:#111;border:3px solid #111;"
            "border-radius:0;padding:8px 15px;font-weight:800;}"
            "QPushButton:hover{background:#fff1c1;}")
        hard_shadow(prev_btn, 3, 3)
        prev_btn.clicked.connect(
            lambda: self.learn(level_index, page_index - 1) if page_index else self.home())
        nav.addWidget(prev_btn)
        if self.is_done(level_index) and not last:
            skip = button(f"{self.t('Lewati')} ▸▸", None, "white", 14)
            skip.clicked.connect(lambda: self.start_case(level_index))
            nav.addWidget(skip)
        nav.addStretch(1)
        next_text = (f"🔎 {self.t('Mulai Penyelidikan')} ▸" if last
                     else f"{self.t('Selanjutnya')} ▸")
        next_btn = button(next_text, None, "primary", 14)
        next_btn.setStyleSheet(
            "QPushButton{background:#6cc4ff;color:#111;border:3px solid #111;"
            "border-radius:0;padding:8px 15px;font-weight:800;}"
            "QPushButton:hover{background:#8ed2ff;}"
            "QPushButton:pressed{background:#3dc6ff;}")
        hard_shadow(next_btn, 3, 3)
        next_btn.clicked.connect(
            lambda: self.start_case(level_index) if last
            else self.learn(level_index, page_index + 1))
        nav.addWidget(next_btn)
        box.addLayout(nav)
        self.show_screen(page, "📖 FaseBelajar.exe", "learning")

    # -- taskbar helpers ----------------------------------------------------
    def refresh_xp(self) -> None:
        desk = self.shell.desk
        if desk is not None:
            desk.xp_label.setText(
                f"{int(self.state.get('xp', 0))} XP · {self.rank()}")

    def linkify(self, markup: str) -> str:
        def repl(match: re.Match) -> str:
            value = html.escape(match.group(2), quote=True)
            text = match.group(3)
            return (f"<a href=\"{value}\" style=\"color:#3d4bb8;font-weight:700;\">"
                    f"{text}</a>")

        return re.sub(
            r"<u\s+data-v=(['\"])(.*?)\1\s*>(.*?)</u>",
            repl, markup, flags=re.I | re.S)

    # -- home desk ----------------------------------------------------------
    def home(self) -> None:
        self.in_case = False
        self.active_level = -1
        self.setWindowTitle(self.t(APP_TITLE))
        desk = self.fresh_desk()
        desk.mode = "desk"
        desk.taskbar.show()
        desk.watermark.show()
        desk.set_status(
            f"{self.t('Kasus')} {self.done_count()}/{len(self.levels)}",
            f"{int(self.state.get('xp', 0))} XP · {self.rank()}",
            f"← {self.t('Layar Awal')}", self.landing,
            f"{self.t('Kasus selesai:')} "
            f"{self.done_count()}/{len(self.levels)}")

        desk.add_icon(self.t("Selamat Datang"), "penyelidik",
                      lambda: desk.open_window("halo"), 1)
        desk.add_icon(self.t("Kasus"), "kasus",
                      lambda: desk.open_window("kasus"), 1)
        desk.add_icon(self.t("Buku Panduan"), "buku-panduan",
                      lambda: desk.open_window("edu"), 1)
        desk.add_icon(self.t("Profil"), "profil",
                      lambda: desk.open_window("profil"), 1)
        desk.add_icon(self.t("Pengaturan"), "pengaturan",
                      lambda: desk.open_window("set"), 1)

        welcome = QWidget()
        wb = QVBoxLayout(welcome)
        wb.setContentsMargins(10, 10, 10, 10)
        wb.setSpacing(0)
        wb.addWidget(rich(
            "<p style='margin:0 0 8px'><b>" + self.t(APP_TITLE) + "</b>: "
            + self.t("selidiki kejahatan digital tanpa koding.") + "</p>"
            "<p style='margin:0'>1. " + self.t("Buka ikon") + " <b>📁 "
            + self.t("Kasus") + "</b>.<br>2. " + self.t("Pilih level dan baca edukasinya.")
            + "<br>3. " + self.t("Cari bukti di Tabel dan Browser.") + "</p>", 14))

        desk.add_window("halo", "penyelidik", self.t("Selamat Datang"),
                        welcome, 156, 40, 440)
        desk.add_window("kasus", "kasus", self.t("Kasus"),
                        self.level_list_panel(), 156, 90, 520)
        desk.add_window("edu", "buku-panduan", self.t("Buku Panduan"),
                        self.book_panel(list(self.lessons.keys())), 160, 260, 460)
        desk.add_window("profil", "profil", self.t("Profil"),
                        self.profile_panel(), 156, 50, 520)
        desk.add_window("set", "pengaturan", self.t("Pengaturan"),
                        self.settings_panel(), 190, 70, 470)
        desk.open_window("halo")
        desk.sync_taskbar()

    def level_list_panel(self) -> QWidget:
        panel = QWidget()
        box = QVBoxLayout(panel)
        box.setContentsMargins(10, 12, 10, 12)
        box.setSpacing(8)
        flow = FlowLayout(None, 0, 16, 12)
        for index, level in enumerate(self.levels):
            locked = index > 0 and not self.is_done(index - 1)
            tile = LevelTile(index, level, locked, self.is_done(index),
                             difficulty=self.t(str(level.get("lv", ""))),
                             translated_title=self.t(str(level.get("t", ""))))
            if not locked:
                tile.clicked.connect(lambda i: self.learn(i, 0))
            flow.addWidget(tile)
        box.addLayout(flow)
        return panel

    # -- guide book ---------------------------------------------------------
    def book_panel(self, keys: list[str]) -> QWidget:
        root = QWidget()
        outer = QHBoxLayout(root)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(0)

        book = QWidget()
        book.setFixedHeight(262)
        book_row = QHBoxLayout(book)
        book_row.setContentsMargins(0, 0, 0, 0)
        book_row.setSpacing(0)
        page = QFrame()
        page.setObjectName("bookPage")
        page.setStyleSheet("QFrame#bookPage{background:#fffdf3;border:3px solid #111;}")
        page_box = QVBoxLayout(page)
        page_box.setContentsMargins(0, 0, 0, 0)
        page_scroll = QScrollArea(page)
        page_scroll.setWidgetResizable(True)
        page_scroll.setFrameShape(QFrame.Shape.NoFrame)
        page_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page_scroll.setStyleSheet("QScrollArea{background:#fffdf3;border:0;}")
        page_inner = QWidget()
        page_inner.setStyleSheet("background:#fffdf3;")
        inner_box = QVBoxLayout(page_inner)
        inner_box.setContentsMargins(13, 11, 13, 11)
        inner_box.setSpacing(4)
        page_box.addWidget(page_scroll)
        book_row.addWidget(page, 1)

        tabs = QScrollArea()
        tabs.setFixedWidth(66)
        tabs.setFrameShape(QFrame.Shape.NoFrame)
        tabs.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        tabs.setStyleSheet("QScrollArea{background:transparent;border:0;}")
        tab_inner = QWidget()
        tab_inner.setStyleSheet("background:transparent;")
        tab_inner.setMinimumWidth(44)
        tab_box = QVBoxLayout(tab_inner)
        tab_box.setContentsMargins(0, 14, 0, 0)
        tab_box.setSpacing(6)
        tab_box.addStretch(1)
        book_row.addWidget(tabs, 0)
        outer.addWidget(book)

        buttons: list[QPushButton] = []

        def show_intro() -> None:
            clear_layout(inner_box)
            inner_box.addWidget(label(self.t("BUKU PANDUAN"), 11, True, RED))
            inner_box.addWidget(label(self.t("Pilih bab di sisi kanan"), 19, True, INK, True))
            inner_box.addWidget(label(self.t("Tiap bab yang dibaca memberi +10 EXP."),
                                       14, False, "#666", True))
            inner_box.addStretch(1)

        def show_chapter(index: int) -> None:
            key = keys[index]
            lesson = self.lessons.get(key, ["📖 Materi", "", ""])
            heading = self.t(lesson[0] if lesson else "📖 Materi")
            glyph, _, title = heading.partition(" ")
            clear_layout(inner_box)
            inner_box.addWidget(label(f"{self.t('BAB')} {index + 1}", 11, True, RED))
            inner_box.addWidget(label(title, 19, True, INK, True))
            inner_box.addWidget(rich(self.t(lesson[1] if len(lesson) > 1 else ""), 14))
            cmc = QWidget()
            cmc.setStyleSheet("background:transparent;border:0;")
            cmc_box = QHBoxLayout(cmc)
            cmc_box.setContentsMargins(8, 7, 8, 7)
            cmc_box.setSpacing(10)
            ic = label(glyph or "📖", 34)
            cmc_box.addWidget(ic, 0, Qt.AlignmentFlag.AlignVCenter)
            tip = rich(self.t(lesson[2] if len(lesson) > 2 else ""), 12, INK, True)
            tip.setStyleSheet("background:transparent;border:0;")
            cmc_box.addWidget(tip, 1)
            inner_box.addWidget(cmc)
            inner_box.addStretch(1)
            for pos, btn in enumerate(buttons):
                active = pos == index
                btn.setFixedSize(44 if active else 34, 34)
                btn.setStyleSheet(
                    f"QPushButton{{background:{COL[pos % 5]};border:3px solid #111;"
                    "border-left:0;font-weight:800;color:#111;}")
            if not self.state.get("read", {}).get(key):
                self.add_read(key)
                self.refresh_xp()

        for index in range(len(keys)):
            btn = QPushButton(str(index + 1))
            set_font(btn, 12, True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(34, 34)
            btn.setStyleSheet(
                f"QPushButton{{background:{COL[index % 5]};border:3px solid #111;"
                "border-left:0;font-weight:800;color:#111;}")
            btn.clicked.connect(lambda _, i=index: show_chapter(i))
            buttons.append(btn)
            tab_box.insertWidget(index, btn)

        show_intro()
        page_scroll.setWidget(page_inner)
        tabs.setWidget(tab_inner)
        return root

    # -- profile ------------------------------------------------------------
    def profile_panel(self) -> QWidget:
        root = QWidget()
        outer = QHBoxLayout(root)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(12)
        main = QWidget()
        main_box = QVBoxLayout(main)
        main_box.setContentsMargins(0, 0, 0, 0)
        main_box.setSpacing(3)
        side = QFrame()
        side.setFixedWidth(140)
        side.setStyleSheet("QFrame{background:#fff1c1;border:3px solid #111;}")
        side_box = QVBoxLayout(side)
        side_box.setContentsMargins(9, 11, 9, 11)
        side_box.setSpacing(2)
        outer.addWidget(main, 1)
        outer.addWidget(side, 0)

        def rebuild() -> None:
            clear_layout(main_box)
            clear_layout(side_box)
            done_n = self.done_count()
            rank = self.t(RANKS[min(4, int(done_n / 2.5))])
            xp = int(self.state.get("xp", 0))
            fraction = xp % 300
            avatar = int(self.state.get("avatar", 0))
            head = QWidget()
            head = QWidget()
            hb = QHBoxLayout(head)
            hb.setContentsMargins(0, 0, 0, 6)
            hb.setSpacing(13)
            avatar_view = AvatarView(avatar, 84)
            hb.addWidget(avatar_view, 0, Qt.AlignmentFlag.AlignTop)
            info = QVBoxLayout()
            info.setContentsMargins(0, 0, 0, 0)
            info.setSpacing(1)
            name = label(self.state.get("username") or "Detektif", 21, True, INK, True)
            info.addWidget(name)
            info.addWidget(label(rank, 14, False, "#666"))
            info.addWidget(label(f"Level {1 + xp // 300}", 15, True, INK))
            hb.addLayout(info, 1)
            main_box.addWidget(head)

            bar = QProgressBar()
            bar.setRange(0, 300)
            bar.setValue(fraction)
            bar.setTextVisible(False)
            bar.setFixedHeight(22)
            bar.setStyleSheet(
                "QProgressBar{background:#fff;border:3px solid #111;}"
                "QProgressBar::chunk{background:#6cc4ff;}")
            main_box.addWidget(bar)
            main_box.addWidget(label(
                f"{fraction} / 300 " + self.t("XP menuju level berikutnya"),
                12, False, "#666", True))
            main_box.addWidget(label(self.t("Karakter"), 17, True, INK))
            char_row = QHBoxLayout()
            char_row.setContentsMargins(0, 0, 0, 0)
            char_row.setSpacing(2)
            buttons: list[AvatarButton] = []

            def choose(value: int) -> None:
                for pos, btn in enumerate(buttons):
                    btn.setChecked(pos == value)
                self.state["avatar"] = value
                self.save()
                avatar_view.set_avatar(value)

            for index in range(len(AVS)):
                btn = AvatarButton(index, 46)
                btn.setChecked(index == avatar)
                btn.clicked.connect(lambda _, i=index: choose(i))
                buttons.append(btn)
                char_row.addWidget(btn)
            char_row.addStretch(1)
            main_box.addLayout(char_row)
            main_box.addWidget(label(self.t("Lencana"), 17, True, INK))
            badges = QWidget()
            badge_flow = FlowLayout(badges, 0, 2, 2)
            for index in range(min(len(BIC), len(self.levels))):
                acquired = self.is_done(index)
                chip = QLabel(BIC[index])
                chip.setFixedSize(34, 34)
                chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
                set_font(chip, 15)
                chip.setToolTip(self.levels[index].get("t", ""))
                if acquired:
                    chip.setStyleSheet(
                        "background:#6cc4ff;border:3px solid #111;border-radius:17px;")
                else:
                    chip.setStyleSheet(
                        "background:#fff;border:3px solid #111;border-radius:17px;"
                        "color:#aaa;")
                    from PySide6.QtWidgets import QGraphicsOpacityEffect

                    effect = QGraphicsOpacityEffect(chip)
                    effect.setOpacity(0.35)
                    chip.setGraphicsEffect(effect)
                badge_flow.addWidget(chip)
            main_box.addWidget(badges)
            main_box.addStretch(1)

            side_box.addWidget(label(self.t("Total XP"), 11, False, INK,
                                     align=Qt.AlignmentFlag.AlignHCenter))
            total = label(f"★ {xp}", 25, True, INK, align=Qt.AlignmentFlag.AlignHCenter)
            side_box.addWidget(total)
            side_box.addWidget(spacer(6))
            quote = label(self.t("Langkah kecil adalah bagian dari solusi besar."),
                          12, False, INK, True, Qt.AlignmentFlag.AlignHCenter, True)
            side_box.addWidget(quote)
            side_box.addStretch(1)

        rebuild()
        return root

    # -- settings -----------------------------------------------------------
    def settings_panel(self) -> QWidget:
        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(10, 10, 10, 10)
        box.setSpacing(0)
        box.addWidget(label(self.t("Sesuaikan pengalaman bermain sesuai keinginanmu."),
                           13, False, "#666", True))
        box.addWidget(spacer(6))

        for key, title in (
            ("music", "Musik latar"),
            ("sound", "Efek Suara"),
        ):
            row = QFrame()
            row.setStyleSheet("QFrame{background:transparent;border:0;"
                              "border-bottom:2px solid #c9cbe0;}")
            rb = QHBoxLayout(row)
            rb.setContentsMargins(0, 6, 0, 6)
            rb.setSpacing(8)
            rb.addWidget(label(self.t(title), 14, True, INK), 1)
            switch = Switch(bool(self.state.get(key)))
            switch.toggled.connect(
                lambda checked, k=key: self.toggle_setting(k, bool(checked)))
            rb.addWidget(switch, 0, Qt.AlignmentFlag.AlignRight)
            box.addWidget(row)

        lang_row = QFrame()
        lang_row.setStyleSheet("QFrame{background:transparent;border:0;"
                               "border-bottom:2px solid #c9cbe0;}")
        lb = QHBoxLayout(lang_row)
        lb.setContentsMargins(0, 8, 0, 8)
        lb.setSpacing(6)
        lb.addWidget(label(self.t("Bahasa"), 14, True, INK), 1)
        current = self.state.get("language", "id")
        id_btn = button(self.t("Bahasa Indonesia"),
                        lambda: self.set_language("id"),
                        "primary" if current != "en" else "white", 12)
        en_btn = button("English", lambda: self.set_language("en"),
                        "primary" if current == "en" else "white", 12)
        lb.addWidget(id_btn)
        lb.addWidget(en_btn)
        box.addWidget(lang_row)
        actions = QHBoxLayout()
        actions.setContentsMargins(0, 8, 0, 0)
        actions.setSpacing(6)
        reset_btn = button(self.t("Reset Progres"), None, "white", 13)
        actions.addWidget(reset_btn)
        out_btn = button(self.t("Ganti Nama"), self.logout, "white", 13)
        actions.addWidget(out_btn)
        actions.addStretch(1)
        box.addLayout(actions)

        armed = {"on": False}

        def restore() -> None:
            armed["on"] = False
            try:
                reset_btn.setText(self.t("Reset Progres"))
            except RuntimeError:
                pass

        def reset_click() -> None:
            if not armed["on"]:
                armed["on"] = True
                reset_btn.setText(self.t("Yakin? Klik lagi"))
                QTimer.singleShot(3500, restore)
                return
            armed["on"] = False
            self.reset_progress()
            self.toast("Progres direset.", True)
            desk = self.shell.desk
            if desk is None or desk.mode != "desk":
                return

            def replace_content(key: str, content: QWidget) -> None:
                win = desk.windows.get(key)
                if win is None:
                    return
                old = win.content_scroll.takeWidget()
                win.content = content
                win.content_scroll.setWidget(content)
                if old is not None:
                    old.deleteLater()
                win.fit_height()

            replace_content("profil", self.profile_panel())
            if self.in_case:
                desk.set_status(
                    self.case_status_text(),
                    f"{int(self.state.get('xp', 0))} XP · {self.rank()}",
                    f"← {self.t('Desktop')}", self.home)
            else:
                replace_content("kasus", self.level_list_panel())
                desk.set_status(
                    f"{self.t('Kasus')} "
                    f"{self.done_count()}/{len(self.levels)}",
                    f"{int(self.state.get('xp', 0))} XP · {self.rank()}",
                    f"← {self.t('Layar Awal')}", self.landing,
                    f"{self.t('Kasus selesai:')} "
                    f"{self.done_count()}/{len(self.levels)}")

        reset_btn.clicked.connect(reset_click)
        return root

    def toggle_setting(self, key: str, checked: bool) -> None:
        self.state[key] = checked
        self.save()
        if key == "music":
            self.audio.set_music_enabled(checked)
        elif key == "sound":
            self.audio.set_sound_enabled(checked)

    def set_language(self, language: str) -> None:
        if language not in ("id", "en") or self.state.get("language") == language:
            return
        self.state["language"] = language
        self.save()
        in_case = bool(getattr(self, "in_case", False))
        old_desk = self.shell.desk
        opened: dict[str, tuple[int, int, bool, bool]] = {}
        active_key = ""
        if old_desk is not None and old_desk.mode == "desk":
            if old_desk.active is not None and not old_desk.active.minimized:
                active_key = old_desk.active.key
            for key, win in old_desk.windows.items():
                opened[key] = (win.x(), win.y(), win.opened, win.minimized)
        if in_case:
            # Rebuild the case chrome in the new language without losing the
            # player's current step, hint, pinned evidence, or open windows.
            index = self.active_level
            step = self.step
            hint = self.hint_used
            selected = self.selected_evidence
            source = self.evidence_source
            got = dict(self.got)
            self.start_case(index, reopen=True)
            self.step = step
            self.hint_used = hint
            self.selected_evidence = selected
            self.evidence_source = source
            self.got = got
            self.refresh_tasks()
            self.refresh_case_status()
            self.refresh_board()
            if hint and step < len(self.tasks):
                task = self.tasks[step]
                self.set_task_message(
                    "hint", str(task[3]) if len(task) > 3 else "")
        else:
            self.home()
        desk = self.shell.desk
        if desk is not None:
            for key, (x, y, was_opened, was_min) in opened.items():
                win = desk.windows.get(key)
                if win is None:
                    continue
                win.move(x, y)
                if was_opened:
                    win.open()
                    if was_min:
                        win.minimize()
            if active_key in desk.windows:
                desk.focus_window(desk.windows[active_key])
            if "set" in desk.windows:
                desk.open_window("set")

    def logout(self) -> None:
        self.state["seen"] = False
        self.save()
        self.audio.set_music_enabled(bool(self.state.get("music", True)))
        self.show_login()

    # -- messages -----------------------------------------------------------
    def messages_panel(self, level: dict, pick=None) -> QWidget:
        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(10, 10, 10, 10)
        box.setSpacing(8)
        for author, text in level.get("story", []):
            bubble = QFrame()
            bubble.setObjectName("storyMessageBubble")
            bubble.setStyleSheet(
                "QFrame#storyMessageBubble{background:#fff;"
                "border:2px solid #0d0f24;border-radius:0;}")
            inner = QVBoxLayout(bubble)
            inner.setContentsMargins(10, 6, 10, 6)
            inner.setSpacing(2)
            inner.addWidget(label(self.t(str(author)), 11, True, "#5b5f8f"))
            body = rich(self.linkify(self.translate_markup(str(text))), 14)
            if pick is not None:
                body.linkActivated.connect(lambda value, p=pick: p(value, "Pesan"))
            inner.addWidget(body)
            box.addWidget(bubble)
        box.addStretch(1)
        return root

    # -- case desk ----------------------------------------------------------
    def start_case(self, index: int, reopen: bool = False) -> None:
        if not 0 <= index < len(self.levels):
            return
        self.in_case = True
        self.active_level = index
        level = self.levels[index]
        self.tasks: list[list] = list(level.get("tk", []))
        self.case_level = level
        n = len(self.tasks)
        saved = int(self.state.get("progress", [0] * len(self.levels))[index] or 0)
        self.step = (
            max(0, min(saved, n))
            if reopen and not self.is_done(index)
            else 0
        )
        self.hint_used = False
        self.selected_evidence = None
        self.evidence_source = ""
        raw_got = self.state.get("got", {}).get(str(index), {})
        self.got: dict[int, str] = {}
        if isinstance(raw_got, dict):
            for key, value in raw_got.items():
                try:
                    at = int(key)
                except (TypeError, ValueError):
                    continue
                if 0 <= at < self.step:
                    self.got[at] = str(value)

        desk = self.fresh_desk()
        desk.mode = "desk"
        desk.taskbar.show()
        desk.watermark.hide()

        def icon(title: str, key: str, window: str) -> None:
            desk.add_icon(self.t(title), key, lambda w=window: desk.open_window(w), 1)

        icon("Berkas", "berkas", "kasus")
        icon("Pesan", "pesan", "pesan")
        icon("Tabel", "tabel", "tabel")
        if index >= 4:
            icon("Terminal", "terminal", "term")
        if level.get("cc"):
            icon("CCTV", "cctv", "cctv")
        icon("Papan Bukti", "papan-bukti", "papan")
        if level.get("cc"):
            icon("Foto TKP", "foto-tkp", "rek")
        desk.add_icon(self.t("Browser"), "browser",
                      lambda: desk.open_window("web"), 2)
        desk.add_icon(self.t("Buku Panduan"), "buku-panduan",
                      lambda: desk.open_window("edu"), 2)
        desk.add_icon(self.t("Profil"), "profil",
                      lambda: desk.open_window("profil"), 2)
        desk.add_icon(self.t("Pengaturan"), "pengaturan",
                      lambda: desk.open_window("set"), 2)

        desk.add_window("kasus", "berkas", self.t("Berkas"),
                        self.tasks_panel(), 156, 14, 350)
        desk.add_window("pesan", "pesan", self.t("Pesan"),
                        self.messages_panel(level, self.set_evidence), 470, 40, 320)
        desk.add_window("tabel", "tabel", self.t("Tabel"),
                        self.table_panel(), 156, 30, 450)
        if index >= 4:
            desk.add_window("term", "terminal", self.t("Terminal"),
                            self.terminal_panel(), 156, 50, 500)
        if level.get("cc"):
            desk.add_window("cctv", "cctv", "CCTV",
                            self.cctv_panel(), 156, 60, 490)
            desk.add_window("rek", "foto-tkp", self.t("Foto TKP"),
                            self.scene_panel(), 156, 90, 480)
        desk.add_window("papan", "papan-bukti", self.t("Papan Bukti"),
                        self.board_panel(), 156, 40, 520)
        desk.add_window("web", "browser", self.t("Browser"),
                        self.browser_panel(), 156, 50, 470)
        desk.add_window("edu", "buku-panduan", self.t("Buku Panduan"),
                        self.book_panel(level.get("ed", [])), 330, 90, 460)
        desk.add_window("profil", "profil", self.t("Profil"),
                        self.profile_panel(), 156, 50, 520)
        desk.add_window("set", "pengaturan", self.t("Pengaturan"),
                        self.settings_panel(), 190, 70, 470)

        desk.set_status(
            self.case_status_text(),
            f"{int(self.state.get('xp', 0))} XP · {self.rank()}",
            f"← {self.t('Desktop')}", self.home)
        desk.open_window("kasus")
        desk.open_window("pesan")
        desk.sync_taskbar()
        self.setWindowTitle(
            f"{self.t('Level')} {index + 1}: {self.t(str(level.get('t', '')))}")
        self.refresh_board()

    def case_status_text(self) -> str:
        total = len(getattr(self, "tasks", []))
        if self.step >= total:
            return self.t("Kasus selesai")
        if self.state.get("language") == "en":
            return f"Step {self.step + 1}/{total}"
        return f"Langkah {self.step + 1}/{total}"

    def refresh_case_status(self) -> None:
        desk = self.shell.desk
        if desk is not None:
            desk.status_label.setText(self.case_status_text())
            desk.status_label.setToolTip(
                f"{self.t('Langkah')} {self.step + 1} "
                f"{self.t('dari')} {len(getattr(self, 'tasks', []))}")
            desk.xp_label.setText(f"{int(self.state.get('xp', 0))} XP · {self.rank()}")

    def set_evidence(self, value, source: str = "") -> None:
        self.selected_evidence = "" if value is None else str(value)
        self.evidence_source = source
        self.update_pin()

    def update_pin(self) -> None:
        if not hasattr(self, "pin_label"):
            return
        if self.selected_evidence is None or not self.selected_evidence.strip():
            self.pin_label.setText(f"📌 {self.t('Belum ada bukti dipilih')}")
        else:
            self.pin_label.setText(
                f"📌 {self.t('Bukti dipilih:')} "
                f"<b>{esc(self.t(self.selected_evidence))}</b> "
                f"<small>({esc(self.t(self.evidence_source))})</small>")

    def tasks_panel(self) -> QWidget:
        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(10, 10, 10, 10)
        box.setSpacing(7)
        self.task_list_box = QVBoxLayout()
        self.task_list_box.setContentsMargins(0, 0, 0, 0)
        self.task_list_box.setSpacing(6)
        box.addLayout(self.task_list_box)

        self.pin_frame = QFrame()
        self.pin_frame.setStyleSheet(
            "QFrame{background:#fff1c1;border:2px dashed #111;border-radius:0;}")
        pin_box = QVBoxLayout(self.pin_frame)
        pin_box.setContentsMargins(8, 6, 8, 6)
        self.pin_label = rich("", 13)
        pin_box.addWidget(self.pin_label)
        box.addWidget(self.pin_frame)
        self.task_actions = QWidget()
        self.task_actions = QWidget()
        actions = QHBoxLayout(self.task_actions)
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(6)
        actions.addWidget(button(self.t("Serahkan bukti"), self.submit_evidence,
                                 "primary", 13))
        actions.addWidget(button(self.t("Petunjuk (−20 XP)"), self.show_hint,
                                 "white", 13))
        actions.addStretch(1)
        box.addWidget(self.task_actions)

        self.task_msg = label("", 13, True, PURPLE, True)
        box.addWidget(self.task_msg)
        self.finish_box = QVBoxLayout()
        self.finish_box.setContentsMargins(0, 0, 0, 0)
        self.finish_box.setSpacing(6)
        box.addLayout(self.finish_box)
        box.addStretch(1)
        self.refresh_tasks()
        return root

    def refresh_tasks(self) -> None:
        if not hasattr(self, "task_list_box"):
            return
        n = len(self.tasks)
        clear_layout(self.task_list_box)
        title = label(
            f"{self.t('Level')} {self.active_level + 1}: "
            f"{self.t(str(self.levels[self.active_level].get('t', '')))}",
            14, True, INK, True)
        self.task_list_box.addWidget(title)
        for i, task in enumerate(self.tasks):
            frame = QFrame()
            if i < self.step:
                bg = "#e4f2ff"
            elif i == self.step:
                bg = "#fff1c1"
            else:
                bg = "#fff"
            active = i == self.step
            border = "#3d4bb8" if active else ("#0e6ba8" if i < self.step else "#111")
            frame.setStyleSheet(
                f"QFrame{{background:{bg};border:2px solid {border};border-radius:0;}}")
            row = QHBoxLayout(frame)
            row.setContentsMargins(7, 5, 7, 5)
            row.setSpacing(5)
            tag = QLabel(self.t(str(task[0])))
            tag.setStyleSheet(
                "background:#111;color:#6cc4ff;border-radius:8px;padding:1px 7px;")
            set_font(tag, 10, True)
            row.addWidget(tag, 0, Qt.AlignmentFlag.AlignTop)
            body = label(self.t(str(task[1])) if i <= self.step else self.t("Terkunci"),
                         12, False, INK, True)
            row.addWidget(body, 1)
            self.task_list_box.addWidget(frame)

        self.update_pin()
        finished = self.step >= n
        self.pin_frame.setVisible(not finished)
        self.task_actions.setVisible(not finished)
        if finished:
            self.task_msg.hide()
        else:
            self.task_msg.show()
        clear_layout(self.finish_box)
        if finished:
            level = self.levels[self.active_level]
            done_card = QFrame()
            done_card.setStyleSheet("QFrame{background:#e4f2ff;border:3px solid #111;}")
            db = QVBoxLayout(done_card)
            db.setContentsMargins(9, 7, 9, 7)
            db.setSpacing(3)
            db.addWidget(rich(f"<b>{self.t(str(level.get('end', '')))}</b> "
                              f"{self.t('Baca folder Edukasi untuk cara mencegahnya.')}", 12))
            self.finish_box.addWidget(done_card)
            row = QHBoxLayout()
            row.setSpacing(6)
            row.addWidget(button(f"← {self.t('Desktop')}", self.home, "white", 12))
            if self.active_level < len(self.levels) - 1:
                nxt = button(f"{self.t('Lanjut ke Level')} "
                             f"{self.active_level + 2} ▶", None, "primary", 12)
                nxt.clicked.connect(lambda: self.learn(self.active_level + 1, 0))
                row.addWidget(nxt)
            row.addStretch(1)
            self.finish_box.addLayout(row)

    def wrong_message(self) -> str:
        task = self.tasks[self.step] if self.step < len(self.tasks) else None
        if self.state.get("language") == "en":
            return (f"Incorrect answer for step {self.step + 1}. Review the clue, "
                    "check the selected evidence, and try again.")
        if task is None:
            return "Belum tepat."
        wants_count = task[0] == "Hitung" or bool(re.match(r"^Berapa|Adakah", str(task[1])))
        value = self.selected_evidence or ""
        numeric = bool(re.fullmatch(r"\d+", value))
        quoted = f'"{value}"'
        source = self.evidence_source or "?"
        if wants_count and not numeric:
            return (f"Langkah ini meminta ANGKA jumlah, tapi yang kamu pilih {quoted} "
                    f"(dari {source}) bukan angka. Saring datanya dulu, lalu klik "
                    "📌 Pakai jumlah ini.")
        if wants_count:
            return (f"Angka {quoted} belum tepat. Periksa lagi syarat saringannya "
                    "(kolom, operator, nilai), lihat baris yang cocok, lalu hitung ulang.")
        if numeric:
            return (f"Langkah ini bukan meminta angka, tapi kamu memilih {quoted}. "
                    "Klik nama, tulisan, atau sosok yang diminta di tugas.")
        return (f"Belum tepat. Yang kamu pilih: {quoted} (dari {source}). Baca lagi "
                "tugas di Berkas, cek tabel, halaman, atau sosok yang disebut, "
                "atau tekan Petunjuk.")

    def submit_evidence(self) -> None:
        if self.step >= len(self.tasks):
            return
        if self.selected_evidence is None or not self.selected_evidence.strip():
            self.audio.play(180)
            self.error_window(
                "Belum ada bukti yang dipilih. Klik sel di Tabel, teks bergaris "
                "bawah di Browser, atau sosok di gambar.", "Peringatan")
            return
        task = self.tasks[self.step]
        pattern = ""
        flags = 0
        if len(task) > 2 and isinstance(task[2], dict):
            pattern = task[2].get("$regex", "")
            if "i" in str(task[2].get("$flags", "")):
                flags |= re.IGNORECASE
        try:
            matched = bool(re.fullmatch(pattern, self.selected_evidence, flags))
        except re.error:
            matched = False
        if not matched:
            self.audio.play(180)
            self.error_window(self.wrong_message())
            return

        self.audio.play(780)
        progress = self.state.setdefault("progress", [0] * len(self.levels))
        old_progress = int(progress[self.active_level] or 0)
        new_step = self.step >= old_progress
        level_before = 1 + int(self.state.get("xp", 0)) // 300
        if new_step:
            gain = 80 if self.hint_used else 100
            self.state["xp"] = int(self.state.get("xp", 0)) + gain
            progress[self.active_level] = self.step + 1
        self.got[self.step] = self.selected_evidence
        got_all = self.state.setdefault("got", {})
        got_all[str(self.active_level)] = {str(k): v for k, v in self.got.items()}
        self.step += 1
        self.hint_used = False
        self.selected_evidence = None
        self.evidence_source = ""
        finished = self.step >= len(self.tasks)
        if finished:
            self.state.setdefault("done", [False] * len(self.levels))[self.active_level] = True
        self.save()
        self.refresh_tasks()
        self.refresh_case_status()
        self.refresh_board()
        self.refresh_xp()
        if finished:
            self.set_task_message("good", self.t("Kasus selesai!"))
        else:
            self.set_task_message("good", self.t("Tepat! Langkah berikutnya terbuka."))
        if new_step:
            self.toast(f"Bukti diterima. Total XP: {int(self.state.get('xp', 0))}")
            level_after = 1 + int(self.state.get("xp", 0)) // 300
            if level_after > level_before:
                self.toast(f"Naik ke Level {level_after}!")

    def set_task_message(self, kind: str, text: str) -> None:
        if not hasattr(self, "task_msg"):
            return
        colors = {"good": "#0e6ba8", "hint": PURPLE, "bad": RED}
        self.task_msg.setStyleSheet(
            f"color:{colors.get(kind, INK)};background:transparent;")
        self.task_msg.setText(self.t(text))
        self.task_msg.show()

    def show_hint(self) -> None:
        if self.step >= len(self.tasks):
            return
        task = self.tasks[self.step]
        self.hint_used = True
        self.set_task_message("hint", str(task[3]) if len(task) > 3 else "")

    # -- evidence board -----------------------------------------------------
    def board_panel(self) -> QWidget:
        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(8, 8, 8, 8)
        self.board_view = SvgView(self.board_svg(), 600 / 340)
        self.board_view.setMinimumHeight(290)
        box.addWidget(self.board_view)
        return root

    def board_svg(self) -> str:
        level = self.levels[self.active_level]
        tasks = level.get("tk", [])
        n = len(tasks)
        step = min(self.step, n)
        fin = step >= n
        positions = [(40, 22), (245, 22), (450, 22),
                     (40, 128), (245, 128), (450, 128)]
        parts = ["<rect width='600' height='340' fill='#c8955a'/>"]
        for i in range(70):
            parts.append(
                f"<circle cx='{(i * 97) % 600}' cy='{(i * 53) % 340}' r='1.6' fill='#a87440'/>")
        parts.append("<rect x='3' y='3' width='594' height='334' fill='none' "
                     "stroke='#5a3f3a' stroke-width='6'/>")
        for i in range(min(step, n) - 1):
            parts.append(
                f"<line x1='{positions[i][0] + 55}' y1='{positions[i][1] + 8}' "
                f"x2='{positions[i + 1][0] + 55}' y2='{positions[i + 1][1] + 8}' "
                "stroke='#d9483a' stroke-width='2.5'/>")
        if fin and n:
            parts.append(
                f"<line x1='{positions[n - 1][0] + 55}' y1='{positions[n - 1][1] + 8}' "
                "x2='300' y2='240' stroke='#d9483a' stroke-width='2.5'/>")
        for i in range(n):
            x, y = positions[i]
            ok = i < step
            value = str(self.got.get(i, ""))
            angle = ((i % 3) - 1) * 2.5
            parts.append(f"<g transform='rotate({angle} {x + 55} {y + 42})'>")
            parts.append(f"<rect x='{x}' y='{y}' width='110' height='84' "
                         f"fill='{'#fff6dd' if ok else '#d9d3c4'}' stroke='#0d0f24' "
                         "stroke-width='2'/>")
            if ok:
                label_text = esc(f"{i + 1}. {self.t(str(tasks[i][0])).upper()}")
                translated_value = self.t(value)
                shown = esc(
                    translated_value if len(translated_value) <= 14
                    else translated_value[:13] + "…")
                parts.append(
                    f"<text x='{x + 55}' y='{y + 34}' text-anchor='middle' "
                    "font-size='10' font-weight='800' fill='#3d4bb8' "
                    f"font-family='Segoe UI'>{label_text}</text>")
                parts.append(
                    f"<text x='{x + 55}' y='{y + 58}' text-anchor='middle' "
                    "font-size='13' font-weight='700' fill='#1b1e42' "
                    f"font-family='Segoe UI'>{shown}</text>")
            else:
                parts.append(
                    f"<text x='{x + 55}' y='{y + 56}' text-anchor='middle' "
                    "font-size='34' font-weight='800' fill='#a39c8a'>?</text>")
            parts.append(f"<circle cx='{x + 55}' cy='{y + 8}' r='5' fill='#d9483a'/>")
            parts.append("</g>")
        culprit = level.get("cul", ["PELAKU", "?", "#ff7a6b", ""])
        parts.append(
            f"<rect x='230' y='232' width='140' height='102' "
            f"fill='{'#fff6dd' if fin else '#d9d3c4'}' stroke='#0d0f24' stroke-width='2'/>"
            "<circle cx='300' cy='240' r='5' fill='#d9483a'/>")
        if fin:
            parts.append(
                f"<text x='300' y='256' text-anchor='middle' font-size='11' "
                f"font-weight='800' fill='#d9483a' font-family='Segoe UI'>"
                f"{esc(self.t(str(culprit[0])))}</text>")
            parts.append("<g transform='translate(300,288) scale(1.25)'>"
                         + body_svg(culprit[2], culprit[3]) + "</g>")
            parts.append(
                f"<text x='300' y='329' text-anchor='middle' font-size='12' "
                f"font-weight='800' fill='#1b1e42' font-family='Segoe UI'>"
                f"{esc(self.t(str(culprit[1])))}</text>")
        else:
            parts.append("<text x='300' y='296' text-anchor='middle' font-size='40' "
                         "font-weight='800' fill='#a39c8a'>?</text>")
            parts.append("<text x='300' y='322' text-anchor='middle' font-size='10' "
                         f"fill='#5b5f8f' font-family='Segoe UI'>"
                         f"{esc(self.t('Belum terungkap'))}</text>")
        return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 340'>"
                + "".join(parts) + "</svg>")

    def refresh_board(self) -> None:
        if hasattr(self, "board_view"):
            self.board_view.set_svg(self.board_svg())

    # -- table --------------------------------------------------------------
    def table_panel(self) -> QWidget:
        level = self.case_level
        db = level.get("db") or {}
        table_names = list(db.keys())
        if not table_names:
            table_names = ["Data"]
            db = {"Data": []}
        state = {
            "tb": table_names[0],
            "rules": [{"c": 0, "o": "=", "v": ""}],
            "sk": None,
            "sd": 1,
            "cnt": 0,
        }
        ops = [
            ("=", self.t("sama dengan")),
            ("c", self.t("mengandung")),
            (">", self.t("lebih dari / sesudah")),
            ("<", self.t("kurang dari / sebelum")),
            ("!", self.t("bukan")),
        ]

        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(10, 10, 10, 10)
        box.setSpacing(6)

        table_tabs = QHBoxLayout()
        table_tabs.setContentsMargins(0, 0, 0, 2)
        table_tabs.setSpacing(5)
        tab_buttons: dict[str, QPushButton] = {}
        for name in table_names:
            tab = button(self.t(name), None, "task", 11, shadow=False)
            tab_buttons[name] = tab
            table_tabs.addWidget(tab)
        table_tabs.addStretch(1)
        box.addLayout(table_tabs)

        box.addWidget(label(self.t("Saring data"), 12, True, INK))
        box.addWidget(label(self.t("(kosongkan nilai untuk menampilkan semua)"),
                            11, False, "#666", True))

        rules_box = QVBoxLayout()
        rules_box.setContentsMargins(0, 2, 0, 0)
        rules_box.setSpacing(4)
        box.addLayout(rules_box)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 2, 0, 0)
        actions.setSpacing(5)
        add_btn = button(self.t("+ Syarat"), None, "white", 11, shadow=False)
        reset_btn = button(self.t("Reset"), None, "white", 11, shadow=False)
        count_label = label("", 11, True, INK, rich=True)
        pin_btn = button(f"📌 {self.t('Pakai jumlah ini')}", None,
                         "primary", 11, shadow=False)
        actions.addWidget(add_btn)
        actions.addWidget(reset_btn)
        actions.addWidget(count_label, 1)
        actions.addWidget(pin_btn)
        box.addLayout(actions)

        table = QTableWidget()
        table.setMinimumHeight(190)
        table.setFixedHeight(215)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.setStyleSheet(
            "QTableWidget{background:#fff;border:2px solid #111;gridline-color:#9aa0d8;}"
            "QTableWidget::item{padding:2px 5px;}"
            "QTableWidget::item:hover{background:#ffe9a8;}"
            "QTableWidget::item:selected{background:#6cc4ff;color:#111;}"
            "QHeaderView::section{background:#c7cbf0;border:1px solid #9aa0d8;"
            "padding:3px 6px;font-weight:800;}"
        )
        box.addWidget(table)

        empty_label = rich(
            f"🚨 {self.t('Tidak ada data yang cocok.')} "
            f"{self.t('Coba ubah atau kurangi syaratnya.')}", 12, RED)
        empty_label.hide()
        box.addWidget(empty_label)
        box.addStretch(1)

        def current_rows() -> list[dict]:
            return list(db[state["tb"]])

        def current_keys() -> list[str]:
            rows = current_rows()
            return list(rows[0].keys()) if rows else []

        def number(value):
            try:
                text = str(value).strip()
                if text == "":
                    return None
                return float(text)
            except (TypeError, ValueError):
                return None

        def apply_filters() -> None:
            rows = current_rows()
            keys = current_keys()
            kept: list[dict] = []
            for row in rows:
                ok = True
                for rule in state["rules"]:
                    value = str(rule["v"])
                    if value == "" or not keys:
                        continue
                    col = keys[min(int(rule["c"]), len(keys) - 1)]
                    a = str(row.get(col, ""))
                    b = self.source_text(value)
                    al, bl = a.lower(), b.lower()
                    na, nb = number(a), number(b)
                    op = rule["o"]
                    if op == "=":
                        ok = al == bl
                    elif op == "!":
                        ok = al != bl
                    elif op == "c":
                        ok = bl in al
                    elif op == ">":
                        ok = (na > nb) if (na is not None and nb is not None) else (al > bl)
                    elif op == "<":
                        ok = (na < nb) if (na is not None and nb is not None) else (al < bl)
                    if not ok:
                        break
                if ok:
                    kept.append(row)
            sort_key = state["sk"]
            if sort_key:
                def row_sort_key(row):
                    n = number(row.get(sort_key, ""))
                    if n is not None:
                        return (0, n)
                    return (1, str(row.get(sort_key, "")).lower())

                kept.sort(key=row_sort_key, reverse=state["sd"] < 0)
            state["cnt"] = len(kept)
            count_label.setText(
                f"{self.t('Ditemukan')} <b>{len(kept)}</b> {self.t('dari')} "
                f"{len(rows)} {self.t('baris')}")
            empty_label.setVisible(not kept)
            table.setRowCount(0)
            table.setColumnCount(len(keys))
            if keys:
                table.setHorizontalHeaderLabels(
                    [f"{self.t(str(k))} ↕" for k in keys])
            table.setRowCount(len(kept))
            for row_index, row in enumerate(kept):
                for col_index, key in enumerate(keys):
                    raw_value = str(row.get(key, ""))
                    item = QTableWidgetItem(self.t(raw_value))
                    item.setData(Qt.ItemDataRole.UserRole, raw_value)
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                    item.setToolTip(self.t(raw_value))
                    table.setItem(row_index, col_index, item)
            if keys:
                table.resizeColumnsToContents()
                table.horizontalHeader().setMinimumSectionSize(42)

        def rebuild_rules() -> None:
            clear_layout(rules_box)
            keys = current_keys()
            rows = current_rows()
            for rule in state["rules"]:
                row = QHBoxLayout()
                row.setContentsMargins(0, 0, 0, 0)
                row.setSpacing(5)
                col = QComboBox()
                col.setMinimumWidth(108)
                for index, key in enumerate(keys):
                    col.addItem(self.t(str(key)), index)
                col.setCurrentIndex(min(int(rule["c"]), max(0, len(keys) - 1)))
                op = QComboBox()
                op.setMinimumWidth(138)
                for code, text in ops:
                    op.addItem(text, code)
                op_index = max(0, [c for c, _ in ops].index(rule["o"]))
                op.setCurrentIndex(op_index)
                edit = line_edit(self.t("pilih / isi nilai"), str(rule["v"]))
                edit.setMinimumWidth(96)
                if keys:
                    values = sorted({
                        self.t(str(x.get(keys[int(rule["c"])], ""))) for x in rows
                    })
                    completer = QCompleter(values, edit)
                    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                    completer.setFilterMode(Qt.MatchFlag.MatchContains)
                    edit.setCompleter(completer)

                def change_col(index: int, target=rule) -> None:
                    target["c"] = index
                    target["v"] = ""
                    rebuild_rules()
                    apply_filters()

                def change_op(index: int, target=rule, combo=op) -> None:
                    target["o"] = combo.itemData(index)
                    apply_filters()

                def change_value(text: str, target=rule) -> None:
                    target["v"] = text
                    apply_filters()

                col.currentIndexChanged.connect(change_col)
                op.currentIndexChanged.connect(change_op)
                edit.textChanged.connect(change_value)
                row.addWidget(col, 0)
                row.addWidget(op, 0)
                row.addWidget(edit, 1)
                rules_box.addLayout(row)

        def select_table(name: str) -> None:
            state["tb"] = name
            state["rules"] = [{"c": 0, "o": "=", "v": ""}]
            state["sk"] = None
            state["sd"] = 1
            for key, tab in tab_buttons.items():
                tab.setProperty("active", "yes" if key == name else "no")
                repolish(tab)
            rebuild_rules()
            apply_filters()

        def add_rule() -> None:
            if len(state["rules"]) < 3:
                state["rules"].append({"c": 0, "o": "=", "v": ""})
                rebuild_rules()
                apply_filters()

        def reset_rules() -> None:
            state["rules"] = [{"c": 0, "o": "=", "v": ""}]
            state["sk"] = None
            state["sd"] = 1
            rebuild_rules()
            apply_filters()

        def sort_by(section: int) -> None:
            keys = current_keys()
            if not 0 <= section < len(keys):
                return
            key = keys[section]
            state["sd"] = -state["sd"] if state["sk"] == key else 1
            state["sk"] = key
            apply_filters()

        def pick_cell(row_index: int, col_index: int) -> None:
            item = table.item(row_index, col_index)
            if item is not None:
                raw_value = item.data(Qt.ItemDataRole.UserRole)
                self.set_evidence(
                    str(raw_value) if raw_value is not None else item.text(),
                    state["tb"])

        for name, tab in tab_buttons.items():
            tab.clicked.connect(lambda _, n=name: select_table(n))
        add_btn.clicked.connect(add_rule)
        reset_btn.clicked.connect(reset_rules)
        pin_btn.clicked.connect(lambda: self.set_evidence(str(state["cnt"]),
                                                          self.t("jumlah baris")))
        table.horizontalHeader().sectionClicked.connect(sort_by)
        table.cellClicked.connect(pick_cell)

        select_table(table_names[0])
        return root

    # -- browser ------------------------------------------------------------
    def browser_panel(self) -> QWidget:
        pages = list(self.case_level.get("web") or [])
        values: list[str] = []

        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(10, 10, 10, 10)
        box.setSpacing(6)

        search_row = QHBoxLayout()
        search_row.setContentsMargins(0, 0, 0, 0)
        search_row.setSpacing(5)
        query = line_edit(self.t("Cari di internet..."))
        search_btn = button(self.t("Cari"), None, "primary", 12, shadow=False)
        home_btn = button(self.t("Beranda"), None, "white", 12, shadow=False)
        search_row.addWidget(query, 1)
        search_row.addWidget(search_btn, 0)
        search_row.addWidget(home_btn, 0)
        box.addLayout(search_row)

        url = label("cariaja.id", 11, False, "#5b5f8f")
        url.setStyleSheet(
            "QLabel{background:#fff;border:2px solid #0d0f24;padding:3px 8px;"
            "color:#5b5f8f;font-family:Consolas,'Courier New',monospace;}")
        box.addWidget(url)

        page = QTextBrowser()
        page.setOpenLinks(False)
        page.setOpenExternalLinks(False)
        page.setFrameShape(QFrame.Shape.NoFrame)
        page.setFixedHeight(252)
        page.setStyleSheet(
            "QTextBrowser{background:#fff;border:2px solid #0d0f24;padding:4px;"
            "color:#111;}")
        page.document().setDocumentMargin(8)
        box.addWidget(page)
        box.addStretch(1)

        def render(inner: str, url_text: str) -> None:
            nonlocal values
            values = []

            def repl(match: re.Match) -> str:
                values.append(html.unescape(match.group(2)))
                return (f"<a href='val:{len(values) - 1}' "
                        f"style='color:#3d4bb8;font-weight:700;'>"
                        f"{match.group(3)}</a>")

            body = re.sub(
                r"<u\s+data-v=(['\"])(.*?)\1\s*>(.*?)</u>",
                repl, inner, flags=re.I | re.S)
            doc = (
                "<style>body{font-family:'Segoe UI',Arial,sans-serif;"
                "font-size:13px;color:#111;} h3{margin:2px 0 6px;}"
                "p{margin:5px 0;} a{color:#3d4bb8;font-weight:700;}"
                "small{color:#5b5f8f;}</style>" + body
            )
            page.setHtml(doc)
            page.verticalScrollBar().setValue(0)
            url.setText(url_text)

        def show_home() -> None:
            render(
                "<h3>🔎 CariAja</h3><p>" + self.t(
                    "Cari petunjuk di internet. Coba kata kunci seperti nama, domain, atau topik kasus.")
                + "</p>",
                "cariaja.id")

        def show_page(index: int) -> None:
            if not 0 <= index < len(pages):
                return
            p = pages[index]
            color = COL[len(str(p[0])) % 5]
            banner = (
                f"<table width='100%' cellspacing='0' cellpadding='6' "
                f"bgcolor='{color}'><tr><td><b>{esc(self.t(p[1]))}</b><br>"
                f"<small>{esc(p[0])}</small></td></tr></table>")
            render(banner + self.translate_markup(str(p[3])) +
                   f"<p><a href='back:'>← {self.t('Kembali ke hasil')}</a></p>",
                   str(p[0]))

        def search() -> None:
            text = query.text().strip()
            if not text:
                return
            words = [w for w in text.lower().split() if len(w) > 2]
            found = []
            for index, p in enumerate(pages):
                haystack = f"{p[0]} {p[1]} {self.t(p[1])} {p[2]}".lower()
                score = sum(1 for w in words if w in haystack)
                if score:
                    found.append((score, index, p))
            found.sort(key=lambda item: -item[0])
            if found:
                parts = [f"<p>{len(found)} {self.t('hasil untuk')} "
                         f"\"{esc(text)}\"</p>"]
                for _, index, p in found:
                    parts.append(
                        f"<p><a href='page:{index}'><b>{esc(self.t(p[1]))}</b></a>"
                        f"<br><small>{esc(p[0])}</small></p>")
                body = "".join(parts)
            else:
                body = (f"<p>{self.t('Tidak ada hasil untuk')} "
                        f"\"{esc(text)}\". {self.t('Coba kata kunci lain.')}</p>")
            encoded_query = QUrl.toPercentEncoding(text).toStdString()
            render(body, "cariaja.id/cari?q=" + encoded_query)

        def on_anchor(link: QUrl) -> None:
            scheme = link.scheme()
            path = link.path()
            if scheme == "val":
                try:
                    index = int(path)
                except ValueError:
                    return
                if 0 <= index < len(values):
                    self.set_evidence(values[index], "Browser")
            elif scheme == "page":
                try:
                    show_page(int(path))
                except ValueError:
                    pass
            elif scheme == "back":
                if query.text().strip():
                    search()
                else:
                    show_home()
            elif scheme == "home":
                show_home()

        def go() -> None:
            if query.text().strip():
                search()

        search_btn.clicked.connect(go)
        home_btn.clicked.connect(show_home)
        query.returnPressed.connect(go)
        page.anchorClicked.connect(on_anchor)
        show_home()
        return root

    # -- terminal -----------------------------------------------------------
    def terminal_panel(self) -> QWidget:
        level = self.case_level
        index = self.active_level
        db = level.get("db") or {}
        colors = {
            "kw": "#6cc4ff",
            "tbl": "#3dc6ff",
            "col": "#a9b3ff",
            "op": "#ff7a6b",
            "val": "#ffd95a",
        }
        trn = {
            "SELECT": "Tampilkan",
            "*": "semua kolom",
            "COUNT(*)": "jumlah baris",
            "FROM": "dari tabel",
            "WHERE": "yang",
            "AND": "dan",
            "=": "sama dengan",
            "<>": "bukan",
            "LIKE": "mirip pola",
            ">": "lebih dari",
            "<": "kurang dari",
            "ORDER BY": "urutkan menurut",
            "DESC": "dari terbesar",
            ",": "dan",
        }
        base = ["SELECT", "*", "FROM", "WHERE"]
        operators = ["="]
        if index >= 3:
            base += ["AND"]
            operators += ["<>", "LIKE"]
        if index >= 5:
            base += ["COUNT(*)", "ORDER BY", "DESC", ","]
            operators += [">", "<"]
        table_names = list(db.keys())
        columns: list[str] = []
        for rows in db.values():
            if rows:
                for key in rows[0].keys():
                    if key not in columns:
                        columns.append(key)
        token_groups: list[tuple[str, str, list]] = [
            ("Perintah", "kw", base),
            ("Tabel", "tbl", table_names),
            ("Kolom", "col", columns),
            ("Operator", "op", operators),
            ("Nilai", "val", list(level.get("vals") or [])),
        ]
        tray: list[dict] = []
        count = 0
        for _, kind, items in token_groups:
            for value in items:
                tray.append({"k": kind, "v": value, "i": count})
                count += 1
        state: dict = {"q": []}

        def tv2(token: dict) -> str:
            value = token["v"]
            if token["k"] == "val":
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    return str(value)
                return "'" + self.t(str(value)) + "'"
            return self.t(str(value))

        def run_query(tokens: list[dict]):
            def fail(message: str) -> NoReturn:
                raise ValueError(message)

            pos = 0

            def peek() -> dict | None:
                return tokens[pos] if pos < len(tokens) else None

            def take() -> dict:
                nonlocal pos
                token = peek()
                if token is None:
                    fail("Perintah belum lengkap.")
                pos += 1
                return token

            if not tokens or tokens[0]["v"] != "SELECT":
                fail("Perintah harus diawali bubble SELECT.")
            pos = 1
            cols: list[str] = []
            is_count = False
            token = peek()
            if token is not None and token["v"] == "COUNT(*)":
                is_count = True
                pos += 1
            elif token is not None and token["v"] == "*":
                cols = ["*"]
                pos += 1
            else:
                token = peek()
                while token is not None and token["k"] == "col":
                    cols.append(str(take()["v"]))
                    token = peek()
                    if token is not None and token["v"] == ",":
                        pos += 1
                        token = peek()
                    else:
                        break
                if not cols:
                    fail("Setelah SELECT pilih *, COUNT(*), atau nama kolom.")
            token = peek()
            if token is None or token["v"] != "FROM":
                fail("Tambahkan bubble FROM, lalu nama tabel.")
            pos += 1
            table_token = take()
            if table_token is None or table_token["k"] != "tbl":
                fail("Setelah FROM pilih nama tabel.")
            table_name = str(table_token["v"])
            rows = db.get(table_name)
            if rows is None:
                fail(f"Tabel {table_name} tidak ditemukan.")
            keys = list(rows[0].keys()) if rows else []
            if cols != ["*"]:
                for col in cols:
                    if col not in keys:
                        fail(f'Kolom "{col}" tidak ada di tabel {table_name}.')
            conditions: list[tuple[str, str, object]] = []
            token = peek()
            if token is not None and token["v"] == "WHERE":
                pos += 1
                while True:
                    col = take()
                    op_token = take()
                    val_token = take()
                    if col is None or col["k"] != "col":
                        fail("Setelah WHERE pilih nama kolom.")
                    if str(col["v"]) not in keys:
                        fail(f'Kolom "{col["v"]}" tidak ada di tabel {table_name}.')
                    if op_token is None or op_token["k"] != "op":
                        fail("Setelah kolom pilih operator (=, <>, LIKE ...).")
                    if val_token is None or val_token["k"] != "val":
                        fail("Setelah operator pilih sebuah nilai.")
                    conditions.append((str(col["v"]), str(op_token["v"]), val_token["v"]))
                    token = peek()
                    if token is not None and token["v"] == "AND":
                        pos += 1
                        continue
                    break
            order_col = None
            descending = False
            token = peek()
            if token is not None and token["v"] == "ORDER BY":
                pos += 1
                col = take()
                if col is None or col["k"] != "col" or str(col["v"]) not in keys:
                    fail("Setelah ORDER BY pilih kolom dari tabel ini.")
                order_col = str(col["v"])
                token = peek()
                if token is not None and token["v"] == "DESC":
                    descending = True
                    pos += 1
            if pos < len(tokens):
                fail("Ada bubble berlebih: " + tv2(tokens[pos]))

            def numeric(value):
                try:
                    text = str(value).strip()
                    if text == "":
                        return None
                    return float(text)
                except (TypeError, ValueError):
                    return None

            def matches(row: dict) -> bool:
                for col, op, raw in conditions:
                    a = row.get(col, "")
                    al, bl = str(a).lower(), str(raw).lower()
                    na, nb = numeric(a), numeric(raw)
                    if op == "=":
                        good = al == bl
                    elif op == "<>":
                        good = al != bl
                    elif op == "LIKE":
                        pattern = re.escape(str(raw).lower()).replace("%", ".*")
                        good = re.fullmatch(pattern, al) is not None
                    elif op == ">":
                        good = (na > nb) if (na is not None and nb is not None) else (al > bl)
                    else:
                        good = (na < nb) if (na is not None and nb is not None) else (al < bl)
                    if not good:
                        return False
                return True

            result = [row for row in rows if matches(row)]
            if order_col:
                def key(row: dict):
                    n = numeric(row.get(order_col, ""))
                    if n is not None:
                        return (0, n)
                    return (1, str(row.get(order_col, "")).lower())

                result.sort(key=key, reverse=descending)
            if is_count:
                return ["COUNT(*)"], [{"COUNT(*)": len(result)}], True
            return (keys if cols == ["*"] else cols), result, False

        def expected() -> list[dict] | None:
            if self.step >= len(self.tasks):
                return None
            task = self.tasks[self.step]
            sources = []
            if len(task) > 3:
                sources.append(str(task[3]))
            sources.append(str(task[1]))
            ordered = sorted(tray, key=lambda t: len(tv2(t)), reverse=True)
            for source in sources:
                start = source.find("SELECT")
                if start < 0:
                    continue
                rest = source[start:]
                picked: list[dict] = []
                while True:
                    rest = rest.lstrip()
                    found = None
                    for token in ordered:
                        if rest.startswith(tv2(token)):
                            found = token
                            break
                    if found is None:
                        break
                    picked.append(found)
                    rest = rest[len(tv2(found)):]
                if len(picked) > 3:
                    return picked
            return None

        def check_html() -> str:
            want = expected()
            if not want:
                return ""
            have = [tv2(t) for t in state["q"]]
            target = [tv2(t) for t in want]
            at = 0
            while at < len(have) and at < len(target) and have[at] == target[at]:
                at += 1
            if at == len(target) and len(have) == len(target):
                return ("<span style='color:#7ce3a0;font-weight:700;'>"
                        "✅ Susunan sudah benar.</span>")
            if at == len(have):
                return ("<span style='color:#ffd95a;font-weight:700;'>🧭 Benar sejauh "
                        f"ini. Berikutnya: <b>{esc(target[at])}</b></span>")
            if at == len(target):
                return ("<span style='color:#ff9c93;font-weight:700;'>🧭 Bubble "
                        f"<b>{esc(have[at])}</b> berlebih.</span>")
            return ("<span style='color:#ff9c93;font-weight:700;'>🧭 Bubble ke-"
                    f"{at + 1} kurang tepat. Coba: <b>{esc(target[at])}</b></span>")

        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        term = QFrame()
        term.setObjectName("terminal")
        term.setStyleSheet("QFrame#terminal{background:#0f1129;border:0;}")
        term_box = QVBoxLayout(term)
        term_box.setContentsMargins(10, 9, 10, 10)
        term_box.setSpacing(5)
        outer.addWidget(term)

        prompt_line = QHBoxLayout()
        prompt_line.setContentsMargins(0, 0, 0, 0)
        prompt_line.setSpacing(6)
        prompt_label = label("detektif@db:~$", 12, True, "#38bdf8")
        prompt_label.setStyleSheet(
            "color:#38bdf8;background:transparent;font-family:Consolas,monospace;")
        prompt_line.addWidget(prompt_label, 0, Qt.AlignmentFlag.AlignTop)
        prompt_holder = QWidget()
        prompt_holder.setStyleSheet("background:transparent;")
        prompt_flow = FlowLayout(prompt_holder, 0, 4, 2)
        prompt_line.addWidget(prompt_holder, 1)
        term_box.addLayout(prompt_line)

        translation = label("", 12, False, "#a9acd0", True, italic=True)
        translation.setStyleSheet("color:#a9acd0;background:transparent;")
        term_box.addWidget(translation)

        tray_holder = QWidget()
        tray_holder.setStyleSheet("background:transparent;")
        tray_box = QVBoxLayout(tray_holder)
        tray_box.setContentsMargins(0, 0, 0, 0)
        tray_box.setSpacing(2)
        tray_height = 0
        for group_name, kind, items in token_groups:
            caption = label(self.t(str(group_name)).upper(), 9, True, "#a9acd0")
            caption.setStyleSheet(
                "color:#a9acd0;background:transparent;letter-spacing:1px;")
            tray_box.addWidget(caption)
            flow = FlowLayout(None, 0, 2, 2)
            chip_sizes: list[QSize] = []
            for value in items:
                token = next(t for t in tray if t["v"] == value and t["k"] == kind)
                chip = QPushButton(tv2(token))
                chip.setCursor(Qt.CursorShape.PointingHandCursor)
                chip.setStyleSheet(
                    f"QPushButton{{background:{colors[kind]};border:2px solid #111;"
                    "border-radius:9px;padding:2px 7px;color:#111;font-weight:700;"
                    "font-family:Consolas,monospace;font-size:11px;}"
                    "QPushButton:hover{background:#fff1c1;}")
                chip.clicked.connect(
                    lambda _, t=token: add_token(t))
                flow.addWidget(chip)
                chip_sizes.append(chip.sizeHint())
            tray_box.addLayout(flow)
            tray_height += 12 + wrapped_height(chip_sizes, 452) + 2
        tray_holder.setMinimumHeight(tray_height)
        term_box.addWidget(tray_holder)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 3, 0, 0)
        actions.setSpacing(6)
        run_btn = button(f"▶ {self.t('Jalankan')}", None, "primary", 12, shadow=False)
        undo_btn = button(f"⌫ {self.t('Hapus')}", None, "white", 12, shadow=False)
        clear_btn = button(f"✕ {self.t('Bersihkan')}", None, "white", 12, shadow=False)
        actions.addWidget(run_btn)
        actions.addWidget(undo_btn)
        actions.addWidget(clear_btn)
        actions.addStretch(1)
        term_box.addLayout(actions)

        results = QWidget()
        results_box = QVBoxLayout(results)
        results_box.setContentsMargins(0, 3, 0, 0)
        results_box.setSpacing(5)
        term_box.addWidget(results)

        def refit() -> None:
            desk = self.shell.desk
            win = desk.windows.get("term") if desk is not None else None
            if win is not None:
                QTimer.singleShot(0, win.fit_height)

        def redraw() -> None:
            clear_layout(prompt_flow)
            chip_sizes: list[QSize] = []
            if not state["q"]:
                empty = label("(kosong)", 12, False, "#a9acd0", italic=True)
                empty.setStyleSheet("color:#a9acd0;background:transparent;")
                prompt_flow.addWidget(empty)
                chip_sizes.append(empty.sizeHint())
            else:
                for position, token in enumerate(state["q"]):
                    chip = QPushButton(tv2(token))
                    chip.setToolTip("Klik untuk menghapus")
                    chip.setCursor(Qt.CursorShape.PointingHandCursor)
                    chip.setStyleSheet(
                        f"QPushButton{{background:{colors[token['k']]};"
                        "border:2px solid #111;border-radius:9px;padding:2px 7px;"
                        "color:#111;font-weight:700;font-family:Consolas,monospace;"
                        "font-size:11px;}"
                        "QPushButton:hover{background:#fff1c1;}")
                    chip.clicked.connect(
                        lambda _, at=position: remove_token(at))
                    prompt_flow.addWidget(chip)
                    chip_sizes.append(chip.sizeHint())
            prompt_holder.setMinimumHeight(wrapped_height(chip_sizes, 345))
            if state["q"]:
                parts = []
                for token in state["q"]:
                    if token["k"] == "val":
                        parts.append(tv2(token))
                    else:
                        translated = trn.get(str(token["v"]))
                        parts.append(
                            self.t(translated) if translated is not None
                            else str(token["v"]))
                translation.setText(" ".join(parts))
            else:
                translation.setText(self.t(
                    "Susun bubble di bawah menjadi sebuah perintah."))

        def add_token(token: dict) -> None:
            state["q"].append(token)
            redraw()
            refit()

        def remove_token(position: int) -> None:
            if 0 <= position < len(state["q"]):
                state["q"].pop(position)
                redraw()
                render_results()

        def render_results(count_run: bool = False) -> None:
            clear_layout(results_box)
            if not state["q"]:
                refit()
                return
            try:
                columns, rows, is_count = run_query(state["q"])
            except ValueError as error:
                error_label = rich(f"🚨 {esc(self.t(str(error)))}", 12, "#ff9c93")
                error_label.setStyleSheet("color:#ff9c93;background:transparent;")
                results_box.addWidget(error_label)
                check = check_html()
                if check:
                    check_label = rich(self.t(check), 12)
                    check_label.setStyleSheet("background:transparent;")
                    results_box.addWidget(check_label)
                refit()
                return
            if count_run:
                self.state["query_runs"] = int(self.state.get("query_runs", 0)) + 1
                self.save()
            if rows:
                table = QTableWidget()
                table.setColumnCount(len(columns))
                table.setHorizontalHeaderLabels(
                    [self.t(str(c)) for c in columns])
                table.setRowCount(len(rows))
                table.verticalHeader().setVisible(False)
                table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
                table.setFixedHeight(min(170, 34 + min(len(rows), 4) * 27))
                table.setStyleSheet(
                    "QTableWidget{background:#fff;border:2px solid #111;"
                    "gridline-color:#9aa0d8;}"
                    "QTableWidget::item{padding:2px 5px;}"
                    "QTableWidget::item:hover{background:#ffe9a8;}"
                    "QTableWidget::item:selected{background:#6cc4ff;color:#111;}"
                    "QHeaderView::section{background:#c7cbf0;border:1px solid #9aa0d8;"
                    "padding:3px 6px;font-weight:800;}"
                )
                for row_index, row in enumerate(rows):
                    for col_index, key in enumerate(columns):
                        raw_value = str(row.get(key, ""))
                        item = QTableWidgetItem(self.t(raw_value))
                        item.setData(Qt.ItemDataRole.UserRole, raw_value)
                        item.setFlags(Qt.ItemFlag.ItemIsEnabled |
                                      Qt.ItemFlag.ItemIsSelectable)
                        table.setItem(row_index, col_index, item)

                def pick_result(row_index: int, col_index: int) -> None:
                    item = table.item(row_index, col_index)
                    if item is not None:
                        raw_value = item.data(Qt.ItemDataRole.UserRole)
                        self.set_evidence(
                            str(raw_value) if raw_value is not None else item.text(),
                            "Terminal")

                table.cellClicked.connect(pick_result)
                table.resizeColumnsToContents()
                results_box.addWidget(table)
            elif not is_count:
                missing = rich(f"🚨 {self.t('Tidak ada data yang cocok.')}", 12,
                               "#ff9c93")
                missing.setStyleSheet("color:#ff9c93;background:transparent;")
                results_box.addWidget(missing)
            footer = QHBoxLayout()
            footer.setContentsMargins(0, 0, 0, 0)
            footer.setSpacing(6)
            if is_count:
                hint_text = self.t("Klik angka hasilnya untuk dijadikan bukti.")
            else:
                hint_text = f"{len(rows)} {self.t('baris')}"
            footer_label = label(hint_text, 11, False, "#e9e7f7")
            footer_label.setStyleSheet("color:#e9e7f7;background:transparent;")
            footer.addWidget(footer_label, 1)
            if not is_count:
                use_btn = button(f"📌 {self.t('Pakai jumlah ini')}", None,
                                 "white", 11, shadow=False)
                use_btn.clicked.connect(
                    lambda: self.set_evidence(str(len(rows)),
                                              self.t("jumlah baris")))
                footer.addWidget(use_btn)
            results_box.addLayout(footer)
            check = check_html()
            if check:
                check_label = rich(check, 11)
                check_label.setStyleSheet("background:transparent;")
                results_box.addWidget(check_label)
            refit()

        def run() -> None:
            render_results(count_run=True)

        def undo() -> None:
            if state["q"]:
                state["q"].pop()
                redraw()
                render_results()

        def clear() -> None:
            state["q"] = []
            redraw()
            clear_layout(results_box)
            refit()

        run_btn.clicked.connect(run)
        undo_btn.clicked.connect(undo)
        clear_btn.clicked.connect(clear)
        redraw()
        return root

    # -- CCTV and crime-scene photo ----------------------------------------
    def scene_panel(self) -> QWidget:
        sc = self.case_level.get("sc") or {}
        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(8, 8, 8, 8)
        box.setSpacing(6)
        view = ScenarioCanvas(
            "scene", str(sc.get("bg", "")), list(sc.get("ch") or []),
            list(sc.get("bub") or []), pick=self.set_evidence)
        box.addWidget(view)
        caption = label(str(sc.get("cap", "")), 12, False, "#38bdf8", True)
        caption.setStyleSheet(
            "background:#0f1129;color:#38bdf8;padding:6px 8px;border-radius:6px;"
            "font-family:Consolas,'Courier New',monospace;")
        box.addWidget(caption)
        box.addStretch(1)
        return root

    def cctv_panel(self) -> QWidget:
        sc = self.case_level.get("sc") or {}
        cc = self.case_level.get("cc") or {}
        duration = float(cc.get("dur", 0) or 0)
        background = str(sc.get("bg", "")).replace("TKP ·", "CCTV ·")
        root = QWidget()
        box = QVBoxLayout(root)
        box.setContentsMargins(8, 8, 8, 8)
        box.setSpacing(6)
        view = ScenarioCanvas(
            "cctv", background, list(cc.get("ch") or []),
            list(cc.get("bub") or []), cc=cc, pick=self.set_evidence)
        box.addWidget(view)

        controls = QHBoxLayout()
        controls.setContentsMargins(0, 0, 0, 0)
        controls.setSpacing(6)
        play_btn = button(f"▶ {self.t('Putar')}", None, "primary", 12, shadow=False)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, int(duration * 10))
        slider.setValue(0)
        slider.setStyleSheet(
            "QSlider::groove:horizontal{height:8px;background:#fff;"
            "border:2px solid #111;}"
            "QSlider::handle:horizontal{width:16px;margin:-5px 0;background:#6cc4ff;"
            "border:2px solid #111;}")
        reset_btn = button("↺", None, "white", 12, shadow=False)
        reset_btn.setToolTip("Ulangi rekaman")
        controls.addWidget(play_btn, 0)
        controls.addWidget(slider, 1)
        controls.addWidget(reset_btn, 0)
        box.addLayout(controls)

        log_label = label("", 11, False, "#38bdf8", True)
        log_label.setMinimumHeight(54)
        log_label.setStyleSheet(
            "background:#0f1129;color:#38bdf8;padding:6px 8px;border-radius:6px;"
            "font-family:Consolas,'Courier New',monospace;")
        box.addWidget(log_label)
        box.addStretch(1)

        def on_time(value: float, playing: bool) -> None:
            play_btn.setText(("⏸ " if playing else "▶ ") + self.t("Jeda" if playing else "Putar"))
            slider.blockSignals(True)
            slider.setValue(int(value * 10))
            slider.blockSignals(False)
            events = [str(event[1]) for event in cc.get("ev") or []
                      if float(event[0]) <= value + 0.001]
            log_label.setText("\n".join(f"• {event}" for event in events))

        def on_slider(value: int) -> None:
            view.seek(value / 10.0)

        view.on_time = on_time
        play_btn.clicked.connect(view.toggle_play)
        reset_btn.clicked.connect(view.reset)
        slider.valueChanged.connect(on_slider)
        on_time(0, False)
        return root

    # -- error window ------------------------------------------------------
    def error_window(self, message: str, title_text: str = "Jawaban salah") -> None:
        desk = self.shell.desk
        if desk is None:
            return
        old = getattr(self, "err_win", None)
        if old is not None:
            old.deleteLater()

        frame = QFrame(desk)
        frame.setObjectName("errorWindow")
        frame.setFixedWidth(min(440, max(240, desk.width() - 32)))
        frame.setStyleSheet(
            "QFrame#errorWindow{background:#f3f3f3;border:3px solid #111;}")
        hard_shadow(frame, 5, 5)
        outer = QVBoxLayout(frame)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        title_bar = QFrame()
        title_bar.setStyleSheet("background:#d9483a;border:0;")
        title_row = QHBoxLayout(title_bar)
        title_row.setContentsMargins(8, 4, 5, 4)
        title_row.setSpacing(4)
        title_label = label(f"⛔ {self.t(title_text)}", 12, True, "#fff")
        title_label.setStyleSheet("color:#fff;background:transparent;")
        title_row.addWidget(title_label)
        title_row.addStretch(1)

        def close() -> None:
            frame.deleteLater()

        close_btn = QPushButton("✕")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFixedSize(22, 20)
        close_btn.setStyleSheet(
            "QPushButton{background:transparent;color:#fff;border:0;"
            "font-weight:800;padding:0;}QPushButton:hover{background:#ffffff44;}")
        close_btn.clicked.connect(close)
        title_row.addWidget(close_btn)
        outer.addWidget(title_bar)

        body = QWidget()
        body_row = QHBoxLayout(body)
        body_row.setContentsMargins(11, 10, 11, 6)
        body_row.setSpacing(10)
        glyph = label("⛔", 38)
        glyph.setFixedWidth(48)
        glyph.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        body_row.addWidget(glyph, 0)
        text = label(self.t(message), 13, False, INK, True)
        text_width = max(1, frame.width() - 92)
        text.setMinimumHeight(max(
            text.sizeHint().height(), text.heightForWidth(text_width)))
        body_row.addWidget(text, 1)
        outer.addWidget(body)

        bottom = QWidget()
        bottom_row = QHBoxLayout(bottom)
        bottom_row.setContentsMargins(11, 0, 11, 10)
        bottom_row.addStretch(1)
        ok_btn = button("OK", close, "primary", 12)
        bottom_row.addWidget(ok_btn)
        outer.addWidget(bottom)

        frame.adjustSize()
        width, height = frame.width(), frame.height()
        frame.move(max(8, (desk.width() - width) // 2),
                   max(8, int(desk.height() * 0.34) - height // 2))
        frame.show()
        frame.raise_()
        self.err_win = frame


# ===========================================================================
# Painted CCTV / crime-scene surface
# ===========================================================================

_CHAR_CACHE: dict[tuple[str, str, str], QPixmap] = {}


def full_character_pixmap(name: str, color: str, marks: str) -> QPixmap:
    key = (name, color, marks)
    if key in _CHAR_CACHE:
        return _CHAR_CACHE[key]
    doc = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='-20 -34 40 84'>"
        "<ellipse cy='27' rx='13' ry='4' fill='#00000055'/>"
        + body_svg(color, marks)
        + "<text y='46' text-anchor='middle' font-size='10' font-weight='700' "
        "fill='#fff' stroke='#0d0f24' stroke-width='3' paint-order='stroke' "
        "font-family='Segoe UI'>" + esc(name) + "</text></svg>"
    )
    pixmap = svg_pixmap(doc, 54, 114, 2.0)
    _CHAR_CACHE[key] = pixmap
    return pixmap


class ScenarioCanvas(QWidget):
    """Paints a 600x340 scene and handles clicking a person."""

    def __init__(self, mode: str, background: str, chars: list, bubbles: list,
                 caption: str = "", cc: dict | None = None,
                 pick: Callable[[str, str], None] | None = None, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.background = background
        self.chars: list[list] = chars
        self.bubbles = bubbles
        self.caption = caption
        self.cc = cc or {}
        self.pick = pick
        self.duration = float(self.cc.get("dur", 0) or 0)
        self.time = 0.0
        self.playing = False
        self.on_time: Callable[[float, bool], None] | None = None
        self.renderer = QSvgRenderer(background.encode("utf-8")) if background else QSvgRenderer()
        policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setMinimumHeight(130)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.timer = None
        if mode == "cctv":
            self.timer = QTimer(self)
            self.timer.setInterval(40)
            self.timer.timeout.connect(self._tick)
            self.timer.start()

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        return max(130, int((width - 4) * 340 / 600) + 4)

    # -- playback -----------------------------------------------------------
    def _emit_time(self) -> None:
        if callable(self.on_time):
            self.on_time(self.time, self.playing)

    def _tick(self) -> None:
        if not self.playing:
            return
        self.time = min(self.duration, self.time + 0.04)
        if self.time >= self.duration:
            self.playing = False
        self.update()
        self._emit_time()

    def toggle_play(self) -> None:
        if self.duration <= 0:
            return
        if self.time >= self.duration:
            self.time = 0.0
        self.playing = not self.playing
        self.update()
        self._emit_time()

    def reset(self) -> None:
        self.time = 0.0
        self.playing = False
        self.update()
        self._emit_time()

    def seek(self, value: float) -> None:
        self.time = max(0.0, min(self.duration, float(value)))
        self.playing = False
        self.update()
        self._emit_time()

    # -- geometry helpers ---------------------------------------------------
    def _stage_rect(self) -> tuple[QRectF, float, float, float]:
        target = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        scale = min(target.width() / 600.0, target.height() / 340.0)
        offset_x = target.x() + (target.width() - 600 * scale) / 2
        offset_y = target.y() + (target.height() - 340 * scale) / 2
        return target, scale, offset_x, offset_y

    def _position(self, char: list) -> tuple[float, float, bool]:
        if self.mode == "scene":
            point = char[2]
            return float(point[0]), float(point[1]), False
        keys = char[2] or []
        if not keys:
            return 300.0, 208.0, False
        for index in range(len(keys) - 1):
            first, second = keys[index], keys[index + 1]
            if float(first[0]) <= self.time <= float(second[0]):
                span = float(second[0]) - float(first[0])
                fraction = (self.time - float(first[0])) / span if span else 0.0
                x = float(first[1]) + (float(second[1]) - float(first[1])) * fraction
                y = float(first[2]) + (float(second[2]) - float(first[2])) * fraction
                moving = first[1] != second[1] or first[2] != second[2]
                return x, y, moving
        last = keys[-1]
        return float(last[1]), float(last[2]), False

    def _positions(self) -> list[tuple[list, float, float, bool]]:
        result: list[tuple[list, float, float, bool]] = []
        for char in self.chars:
            x, y, moving = self._position(char)
            result.append((char, x, y, moving))
        return result

    def _stage_point(self, point) -> tuple[float, float]:
        _, scale, offset_x, offset_y = self._stage_rect()
        if scale <= 0:
            return 0.0, 0.0
        return ((point.x() - offset_x) / scale, (point.y() - offset_y) / scale)

    # -- painting -----------------------------------------------------------
    def paintEvent(self, _) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        target, scale, offset_x, offset_y = self._stage_rect()
        painter.fillRect(target, QColor("#dfe8ff"))
        painter.save()
        painter.translate(offset_x, offset_y)
        painter.scale(scale, scale)
        if self.renderer.isValid():
            self.renderer.render(painter, QRectF(0, 0, 600, 340))

        positions = self._positions()
        bubble_font = QFont("Segoe UI")
        bubble_font.setPixelSize(11)
        bubble_font.setWeight(QFont.Weight.Bold)
        for char, x, y, moving in positions:
            bob = 0.0
            if self.mode == "cctv":
                if moving:
                    bob = -abs(math.sin(self.time * 14)) * 2.0
                else:
                    bob = math.sin(self.time * 5) * 0.8
            pixmap = full_character_pixmap(str(char[0]), str(char[1]),
                                           str(char[3]) if len(char) > 3 else "")
            painter.drawPixmap(QPointF(x - 27, y + bob - 46), pixmap)

        for bubble in self.bubbles:
            if self.mode == "cctv":
                if not (float(bubble[0]) <= self.time <= float(bubble[1])):
                    continue
                name, text = bubble[2], bubble[3]
            else:
                name, text = bubble[0], bubble[1]
            match = next((p for p in positions if str(p[0][0]) == str(name)), None)
            if match is None:
                continue
            _, x, y, moving = match
            bob = 0.0
            if self.mode == "cctv":
                if moving:
                    bob = -abs(math.sin(self.time * 14)) * 2.0
                else:
                    bob = math.sin(self.time * 5) * 0.8
            width = len(str(text)) * 6.3 + 14
            bx, by = x - width / 2, y + bob - 70
            painter.setPen(QPen(QColor(DEEP), 2))
            painter.setBrush(QColor("#fff"))
            painter.drawRoundedRect(QRectF(bx, by, width, 18), 6, 6)
            painter.setPen(QColor("#1b1e42"))
            painter.setFont(bubble_font)
            painter.drawText(QRectF(bx + 7, by, width - 8, 18),
                             Qt.AlignmentFlag.AlignVCenter, str(text))

        if self.mode == "cctv":
            start = str(self.cc.get("t0", "00:00:00")).split(":")
            try:
                base = int(start[0]) * 3600 + int(start[1]) * 60 + int(start[2])
            except (ValueError, IndexError):
                base = 0
            clock = base + int(self.time)
            stamp = (f"{clock // 3600:02d}:{(clock % 3600) // 60:02d}:"
                     f"{clock % 60:02d}")
            label_font = QFont("Consolas")
            label_font.setPixelSize(13)
            label_font.setWeight(QFont.Weight.Bold)
            painter.setFont(label_font)
            painter.setPen(QColor(RED))
            painter.drawText(QPointF(14, 332), f"● REC {stamp}")
        painter.restore()

        if self.mode == "cctv":
            path = QPainterPath()
            path.addRoundedRect(target.adjusted(1, 1, -1, -1), 6, 6)
            painter.save()
            painter.setClipPath(path)
            scan_pen = QPen(QColor(0, 0, 0, 34))
            scan_pen.setWidth(1)
            painter.setPen(scan_pen)
            y = target.top()
            while y < target.bottom():
                painter.drawLine(QPointF(target.left(), y), QPointF(target.right(), y))
                y += 3
            painter.restore()

        painter.setPen(QPen(QColor(DEEP), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(target, 6, 6)
        painter.end()

    # -- interaction --------------------------------------------------------
    def _hit(self, point) -> list | None:
        x, y = self._stage_point(point)
        for char, cx, cy, _ in reversed(self._positions()):
            if abs(x - cx) <= 27 and (cy - 50) <= y <= (cy + 68):
                return char
        return None

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self._hit(event.position()) is not None:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        char = self._hit(event.position())
        if char is not None and callable(self.pick):
            self.pick(str(char[0]), "CCTV" if self.mode == "cctv" else "Foto TKP")
        super().mouseReleaseEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    app.setOrganizationName("Detektif Siber")
    app.setStyle("Fusion")
    base = QFont("Segoe UI")
    base.setPixelSize(14)
    app.setFont(base)
    window = NativeGame()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
