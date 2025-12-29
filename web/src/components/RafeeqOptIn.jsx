import React, { useState } from 'react';

const API_BASE = "http://localhost:8000";

const RafeeqOptIn = ({ isOpen, onClose, lat, lng }) => {
    // Wizard State
    const [step, setStep] = useState(1);
    const [status, setStatus] = useState("idle");
    const [msg, setMsg] = useState("");

    // Form Data
    const [phone, setPhone] = useState("");
    const [name, setName] = useState("");
    const [prayers, setPrayers] = useState(["fajr", "zuhr", "asr", "maghrib", "isha"]);
    const [method, setMethod] = useState("text"); // text, call
    const [intensity, setIntensity] = useState("steady"); // light, steady, strong

    if (!isOpen) return null;

    const handleNext = () => setStep(step + 1);
    const handleBack = () => setStep(step - 1);

    const togglePrayer = (p) => {
        if (prayers.includes(p)) {
            setPrayers(prayers.filter(item => item !== p));
        } else {
            setPrayers([...prayers, p]);
        }
    };

    const handleSubmit = async () => {
        setStatus("loading");
        try {
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            const res = await fetch(`${API_BASE}/rafeeq/opt-in`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    phone_number: phone,
                    name: name,
                    timezone: timezone,
                    latitude: lat || 0.0,
                    longitude: lng || 0.0,
                    preferences: {
                        prayers: prayers,
                        method: method,
                        intensity: intensity
                    }
                })
            });

            const data = await res.json();

            if (res.ok) {
                setStatus("success");
                setMsg("Accountability Active. Check WhatsApp.");
                setTimeout(() => {
                    onClose();
                    // Reset
                    setStep(1);
                    setStatus("idle");
                    setPhone("");
                    setName("");
                }, 3000);
            } else {
                throw new Error(data.detail || "Opt-in failed");
            }
        } catch (err) {
            setStatus("error");
            setMsg(err.message);
        }
    };

    // --- Render Steps ---
    const renderStep1 = () => (
        <div className="wizard-step">
            <h3>Let's get started</h3>
            <p className="step-desc">Who should Rafeeq contact?</p>
            <div className="form-group">
                <label>Phone Number (with country code)</label>
                <input
                    type="text"
                    placeholder="+447..."
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                />
            </div>
            <div className="form-group">
                <label>Name (Optional)</label>
                <input
                    type="text"
                    placeholder="Your Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </div>
            <button className="cta-primary-btn full-width" onClick={handleNext} disabled={!phone}>
                Next: Preferences
            </button>
        </div>
    );

    const renderStep2 = () => (
        <div className="wizard-step">
            <h3>Customize your Partner</h3>

            <div className="pref-section">
                <label>Which prayers need focus?</label>
                <div className="prayer-toggles">
                    {['fajr', 'zuhr', 'asr', 'maghrib', 'isha'].map(p => (
                        <button
                            key={p}
                            className={`toggle-btn ${prayers.includes(p) ? 'active' : ''}`}
                            onClick={() => togglePrayer(p)}
                        >
                            {p.charAt(0).toUpperCase() + p.slice(1)}
                        </button>
                    ))}
                </div>
            </div>

            <div className="pref-section">
                <label>Reminder Method</label>
                <div className="radio-group-modern">
                    <button className={`radio-btn ${method === 'text' ? 'selected' : ''}`} onClick={() => setMethod('text')}>
                        💬 Text
                    </button>
                    <button className={`radio-btn ${method === 'call' ? 'selected' : ''}`} onClick={() => setMethod('call')}>
                        📞 Call (Pro)
                    </button>
                </div>
            </div>

            <div className="pref-section">
                <label>Intensity</label>
                <div className="intensity-slider-mock">
                    {['light', 'steady', 'strong'].map(lvl => (
                        <button
                            key={lvl}
                            className={`intensity-btn ${intensity === lvl ? 'selected' : ''}`}
                            onClick={() => setIntensity(lvl)}
                        >
                            {lvl.charAt(0).toUpperCase() + lvl.slice(1)}
                        </button>
                    ))}
                </div>
                <p className="intensity-desc">
                    {intensity === 'light' && "Gentle text only if you miss 2 days."}
                    {intensity === 'steady' && "Daily reminders and nightly summary."}
                    {intensity === 'strong' && "Strict accountability. Follow-ups if missed."}
                </p>
            </div>

            <div className="wizard-actions">
                <button className="btn-secondary" onClick={handleBack}>Back</button>
                <button className="cta-primary-btn" onClick={handleSubmit} disabled={status === 'loading'}>
                    {status === 'loading' ? 'Activating...' : 'Enable Rafeeq'}
                </button>
            </div>
            {status === "error" && <p className="error-text">{msg}</p>}
        </div>
    );

    return (
        <div className="modal-overlay">
            <div className="modal-content opt-in-modal">
                <button className="close-btn-modal" onClick={onClose}>&times;</button>
                <div className="modal-header-clean">
                    <h2>Rafeeq Setup</h2>
                    <div className="step-dots">
                        <span className={`dot ${step >= 1 ? 'active' : ''}`}></span>
                        <span className={`dot ${step >= 2 ? 'active' : ''}`}></span>
                    </div>
                </div>

                {status === "success" ? (
                    <div className="success-message">
                        <span style={{ fontSize: '3rem' }}>🎉</span>
                        <h3>You're all set!</h3>
                        <p>{msg}</p>
                    </div>
                ) : (
                    <>
                        {step === 1 && renderStep1()}
                        {step === 2 && renderStep2()}
                    </>
                )}
            </div>
        </div>
    );
};

export default RafeeqOptIn;
