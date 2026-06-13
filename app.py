"""
ACADTECNO Smart Campus — Flask backend.

Demo akademik untuk portofolio: menjawab jadwal kuliah, KRS, skripsi,
sidang, kalender akademik, beasiswa, presensi, UKT, magang, wisuda,
dan analisis mahasiswa berbasis data dummy.
"""

from __future__ import annotations

import html
import re
from difflib import SequenceMatcher
from statistics import mean
from typing import Any

from flask import Flask, jsonify, render_template, request


app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static",
)

ALLOWED_ORIGINS = {
    "http://localhost:3000",
    "http://127.0.0.1:3000",
}


@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


CAMPUS_PROFILE = {
    "nama": "Fakultas Teknologi Industri dan Informatika",
    "tahun_akademik": "2025/2026",
    "semester": "Genap",
    "portal": "https://siakad.ftii.ac.id",
    "helpdesk": "helpdesk@ftii.ac.id",
}

JADWAL_KULIAH = [
    {"hari": "Senin", "jam": "08.00–10.00", "matkul": "Algoritma & Pemrograman", "ruang": "Lab A1", "dosen": "Dr. Budi Santoso", "mode": "Praktikum"},
    {"hari": "Senin", "jam": "13.00–15.00", "matkul": "Basis Data", "ruang": "R.204", "dosen": "Ir. Sari Dewi, M.T.", "mode": "Tatap muka"},
    {"hari": "Selasa", "jam": "09.00–11.00", "matkul": "Kecerdasan Buatan", "ruang": "Lab AI", "dosen": "Dr. Maya Putri", "mode": "Hybrid"},
    {"hari": "Rabu", "jam": "10.00–12.00", "matkul": "Jaringan Komputer", "ruang": "Lab B2", "dosen": "Drs. Hendra, M.Kom.", "mode": "Praktikum"},
    {"hari": "Kamis", "jam": "08.00–10.00", "matkul": "Rekayasa Perangkat Lunak", "ruang": "R.305", "dosen": "Dr. Nadia Kirana", "mode": "Tatap muka"},
    {"hari": "Jumat", "jam": "13.00–15.00", "matkul": "Etika Profesi", "ruang": "R.102", "dosen": "Drs. Bambang, M.H.", "mode": "Tatap muka"},
]

KRS = [
    {"kode": "IF301", "nama": "Algoritma & Pemrograman", "sks": 3, "status": "Disetujui"},
    {"kode": "IF302", "nama": "Basis Data", "sks": 3, "status": "Disetujui"},
    {"kode": "IF309", "nama": "Kecerdasan Buatan", "sks": 3, "status": "Disetujui"},
    {"kode": "IF303", "nama": "Jaringan Komputer", "sks": 3, "status": "Menunggu"},
    {"kode": "IF304", "nama": "Rekayasa Perangkat Lunak", "sks": 3, "status": "Disetujui"},
    {"kode": "UN101", "nama": "Etika Profesi", "sks": 2, "status": "Disetujui"},
]

KALENDER_AKADEMIK = [
    {"kegiatan": "Pendaftaran KRS", "mulai": "2 Feb 2026", "akhir": "14 Feb 2026", "status": "Selesai"},
    {"kegiatan": "Perubahan KRS", "mulai": "16 Feb 2026", "akhir": "21 Feb 2026", "status": "Selesai"},
    {"kegiatan": "Perkuliahan Semester Genap", "mulai": "17 Feb 2026", "akhir": "29 Mei 2026", "status": "Selesai"},
    {"kegiatan": "UTS", "mulai": "30 Mar 2026", "akhir": "10 Apr 2026", "status": "Selesai"},
    {"kegiatan": "UAS", "mulai": "8 Jun 2026", "akhir": "20 Jun 2026", "status": "Berlangsung"},
    {"kegiatan": "Sidang Skripsi Gelombang I", "mulai": "12 Jun 2026", "akhir": "19 Jun 2026", "status": "Berlangsung"},
    {"kegiatan": "Input Nilai Akhir", "mulai": "22 Jun 2026", "akhir": "30 Jun 2026", "status": "Mendatang"},
    {"kegiatan": "Perwalian Semester Ganjil", "mulai": "13 Jul 2026", "akhir": "25 Jul 2026", "status": "Mendatang"},
]

JADWAL_SIDANG = [
    {"nama": "Ahmad Fauzan", "tanggal": "12 Jun 2026", "jam": "09.00", "ruang": "Aula A", "penguji": "Dr. Budi S.", "status": "Terjadwal"},
    {"nama": "Siti Nurhaliza", "tanggal": "12 Jun 2026", "jam": "11.00", "ruang": "Aula A", "penguji": "Prof. Agus W.", "status": "Terjadwal"},
    {"nama": "Arif Hidayat", "tanggal": "15 Jun 2026", "jam": "09.00", "ruang": "R.501", "penguji": "Dr. Maya P.", "status": "Terjadwal"},
    {"nama": "Reza Saputra", "tanggal": "16 Jun 2026", "jam": "13.00", "ruang": "R.501", "penguji": "Ir. Sari D.", "status": "Menunggu berkas"},
    {"nama": "Dimas Saputra", "tanggal": "19 Jun 2026", "jam": "10.00", "ruang": "Aula B", "penguji": "Drs. Hendra", "status": "Terjadwal"},
]

SKRIPSI_INFO = {
    "syarat": [
        "IPK minimal 2.75 dan SKS lulus minimal 120",
        "Lulus mata kuliah Metodologi Penelitian",
        "Tidak memiliki tunggakan administrasi akademik",
        "Mengunggah proposal, transkrip sementara, dan kartu bimbingan",
        "Mendapat persetujuan dosen wali serta ketua program studi",
    ],
    "tahapan": [
        "Pengajuan judul melalui SIAKAD",
        "Validasi kaprodi dan penunjukan pembimbing",
        "Seminar proposal",
        "Bimbingan penelitian minimal 8 kali",
        "Seminar hasil",
        "Sidang skripsi",
        "Revisi final dan unggah repository kampus",
    ],
    "tips": [
        "Gunakan topik yang datanya bisa diakses dalam 2–4 minggu.",
        "Buat log bimbingan setiap pertemuan agar proses revisi terlacak.",
        "Cek plagiarisme sebelum mendaftar seminar hasil.",
    ],
}

BEASISWA = [
    {"nama": "Beasiswa Prestasi Akademik", "syarat": "IPK ≥ 3.50", "deadline": "30 Jun 2026"},
    {"nama": "Beasiswa KIP-Kuliah", "syarat": "Mahasiswa aktif dan memenuhi syarat ekonomi", "deadline": "Hubungi BAK"},
    {"nama": "Beasiswa Industri Digital", "syarat": "IPK ≥ 3.30, portofolio/proyek aktif", "deadline": "15 Jul 2026"},
    {"nama": "Beasiswa Riset Mahasiswa", "syarat": "Proposal riset disetujui pembimbing", "deadline": "25 Jul 2026"},
]

LAYANAN = [
    {"layanan": "Surat aktif kuliah", "estimasi": "1 hari kerja", "kanal": "BAAK / SIAKAD"},
    {"layanan": "Legalisir transkrip", "estimasi": "2 hari kerja", "kanal": "Loket akademik"},
    {"layanan": "Cuti akademik", "estimasi": "3 hari kerja", "kanal": "Dosen wali + BAAK"},
    {"layanan": "Perubahan biodata", "estimasi": "1–2 hari kerja", "kanal": "Helpdesk SIAKAD"},
]

DOSEN_BIMBINGAN = [
    {
        "nama": "Dr. Budi Santoso",
        "bidang": "Kecerdasan Buatan & Machine Learning",
        "email": "budi.santoso@ftii.ac.id",
        "keywords": ["budi", "budi santoso", "santoso"],
        "jam_konsultasi": [
            {"hari": "Senin", "jam": "10.00–12.00", "ruang": "R.301", "status": "Tersedia"},
            {"hari": "Rabu", "jam": "13.00–15.00", "ruang": "R.301", "status": "Tersedia"},
            {"hari": "Jumat", "jam": "09.00–11.00", "ruang": "R.301", "status": "Penuh"},
        ],
        "bimbingan": [
            {"tanggal": "2 Jun 2026", "mahasiswa": "Ahmad Fauzan", "nim": "2023001", "topik": "Revisi BAB III – Metodologi Penelitian", "status": "Selesai"},
            {"tanggal": "5 Jun 2026", "mahasiswa": "Fajar Ramadhan", "nim": "2023007", "topik": "Pengajuan judul penelitian", "status": "Selesai"},
            {"tanggal": "10 Jun 2026", "mahasiswa": "Ahmad Fauzan", "nim": "2023001", "topik": "Revisi BAB IV – Hasil & Pembahasan", "status": "Selesai"},
            {"tanggal": "16 Jun 2026", "mahasiswa": "Reza Saputra", "nim": "2023013", "topik": "Persiapan sidang skripsi", "status": "Berlangsung"},
            {"tanggal": "20 Jun 2026", "mahasiswa": "Fajar Ramadhan", "nim": "2023007", "topik": "Seminar proposal", "status": "Mendatang"},
            {"tanggal": "25 Jun 2026", "mahasiswa": "Ahmad Fauzan", "nim": "2023001", "topik": "Revisi final & persiapan unggah", "status": "Mendatang"},
        ],
    },
    {
        "nama": "Dr. Maya Putri",
        "bidang": "Data Science & Analitik Bisnis",
        "email": "maya.putri@ftii.ac.id",
        "keywords": ["maya", "maya putri", "putri"],
        "jam_konsultasi": [
            {"hari": "Selasa", "jam": "09.00–11.00", "ruang": "Lab AI", "status": "Tersedia"},
            {"hari": "Kamis", "jam": "13.00–15.00", "ruang": "Lab AI", "status": "Tersedia"},
        ],
        "bimbingan": [
            {"tanggal": "3 Jun 2026", "mahasiswa": "Siti Nurhaliza", "nim": "2023002", "topik": "Analisis dataset penelitian", "status": "Selesai"},
            {"tanggal": "8 Jun 2026", "mahasiswa": "Rina Oktavia", "nim": "2023006", "topik": "Pengolahan dan visualisasi data", "status": "Selesai"},
            {"tanggal": "13 Jun 2026", "mahasiswa": "Dimas Saputra", "nim": "2023018", "topik": "Revisi proposal penelitian", "status": "Selesai"},
            {"tanggal": "17 Jun 2026", "mahasiswa": "Siti Nurhaliza", "nim": "2023002", "topik": "Finalisasi BAB V – Penutup", "status": "Berlangsung"},
            {"tanggal": "22 Jun 2026", "mahasiswa": "Rina Oktavia", "nim": "2023006", "topik": "Seminar hasil penelitian", "status": "Mendatang"},
        ],
    },
    {
        "nama": "Ir. Sari Dewi, M.T.",
        "bidang": "Basis Data & Sistem Informasi Enterprise",
        "email": "sari.dewi@ftii.ac.id",
        "keywords": ["sari", "sari dewi", "dewi"],
        "jam_konsultasi": [
            {"hari": "Senin", "jam": "13.00–15.00", "ruang": "R.204", "status": "Tersedia"},
            {"hari": "Kamis", "jam": "09.00–11.00", "ruang": "R.204", "status": "Tersedia"},
        ],
        "bimbingan": [
            {"tanggal": "4 Jun 2026", "mahasiswa": "Muhammad Rizki", "nim": "2023003", "topik": "Desain ERD & normalisasi database", "status": "Selesai"},
            {"tanggal": "9 Jun 2026", "mahasiswa": "Dewi Lestari", "nim": "2023010", "topik": "Implementasi dan uji coba sistem", "status": "Selesai"},
            {"tanggal": "14 Jun 2026", "mahasiswa": "Muhammad Rizki", "nim": "2023003", "topik": "Pengujian fungsional sistem", "status": "Berlangsung"},
            {"tanggal": "23 Jun 2026", "mahasiswa": "Dewi Lestari", "nim": "2023010", "topik": "Revisi laporan akhir", "status": "Mendatang"},
        ],
    },
    {
        "nama": "Dr. Nadia Kirana",
        "bidang": "Rekayasa Perangkat Lunak & UI/UX",
        "email": "nadia.kirana@ftii.ac.id",
        "keywords": ["nadia", "nadia kirana", "kirana"],
        "jam_konsultasi": [
            {"hari": "Rabu", "jam": "10.00–12.00", "ruang": "R.305", "status": "Tersedia"},
            {"hari": "Jumat", "jam": "13.00–15.00", "ruang": "R.305", "status": "Tersedia"},
        ],
        "bimbingan": [
            {"tanggal": "1 Jun 2026", "mahasiswa": "Dinda Maharani", "nim": "2023004", "topik": "Prototipe aplikasi & user testing", "status": "Selesai"},
            {"tanggal": "6 Jun 2026", "mahasiswa": "Arif Hidayat", "nim": "2023009", "topik": "Review draft skripsi final", "status": "Selesai"},
            {"tanggal": "11 Jun 2026", "mahasiswa": "Intan Permata", "nim": "2023012", "topik": "Pengujian usability SUS score", "status": "Selesai"},
            {"tanggal": "16 Jun 2026", "mahasiswa": "Arif Hidayat", "nim": "2023009", "topik": "Revisi pra-sidang skripsi", "status": "Berlangsung"},
            {"tanggal": "24 Jun 2026", "mahasiswa": "Dinda Maharani", "nim": "2023004", "topik": "Seminar proposal lanjutan", "status": "Mendatang"},
            {"tanggal": "30 Jun 2026", "mahasiswa": "Intan Permata", "nim": "2023012", "topik": "Finalisasi & unggah skripsi", "status": "Mendatang"},
        ],
    },
    {
        "nama": "Prof. Agus Wijaya",
        "bidang": "Teknik Industri & Manajemen Operasional",
        "email": "agus.wijaya@ftii.ac.id",
        "keywords": ["agus", "agus wijaya", "wijaya"],
        "jam_konsultasi": [
            {"hari": "Selasa", "jam": "10.00–12.00", "ruang": "R.401", "status": "Tersedia"},
            {"hari": "Kamis", "jam": "14.00–16.00", "ruang": "R.401", "status": "Tersedia"},
        ],
        "bimbingan": [
            {"tanggal": "2 Jun 2026", "mahasiswa": "Budi Santoso", "nim": "2023005", "topik": "Analisis waktu & gerak produksi", "status": "Selesai"},
            {"tanggal": "7 Jun 2026", "mahasiswa": "Putri Ayuningtyas", "nim": "2023014", "topik": "Pemodelan sistem produksi", "status": "Selesai"},
            {"tanggal": "12 Jun 2026", "mahasiswa": "Salsa Billa", "nim": "2023020", "topik": "Peta kendali kualitas & SPC", "status": "Selesai"},
            {"tanggal": "17 Jun 2026", "mahasiswa": "Riska Amelia", "nim": "2023017", "topik": "Revisi dan finalisasi proposal", "status": "Berlangsung"},
            {"tanggal": "21 Jun 2026", "mahasiswa": "Budi Santoso", "nim": "2023005", "topik": "Persiapan sidang skripsi", "status": "Mendatang"},
            {"tanggal": "28 Jun 2026", "mahasiswa": "Putri Ayuningtyas", "nim": "2023014", "topik": "Seminar hasil penelitian", "status": "Mendatang"},
        ],
    },
    {
        "nama": "Drs. Hendra, M.Kom.",
        "bidang": "Jaringan Komputer & Keamanan Sistem",
        "email": "hendra@ftii.ac.id",
        "keywords": ["hendra"],
        "jam_konsultasi": [
            {"hari": "Rabu", "jam": "08.00–10.00", "ruang": "Lab B2", "status": "Tersedia"},
            {"hari": "Jumat", "jam": "10.00–12.00", "ruang": "Lab B2", "status": "Penuh"},
        ],
        "bimbingan": [
            {"tanggal": "3 Jun 2026", "mahasiswa": "Yoga Pratama", "nim": "2023011", "topik": "Desain topologi jaringan kampus", "status": "Selesai"},
            {"tanggal": "8 Jun 2026", "mahasiswa": "Aulia Rahman", "nim": "2023016", "topik": "Implementasi kebijakan firewall", "status": "Selesai"},
            {"tanggal": "13 Jun 2026", "mahasiswa": "Naufal Akbar", "nim": "2023019", "topik": "Konfigurasi VPN & tunneling", "status": "Berlangsung"},
            {"tanggal": "19 Jun 2026", "mahasiswa": "Yoga Pratama", "nim": "2023011", "topik": "Pengujian penetrasi jaringan", "status": "Mendatang"},
            {"tanggal": "26 Jun 2026", "mahasiswa": "Aulia Rahman", "nim": "2023016", "topik": "Finalisasi laporan keamanan sistem", "status": "Mendatang"},
        ],
    },
]

DATA_MAHASISWA = [
    {"nim": "2023001", "nama": "Ahmad Fauzan", "prodi": "Teknik Informatika", "semester": 6, "sks_lulus": 108, "ipk": 3.75, "presensi": 88, "status": "Aktif"},
    {"nim": "2023002", "nama": "Siti Nurhaliza", "prodi": "Sistem Informasi", "semester": 6, "sks_lulus": 102, "ipk": 3.60, "presensi": 91, "status": "Aktif"},
    {"nim": "2023003", "nama": "Muhammad Rizki", "prodi": "Teknik Informatika", "semester": 4, "sks_lulus": 72, "ipk": 3.20, "presensi": 80, "status": "Aktif"},
    {"nim": "2023004", "nama": "Dinda Maharani", "prodi": "Sistem Informasi", "semester": 4, "sks_lulus": 68, "ipk": 3.45, "presensi": 85, "status": "Aktif"},
    {"nim": "2023005", "nama": "Budi Santoso", "prodi": "Teknik Informatika", "semester": 8, "sks_lulus": 136, "ipk": 2.90, "presensi": 75, "status": "Aktif"},
    {"nim": "2023006", "nama": "Rina Oktavia", "prodi": "Teknik Industri", "semester": 6, "sks_lulus": 106, "ipk": 3.55, "presensi": 89, "status": "Aktif"},
    {"nim": "2023007", "nama": "Fajar Ramadhan", "prodi": "Teknik Informatika", "semester": 4, "sks_lulus": 70, "ipk": 3.30, "presensi": 82, "status": "Aktif"},
    {"nim": "2023008", "nama": "Nabila Putri", "prodi": "Sistem Informasi", "semester": 2, "sks_lulus": 36, "ipk": 3.80, "presensi": 95, "status": "Aktif"},
    {"nim": "2023009", "nama": "Arif Hidayat", "prodi": "Teknik Informatika", "semester": 8, "sks_lulus": 140, "ipk": 3.50, "presensi": 83, "status": "Aktif"},
    {"nim": "2023010", "nama": "Dewi Lestari", "prodi": "Teknik Industri", "semester": 6, "sks_lulus": 108, "ipk": 3.70, "presensi": 90, "status": "Aktif"},
    {"nim": "2023011", "nama": "Yoga Pratama", "prodi": "Teknik Informatika", "semester": 4, "sks_lulus": 66, "ipk": 2.85, "presensi": 77, "status": "Aktif"},
    {"nim": "2023012", "nama": "Intan Permata", "prodi": "Sistem Informasi", "semester": 6, "sks_lulus": 110, "ipk": 3.85, "presensi": 93, "status": "Aktif"},
    {"nim": "2023013", "nama": "Reza Saputra", "prodi": "Teknik Informatika", "semester": 8, "sks_lulus": 138, "ipk": 3.40, "presensi": 81, "status": "Aktif"},
    {"nim": "2023014", "nama": "Putri Ayuningtyas", "prodi": "Teknik Industri", "semester": 4, "sks_lulus": 72, "ipk": 3.65, "presensi": 88, "status": "Aktif"},
    {"nim": "2023015", "nama": "Bagas Maulana", "prodi": "Teknik Informatika", "semester": 2, "sks_lulus": 34, "ipk": 3.10, "presensi": 79, "status": "Aktif"},
    {"nim": "2023016", "nama": "Aulia Rahman", "prodi": "Sistem Informasi", "semester": 6, "sks_lulus": 112, "ipk": 3.90, "presensi": 97, "status": "Aktif"},
    {"nim": "2023017", "nama": "Riska Amelia", "prodi": "Teknik Industri", "semester": 4, "sks_lulus": 70, "ipk": 3.25, "presensi": 84, "status": "Aktif"},
    {"nim": "2023018", "nama": "Dimas Saputra", "prodi": "Teknik Informatika", "semester": 8, "sks_lulus": 132, "ipk": 2.80, "presensi": 75, "status": "Aktif"},
    {"nim": "2023019", "nama": "Naufal Akbar", "prodi": "Sistem Informasi", "semester": 2, "sks_lulus": 40, "ipk": 3.95, "presensi": 100, "status": "Aktif"},
    {"nim": "2023020", "nama": "Salsa Billa", "prodi": "Teknik Industri", "semester": 4, "sks_lulus": 68, "ipk": 3.55, "presensi": 86, "status": "Aktif"},
]


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def badge(label: str, tone: str | None = None) -> str:
    tone_map = {
        "Disetujui": "green",
        "Berlangsung": "green",
        "Terjadwal": "green",
        "Aktif": "green",
        "Menunggu": "yellow",
        "Menunggu berkas": "yellow",
        "Mendatang": "yellow",
        "Selesai": "blue",
        "Ditolak": "red",
    }
    badge_tone = tone or tone_map.get(label, "gray")
    return f'<span class="badge badge-{badge_tone}">{escape(label)}</span>'


def ipk_badge(ipk: float) -> str:
    if ipk >= 3.51:
        return badge(f"{ipk:.2f}", "green")
    if ipk >= 3.01:
        return badge(f"{ipk:.2f}", "blue")
    if ipk >= 2.76:
        return badge(f"{ipk:.2f}", "yellow")
    return badge(f"{ipk:.2f}", "red")


def ipk_indicator(ipk: float) -> tuple[str, str]:
    if ipk >= 3.75:
        return "Sangat Memuaskan", "green"
    if ipk >= 3.25:
        return "Baik", "blue"
    return "Perlu Peningkatan", "red"


def presensi_indicator(presensi: int) -> tuple[str, str]:
    if presensi >= 90:
        return "Kehadiran Sangat Baik", "green"
    if presensi >= 80:
        return "Kehadiran Baik", "yellow"
    return "Perlu Peningkatan Kehadiran", "red"


def predikat_ipk(ipk: float) -> str:
    if ipk >= 3.51:
        return "Dengan Pujian"
    if ipk >= 3.01:
        return "Sangat Memuaskan"
    if ipk >= 2.76:
        return "Memuaskan"
    return "Perlu Pendampingan"


def table_html(headers: list[str], rows: list[list]) -> str:  # type: ignore[type-arg]
    header_html = "".join(f"<th>{escape(header)}</th>" for header in headers)
    row_html = ""
    for row in rows:
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        row_html += f"<tr>{cells}</tr>"
    return f'<div class="table-wrap"><table class="info-table"><thead><tr>{header_html}</tr></thead><tbody>{row_html}</tbody></table></div>'


def chips(items: list[tuple[str, str]]) -> str:
    chip_html = "".join(
        f'<button class="chip" type="button" data-query="{escape(query)}">{escape(label)}</button>'
        for label, query in items
    )
    return f'<div class="chip-row">{chip_html}</div>'


def metric_cards(items: list[tuple[str, str, str]]) -> str:
    card_html = "".join(
        f'<div class="metric-card"><span>{escape(label)}</span><strong>{value}</strong><small>{escape(note)}</small></div>'
        for label, value, note in items
    )
    return f'<div class="metric-grid">{card_html}</div>'


def bullet_list(items: list[str], ordered: bool = False) -> str:
    tag = "ol" if ordered else "ul"
    entries = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f'<{tag} class="info-list">{entries}</{tag}>'


def answer_welcome() -> str:
    total_sks = sum(item["sks"] for item in KRS)
    rata_ipk = mean(student["ipk"] for student in DATA_MAHASISWA)
    return f"""
<strong>🎓 Selamat datang di ACADTECNO Smart Campus!</strong>
<p>ACADTECNO siap membantu mahasiswa mendapatkan informasi akademik, analisis mahasiswa, jadwal kuliah, KRS, skripsi, sidang, beasiswa, presensi, UKT, magang, dan kalender akademik.</p>
{metric_cards([
    ("Mahasiswa", str(len(DATA_MAHASISWA)), "data aktif"),
    ("Rata-rata IPK", f"{rata_ipk:.2f}", "angkatan 2023"),
    ("SKS KRS aktif", str(total_sks), "semester genap"),
    ("Status semester", "UAS", "8–20 Jun 2026"),
])}
<p class="hint">Coba ketik: <em>analisis 2023001</em>, <em>syarat skripsi</em>, atau <em>deadline beasiswa</em>.</p>
{chips(DEFAULT_SUGGESTIONS)}
"""


def answer_jadwal() -> str:
    rows = [
        [escape(item["hari"]), escape(item["jam"]), escape(item["matkul"]), escape(item["ruang"]), escape(item["dosen"]), badge(item["mode"], "gray")]
        for item in JADWAL_KULIAH
    ]
    return (
        f'<strong>📅 Jadwal Kuliah — {escape(CAMPUS_PROFILE["semester"])} {escape(CAMPUS_PROFILE["tahun_akademik"])}</strong>'
        + table_html(["Hari", "Jam", "Mata Kuliah", "Ruang", "Dosen", "Mode"], rows)
        + '<p class="hint">Catatan: keterlambatan lebih dari 15 menit masuk kategori terlambat pada rekap presensi.</p>'
        + chips([("Cek presensi", "presensi"), ("Kalender UAS", "kapan uas"), ("KRS aktif", "krs")])
    )


def answer_krs() -> str:
    total_sks = sum(item["sks"] for item in KRS)
    approved = sum(1 for item in KRS if item["status"] == "Disetujui")
    rows = [[escape(item["kode"]), escape(item["nama"]), item["sks"], badge(item["status"])] for item in KRS]
    return (
        "<strong>📋 KRS — Kartu Rencana Studi</strong>"
        + table_html(["Kode", "Mata Kuliah", "SKS", "Status"], rows)
        + metric_cards([
            ("Total SKS", str(total_sks), "maksimum demo 24 SKS"),
            ("Disetujui", str(approved), "mata kuliah"),
            ("Menunggu", str(len(KRS) - approved), "perlu validasi dosen wali"),
        ])
        + '<p class="hint">Saran: jika status masih menunggu, hubungi dosen wali sebelum masa perubahan KRS ditutup.</p>'
    )


def answer_kalender() -> str:
    rows = []
    for item in KALENDER_AKADEMIK:
        k_lower = item["kegiatan"].lower()
        status = item["status"]
        if status == "Berlangsung":
            if "uas" in k_lower:
                act_q, act_label = "uas", "📋 Info UAS"
            elif "sidang" in k_lower:
                act_q, act_label = "jadwal sidang", "🎓 Jadwal Sidang"
            else:
                act_q, act_label = "kalender akademik", "📅 Detail"
            status_cell = (
                f'<span class="badge badge-green badge-live">🟢 {escape(status)}</span>'
                f'<button class="chip" type="button" data-query="{escape(act_q)}"'
                f' style="min-height:24px;padding:3px 10px;font-size:11px;margin-left:6px">{act_label}</button>'
            )
        elif status == "Mendatang":
            if "nilai" in k_lower:
                act_q, act_label = "kapan nilai keluar", "📊 Kapan Nilai?"
            elif "perwalian" in k_lower or "krs" in k_lower:
                act_q, act_label = "krs", "📋 Info KRS"
            else:
                act_q, act_label = "kalender akademik", "ℹ️ Detail"
            status_cell = (
                f'{badge(status)}'
                f'<button class="chip" type="button" data-query="{escape(act_q)}"'
                f' style="min-height:24px;padding:3px 10px;font-size:11px;margin-left:6px">{act_label}</button>'
            )
        else:
            status_cell = badge(status)
        rows.append([escape(item["kegiatan"]), escape(item["mulai"]), escape(item["akhir"]), status_cell])
    return (
        "<strong>🗓 Kalender Akademik 2025/2026</strong>"
        + table_html(["Kegiatan", "Mulai", "Akhir", "Status"], rows)
        + chips([("Jadwal UAS", "uas"), ("Sidang Skripsi", "jadwal sidang"), ("Bimbingan Dosen", "bimbingan dosen"), ("Input Nilai", "kapan nilai keluar")])
    )


def answer_skripsi() -> str:
    return f"""
<strong>📝 Panduan Skripsi / Tugas Akhir</strong>
<div class="split-grid">
  <section>
    <h4>Syarat Pengajuan</h4>
    {bullet_list(SKRIPSI_INFO["syarat"])}
  </section>
  <section>
    <h4>Tahapan</h4>
    {bullet_list(SKRIPSI_INFO["tahapan"], ordered=True)}
  </section>
</div>
<h4>Tips agar lebih siap</h4>
{bullet_list(SKRIPSI_INFO["tips"])}
{chips([("Jadwal sidang", "jadwal sidang"), ("Analisis NIM", "analisis 2023001"), ("Kontak BAAK", "kontak admin")])}
"""


def answer_sidang() -> str:
    rows = [[escape(item["nama"]), escape(item["tanggal"]), escape(item["jam"]), escape(item["ruang"]), escape(item["penguji"]), badge(item["status"])] for item in JADWAL_SIDANG]
    return (
        "<strong>🎓 Jadwal Sidang Skripsi — Gelombang I</strong>"
        + table_html(["Nama", "Tanggal", "Jam", "Ruang", "Penguji", "Status"], rows)
        + '<p class="hint">Checklist sidang: kartu bimbingan, slide presentasi, draft final, bukti bebas administrasi, dan pakaian formal.</p>'
    )


def answer_beasiswa() -> str:
    rows = [[escape(item["nama"]), escape(item["syarat"]), escape(item["deadline"])] for item in BEASISWA]
    return (
        "<strong>🏆 Informasi Beasiswa Aktif</strong>"
        + table_html(["Nama Beasiswa", "Syarat", "Deadline"], rows)
        + '<p class="hint">Tips: siapkan transkrip sementara, CV, portofolio, surat rekomendasi, dan esai motivasi.</p>'
    )


def answer_layanan() -> str:
    rows = [[escape(item["layanan"]), escape(item["estimasi"]), escape(item["kanal"])] for item in LAYANAN]
    return (
        "<strong>🏢 Layanan Administrasi Akademik</strong>"
        + table_html(["Layanan", "Estimasi", "Kanal"], rows)
        + chips([("Kontak admin", "kontak admin"), ("UKT", "ukt"), ("Cuti akademik", "cuti akademik")])
    )


def answer_presensi() -> str:
    warning_count = sum(1 for student in DATA_MAHASISWA if student["presensi"] < 75)
    rows = [
        [escape(student["nim"]), escape(student["nama"]), escape(student["prodi"]), f'{student["presensi"]}%', badge("Aman", "green") if student["presensi"] >= 75 else badge("Perlu perhatian", "red")]
        for student in DATA_MAHASISWA
    ]
    return (
        "<strong>✅ Ringkasan Presensi Mahasiswa</strong>"
        + metric_cards([
            ("Batas minimum", "75%", "syarat ikut UAS"),
            ("Perlu perhatian", str(warning_count), "mahasiswa"),
            ("Rata-rata", f'{mean(student["presensi"] for student in DATA_MAHASISWA):.1f}%', "seluruh demo"),
        ])
        + table_html(["NIM", "Nama", "Prodi", "Presensi", "Status"], rows)
    )


def answer_ukt() -> str:
    return """
<strong>💳 Informasi UKT &amp; Administrasi Pembayaran</strong>
<ul class="info-list">
  <li>Tagihan UKT semester berikutnya dapat dicek di menu Keuangan SIAKAD.</li>
  <li>Batas pembayaran demo: 25 Juli 2026.</li>
  <li>Jika pembayaran belum tervalidasi setelah 1x24 jam, unggah bukti bayar melalui helpdesk.</li>
  <li>Keterlambatan pembayaran dapat menghambat pengisian KRS semester berikutnya.</li>
</ul>
"""


def answer_magang() -> str:
    return """
<strong>💼 Panduan Magang / MBKM</strong>
<ul class="info-list">
  <li>Syarat umum: minimal semester 5, IPK minimal 3.00, dan mendapat persetujuan dosen wali.</li>
  <li>Dokumen: CV, transkrip sementara, surat pengantar kampus, dan proposal aktivitas.</li>
  <li>Konversi SKS dilakukan setelah laporan akhir dan penilaian mitra diterima prodi.</li>
  <li>Rekomendasi: mulai cari mitra 6–8 minggu sebelum semester berjalan.</li>
</ul>
"""


def answer_wisuda() -> str:
    return """
<strong>🎉 Informasi Wisuda</strong>
<ul class="info-list">
  <li>Pra-syarat: lulus seluruh mata kuliah, revisi skripsi selesai, bebas pustaka, dan bebas administrasi.</li>
  <li>Pendaftaran wisuda demo dibuka 1–20 Agustus 2026 melalui SIAKAD.</li>
  <li>Dokumen utama: pas foto, KTP, ijazah terakhir, surat bebas pustaka, dan bukti unggah repository.</li>
</ul>
"""


def answer_contact() -> str:
    return f"""
<strong>☎️ Kontak Layanan Akademik</strong>
<div class="contact-grid">
  <article class="contact-card">
    <h4>BAAK</h4>
    <p>Gedung Rektorat Lt. 1<br>Senin–Jumat, 08.00–16.00<br>baak@ftii.ac.id<br>(021) 555-0100</p>
  </article>
  <article class="contact-card">
    <h4>Helpdesk SIAKAD</h4>
    <p>{escape(CAMPUS_PROFILE["helpdesk"])}<br>WA 0812-3456-7890<br>Respon normal: 1 hari kerja</p>
  </article>
</div>
"""


def answer_students() -> str:
    students = sorted(DATA_MAHASISWA, key=lambda item: item["ipk"], reverse=True)
    rows = [
        [escape(student["nim"]), escape(student["nama"]), escape(student["prodi"]), f'Sem {student["semester"]}', student["sks_lulus"], ipk_badge(student["ipk"]), f'{student["presensi"]}%', predikat_ipk(student["ipk"])]
        for student in students
    ]
    return (
        "<strong>📊 Data Nilai, IPK, dan Presensi Mahasiswa</strong>"
        + metric_cards([
            ("Rata-rata IPK", f'{mean(student["ipk"] for student in DATA_MAHASISWA):.2f}', "seluruh mahasiswa"),
            ("IPK tertinggi", f'{students[0]["ipk"]:.2f}', students[0]["nama"]),
            ("Cumlaude (≥3.51)", str(sum(1 for s in DATA_MAHASISWA if s["ipk"] >= 3.51)), "mahasiswa"),
        ])
        + table_html(["NIM", "Nama", "Prodi", "Semester", "SKS", "IPK", "Presensi", "Predikat"], rows)
        + chips([("Cumlaude", "mahasiswa cumlaude"), ("Analisis NIM", "analisis 2023001"), ("Presensi", "presensi")])
    )


def answer_cumlaude() -> str:
    students = sorted([s for s in DATA_MAHASISWA if s["ipk"] >= 3.51], key=lambda item: item["ipk"], reverse=True)
    rows = [[escape(s["nim"]), escape(s["nama"]), escape(s["prodi"]), f'Sem {s["semester"]}', ipk_badge(s["ipk"])] for s in students]
    return "<strong>🏅 Mahasiswa Berpredikat Cumlaude (IPK ≥ 3.51)</strong>" + table_html(["NIM", "Nama", "Prodi", "Semester", "IPK"], rows)


def find_students(keyword: str) -> list[dict]:
    normalized_keyword = keyword.lower().strip()
    return [
        student
        for student in DATA_MAHASISWA
        if normalized_keyword in student["nim"] or normalized_keyword in student["nama"].lower()
    ]


def readiness_notes(student: dict) -> list[str]:
    notes = []
    if student["ipk"] >= 3.50:
        notes.append("✓ Berpotensi mendapatkan beasiswa prestasi")
    if student["semester"] >= 5:
        notes.append("✓ Siap mengikuti program magang")
    if student["semester"] >= 7 and student["sks_lulus"] >= 120 and student["ipk"] >= 2.75:
        notes.append("✓ Direkomendasikan mengambil skripsi")
    if student["ipk"] >= 3.50:
        notes.append("✓ Pertahankan IPK di atas 3.50")
    if student["presensi"] < 80:
        notes.append("⚠ Tingkatkan kehadiran perkuliahan")
    if student["ipk"] < 3.00:
        notes.append("⚠ Prioritaskan peningkatan nilai pada mata kuliah dengan bobot SKS besar")
    if not notes:
        notes.append("✓ Fokus menjaga IPK dan presensi semester ini")
    return notes


def answer_student_analysis(keyword: str) -> str:
    results = find_students(keyword)
    if not results:
        return (
            f'<strong>🔎 Data mahasiswa tidak ditemukan.</strong><p>Keyword: <em>{escape(keyword)}</em></p>'
            + chips([("Lihat semua mahasiswa", "nilai ipk mahasiswa"), ("Contoh analisis", "analisis 2023001")])
        )

    student = results[0]
    ipk_label, ipk_tone = ipk_indicator(student["ipk"])
    pres_label, pres_tone = presensi_indicator(student["presensi"])

    tone_color = {"green": "#16a34a", "blue": "#1d4ed8", "yellow": "#d97706", "red": "#dc2626"}
    ipk_color = tone_color.get(ipk_tone, "#333")
    pres_color = tone_color.get(pres_tone, "#333")

    return f"""
<strong>🧭 Dashboard Analisis Mahasiswa — ACADTECNO</strong>
{metric_cards([
    ("Nama", escape(student["nama"]), student["nim"]),
    ("Program Studi", escape(student["prodi"]), f'Semester {student["semester"]}'),
    ("IPK", f'<span style="color:{ipk_color};font-size:22px">{student["ipk"]:.2f}</span>', ipk_label),
    ("SKS Lulus", str(student["sks_lulus"]), "dari 144 SKS total"),
])}
{metric_cards([
    ("Presensi", f'<span style="color:{pres_color};font-size:22px">{student["presensi"]}%</span>', pres_label),
    ("Status Akademik", badge(student["status"]), "Angkatan 2023"),
    ("Predikat Akademik", escape(predikat_ipk(student["ipk"])), "berdasarkan IPK"),
    ("Semester Aktif", f'Semester {student["semester"]}', "T.A. 2025/2026"),
])}
<h4>Rekomendasi Cerdas ACADTECNO</h4>
{bullet_list(readiness_notes(student))}
{chips([("Skripsi", "syarat skripsi"), ("Beasiswa", "beasiswa"), ("Presensi", "presensi")])}
"""


def answer_analisis_form() -> str:
    return f"""
<strong>🧭 Analisis Mahasiswa ACADTECNO</strong>
<p>Masukkan NIM mahasiswa yang ingin dianalisis atau gunakan tombol <strong>Analisis NIM</strong> di sidebar.</p>
{metric_cards([
    ("Total Mahasiswa", str(len(DATA_MAHASISWA)), "data aktif"),
    ("Angkatan", "2023", "semua program studi"),
    ("Program Studi", "3", "TI · SI · Teknik Industri"),
])}
<p class="hint">Contoh: ketik <em>analisis 2023001</em> untuk melihat dashboard Ahmad Fauzan.</p>
{chips([
    ("Analisis 2023001", "analisis 2023001"),
    ("Analisis 2023012", "analisis 2023012"),
    ("Analisis 2023019", "analisis 2023019"),
    ("Semua Mahasiswa", "nilai ipk mahasiswa"),
])}
"""


def answer_bimbingan_list() -> str:
    card_html = ""
    for d in DOSEN_BIMBINGAN:
        selesai = sum(1 for b in d["bimbingan"] if b["status"] == "Selesai")
        aktif = sum(1 for b in d["bimbingan"] if b["status"] in ("Berlangsung", "Mendatang"))
        kw = d["keywords"][0]
        card_html += (
            f'<div class="metric-card" data-query="bimbingan {escape(kw)}" style="cursor:pointer">'
            f'<span>👨‍🏫 {escape(d["nama"])}</span>'
            f'<strong style="font-size:13px">{escape(d["bidang"])}</strong>'
            f'<small>{selesai} selesai · {aktif} mendatang</small>'
            f'</div>'
        )
    chip_items = [(d["keywords"][0].capitalize(), f'bimbingan {d["keywords"][0]}') for d in DOSEN_BIMBINGAN]
    return (
        "<strong>🧑‍🏫 Jadwal Bimbingan Dosen — ACADTECNO</strong>"
        "<p>Klik kartu dosen di bawah untuk melihat jadwal konsultasi dan riwayat bimbingan lengkap.</p>"
        f'<div class="metric-grid">{card_html}</div>'
        + chips(chip_items)
    )


def answer_bimbingan_detail(keyword: str) -> str:
    kw_lower = keyword.lower().strip()
    dosen = None
    for d in DOSEN_BIMBINGAN:
        if any(kw in kw_lower for kw in d["keywords"]):
            dosen = d
            break
    if not dosen:
        return (
            f'<strong>🔎 Dosen tidak ditemukan.</strong>'
            f'<p>Keyword: <em>{escape(keyword)}</em></p>'
            + chips([("← Semua Dosen", "bimbingan dosen")])
        )
    konsultasi_rows = [
        [escape(j["hari"]), escape(j["jam"]), escape(j["ruang"]), badge(j["status"], "green" if j["status"] == "Tersedia" else "red")]
        for j in dosen["jam_konsultasi"]
    ]
    bimbingan_rows = []
    for b in dosen["bimbingan"]:
        if b["status"] == "Berlangsung":
            s_cell = (
                badge(b["status"])
                + f' <button class="chip" type="button" data-query="analisis {escape(b["nim"])}"'
                f' style="min-height:24px;padding:3px 9px;font-size:11px;margin-left:4px">🔍 Profil</button>'
            )
        else:
            s_cell = badge(b["status"])
        bimbingan_rows.append([
            escape(b["tanggal"]),
            f'{escape(b["mahasiswa"])} <span style="font-size:11px;opacity:.55">({escape(b["nim"])})</span>',
            escape(b["topik"]),
            s_cell,
        ])
    total = len(dosen["bimbingan"])
    selesai = sum(1 for b in dosen["bimbingan"] if b["status"] == "Selesai")
    aktif = sum(1 for b in dosen["bimbingan"] if b["status"] in ("Berlangsung", "Mendatang"))
    bidang_html = f'<span style="font-size:12px;font-weight:600;color:inherit;line-height:1.4;display:block">{escape(dosen["bidang"])}</span>'
    email_html  = f'<span style="font-size:11px;opacity:.65">{escape(dosen["email"])}</span>'
    return (
        f'<strong>🧑‍🏫 Bimbingan — {escape(dosen["nama"])}</strong>'
        + metric_cards([
            ("Bidang Keahlian", bidang_html, ""),
            ("Total Bimbingan", str(total), "bulan ini"),
            ("Selesai", str(selesai), "sesi"),
            ("Aktif / Mendatang", str(aktif), "sesi"),
        ])
        + '<h4 style="margin:14px 0 6px;font-size:13px;color:#3730a3">📅 Jadwal Konsultasi Rutin</h4>'
        + table_html(["Hari", "Jam", "Ruang", "Ketersediaan"], konsultasi_rows)
        + '<h4 style="margin:14px 0 6px;font-size:13px;color:#3730a3">📋 Riwayat Bimbingan — Juni 2026</h4>'
        + table_html(["Tanggal", "Mahasiswa", "Topik Bimbingan", "Status"], bimbingan_rows)
        + chips([("← Semua Dosen", "bimbingan dosen"), ("Analisis NIM", "analisis nim")])
    )


def answer_unknown(message: str) -> str:
    escaped_message = escape(message)
    return f"""
<strong>🤔 ACADTECNO belum menangkap maksudnya.</strong>
<p>Pertanyaan kamu: <em>{escaped_message}</em></p>
<p class="hint">Coba gunakan kata kunci seperti jadwal, KRS, skripsi, UKT, presensi, beasiswa, magang, atau analisis NIM.</p>
{chips(DEFAULT_SUGGESTIONS)}
"""


def normalize(message: str) -> str:
    lowered = message.lower().strip()
    return re.sub(r"\s+", " ", lowered)


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, left, right).ratio()


def intent_score(message: str, patterns: Any, keywords: Any) -> int:
    score = 0
    for pattern in patterns:
        if re.search(pattern, message):
            score += 8
    for keyword in keywords:
        if keyword in message:
            score += 3
        elif any(similarity(keyword, token) > 0.84 for token in message.split()):
            score += 1
    return score


DEFAULT_SUGGESTIONS = [
    ("Jadwal", "jadwal kuliah"),
    ("KRS", "krs"),
    ("Skripsi", "syarat skripsi"),
    ("Kalender", "kalender akademik"),
    ("Beasiswa", "beasiswa"),
    ("Analisis NIM", "analisis nim"),
]

INTENTS: list[dict[str, object]] = [
    {"name": "jadwal", "patterns": [r"jadwal.*(kuliah|kelas|matkul)|kuliah.*jadwal|hari (senin|selasa|rabu|kamis|jumat)"], "keywords": ["jadwal", "kuliah", "kelas", "matkul"], "handler": answer_jadwal},
    {"name": "krs", "patterns": [r"\bkrs\b|kartu rencana|ambil.*matkul|sks"], "keywords": ["krs", "sks", "matakuliah", "matkul"], "handler": answer_krs},
    {"name": "skripsi", "patterns": [r"skripsi|tugas akhir|\bta\b|proposal|dosen pembimbing|seminar"], "keywords": ["skripsi", "proposal", "pembimbing", "seminar"], "handler": answer_skripsi},
    {"name": "sidang", "patterns": [r"sidang|penguji|jadwal.*skripsi"], "keywords": ["sidang", "penguji"], "handler": answer_sidang},
    {"name": "kalender", "patterns": [r"kalender|uas|uts|ujian|nilai keluar|semester"], "keywords": ["kalender", "uas", "uts", "ujian", "semester"], "handler": answer_kalender},
    {"name": "beasiswa", "patterns": [r"beasiswa|kip|bantuan kuliah|prestasi"], "keywords": ["beasiswa", "kip", "prestasi"], "handler": answer_beasiswa},
    {"name": "layanan", "patterns": [r"layanan|surat aktif|legalisir|cuti|administrasi"], "keywords": ["layanan", "legalisir", "cuti", "administrasi"], "handler": answer_layanan},
    {"name": "presensi", "patterns": [r"presensi|absen|kehadiran"], "keywords": ["presensi", "absen", "kehadiran"], "handler": answer_presensi},
    {"name": "ukt", "patterns": [r"\bukt\b|bayar|pembayaran|tagihan|keuangan"], "keywords": ["ukt", "tagihan", "bayar"], "handler": answer_ukt},
    {"name": "magang", "patterns": [r"magang|mbkm|kampus merdeka|praktik kerja"], "keywords": ["magang", "mbkm"], "handler": answer_magang},
    {"name": "wisuda", "patterns": [r"wisuda|yudisium|ijazah|bebas pustaka"], "keywords": ["wisuda", "yudisium", "ijazah"], "handler": answer_wisuda},
    {"name": "kontak", "patterns": [r"kontak|admin|baak|helpdesk|hubungi"], "keywords": ["kontak", "admin", "baak", "helpdesk"], "handler": answer_contact},
    {"name": "nilai", "patterns": [r"nilai|ipk|transkrip|cumlaude|mahasiswa"], "keywords": ["nilai", "ipk", "transkrip", "mahasiswa"], "handler": answer_students},
    {"name": "bimbingan", "patterns": [r"bimbingan|konsultasi dosen|jadwal dosen"], "keywords": ["bimbingan", "konsultasi"], "handler": answer_bimbingan_list},
]


def process_message(message: str) -> tuple[str, str]:
    normalized_message = normalize(message)

    if re.search(r"^(halo|hai|hi|hello|selamat|pagi|siang|sore|malam|start|mulai)$", normalized_message):
        return answer_welcome(), "welcome"

    # "analisis nim" or "analisis mahasiswa" without a specific NIM number
    if re.search(r"^analisis\s+(nim|mahasiswa)$", normalized_message):
        return answer_analisis_form(), "analisis_nim_form"

    analysis_match = re.search(r"(analisis|cek|cari|profil|nim)\s+(?:mahasiswa\s+)?([a-z\s]*\d{4,}|[a-zA-Z\s]{4,})", normalized_message)
    if analysis_match:
        return answer_student_analysis(analysis_match.group(2).strip()), "student_analysis"

    if re.search(r"cumlaude|cum laude|ipk terbaik|peringkat|ranking", normalized_message):
        return answer_cumlaude(), "cumlaude"

    bimbingan_match = re.search(
        r"bimbingan(?:\s+dosen)?\s*(.+)?|jadwal\s+(?:konsultasi|bimbingan)\s*(.+)?|konsultasi\s+dosen",
        normalized_message,
    )
    if bimbingan_match:
        extra = ((bimbingan_match.group(1) or "") + (bimbingan_match.group(2) or "")).strip()
        if not extra or extra in ("dosen", "semua", "list"):
            return answer_bimbingan_list(), "bimbingan_list"
        return answer_bimbingan_detail(extra), "bimbingan_detail"

    scored_intents = []
    for intent in INTENTS:
        score = intent_score(normalized_message, intent["patterns"], intent["keywords"])
        if score > 0:
            scored_intents.append((score, intent))

    if scored_intents:
        selected_intent = sorted(scored_intents, key=lambda item: item[0], reverse=True)[0][1]
        handler = selected_intent["handler"]
        return handler(), str(selected_intent["name"])

    return answer_unknown(message), "unknown"


@app.route("/")
def index():
    return render_template("index.html", campus=CAMPUS_PROFILE)


def build_chat_response(message: str, *, include_legacy_reply: bool = False):
    if not message:
        payload = {
            "answer": "Silakan ketik pertanyaan kamu terlebih dahulu.",
            "intent": "empty",
        }
        if include_legacy_reply:
            payload["reply"] = payload["answer"]
        return jsonify(payload), 400

    answer, intent = process_message(message)
    payload = {
        "answer": answer,
        "intent": intent,
        "suggestions": DEFAULT_SUGGESTIONS,
    }
    if include_legacy_reply:
        payload["reply"] = answer
    return jsonify(payload)


@app.route("/api/chat", methods=["POST", "OPTIONS"])
def api_chat():
    if request.method == "OPTIONS":
        return ("", 204)

    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    return build_chat_response(message)


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    return build_chat_response(message, include_legacy_reply=True)


@app.route("/api/mahasiswa")
def api_mahasiswa():
    return jsonify({
        "mahasiswa": [
            {"nim": s["nim"], "nama": s["nama"], "prodi": s["prodi"]}
            for s in DATA_MAHASISWA
        ]
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "acadtecno-smart-campus"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
