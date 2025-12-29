import React from 'react';
import { prayerContent } from '../data/prayerContent';

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

const arabic = {
    fajr: 'الفجر',
    sunrise: 'الشروق',
    zuhr: 'الظهر',
    asr: 'العصر',
    maghrib: 'المغرب',
    isha: 'العشاء'
};

const PrayerDetailList = ({ times }) => {
    if (!times) return null;

    const order = ['fajr', 'sunrise', 'zuhr', 'asr', 'maghrib', 'isha'];

    return (
        <div className="prayer-detail-list">
            {order.map(key => {
                // Handle Asr Standard vs Hanafi
                let timeDisplay = times[key];
                let secondaryTime = null;

                if (key === 'asr') {
                    timeDisplay = times.asr_standard || times.asr; // Default to Standard
                    secondaryTime = times.asr_hanafi;
                }

                const content = prayerContent[key];

                return (
                    <section key={key} className={`prayer-detail-item ${key}`}>
                        <div className="prayer-detail-content">
                            <div className="detail-header">
                                <h2 className="detail-name">
                                    {labels[key]}
                                    <span className="arabic-script">{arabic[key]}</span>
                                </h2>
                                <div className="detail-time-group">
                                    <span className="detail-time-main">{timeDisplay}</span>
                                    {secondaryTime && (
                                        <span className="detail-time-sub">Hanafi: {secondaryTime}</span>
                                    )}
                                </div>
                            </div>

                            <div className="detail-body">
                                {content.limitations && (
                                    <div className="content-warning">{content.limitations}</div>
                                )}

                                {content.significance && (
                                    <div className="detail-block">
                                        <p>{content.significance}</p>
                                    </div>
                                )}

                                {content.jurisprudence && (
                                    <div className="detail-block">
                                        <p>{content.jurisprudence}</p>
                                    </div>
                                )}

                                {content.hadith && (
                                    <div className="content-hadith">
                                        "{content.hadith}"
                                    </div>
                                )}
                            </div>
                        </div>
                    </section>
                );
            })}
        </div>
    );
};

export default PrayerDetailList;
