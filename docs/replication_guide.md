# 🎓 Building Rafeeq: A Student's Guide

## Introduction
This guide explains how to build **Rafeeq**, an AI Accountability Partner.
It is designed for students who want to understand how to architect a modern, hybrid web application.

## The Architecture: "The Three Pillars"
Instead of building one giant "Monolith", we split the project into three distinct parts.

| Pillar | Technology | Purpose | Port |
| :--- | :--- | :--- | :--- |
| **1. The Brain (Math)** | Python (FastAPI) | Calculates Prayer Times strictly using Astronomy & Fiqh. | `8000` |
| **2. The Face (UI)** | React (Vite) | The beautiful interface the user sees. | `5173` |
| **3. The Soul (Logic)** | Python (Django) | The AI partner that tracks habits and holds you accountable. | `8001` |

---

## Pillar 1: The Math Kernel (Al-Vaqth)
**Goal**: Calculate prayer times accurately without relying on external APIs (offline first).

### How we built it:
1.  **Astronomy Layer** (`core/solar_calculations.py`):
    -   We used NOAA solar algorithms to calculate the exact position of the sun.
    -   *Key Concept*: `Solar Noon`, `Declination`, `Hour Angle`.
2.  **Fiqh Layer** (`core/methods.py`):
    -   Different schools of thought (Hanafi vs Shafi) have different rules for Asr and Isha.
    -   We created a dictionary of "Methods" (e.g., Muslim World League) to store these rules.
3.  **API Layer** (`api/main.py`):
    -   We used **FastAPI** to expose these calculations as a simple URL:
    -   `GET /times?lat=51.5&lng=-0.1` -> Returns JSON times.

---

## Pillar 2: The Interface (Frontend)
**Goal**: A premium, app-like experience on body mobile and desktop.

### How we built it:
1.  **Framework**: React + Vite (Fast and modern).
2.  **Design System**:
    -   **Glassmorphism**: Using semi-transparent backgrounds (`backdrop-filter: blur`).
    -   **Cards**: Each prayer is a card that stacks vertically.
3.  **State Management**:
    -   The frontend calls Pillar 1 (`localhost:8000`) to get times.
    -   It stores the user's location in `localStorage`.

---

## Pillar 3: The Accountability Engine (Rafeeq)
**Goal**: An active partner that tracks *if* you prayed, not just when.

### How we built it:
1.  **Framework**: **Django** (The "Batteries Included" framework).
2.  **Database**:
    -   We need to store **Users** and **History**.
    -   Models: `User` (Phone number), `Subscription` (Preferences), `ActivityLog` (Did they pray?).
3.  **The LogicService** (`rafeeq/services.py`):
    -   This is the brain. It runs every minute.
    -   It checks: *"Is it prayer time? Did the user want a Call or Text?"*
    -   It uses a **copy** of Pillar 1's math logic to remain independent.

---

## 🚀 How to Run this Project (Replication)

### Prerequisites
-   Python 3.10+
-   Node.js 18+

### Step 1: Setup the Environment
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn django djangorestframework psycopg2-binary
```

### Step 2: Run Al-Vaqth (The Math)
```bash
cd backend
# Running on Port 8000
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Run Rafeeq (The Logic)
```bash
cd backend_django
# Running on Port 8001
python manage.py runserver 0.0.0.0:8001
```

### Step 4: Run the Frontend
```bash
cd web
npm install
npm run dev
# Opens on Port 5173
```

---

## 🧠 Theory for Students
**Why separate Backends?**
-   **Stability**: If the "AI" crashes, your "Clock" (Al-Vaqth) still works.
-   **Scalability**: You can put the AI on a super-computer and the Clock on a tiny Raspberry Pi.
-   **Modularity**: Different teams can work on different parts without breaking each other's code.
