import React, { useState } from 'react';
import RafeeqOptIn from '../components/RafeeqOptIn';
import PhoneMockup from '../components/PhoneMockup';
import RafeeqNavbar from '../components/RafeeqNavbar';
import '../App.css'; // Ensure CSS is loaded

const Rafeeq = () => {
    const [isOptInOpen, setIsOptInOpen] = useState(false);

    // Initial Messages for Hero Mockup
    const heroMessages = [
        { text: "Assalamu Alaikum! It is time for Asr (4:45 PM).", time: "4:45 PM", sender: "bot" },
        { text: "Prayed", time: "5:15 PM", sender: "user" },
        { text: "Alhamdulillah. May Allah accept it.", time: "5:15 PM", sender: "bot" }
    ];

    return (
        <div className="rafeeq-page-v2">
            <RafeeqNavbar onGetStarted={() => setIsOptInOpen(true)} />

            {/* 1. Hero Section (Split) */}
            <section className="rafeeq-hero-split">
                <div className="hero-content">
                    <span className="badge-pill">New V1 Beta</span>
                    <h1>Your AI Accountability Partner for <span className="text-highlight">Salah</span></h1>
                    <p className="hero-subtitle">
                        Gentle reminders via WhatsApp. No guilt, no coaching, just a quiet tap on the shoulder to keep you consistent.
                    </p>
                    <button className="cta-primary-btn" onClick={() => setIsOptInOpen(true)}>
                        Start Accountability
                    </button>
                    <p className="micro-copy">Free to use • No app install required</p>
                </div>
                <div className="hero-visual">
                    <div className="phone-wrapper-3d">
                        <PhoneMockup messages={heroMessages} />
                    </div>
                    {/* Abstract Blur Background */}
                    <div className="blur-circle blur-blue"></div>
                    <div className="blur-circle blur-green"></div>
                </div>
            </section>

            {/* 2. ZigZag Feature: Seamless Integration */}
            <section className="feature-section">
                <div className="feature-container">
                    <div className="feature-visual left">
                        {/* Simple Chat Bubble Visual or Icon */}
                        <div className="visual-card">
                            <div className="chat-bubble-lg">
                                <span className="wa-icon-lg">💬</span>
                                <p>Lives right in your WhatsApp.</p>
                            </div>
                        </div>
                    </div>
                    <div className="feature-content right">
                        <h2>Seamless Integration</h2>
                        <p>
                            No new apps to download or check. Rafeeq lives where you already chat.
                            Receive prayer times and reply instantly.
                        </p>
                    </div>
                </div>
            </section>

            {/* 3. ZigZag Feature: Nightly Summary */}
            <section className="feature-section bg-offset">
                <div className="feature-container reverse">
                    <div className="feature-content left">
                        <h2>Nightly Reflection</h2>
                        <p>
                            At the end of the day, get a gentle summary of your prayers.
                            Reflect on your consistency without judgment.
                        </p>
                    </div>
                    <div className="feature-visual right">
                        <div className="visual-card-glass">
                            <div className="summary-mock">
                                <h4>🌙 Daily Summary</h4>
                                <div className="stat-row">
                                    <span>Fajr</span> <span className="check">✅</span>
                                </div>
                                <div className="stat-row">
                                    <span>Zuhr</span> <span className="check">✅</span>
                                </div>
                                <div className="stat-row">
                                    <span>Asr</span> <span className="check">✅</span>
                                </div>
                                <div className="stat-row">
                                    <span>Maghrib</span> <span className="miss">❌</span>
                                </div>
                                <div className="stat-row">
                                    <span>Isha</span> <span className="check">✅</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Sticky Bottom Bar for Mobile */}
            <div className="sticky-bottom-bar">
                <div className="sticky-content">
                    <span>Ready to improve?</span>
                    <button className="cta-sm-btn" onClick={() => setIsOptInOpen(true)}>Get Started</button>
                </div>
            </div>

            {/* Modals */}
            <RafeeqOptIn
                isOpen={isOptInOpen}
                onClose={() => setIsOptInOpen(false)}
                lat={localStorage.getItem("user_lat")}
                lng={localStorage.getItem("user_lng")}
            />
        </div>
    );
};

export default Rafeeq;
