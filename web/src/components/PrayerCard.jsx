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
            <div className="prayer-name">
                {labels[id]} {icons[id]}
            </div>
            <div className="prayer-time">{time}</div>

            {extra && <div className="sub-info">{extra}</div>}

            {isActive && <div className="time-remaining">Next</div>}
        </div>
    );
};

export default PrayerCard;
