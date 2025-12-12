import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filterSentiment, setFilterSentiment] = useState('ALL'); // Filter: ALL, POSITIVE, NEUTRAL, NEGATIVE

  // URL Backend kita (Pastikan portnya 6543)
  const API_URL = 'http://localhost:6543/api';

  // Ambil data saat web pertama dibuka
  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const res = await axios.get(`${API_URL}/reviews`);
      setReviews(res.data);
    } catch (err) {
      console.error("Gagal mengambil data:", err);
      setError("Gagal koneksi ke Backend. Pastikan backend jalan!");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText) return;

    setLoading(true);
    setError(null);

    try {
      // Kirim text ke backend untuk dianalisis AI
      await axios.post(`${API_URL}/analyze-review`, {
        text: inputText
      });
      setInputText(''); // Kosongkan form
      fetchReviews();   // Refresh daftar review
    } catch (err) {
      setError("Gagal menganalisis. Cek console untuk detail.");
    } finally {
      setLoading(false);
    }
  };

  // Filter reviews berdasarkan sentiment
  const filteredReviews = filterSentiment === 'ALL' 
    ? reviews 
    : reviews.filter(review => review.sentiment === filterSentiment);

  return (
    <div className="container">
      <header>
        <h1>🤖 Product Review Analyzer</h1>
        <p>Powered by Gemini & Hugging Face</p>
      </header>
      
      {/* Form Input */}
      <div className="card input-section">
        <form onSubmit={handleSubmit}>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Tulis review produk di sini (Bahasa Inggris)... Contoh: This laptop is fast but the battery is bad."
            rows="4"
            disabled={loading}
          />
          <button type="submit" disabled={loading} className={loading ? 'loading' : ''}>
            {loading ? 'Sedang Menganalisis...' : 'Analyze Review'}
          </button>
        </form>
        {error && <p className="error-msg">{error}</p>}
      </div>

      {/* Hasil Analysis */}
      <div className="results-section">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>Riwayat Analisis ({filteredReviews.length})</h2>
          
          {/* Filter Buttons */}
          <div className="filter-buttons">
            <button 
              className={filterSentiment === 'ALL' ? 'filter-btn active' : 'filter-btn'}
              onClick={() => setFilterSentiment('ALL')}
            >
              All ({reviews.length})
            </button>
            <button 
              className={filterSentiment === 'POSITIVE' ? 'filter-btn active positive' : 'filter-btn positive'}
              onClick={() => setFilterSentiment('POSITIVE')}
            >
              Positive ({reviews.filter(r => r.sentiment === 'POSITIVE').length})
            </button>
            <button 
              className={filterSentiment === 'NEUTRAL' ? 'filter-btn active neutral' : 'filter-btn neutral'}
              onClick={() => setFilterSentiment('NEUTRAL')}
            >
              Neutral ({reviews.filter(r => r.sentiment === 'NEUTRAL').length})
            </button>
            <button 
              className={filterSentiment === 'NEGATIVE' ? 'filter-btn active negative' : 'filter-btn negative'}
              onClick={() => setFilterSentiment('NEGATIVE')}
            >
              Negative ({reviews.filter(r => r.sentiment === 'NEGATIVE').length})
            </button>
          </div>
        </div>
        
        {filteredReviews.length === 0 && <p className="empty-state">Tidak ada review dengan filter ini.</p>}
        
        <div className="grid">
          {filteredReviews.map((review) => (
            <div key={review.id} className="review-card">
              <div className="card-header">
                {/* Badge Sentiment */}
                <span className={`badge ${review.sentiment.toLowerCase()}`}>
                  {review.sentiment}
                </span>
                <span className="date">
                  {new Date(review.created_at).toLocaleDateString()}
                </span>
              </div>
              
              <p className="original-text">"{review.product_text}"</p>
              
              <div className="ai-insight">
                <strong>✨ Key Points (Gemini):</strong>
                <div style={{whiteSpace: "pre-wrap"}}>{review.key_points}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;