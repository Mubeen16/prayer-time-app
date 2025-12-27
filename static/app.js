
const API_BASE = window.location.origin;

// Init
document.addEventListener('DOMContentLoaded', () => {
    // Check for location on load
    detectLocationAndLoad();

    // Search Listener
    document.getElementById('search-btn').addEventListener('click', () => {
        const query = document.getElementById('location-input').value;
        if (query) searchLocation(query);
    });

    document.getElementById('location-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = document.getElementById('location-input').value;
            if (query) searchLocation(query);
        }
    });

    // Hamburger Logic
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-sidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    function toggleMenu() {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('visible');
    }

    menuBtn.addEventListener('click', toggleMenu);
    closeBtn.addEventListener('click', toggleMenu);
    overlay.addEventListener('click', toggleMenu);
});

function detectLocationAndLoad() {
    const status = document.getElementById('location-name');
    status.innerText = "Detecting Location...";

    if (!navigator.geolocation) {
        status.innerText = "Location invalid. Defaulting to London.";
        fetchTimes(51.5074, -0.1278);
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            status.innerText = `${lat.toFixed(2)}, ${lng.toFixed(2)} `;
            fetchTimes(lat, lng);
        },
        (error) => {
            console.error(error);
            status.innerText = "Location Denied. Defaulting to London.";
            fetchTimes(51.5074, -0.1278);
        }
    );
}

async function searchLocation(query) {
    const status = document.getElementById('location-name');
    status.innerText = "Searching...";

    try {
        // Use OpenStreetMap Nominatim for free geocoding
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data && data.length > 0) {
            const lat = data[0].lat;
            const lon = data[0].lon;
            const displayName = data[0].display_name.split(',')[0]; // First part usually city

            status.innerText = displayName;
            fetchTimes(lat, lon);
        } else {
            status.innerText = "Location not found.";
        }
    } catch (error) {
        console.error(error);
        status.innerText = "Error searching.";
    }
}

async function fetchTimes(lat, lng) {
    const container = document.getElementById('prayer-cards');
    try {
        const date = new Date().toISOString().split('T')[0];
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

        const response = await fetch(`${API_BASE}/times?lat=${lat}&lng=${lng}&date=${date}&timezone=${timezone}`);
        if (!response.ok) throw new Error("Failed to load times");

        const data = await response.json();
        renderPrayerCards(data); // Pass full data to get asr variants

    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="error">Could not load prayer times.</div>`;
    }
}

function renderPrayerCards(data) {
    const container = document.getElementById('prayer-cards');
    container.innerHTML = '';
    const times = data.times;

    // Explicit order including Sunrise
    const items = [
        { key: 'fajr', label: 'Fajr', icon: '🌙' },
        { key: 'sunrise', label: 'Sunrise', icon: '🌅' },
        { key: 'zuhr', label: 'Zuhr', icon: '☀️' },
        { key: 'asr', label: 'Asr', icon: '⛅' }, // Special logic for Asr
        { key: 'maghrib', label: 'Maghrib', icon: '🌇' },
        { key: 'isha', label: 'Isha', icon: '🌑' }
    ];

    const now = new Date();
    const currentHM = now.getHours() + ":" + String(now.getMinutes()).padStart(2, '0');
    let activeFound = false;

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'prayer-card';

        // Check active (Skip sunrise for "Next Prayer" logic typically, but we include for visibility)
        if (!activeFound && times[item.key] > currentHM) {
            card.classList.add('active');
            activeFound = true;
        }

        let timeHtml = `<div class="prayer-time">${times[item.key]}</div>`;
        let subInfo = '';

        // Special handling for Asr diffs
        if (item.key === 'asr') {
            timeHtml = `<div class="prayer-time">${times.asr_standard}</div>`;
            subInfo = `<div class="sub-info">Hanafi: ${times.asr_hanafi}</div>`;
        }

        // Special info for Sunrise
        if (item.key === 'sunrise') {
            // Ishraq/Duha info usually 15-20 mins after sunrise
            subInfo = `<div class="sub-info">Ishraq: +20m</div>`;
        }

        card.innerHTML = `
            <div class="prayer-name">${item.label} ${item.icon}</div>
            ${timeHtml}
            ${subInfo}
            ${card.classList.contains('active') ? '<div class="time-remaining">Next</div>' : ''}
        `;
        container.appendChild(card);
    });
}


