import React from 'react';
import RafeeqLogo from './RafeeqLogo';

const PhoneMockup = ({ messages = [] }) => {
    return (
        <div className="phone-mockup">
            <div className="phone-bezel">
                <div className="phone-camera"></div>
                <div className="phone-screen">
                    {/* WhatsApp Header Mock */}
                    <div className="wa-header">
                        <div className="wa-avatar" style={{ overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <RafeeqLogo size="sm" showText={false} color="#008069" />
                        </div>
                        <div className="wa-info">
                            <span className="wa-name">Rafeeq AI</span>
                            <span className="wa-status">online</span>
                        </div>
                    </div>

                    {/* Messages Container */}
                    <div className="wa-chat-body">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`wa-message ${msg.sender === 'user' ? 'wa-out' : 'wa-in'}`}>
                                {msg.text}
                                <span className="wa-time">{msg.time}</span>
                            </div>
                        ))}
                    </div>

                    {/* Input Bar Mock */}
                    <div className="wa-input-bar">
                        <div className="wa-input-field"></div>
                        <div className="wa-mic-icon"></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PhoneMockup;
