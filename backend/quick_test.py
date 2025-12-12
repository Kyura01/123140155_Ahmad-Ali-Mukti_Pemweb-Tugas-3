import requests

# Test API endpoint
API_URL = "http://localhost:6543/api/analyze-review"

test_reviews = [
    "This is the worst item I have ever bought. It stopped working after just two days and the customer service is terrible. Do not buy this",
    "This product is absolutely amazing! I love it so much, highly recommend to everyone!",
    "The product is okay, nothing special, average quality"
]

for review in test_reviews:
    print(f"\n{'='*60}")
    print(f"Testing: {review[:50]}...")
    response = requests.post(API_URL, json={"text": review})
    result = response.json()
    print(f"✅ Sentiment: {result.get('sentiment', 'N/A')}")
    print(f"{'='*60}")
