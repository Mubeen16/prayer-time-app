# Django Migration Walkthrough

## Summary
I have successfully initialized the new **Django + PostgreSQL** backend infrastructure.
This replaces the old FastAPI/SQLite setup with a production-ready foundation that supports:
1.  **Strict Data Models** (User, Habit, Subscription, Logs).
2.  **Admin Panel** (Built-in).
3.  **Future Scalability** (PostgreSQL ready).

## Work Completed

### 1. Project Initialization
- Created `frontend_django/` directory (Note: Created as `backend_django` but effectively the new backend).
- Installed `django`, `djangorestframework`, `psycopg2-binary`.
- Applications created:
    - `core`: Shared logic.
    - `users`: Custom User model.
    - `rafeeq`: Habit logic (Subscription, ActivityLog).
    - `api`: REST Framework endpoints.

### 2. Database Models
Defined the core schema in `rafeeq/models.py`:
```python
class Subscription(models.Model):
    user = models.ForeignKey(User, ...)
    habit = models.ForeignKey(Habit, ...)
    preferences = models.JSONField(default=dict)
```

### 3. API Parity
Implemented the exact same endpoints as the prototype to ensuring the frontend continues working without massive changes yet:
- `POST /rafeeq/opt-in`: Registers user and creates subscription.
- `GET /rafeeq/status`: Fetches user preferences.

### 4. Logic Porting (Accountability Engine)
I have ported the calculating logic to `backend_django/core/` and implemented the **Preferences Logic** in `SalahService`:
- It now filtering prayers based on user selection (e.g. `['fajr', 'isha']`).
- It determines the action (`text` vs `call`) based on intensity.

### 5. Intervention Engine (The Scheduler)
I implemented the "Loop" that makes Rafeeq active.
- **Command**: `python manage.py run_scheduler`
- **Behavior**: Checks for upcoming prayers every 60 seconds.
- **Output**: Logs actions like `Action: CALL` or `Action: TEXT` based on user settings.

## Verification
I updated the verification script `verify_status_fetch.py` and ran the scheduler.

**Scheduler Log:**
```
Starting Rafeeq Scheduler...
User +447999888777: Event isha due at 17:39. Action: CALL
```

## How to Run (New Backend)
1.  **Stop** the old FastAPI server (Port 8000).
2.  **Start** the new Django server:
    ```bash
    cd backend_django
    source ../venv/bin/activate
    python manage.py runserver 0.0.0.0:8000
    ```
3.  **Run the Scheduler** (in new tab):
    ```bash
    cd backend_django
    source ../venv/bin/activate
    python manage.py run_scheduler
    ```
