import React, { useState, useEffect } from 'react';
import PrayerCard from '../components/PrayerCard';
import PrayerDetailList from '../components/PrayerDetailList';
import { prayerContent } from '../data/prayerContent';

// Assuming server is on 8000. In prod this would be env var.
const API_BASE = "http://localhost:8000";

const Home = () => {
    // 1. Initialize State from LocalStorage if available
    const [times, setTimes] = useState(null);
    const [locationName, setLocationName] = useState(() => {
        return localStorage.getItem("user_city") || "Detecting...";
    });
    const [searchQuery, setSearchQuery] = useState("");
    const [loading, setLoading] = useState(true);
    const [errorMsg, setErrorMsg] = useState(null);

    useEffect(() => {
        // 2. Priority: Saved -> GPS -> Default
        const savedLat = localStorage.getItem("user_lat");
        const savedLng = localStorage.getItem("user_lng");

        if (savedLat && savedLng) {
            // Use saved location
            fetchTimes(savedLat, savedLng);
        } else {
            // Try GPS
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        const { latitude, longitude } = pos.coords;
                        fetchCityName(latitude, longitude);
                        fetchTimes(latitude, longitude);
                        // Save GPS as preference
                        saveLocationPreference(latitude, longitude, "Current Location");
                    },
                    () => {
                        // Permission denied or error -> Fallback
                        setLocationName("London, UK");
                        fetchTimes(51.5074, -0.1278);
                    }
                );
            } else {
                // No Geolocation support
                setLocationName("London, UK");
                fetchTimes(51.5074, -0.1278);
            }
        }
    }, []);

    const saveLocationPreference = (lat, lng, name) => {
        localStorage.setItem("user_lat", lat);
        localStorage.setItem("user_lng", lng);
        if (name) localStorage.setItem("user_city", name);
    };

    const fetchCityName = async (lat, lon) => {
        try {
            const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
            const data = await res.json();
            if (data && data.address) {
                const city = data.address.city || data.address.town || data.address.village || data.address.county || "Unknown Location";
                setLocationName(city);
                localStorage.setItem("user_city", city); // Update name in storage
            }
        } catch (e) {
            const fallbackName = `${lat.toFixed(2)}, ${lon.toFixed(2)}`;
            setLocationName(fallbackName);
        }
    };

    const fetchTimes = async (lat, lng) => {
        setLoading(true);
        setErrorMsg(null);
        try {
            const date = new Date().toISOString().split('T')[0];
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

            const res = await fetch(`${API_BASE}/times?lat=${lat}&lng=${lng}&date=${date}&timezone=${timezone}`);
            if (!res.ok) throw new Error("API Error");

            const data = await res.json();
            setTimes(data.times);
        } catch (err) {
            console.error(err);
            setErrorMsg("Could not load times. Check connection.");
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async () => {
        if (!searchQuery) return;
        setLocationName("Searching...");
        setErrorMsg(null);
        try {
            const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}`);
            const data = await res.json();
            if (data && data.length > 0) {
                const place = data[0];
                const name = place.display_name.split(',')[0];

                setLocationName(name);
                fetchTimes(place.lat, place.lon);

                // Save user preference!
                saveLocationPreference(place.lat, place.lon, name);
                setSearchQuery(""); // Clear input on success
            } else {
                setLocationName("Not found");
                setErrorMsg("City not found.");
            }
        } catch (err) {
            console.error(err);
            setLocationName("Error");
            setErrorMsg("Search failed.");
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
            let timeVal = times[key];
            if (!timeVal && key === 'asr_standard') timeVal = times.asr_standard || times.asr;

            if (timeVal > currentHM) return key === 'asr_standard' ? 'asr' : key;
        }
        return 'fajr'; // Wrap around to next day
    };

    const activeKey = getActiveKey();

    return (
        <div className="home-page">
            <h2 className="section-title">Prayer Times</h2>
            {/* Search and Header */}
            <div className="hero-section" style={{ marginTop: '0', paddingBottom: '60px', position: 'relative' }}>

                <header className="page-header" style={{ position: 'relative', zIndex: 10, maxWidth: '1200px', margin: '0 auto' }}>

                    <div className="hero-layout-grid">

                        {/* Center Column: Title & Search */}
                        <div className="hero-center-col">
                            <h2 className="page-title">Al-Vaqth</h2>
                            <p className="page-subtitle">Prayer Times</p>

                            <div className="search-container">
                                <input
                                    type="text"
                                    placeholder="Find your city..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                                />
                                <button onClick={handleSearch}>Search</button>
                            </div>
                            {errorMsg && <p style={{ color: 'red', marginTop: '10px', fontSize: '0.9rem' }}>{errorMsg}</p>}

                            <div className="location-pill-clean" style={{ marginTop: '20px', display: 'inline-flex' }}>
                                <span className="location-icon">📍</span>
                                <span className="location-text">{locationName}</span>
                            </div>
                        </div>

                        {/* Right Column: Rafeeq Promo (Desktop) */}
                        <div className="hero-side-col">
                            <div className="rafeeq-promo-card" onClick={() => window.location.href = '/rafeeq'}>
                                <div className="promo-icon">🤝</div>
                                <div className="promo-text">
                                    <h4>Struggling with Consistency?</h4>
                                    <p>Meet <strong>Rafeeq</strong>, your AI Accountability Partner.</p>
                                    <span className="promo-link">Try it now &rarr;</span>
                                </div>
                            </div>
                        </div>

                    </div>
                </header>

                <main style={{ width: '100%' }}>
                    <section className="prayer-cards-container">
                        {loading ? (
                            <div style={{ textAlign: 'center', width: '100%', padding: '40px' }}>Loading beautiful times...</div>
                        ) : (times && (
                            <>
                                <PrayerCard id="fajr" time={times.fajr} isActive={activeKey === 'fajr'} />
                                <PrayerCard id="sunrise" time={times.sunrise} extra="Ishraq: +20m" isActive={activeKey === 'sunrise'} />
                                <PrayerCard id="zuhr" time={times.zuhr} isActive={activeKey === 'zuhr'} />
                                <PrayerCard id="asr" time={times.asr_standard} extra={<><span>Standard</span><br /><span style={{ fontSize: '0.9em', opacity: 0.8, fontWeight: 400 }}>Hanafi: {times.asr_hanafi}</span></>} isActive={activeKey === 'asr'} />
                                <PrayerCard id="maghrib" time={times.maghrib} isActive={activeKey === 'maghrib'} />
                                <PrayerCard id="isha" time={times.isha} isActive={activeKey === 'isha'} />
                            </>
                        ))}
                    </section>
                </main>

                {/* Decorative Mosque Skyline SVG */}
                <div className="hero-bg-decoration">
                    <svg viewBox="0 0 1440 320" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill="currentColor" fillOpacity="0.1" d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,224C672,245,768,267,864,261.3C960,256,1056,224,1152,197.3C1248,171,1344,149,1392,138.7L1440,128V320H1392C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320H0Z"></path>
                        <path fill="currentColor" fillOpacity="0.15" d="M0,288L48,272C96,256,192,224,288,213.3C384,203,480,213,576,229.3C672,245,768,267,864,250.7C960,235,1056,181,1152,165.3C1248,149,1344,171,1392,181.3L1440,192V320H1392C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320H0Z"></path>
                        <path fill="currentColor" fillOpacity="0.2" d="M980,320V230H1060V320Z M1100,320V180H1120V320Z M1020,320 C1020,280 1060,280 1060,320Z" />
                    </svg>
                </div>
            </div>

            {times && <PrayerDetailList times={times} />}

            {/* Rafeeq CTA Banner */}
            <div className="container" style={{ marginTop: '30px' }}>
                <div className="rafeeq-cta-card" onClick={() => window.location.href = '/rafeeq'}>
                    <div className="rafeeq-cta-content">
                        <span className="cta-badge">New</span>
                        <h3>Meet <span style={{ color: '#008069' }}>Rafeeq AI</span></h3>
                        <p>Your personal Salah accountability partner on WhatsApp.</p>
                    </div>
                    <div className="rafeeq-cta-arrow">→</div>
                </div>
            </div>

            <div className="container" style={{ marginTop: 0 }}>
                <section className="info-section">
                    <h3>{prayerContent.general.miraj.title}</h3>
                    <p>{prayerContent.general.miraj.content}</p>
                </section>
            </div>
        </div>
    );
};

export default Home;
