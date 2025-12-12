import google.generativeai as genai

# --- TEMPEL API KEY KAMU DI SINI ---
API_KEY = "AIzaSyB_b4EF9beuC3nokCmST9UjaZDwT22OVaM" 
# -----------------------------------

genai.configure(api_key=API_KEY)

print("Sedang mengecek ke Google...")
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- Ditemukan: {m.name}")
            available_models.append(m.name)
    
    if not available_models:
        print("\nGAWAT! Tidak ada model yang tersedia untuk API Key ini.")
    else:
        print("\n PILIH SALAH SATU MODEL DI ATAS UNTUK app.py")
        
except Exception as e:
    print(f"\nERROR KONEKSI: {e}")