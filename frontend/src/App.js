import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';

function App() {
  return (
    <div className="App">
      <Header title="EasyX System" />
      <main style={{ minHeight: '60vh' }}>
        <Home />
      </main>
      <Footer />
    </div>
  );
}

export default App;
