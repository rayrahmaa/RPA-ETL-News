import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re 

# --- Konfigurasi Awal ---
CHROME_DRIVER_PATH = 'chromedriver.exe' 
TARGET_URL = "https://www.cnbcindonesia.com/tech" 

# --- Setup Driver (dengan opsi anti-deteksi) ---
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
    time.sleep(5) 

    # 2. [Scraping] Mengambil kode HTML halaman yang sudah dimuat
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # 3. [Ekstraksi Data] Mencari elemen berita
    articles = soup.find_all('article', class_='list-content') 
    
    print(f"2. [Scraping] Ditemukan {len(articles)} potensi artikel.")

    for article in articles:
        try:
            # Cari link dan judul di dalam elemen 'a'
            link_tag = article.find('a', class_='listmedia') 
            title = link_tag['title'] if link_tag and 'title' in link_tag.attrs else 'N/A'
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else 'N/A'
            
            # Cari waktu/tanggal publikasi
            date_tag = article.find('span', class_='date')
            date_text = date_tag.get_text(strip=True) if date_tag else time.strftime("%Y-%m-%d") 
            
            if title != 'N/A' and link != 'N/A':
                data_berita.append({
                    'Judul': title,
                    'URL': link,
                    'Tanggal_Publikasi_Mentah': date_text,
                    'Tanggal_Ekstraksi': time.strftime("%Y-%m-%d")
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
    df['Tanggal_Bersih'] = df['Tanggal_Publikasi_Mentah'].apply(lambda x: re.sub(r'[\d]{1,2} [A-Za-z]+, ', '', x).strip())
    
    # 5.2 Contoh Analisis: Menambahkan kolom kategori
    df['Kategori_Fokus'] = df['Judul'].apply(
        lambda x: 'AI & ML' if any(keyword in x for keyword in ['AI', 'ChatGPT', 'Machine Learning']) else (
                  'Laptop' if 'Laptop' in x else 'Umum Teknologi')
    )
    
    # --- Menyimpan Laporan ---
    file_output = 'Laporan_Berita_Teknologi.xlsx'
    df.to_excel(file_output, index=False)
    
    print(f"Sukses! Data dibersihkan dan disimpan ke: {file_output}")
    print("\n--- Ringkasan Laporan ---")
    print(df['Kategori_Fokus'].value_counts())
    print("-" * 25)
    print(df.head()) 
else:
    print("Data kosong, tidak ada laporan yang dihasilkan.")