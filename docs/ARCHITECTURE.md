# 🏗️ Project Structure & Architecture

## High-Level Overview
This project is a **Hybrid Architecture** containing a frontend and two backends (one legacy, one new).

| Component | Tech Stack | Role | Port |
| :--- | :--- | :--- | :--- |
| **Pillar A: Frontend** | React + Vite | The User Interface (PWA) | `5173` |
| **Pillar B: Al-Vaqth** | FastAPI (Python) | **Prayer Times Engine** (Legacy/Stable) | `8000` |
| **Pillar C: Rafeeq** | Django (Python) | **Accountability Engine** (New/Standalone) | `8001` |

## 🛠️ Technology Stack (Details)

### Frontend (User Interface)
*   **Core**: React 19, Vite (Build Tool)
*   **Routing**: React Router DOM 7
*   **Styling**: Pure CSS (Glassmorphism design system)
*   **State**: LocalStorage + React Hooks

### Backend 1: Al-Vaqth (Prayer Engine)
*   **Core**: Python 3.13, FastAPI
*   **Server**: Uvicorn (ASGI)
*   **Logic**: Pure Python (No external APIs, offline math)

### Backend 2: Rafeeq (Accountability Engine)
*   **Core**: Python 3.13, Django 5.x
*   **API**: Django REST Framework (DRF)
*   **Database**: PostgreSQL (Production) / SQLite (Dev)
*   **Task Queue**: Custom Loop (Phase 1) -> Celery/Redis (Phase 2)

---

## 📂 Canvas Map (File Structure)

### 1. `web/` (The Frontend)
> The visual interface the user interacts with.
- `src/components/`: Reusable UI parts (`PrayerCard`, `RafeeqOptIn`).
- `src/pages/`: Full screen layouts (`Home`, `Rafeeq`).
- `src/App.jsx`: Main router.
- **Integration**:
    - Calls `localhost:8000` for Prayer Times.
    - Calls `localhost:8001` for Rafeeq (Accountability).

### 2. `backend/` (Al-Vaqth - The Prayer Engine)
> The original backend. It does ONE thing well: Calculate Prayer Times.
- `core/`: The math logic (`prayer_times.py`).
- `api/`: Endpoints to serve times (`GET /prayer-times`).
- **Status**: **Stable**. We do not touch this anymore. It just works.

### 3. `backend_django/` (Rafeeq - The Accountability Engine)
> The new "Brain" for the Accountability Partner.
- `config/`: Project settings (DB, Apps).
- `core/`: **Ported Logic**. Contains a Copy of the Prayer Math so Rafeeq is independent.
- `rafeeq/`: The Core Logic.
    - `models.py`: Database Schema (`User`, `Subscription`, `ActivityLog`).
    - `services.py`: The Logic (`SalahService` that decides *when* to call you).
- `users/`: User data management.
- `api/`: Endpoints (`POST /opt-in`, `GET /status`).
- **Status**: **Active Development**. This is where we build the AI features.

---

## 🔄 Data & Logic Flow

### The "Dual-Brain" Strategy
We intentionally separated the **Utility** (Prayer Times) from the **Service** (Accountability).

1.  **Frontend Request (Prayer Times)**:
    - User wants to see time.
    - `Frontend` -> `backend/ (Port 8000)`
    - *Why?* Because it's fast, stateless, and already built.

2.  **Frontend Request (Accountability)**:
    - User signs up for Rafeeq.
    - `Frontend` -> `backend_django/ (Port 8001)`
    - *Why?* Because we need User Accounts, History, Admin Panel, and complex AI logic.

3.  **The Rafeeq Loop (Internal)**:
    - Rafeeq needs to know prayer times to hold you accountable.
    - Instead of asking the old backend, it uses its own **Internal Core** (`backend_django/core/`).
    - This makes Rafeeq **Standalone**. You could delete the old backend tomorrow, and Rafeeq would still work.
