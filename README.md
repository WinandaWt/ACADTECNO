
saya disuruh buat codingan AI Chatbot mengenai 
Smart Academic Chatbot
Bangun chatbot akademik yang mampu menjawab pertanyaan terkait:

Jadwal kuliah
KRS
Skripsi
Jadwal sidang
Informasi akademik lainnya nah saya bingung mengenai akademik buat apa
20.29
P: Chatbot ini untuk kampus nyata atau demo/portofolio?
J: Demo/Portofolio (data dummy)

P: Fitur apa saja yang ingin ditampilkan? (Pilih semua yang sesuai)
J: Kalender akademik, saya

P: Teknologi yang diinginkan?
J: Bebas, yang penting jadi

20.30
Oke, saya akan buatkan Smart Academic Chatbot lengkap dengan data dummy, semua fitur (Jadwal kuliah & KRS, Info skripsi & sidang, Kalender akademik, FAQ umum), pakai React yang sudah di-power oleh Claude AI!

V

Menghubungkan ke visualize...
Ini chatbot akademik kamu sudah jadi! Berikut ringkasan fitur yang sudah ada:

Fitur yang tersedia:

Jadwal Kuliah — tabel lengkap hari, jam, ruang, dan dosen
KRS — daftar mata kuliah + status persetujuan + total SKS
Skripsi — syarat, tahapan, dan batas waktu
Jadwal Sidang — daftar peserta sidang gelombang I
Kalender Akademik — semua periode akademik dengan status (berlangsung/selesai/mendatang)
Beasiswa — info beasiswa yang tersedia
Kontak Admin — info BAAK dan helpdesk
Nilai/IPK — panduan cek nilai dan transkrip
Cara pakai:

Klik tombol di sidebar kiri untuk topik cepat
Atau ketik pertanyaan bebas seperti "Kapan UAS?", "Syarat skripsi apa?", dll.
Klik chip/tag yang muncul di jawaban bot untuk navigasi cepat
Kalau kamu mau lanjut, saya bisa bantu:

Export ke file HTML yang bisa langsung dibuka di browser
Integrasikan Claude AI supaya bisa jawab pertanyaan bebas (bukan hanya keyword)
Tambah fitur login mahasiswa dengan NIM/password
Mau lanjut yang mana?

Klik tombol di sidebar kiri untuk topik cepat

Atau ketik pertanyaan bebas seperti "Kapan UAS?", "Syarat skripsi apa?", dll.
Klik chip/tag yang muncul di jawaban bot untuk navigasi cepat dan buatkan codingan phyton nya
20.37
Oke, saya buatkan versi Python-nya! Ini akan jadi chatbot berbasis terminal (CLI) yang bisa dijalankan langsung.


Melihat file, membuat file, menjalankan perintah
Melihat file, membuat file, menjalankan perintah
Berjalan sempurna! ✅


Presented file
Presented file
Chatbot Python-nya sudah siap! Cara menjalankan:

bash
python3 academic_chatbot.py
Fitur yang ada di versi Python ini:

Fitur	Detail
Menu bernomor	Ketik 1–8 langsung masuk ke topik
Pertanyaan bebas	Ketik "syarat skripsi?", "kapan uas?" dll
Tabel berwarna	Output rapi dengan warna di terminal
Badge status	[Disetujui] hijau, [Menunggu] kuning, dll
Salam dinamis	Otomatis deteksi pagi/siang/sore/malam
Regex matching	Mengenali variasi kata kunci
Contoh input yang bisa dicoba:

1 atau jadwal kuliah
krs atau matkul diambil
syarat skripsi atau tugas akhir
kapan uas atau kalender
beasiswa atau info kip
menu untuk kembali ke daftar
Mau ditambahkan fitur lain? Misalnya simpan data ke file JSON, login NIM mahasiswa, atau ekspor ke format lain?


Academic chatbot
PY 
Klik tombol di sidebar kiri untuk topik cepat
* Atau ketik pertanyaan bebas seperti "Kapan UAS?", "Syarat skripsi apa?", dll.
* Klik chip/tag yang muncul di jawaban bot untuk navigasi cepat dan  buatkan website chatbot ini dengan codingan phyton nya dan juga cara langkah 2

20.39
Oke! Saya buatkan website chatbot lengkap dengan backend Python (Flask) + frontend HTML, beserta langkah-langkah menjalankannya.


Membuat 6 file, menjalankan 3 perintah
Membuat 6 file, menjalankan 3 perintah
Semua topik berjalan sempurna ✅


Presented 6 files
Presented 6 files
Semua file sudah siap! Berikut langkah-langkah lengkapnya:

📁 Struktur File yang Dibuat
academic_chatbot_web/
├── app.py              ← Backend Python (Flask)
├── requirements.txt    ← Library yang dibutuhkan
├── README.md           ← Panduan lengkap
├── templates/
│   └── index.html      ← Halaman website
└── static/
    ├── style.css       ← Tampilan/desain
    └── app.js          ← Logika kirim-terima pesan
🚀 Cara Menjalankan (6 Langkah)
Langkah 1 — Pastikan Python 3.8+ sudah terinstall:

bash
python --version
Langkah 2 — Masuk ke folder project:

bash
cd academic_chatbot_web
Langkah 3 — Buat virtual environment (disarankan):

bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
Langkah 4 — Install Flask:

bash
pip install -r requirements.txt
Langkah 5 — Jalankan server:

bash
python app.py
Langkah 6 — Buka browser, ketik:

http://localhost:5000
Chatbot langsung bisa dipakai! Mau ditambahkan fitur login NIM mahasiswa, database MySQL, atau deploy ke hosting?


App
PY 

Index
Kode · HTML 

Style
Kode · CSS 

App
JS 

Requirements
TXT 

Readme
Dokumen · MD 





Claude adalah AI dan bisa keliru. Harap periksa kembali respons.


raw
Readme · MD
# 🎓 Smart Academic Chatbot — Universitas Nusantara
 
Chatbot akademik berbasis web menggunakan **Python (Flask)** sebagai backend
dan **HTML/CSS/JavaScript** sebagai frontend.
 
---
 
## 📁 Struktur Project
 
```
academic_chatbot_web/
├── app.py                  ← Backend utama (Flask + logika chatbot)
├── requirements.txt        ← Daftar library Python
├── templates/
│   └── index.html          ← Halaman website chatbot
└── static/
    ├── style.css           ← Tampilan / desain
    └── app.js              ← Logika frontend (kirim & terima pesan)
```
 
---
 
## 🚀 Langkah-Langkah Menjalankan
 
### LANGKAH 1 — Pastikan Python sudah terinstall
 
Buka terminal / command prompt, ketik:
 
```bash
python --version
```
 
Harus muncul versi Python 3.8 ke atas. Jika belum ada, download di:
👉 https://www.python.org/downloads/
 
---
 
### LANGKAH 2 — Pindah ke folder project
 
```bash
cd academic_chatbot_web
```
 
---
 
### LANGKAH 3 — (Opsional tapi disarankan) Buat Virtual Environment
 
```bash
# Buat virtual environment
python -m venv venv
 
# Aktifkan (Windows)
venv\Scripts\activate
 
# Aktifkan (Mac / Linux)
source venv/bin/activate
```
 
---
 
### LANGKAH 4 — Install library Flask
 
```bash
pip install -r requirements.txt
```
 
Tunggu hingga selesai. Hanya perlu dilakukan sekali.
 
---
 
### LANGKAH 5 — Jalankan server
 
```bash
python app.py
```
 
Akan muncul output seperti:
 
```
=======================================================
  🎓  Smart Academic Chatbot — Universitas Nusantara
  🌐  Buka browser: http://localhost:5000
  🛑  Stop server: tekan CTRL+C
=======================================================
 * Running on http://127.0.0.1:5000
```
 
---
 
### LANGKAH 6 — Buka di browser
 
Buka browser (Chrome / Firefox / Edge), ketik di address bar:
 
```
http://localhost:5000
```
 
Chatbot siap digunakan! ✅
 
---
 
## 💬 Cara Pakai Chatbot
 
| Cara | Contoh |
|------|--------|
| Klik sidebar kiri | Klik "Jadwal Kuliah" |
| Ketik pertanyaan bebas | "Kapan UAS dimulai?" |
| Klik chip/tag di jawaban | Klik chip yang muncul |
| Ketik nomor/kata kunci | "krs", "skripsi", "sidang" |
 
---
 
## 🛑 Menghentikan Server
 
Tekan `CTRL + C` di terminal.
 
---
 
## 🔧 Kustomisasi Data
 
Semua data dummy ada di bagian atas `app.py`:
 
- `JADWAL_KULIAH` — jadwal kuliah
- `KRS` — daftar mata kuliah
- `JADWAL_SIDANG` — jadwal sidang skripsi
- `KALENDER_AKADEMIK` — kalender akademik
- `SKRIPSI_INFO` — info skripsi
- `BEASISWA` — daftar beasiswa
Ubah sesuai data kampus kamu, lalu restart server.
 
