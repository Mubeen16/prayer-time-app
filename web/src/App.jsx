import React, { useState, useEffect } from 'react';
import './App.css';
import PrayerCard from './components/PrayerCard';
import Sidebar from './components/Sidebar';

// Assuming server is on 8000. In prod this would be env var.
const API_BASE = "http://localhost:8000";

function App() {
  const [times, setTimes] = useState(null);
  const [locationName, setLocationName] = useState("Detecting...");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          fetchCityName(latitude, longitude);
          fetchTimes(latitude, longitude);
        },
        () => {
          setLocationName("London, UK");
          fetchTimes(51.5074, -0.1278);
        }
      );
    } else {
      setLocationName("London, UK");
      fetchTimes(51.5074, -0.1278);
    }
  }, []);

  const fetchCityName = async (lat, lon) => {
    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
      const data = await res.json();
      if (data && data.address) {
        const city = data.address.city || data.address.town || data.address.village || data.address.county || "Unknown Location";
        setLocationName(city);
      }
    } catch (e) {
      setLocationName(`${lat.toFixed(2)}, ${lon.toFixed(2)}`);
    }
  };

  const fetchTimes = async (lat, lng) => {
    setLoading(true);
    try {
      const date = new Date().toISOString().split('T')[0];
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

      const res = await fetch(`${API_BASE}/times?lat=${lat}&lng=${lng}&date=${date}&timezone=${timezone}`);
      if (!res.ok) throw new Error("API Error");

      const data = await res.json();
      setTimes(data.times);
    } catch (err) {
      console.error(err);
      alert("Failed to fetch times. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery) return;
    setLocationName("Searching...");
    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}`);
      const data = await res.json();
      if (data && data.length > 0) {
        const place = data[0];
        const name = place.display_name.split(',')[0];
        setLocationName(name);
        fetchTimes(place.lat, place.lon);
      } else {
        setLocationName("Not found");
      }
    } catch (err) {
      console.error(err);
      setLocationName("Error");
    }
  };

  // Determine active prayer
  const getActiveKey = () => {
    if (!times) return null;
    const now = new Date();
    const currentHM = now.getHours() + ":" + String(now.getMinutes()).padStart(2, '0');

    // Order for checking "next"
    const order = ['fajr', 'sunrise', 'zuhr', 'asr_standard', 'maghrib', 'isha'];
    for (let key of order) {
      // Simple comparison HH:MM (works if 24h)
      // Note: we use 'asr_standard' for comparison but 'asr' key for display in standard way usually
      // Let's simplify: just check the values in `times` object
      let timeVal = times[key];
      if (!timeVal && key === 'asr_standard') timeVal = times.asr_standard || times.asr; // handling varying API structure if needed

      if (timeVal > currentHM) return key === 'asr_standard' ? 'asr' : key;
    }
    return 'fajr'; // Wrap around to next day (simplified)
  };

  const activeKey = getActiveKey();

  return (
    <div className="container">
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />

      <nav className="top-nav">
        <button className="icon-btn" onClick={() => setIsSidebarOpen(true)}>☰</button>
        <div className="location-display">📍 {locationName}</div>
      </nav>

      <header>
        <div className="super-brand">Rafeeq Project</div>
        <h1>Al-Vaqth <span className="arabic">الوقت</span></h1>

        <div className="search-container">
          <input
            type="text"
            placeholder="City or Postcode"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch}>Search</button>
        </div>
      </header>

      <main>
        <section className="prayer-cards-container">
          {loading ? (
            <div style={{ textAlign: 'center', width: '100%' }}>Loading beautiful times...</div>
          ) : (
            <>
              <PrayerCard id="fajr" time={times.fajr} isActive={activeKey === 'fajr'} />
              <PrayerCard id="sunrise" time={times.sunrise} extra="Ishraq: +20m" isActive={activeKey === 'sunrise'} />
              <PrayerCard id="zuhr" time={times.zuhr} isActive={activeKey === 'zuhr'} />
              <PrayerCard
                id="asr"
                time={times.asr_standard}
                extra={`Hanafi: ${times.asr_hanafi}`}
                isActive={activeKey === 'asr'}
              />
              <PrayerCard id="maghrib" time={times.maghrib} isActive={activeKey === 'maghrib'} />
              <PrayerCard id="isha" time={times.isha} isActive={activeKey === 'isha'} />
            </>
          )}
        </section>

        <section className="ai-section teaser">
          <h3>Rafeeq AI &trade;</h3>
          <p className="desc-text">Your Personal Accountability Partner.</p>
          <div className="coming-soon-badge">Coming Soon</div>
        </section>
      </main>
    </div>
  );
}

export default App;
