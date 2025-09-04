// App.js
import React, { useState, useEffect } from 'react';

function App() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch('/api/items');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setItems(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchItems();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newItem }),
      });
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setItems([...items, data]);
      setNewItem('');
    } catch (err) {
      setError(err);
    }
  };

  const handleVote = async (id, direction) => {
    try {
      const response = await fetch(`/api/items/${id}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction }),
      });
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      const updatedItem = await response.json();
      setItems(items.map(item => item.id === updatedItem.id ? updatedItem : item));
    } catch (err) {
      setError(err);
    }
  };


  if (loading) return <div style={{ textAlign: 'center', marginTop: '200px' }}>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error.message}</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h1>Community Voting Platform</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="Add new item"
          style={{ padding: '10px', border: '1px solid #ccc' }}
        />
        <button type="submit" style={{ padding: '10px', backgroundColor: '#4CAF50', color: 'white', border: 'none', cursor: 'pointer' }}>Add</button>
      </form>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {items.map((item) => (
          <li key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px', padding: '10px', border: '1px solid #ccc' }}>
            <span>{item.title}</span>
            <div>
              <button onClick={() => handleVote(item.id, 'up')} style={{ backgroundColor: '#4CAF50', color: 'white', border: 'none', padding: '5px 10px', marginRight: '5px', cursor: 'pointer' }}>Upvote ({item.votes})</button>
              <button onClick={() => handleVote(item.id, 'down')} style={{ backgroundColor: 'red', color: 'white', border: 'none', padding: '5px 10px', cursor: 'pointer' }}>Downvote</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;