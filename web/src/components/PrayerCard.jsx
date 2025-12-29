import React from 'react';

const icons = {
    fajr: '🌙',
    sunrise: '🌅',
    zuhr: '☀️',
    asr: '⛅',
    maghrib: '🌇',
    isha: '🌑'
};

const labels = {
    fajr: 'Fajr',
    sunrise: 'Sunrise',
    zuhr: 'Zuhr',
    asr: 'Asr',
    maghrib: 'Maghrib',
    isha: 'Isha'
};

const PrayerCard = ({ id, time, extra, isActive }) => {
    return (
        <div className={`prayer-card ${isActive ? 'active' : ''}`}>
            {/* 1. Name & Icon */}
            <div className="prayer-name">
                {labels[id]} {icons[id]}
            </div>

            {/* 2. Time */}
            <div className="prayer-time">{time}</div>

            {/* 3. Info */}
            {extra && <div className="sub-info">{extra}</div>}

            {/* 4. Badge (Bottom) */}
            {isActive && <div className="time-remaining">Next</div>}
        </div>
    );
};

export default PrayerCard;
