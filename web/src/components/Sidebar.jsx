import React from 'react';

const Sidebar = ({ isOpen, onClose, onOpenRafeeq }) => {
    return (
        <>
            {isOpen && <div className="overlay" onClick={onClose} />}
            <nav className={`sidebar ${isOpen ? 'open' : ''}`}>
                <button className="close-btn" onClick={onClose}>&times;</button>
                <h2>Rafeeq Roadmap</h2>
                <ul className="nav-links">
                    <li>
                        <button className="rafeeq-btn" onClick={onOpenRafeeq}>
                            <span style={{ marginRight: '8px' }}>🤖</span>
                            <strong>Rafeeq AI</strong>
                        </button>
                    </li>
                    <div className="divider" style={{ margin: '10px 0', borderBottom: '1px solid #333' }}></div>
                    <li><strong>Phase 1:</strong> Time Engine (Done ✅)</li>
                    <li><strong>Phase 2:</strong> Al-Vaqth Web (Done ✅)</li>
                    <li><strong>Phase 3:</strong> Mobile App (In Progress 🚧)</li>
                    <li><strong>Phase 4:</strong> Community (Planned)</li>
                </ul>
                <div style={{ marginTop: 'auto', fontSize: '0.8rem', color: '#888' }}>
                    <p>Version 0.3.0 (React)</p>
                </div>
            </nav>
        </>
    );
};

export default Sidebar;
