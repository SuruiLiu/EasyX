import React, { useState, useEffect } from 'react';

const Home = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Fetch welcome message from backend
    fetch('http://localhost:5001/')
      .then(response => response.text())
      .then(data => setMessage(data))
      .catch(error => {
        console.error('Error fetching data:', error);
        setMessage('Failed to connect to backend');
      });
  }, []);

  return (
    <div style={{ padding: '40px', textAlign: 'center' }}>
      <h2>Home Page</h2>
      <p>Backend Message: <strong>{message}</strong></p>
      <div style={{ marginTop: '20px' }}>
        <p>This is a simple React frontend connected to a Flask backend.</p>
      </div>
    </div>
  );
};

export default Home;
