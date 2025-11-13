# RPA-Driven Market Intelligence Dashboard (E-T-L Project)

## Overview Bisnis

Proyek ini adalah solusi **Robotic Process Automation (RPA)** yang berfokus pada **Web Scraping** dinamis. Skrip ini menggunakan Python, Selenium, dan BeautifulSoup untuk secara otomatis mengambil data dari website berita CNBN Indonesia dan menyimpannya sebagai laporan Excel.

Adapun target bisnis dari RPA Generated ini diantaranya adalah sebagai berikut.
1. Penghematan Waktu (Efisiensi & Skalabilitas)
   
Penghematan waktu paling jelas diukur dengan membandingkan pekerjaan manual (Before RPA) dengan pekerjaan otomatis (After RPA). Berdasarkan waktunya, Proyek ini memberikan efisiensi waktu sebesar minimal 90% untuk proses pengumpulan dan penyusunan laporan data tren. Waktu yang dihemat ini dapat dialokasikan untuk pekerjaan yang bernilai lebih tinggi.

3. Pengurangan Biaya (Kualitas & Fokus SDM)
   
Meskipun perusahaan tidak langsung memecat karyawan, RPA secara efektif mengurangi "biaya" operasional dan meningkatkan output per karyawan.

5. Nilai Tambah Melalui Otomatisasi End-to-End
   
Aspek E-T-L yang Anda terapkan memberikan nilai yang tidak bisa diberikan oleh manusia secara konsisten. Adapun hal itu adalah terkait transformasi cepat pada data yaitu untuk langsung dikategorikan (Transform) oleh Pandas saat itu juga, memberikan wawasan real-time tentang tren (misalnya, mendeteksi puncak berita AI dalam 1 jam terakhir). Selain itu juga, terkait distribusi otomatis bahwa laporan dapat langsung didistribusikan ke penerima yang tepat (Load) tanpa campur tangan manusia.

## Detail Teknis

### 1. Install Python dan chromedriver.exe sesuai dengan versi

### 2. Instalasi Python Libraries

Semua dependensi Python yang dibutuhkan terdaftar dalam `requirements.txt`. Buka Terminal/Command Prompt, arahkan ke direktori proyek ini (`cd /path/ke/folder/proyek`), lalu jalankan:

```
pip install -r requirements.txt
```
### 3. Ubah skrip rpa_dataproject.py terkait email untuk disesuaikan dengan yang dimiliki. Gunakan Application Password (Sandi Aplikasi) dari akun Google Anda

### 4. Menjalankan Skrip Pengujian
Jika ingin menjalankan skrip pengujian atau skrip kedua:
```
python rpa_test.py
````
### 5. Menjalankan Skrip Utama
Jalankan skrip utama yang akan memulai proses scraping:
```
python rpa_dataproject.py
```
Catatan: Skrip ini akan otomatis membuka jendela browser Chrome baru (dikontrol oleh Selenium), melakukan proses scraping, dan menutupnya setelah selesai. Harap jangan ganggu jendela browser saat proses berjalan.

### 6. Setelah skrip rpa_dataproject.py selesai dieksekusi, data yang diambil akan disimpan sebagai file laporan di direktori proyek ini:
Nama File: Laporan_Berita_Teknologi.xlsx

## Dashboard Data
<img width="1653" height="993" alt="Kategori Fokus Pie Chart" src="https://github.com/user-attachments/assets/f3edcc8d-c39b-4162-97fc-97f3d4c71b86" />

## Manual User
