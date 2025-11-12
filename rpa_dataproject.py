import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import datetime
import yagmail

# --- Konfigurasi Awal ---
CHROME_DRIVER_PATH = 'chromedriver.exe' 
TARGET_URL = "https://www.cnbcindonesia.com/tech" 

# --- Setup Driver ---
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options) 

# --- List untuk menyimpan data ---
data_berita = []

print(f"1. [RPA] Membuka URL Target: {TARGET_URL}")

try:
    driver.get(TARGET_URL)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4) 

    # 2. [Scraping] Mengambil kode HTML
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    print("2. [Scraping] Memulai Ekstraksi Judul dan Link...")
    
    # MENGGUNAKAN CSS SELECTOR: Mencari semua tag <h2> yang berada di dalam <a>.group di dalam <article>
    # Berdasarkan inspeksi : artikel -> link (class group) -> h2 (judul)
    judul_tags = soup.select('article a.group h2')

    print(f"2. [Scraping] Ditemukan {len(judul_tags)} Judul potensial.")
    
    for h2_tag in judul_tags:
        try:
            title = h2_tag.get_text(strip=True)
            
            # Cari tag <a> terdekat (induk) dari h2 untuk mendapatkan link
            link_tag = h2_tag.find_parent('a') 
            link = link_tag.get('href').strip() if link_tag and link_tag.get('href') else 'N/A'
            # Cari tanggal publikasi di dalam artikel terkait
            article_tag = h2_tag.find_parent('article')
            date_span = article_tag.find('span', class_='date') if article_tag else None
            date_text = date_span.get_text(strip=True) if date_span else 'N/A'
            
            # Filter dan Simpan Data
            if title != 'N/A' and link != 'N/A' and 'cnbcindonesia.com' in link:
                data_berita.append({
                    'Judul': title,
                    'URL': link,
                    'Tanggal_Publikasi_Mentah': date_text, 
                    'Tanggal_Ekstraksi': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        except Exception:
            continue
            
    print(f"3. [Ekstraksi] Berhasil mengambil {len(data_berita)} data berita.")
    
except Exception as e:
    print(f"Terjadi Error saat Akuisisi Data: {e}")

finally:
    # 4. [RPA] Tutup Browser setelah selesai
    driver.quit()

# 5. [Data Processing] Menggunakan Pandas untuk membersihkan dan membuat laporan
if data_berita:
    print("\n4. [Pandas] Memulai Pemrosesan Data...")
    
    df = pd.DataFrame(data_berita)
    
    # --- Data Wrangling dan Pembersihan ---
    
    # 5.1 Contoh Pembersihan Tanggal:
    df['Waktu_Kategori'] = df['Tanggal_Publikasi_Mentah'].apply(
        lambda x: 'Hari Ini' if 'jam' in x or 'menit' in x else ('Bulan Ini' if 'bulan' in x else 'Lama')
    )
    
    # 5.2 Contoh Analisis: Menambahkan kolom kategori
    df['Kategori_Fokus'] = df['Judul'].apply(
        lambda x: 'AI & ML' if any(keyword in x.upper() for keyword in ['AI', 'CHATGPT', 'MACHINE LEARNING']) else (
                  'Fintech/Kripto' if any(keyword in x.upper() for keyword in ['KRIPTO', 'FINTECH', 'BANK DIGITAL']) else 'Teknologi Umum')
    )
    
    # --- Menyimpan Laporan ---
    file_output = 'Laporan_Berita_Teknologi.xlsx'
    df.to_excel(file_output, index=False)
    
    print(f"\nSukses! Data dibersihkan dan disimpan ke: {file_output}")

    try:
            SENDER_EMAIL = 'akungmail@gmail.com'
            APP_PASSWORD = 'gantipassword' 
            RECEIVER_EMAIL = 'akungmail@gmail.com' 

            yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
            
            yag.send(
                to=RECEIVER_EMAIL,
                subject=f"Laporan Otomatis: Tren Berita Teknologi {datetime.date.today()}",
                contents="Laporan (RPA-Generated) telah dilampirkan.",
                attachments=file_output
            )
            print(f"Laporan Excel berhasil dikirim ke {RECEIVER_EMAIL}!")

    except Exception as e:
        print(f"Gagal mengirim email otomatis. Pastikan 'yagmail' terinstal dan 'App Password' Gmail sudah benar.")

    print("\n--- Ringkasan Analisis ---")
    print(f"Total Artikel Diambil: {len(df)}")
    print("Distribusi Kategori:")
    print(df['Kategori_Fokus'].value_counts())
    print("-" * 25)
    print(df[['Judul', 'URL', 'Tanggal_Publikasi_Mentah', 'Kategori_Fokus']].head())    
else:

    print("Data kosong, tidak ada laporan yang dihasilkan.")
