import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def test_sentiment(text):
    print(f"\n🧪 Testing: {text[:50]}...")
    
    api_url = "https://router.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    response = requests.post(api_url, headers=headers, json={"inputs": text})
    result = response.json()
    
    print(f"📥 Raw Response: {result}")
    
    if isinstance(result, list) and len(result) > 0:
        data = result[0]
        if isinstance(data, list):
            for item in data:
                print(f"   - {item['label']}: {item['score']:.4f}")
            top = max(data, key=lambda x: x['score'])
            print(f"✅ Winner: {top['label']} ({top['score']:.4f})")

# Test dengan berbagai sentimen
print("="*60)
test_sentiment("This is the worst item I have ever bought. It stopped working after just two days and the customer service is terrible. Do not buy this")
print("="*60)
test_sentiment("This product is absolutely amazing! I love it so much, highly recommend to everyone!")
print("="*60)
test_sentiment("The product is okay, nothing special")
print("="*60)
