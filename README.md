# 🤖 Product Review Analyzer

Aplikasi web untuk menganalisis sentiment review produk menggunakan AI (Google Gemini & TextBlob). Aplikasi ini dapat mengklasifikasikan review menjadi **Positive**, **Neutral**, atau **Negative**, serta mengekstrak key points dari review tersebut.

## 👨‍💻 Identitas Mahasiswa

| Nama | NIM |
|------|-----|
| Ahmad Ali Mukti | 123140155 |

## 📸 Screenshot Aplikasi

![Product Review Analyzer Screenshot](ui.png)

*Tampilan utama aplikasi dengan fitur sentiment analysis dan filter*

## 🚀 Cara Instalasi

### Prerequisites
Pastikan Anda sudah menginstall:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **PostgreSQL** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/downloads))

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Kyura01/123140155_Ahmad-Ali-Mukti_Pemweb-Tugas-3.git
cd 123140155_Ahmad-Ali-Mukti_Pemweb-Tugas-3
```

### 2️⃣ Setup Backend

```bash
# Masuk ke folder backend
cd backend

# Install dependencies Python
pip install sqlalchemy pyramid waitress google-generativeai requests python-dotenv transaction zope.sqlalchemy psycopg2-binary textblob

# Buat file .env dan isi dengan API keys Anda
# File .env:
HF_TOKEN=your_huggingface_token_here
GEMINI_KEY=your_google_gemini_api_key_here
DB_URL=postgresql://postgres:your_password@localhost:5432/product_reviews_db

# Jalankan backend server
python app.py
```

Backend akan berjalan di: **http://localhost:6543**

### 3️⃣ Setup Database PostgreSQL

```bash
# Login ke PostgreSQL
psql -U postgres

# Buat database baru
CREATE DATABASE product_reviews_db;

# Keluar dari psql
\q
```

Database akan otomatis membuat tabel saat backend pertama kali dijalankan.

### 4️⃣ Setup Frontend

```bash
# Buka terminal baru, masuk ke folder frontend
cd frontend

# Install dependencies Node.js
npm install

# Jalankan development server
npm run dev
```

Frontend akan berjalan di: **http://localhost:5173** atau **http://localhost:5174**

### 5️⃣ Akses Aplikasi

Buka browser dan akses: **http://localhost:5173** (atau port yang ditampilkan di terminal)

## 🔑 Mendapatkan API Keys

### Google Gemini API Key
1. Kunjungi: [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Login dengan akun Google
3. Klik "Create API Key"
4. Copy API key dan masukkan ke file `.env`

### Hugging Face Token (Opsional - untuk fitur tambahan)
1. Kunjungi: [Hugging Face](https://huggingface.co/settings/tokens)
2. Login atau daftar akun
3. Klik "New Token"
4. Copy token dan masukkan ke file `.env`

## 📦 Dependencies

### Backend
- **Python 3.8+**
- `pyramid` - Web framework
- `sqlalchemy` - ORM database
- `waitress` - WSGI server
- `google-generativeai` - Google Gemini API
- `textblob` - Sentiment analysis
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variables
- `transaction` - Transaction management
- `zope.sqlalchemy` - SQLAlchemy integration

### Frontend
- **React 18+**
- **Vite** - Build tool
- **Axios** - HTTP client

## 🎯 Fitur Aplikasi

✅ **Sentiment Analysis** - Klasifikasi review menjadi Positive, Neutral, atau Negative  
✅ **Key Points Extraction** - Ekstrak poin penting dari review menggunakan Google Gemini  
✅ **Filter Review** - Filter review berdasarkan sentiment  
✅ **Real-time Analysis** - Analisis langsung saat submit review  
✅ **Persistent Storage** - Menyimpan hasil analisis ke database PostgreSQL

## 📱 Cara Penggunaan

1. **Input Review**: Masukkan review produk dalam bahasa Inggris di text area
2. **Analyze**: Klik tombol "Analyze Review"
3. **Lihat Hasil**: Review akan dianalisis dan ditampilkan dengan:
   - Badge sentiment (Positive/Neutral/Negative)
   - Key points dari Gemini AI
   - Tanggal analisis
4. **Filter**: Gunakan tombol filter untuk melihat review berdasarkan sentiment tertentu

## 🛠️ Troubleshooting

### Backend tidak bisa start
- Pastikan PostgreSQL sudah running
- Cek koneksi database di file `.env`
- Pastikan semua dependencies terinstall

### Frontend tidak bisa connect ke backend
- Pastikan backend sudah running di port 6543
- Cek CORS settings di `backend/app.py`

### Error API Keys
- Pastikan file `.env` ada di folder `backend`
- Pastikan API keys valid dan tidak expired

## 📄 Lisensi

Tugas 3 - Pemrograman Web
