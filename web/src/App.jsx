import React, { useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import WhatsAppButton from './components/WhatsAppButton';
import Home from './pages/Home';
import Rafeeq from './pages/Rafeeq';

// Navigation Wrapper to handle hooks inside Router
const AppContent = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Helper to determine active location name for Navbar
  const [locationName, setLocationName] = useState(() => {
    return localStorage.getItem("user_city") || "Loading...";
  });

  // We update locationName if localstorage changes? 
  // Ideally use a context or lifting state, but for V1 simple refactor:
  // We trust that Home updates it and maybe we re-read. 
  // Actually, Home handles its own Navbar header if we want specific controls?
  // BUT the design has a global Fixed Top Nav.
  // Let's keep the global nav here.

  const handleOpenRafeeq = () => {
    setIsSidebarOpen(false);
    navigate('/rafeeq');
  };

  return (
    <>
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onOpenRafeeq={handleOpenRafeeq}
      />

      {/* Fixed Global Nav - Hide on /rafeeq */}
      {location.pathname !== '/rafeeq' && (
        <nav className="fixed-top-nav">
          <div className="nav-left">
            <button className="icon-btn-ghost" onClick={() => setIsSidebarOpen(true)}>
              ☰
            </button>
            <div className="brand-text">
              <span className="brand-english">Al-Vaqth</span>
              <span className="brand-arabic">الوقت</span>
            </div>
          </div>

          <div className="nav-right">
            {/* Only show location if on Home? Or globally? */}
            {location.pathname === '/' && (
              <div className="location-pill-clean">
                <span className="location-icon">📍</span>
                <span className="location-text">{locationName}</span>
              </div>
            )}
          </div>
        </nav>
      )}

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/salah" element={<Home />} /> {/* Alias if needed */}
        <Route path="/rafeeq" element={<Rafeeq />} />
      </Routes>

      <WhatsAppButton />
    </>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
