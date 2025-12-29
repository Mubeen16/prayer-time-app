import React from 'react';

const RafeeqLogo = ({ className = '', size = 'md', showText = true, color = '#008069' }) => {
    // Sizes
    const dim = size === 'lg' ? 48 : size === 'sm' ? 24 : 32;
    // Font sizes
    const fontSizeEn = size === 'lg' ? '1.5rem' : size === 'sm' ? '0.9rem' : '1.2rem';
    const fontSizeAr = size === 'lg' ? '1.4rem' : size === 'sm' ? '0.8rem' : '1.1rem';

    return (
        <div className={`rafeeq-brand ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {/* Elegant SVG Icon: Crescent & Spark */}
            <svg
                width={dim}
                height={dim}
                viewBox="0 0 100 100"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <circle cx="50" cy="50" r="48" fill={color} fillOpacity="0.1" />
                {/* Stylized Crescent */}
                <path
                    d="M70 20C65 15 55 12 45 14C30 17 20 30 20 50C20 70 30 83 45 86C55 88 65 85 70 80"
                    stroke={color}
                    strokeWidth="8"
                    strokeLinecap="round"
                />
                {/* AI Spark/Star Node */}
                <path
                    d="M60 50L65 50M62.5 47.5L62.5 52.5"
                    stroke={color}
                    strokeWidth="4"
                    strokeLinecap="round"
                />
                <circle cx="55" cy="50" r="8" fill={color} />
            </svg>

            {showText && (
                <div className="brand-text-stack" style={{ display: 'flex', flexDirection: 'column', lineHeight: 1 }}>
                    <span
                        style={{
                            fontFamily: '"Inter", sans-serif',
                            fontWeight: 700,
                            fontSize: fontSizeEn,
                            color: '#1e293b',
                            letterSpacing: '-0.02em'
                        }}
                    >
                        Rafeeq
                    </span>
                    <span
                        style={{
                            fontFamily: '"Amiri", "Traditional Arabic", serif',
                            fontWeight: 400,
                            fontSize: fontSizeAr,
                            color: color,
                            marginTop: '-4px'
                        }}
                    >
                        رفيق
                    </span>
                </div>
            )}
        </div>
    );
};

export default RafeeqLogo;
