// App.js
import React, { useState, useEffect } from 'react';

const App = () => {
  const [reviews, setReviews] = useState([]);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [review, setReviewText] = useState('');

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch('/api/reviews');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setReviews(data);
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    };
    fetchReviews();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, author, review: reviewText }),
      });
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      const newReview = await response.json();
      setReviews([...reviews, newReview]);
      setTitle('');
      setAuthor('');
      setReviewText('');
    } catch (error) {
      console.error('Error submitting review:', error);
    }
  };

  return (
    <div style={{ fontFamily: 'sans-serif', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h1>Book Review Platform</h1>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', width: '300px' }}>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ marginBottom: '10px', padding: '8px' }}
        />
        <input
          type="text"
          placeholder="Author"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          style={{ marginBottom: '10px', padding: '8px' }}
        />
        <textarea
          placeholder="Review"
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          style={{ marginBottom: '10px', padding: '8px', height: '100px' }}
        />
        <button type="submit" style={{ padding: '8px', backgroundColor: '#4CAF50', color: 'white', border: 'none', cursor: 'pointer' }}>Submit</button>
      </form>
      <div style={{ marginTop: '20px', width: '300px' }}>
        <h2>Reviews</h2>
        <ul>
          {reviews.map((review) => (
            <li key={review._id} style={{ marginBottom: '10px', padding: '10px', border: '1px solid #ccc' }}>
              <h3>{review.title} by {review.author}</h3>
              <p>{review.review}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;