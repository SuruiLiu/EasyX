import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import TimesheetReview from './pages/TimeSheetReview'; 
import Extract from './pages/Extract';

function App() {
  return (
    <Router>
      <div className="App">
        <Header title="EasyX System" />
        <nav style={{ padding: '10px 20px', backgroundColor: '#e9ecef', borderBottom: '1px solid #dee2e6' }}>
          <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', gap: '20px' }}>
            <li><Link to="/" style={{ textDecoration: 'none', color: '#007bff' }}>Home</Link></li>
            <li><Link to="/extract" style={{ textDecoration: 'none', color: '#007bff' }}>Extract PDF</Link></li>
            <li><Link to="/review" style={{ textDecoration: 'none', color: '#007bff' }}>Timesheet Review</Link></li>
          </ul>
        </nav>
        <main style={{ minHeight: '60vh' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/extract" element={<Extract />} />
            <Route path="/review" element={<TimesheetReview />}/>
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
