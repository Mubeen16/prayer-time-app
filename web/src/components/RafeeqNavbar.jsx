import React from 'react';
import RafeeqLogo from './RafeeqLogo';

const RafeeqNavbar = ({ onGetStarted }) => {
    return (
        <nav className="rafeeq-navbar">
            <div className="rafeeq-nav-container">
                <div className="rafeeq-logo" style={{ cursor: 'pointer' }} onClick={() => window.location.href = '/'}>
                    <RafeeqLogo size="md" />
                </div>

                <div className="rafeeq-nav-links desktop-only">
                    <a href="#features">Features</a>
                    <a href="#how-it-works">How It Works</a>
                    <a href="#pricing">Pricing</a>
                </div>

                <div className="rafeeq-nav-cta">
                    <button className="nav-cta-btn" onClick={onGetStarted}>Get Started</button>
                </div>
            </div>
        </nav>
    );
};

export default RafeeqNavbar;
