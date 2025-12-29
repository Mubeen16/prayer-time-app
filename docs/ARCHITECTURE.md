# Rafeeq Architecture & Strategy

## 1. System Design: The Modular Monorepo
We utilize a **Modular Monorepo** strategy. This allows us to maintain strict code sharing between the Core Engine and various frontend expressions (Web, Mobile) while keeping velocity high.

### Directory Structure
```text
/rafeeq-monorepo (Root)
  ├── core/            # [SHARED] Pure Python Logic (Prayer Engine, AI Scheduler)
  ├── api/             # [BACKEND] FastAPI Service (REST Interface)
  ├── app/             # [FRONTEND] React Native (Expo) - Mobile & Web
  ├── static/          # [PROTOTYPE] Simple HTML dashboard for rapid API testing
  └── tests/           # [QUALITY] Shared verification suite
```

## 2. Frontend Strategy: "Unified Native"
To satisfy the requirement of a cross-platform application (iOS/Android/Web) for the Innovator Visa, we chose **React Native with Expo**.

-   **Technology**: React Native + Expo Router
-   **Justification**:
    1.  **Single Codebase**: Logic is written once in TypeScript/React.
    2.  **Native Capabilities**: Direct access to Notification APIs (critical for Prayer Alerts) and Location Services.
    3.  **Cross-Platform**: Outputs iOS (`.ipa`), Android (`.apk`), and Responsive Web (PWA) from the same source.

## 3. Backend Strategy: "The Transparent Core"
-   **Technology**: Python + FastAPI
-   **Justification**:
    -   Python is the native language of AI/LLM libraries (crucial for Phase 2).
    -   FastAPI provides auto-generated Swagger docs, essential for third-party auditing of our calculation transparency.

## 4. AI Integration (Phase 2)
The backend exposes a `POST /schedule` endpoint that acts as the "Context Engine".
-   **Input**: User Tasks + Location + Time
-   **Logic**: `core/scheduler.py` (Barakah Algorithm)
-   **Output**: Time blocks optimized around Prayer Windows.
