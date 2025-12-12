# backend/app.py
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.events import NewResponse
from sqlalchemy import engine_from_config
from waitress import serve
import transaction
import requests
import google.generativeai as genai
import os
import time 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import DBSession, Base, Review

# ==========================================
# KONFIGURASI API KEY (DARI .ENV)
# ==========================================
HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

if not HF_TOKEN or not GEMINI_KEY:
    print("WARNING: API Keys tidak ditemukan di .env!")

# Setup Database
DB_URL = os.getenv("DB_URL", 'postgresql://postgres:123@localhost:5432/product_reviews_db')

# Setup Gemini
try:
    genai.configure(api_key=GEMINI_KEY)
except Exception as e:
    print(f"Warning Config Gemini: {e}")

# ==========================================
# LOGIKA SENTIMENT ANALYSIS - USING TEXTBLOB (RELIABLE & LOCAL)
# ==========================================
from textblob import TextBlob

def analyze_sentiment_hf(text):
    """
    Analyze sentiment menggunakan TextBlob
    TextBlob mengembalikan polarity score dari -1 (negative) sampai +1 (positive)
    """
    print(f"--- Analyzing sentiment: {text[:50]}... ---", flush=True)
    
    try:
        # Analisis dengan TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to +1
        
        print(f"📊 Polarity score: {polarity:.3f}", flush=True)
        
        # Mapping polarity ke sentiment
        if polarity > 0.1:
            sentiment = "POSITIVE"
        elif polarity < -0.1:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"
        
        print(f"✅ Final sentiment: {sentiment}", flush=True)
        return sentiment
        
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        return "NEUTRAL"
# ==========================================
# LOGIKA GEMINI (KEY POINTS)
# ==========================================
def extract_keypoints_gemini(text):
    print("Mengirim ke Gemini (Model: gemini-2.5-flash)...")
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"Extract 3 pros/cons bullet points from this review (short): {text}"
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        return "No response text."
    except Exception as e:
        print(f"Error Gemini: {e}")
        return "Gagal extract poin."

# --- FUNGSI CORS ---
def add_cors_headers(event):
    event.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Max-Age': '3600',
    })

# --- API ENDPOINTS ---

@view_config(route_name='analyze_review', renderer='json', request_method='POST')
def analyze_review_view(request):
    try:
        data = request.json_body
        text = data.get('text')
        
        print(f"\n🔔 NEW REQUEST - Analyzing: {text[:50]}...")
        
        if not text:
            request.response.status = 400
            return {'error': 'Text is empty'}

        sentiment = analyze_sentiment_hf(text)
        print(f"✅ Sentiment result: {sentiment}")
        
        keypoints = extract_keypoints_gemini(text)
        print(f"✅ Keypoints extracted")

        new_review = Review(product_text=text, sentiment=sentiment, key_points=keypoints)
        DBSession.add(new_review)
        DBSession.flush()
        result = new_review.to_json()
        transaction.commit()

        return result

    except Exception as e:
        print(f"SERVER ERROR: {e}")
        request.response.status = 500
        return {'error': str(e)}

@view_config(route_name='get_reviews', renderer='json', request_method='GET')
def get_reviews_view(request):
    reviews = DBSession.query(Review).order_by(Review.created_at.desc()).all()
    return [r.to_json() for r in reviews]

@view_config(route_name='cors_options', request_method='OPTIONS')
@view_config(route_name='analyze_review', request_method='OPTIONS')
@view_config(route_name='get_reviews', request_method='OPTIONS')
def cors_options_view(request):
    return request.response

# --- MAIN ---
def main():
    settings = {'sqlalchemy.url': DB_URL}
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with Configurator(settings=settings) as config:
        config.add_subscriber(add_cors_headers, NewResponse)
        config.add_route('analyze_review', '/api/analyze-review')
        config.add_route('get_reviews', '/api/reviews')
        config.add_route('cors_options', '/api/{anything:.*}')
        config.scan()
        app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    import sys
    app = main()
    print("BACKEND BERJALAN. Akses: http://localhost:6543", flush=True)
    sys.stdout.flush()
    serve(app, host='0.0.0.0', port=6543)