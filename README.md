# 🛒 Proyek Analisis Data: E-Commerce Public Dataset

![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.2-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2.1-150458?logo=pandas&logoColor=white)
![Dicoding](https://img.shields.io/badge/Dicoding-Submission-2d3e50)

## 📌 Deskripsi Proyek
Proyek ini merupakan *submission* tugas akhir dari kelas **Belajar Analisis Data dengan Python** di Dicoding. Proyek ini berfokus pada analisis mendalam dari *E-Commerce Public Dataset* (Olist Brazil) untuk menggali *insight* bisnis dan ditutup dengan pembuatan *dashboard* interaktif menggunakan Streamlit.

## ❓ Pertanyaan Bisnis
1. Kategori produk apa yang paling laris (terbaik) dan paling sedikit terjual (terburuk)?
2. Bagaimana tren pendapatan penjualan bulanan sepanjang tahun 2017?

## 📂 Struktur Direktori
```text
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── Data/
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   └── ... (file dataset lainnya)
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## 🚀 Cara Menjalankan Project (Lokal)

### 1. Setup Environment
Sangat disarankan menggunakan *virtual environment* untuk menghindari konflik *library*.

**Menggunakan Conda:**
```bash
conda create --name main-ds python=3.10
conda activate main-ds
pip install -r requirements.txt
```

**Menggunakan venv (Windows):**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Streamlit App
Setelah semua library terinstall, jalankan perintah berikut untuk membuka *dashboard*:
```bash
cd dashboard
streamlit run dashboard.py
```
Aplikasi akan secara otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

## 🌐 Live Dashboard
Dashboard ini juga telah di-deploy ke **Streamlit Community Cloud**. Anda dapat mengaksesnya secara langsung melalui tautan berikut:
https://s2squaq9blx48xpxssjr7r.streamlit.app/
---
**Dibuat oleh:** Vito Gunawan 
