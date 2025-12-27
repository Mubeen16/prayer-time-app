# UK Innovator Founder Visa - Project Roadmap
**Project Name:** Rafeeq (رفيق)
**Goal:** Build a cross-platform application that uses AI to harmonize religious discipline with professional productivity, suitable for UK endorsement.

---

## 🏗 Phase 1: The Foundation - "The Time Engine" (✅ COMPLETED)
**Objective**: Build a trustworthy, fiqh-compliant temporal backbone.
*   **Innovation Factor**: Unlike generic apps, this engine handles complex edge cases (high latitude) and legal differences (madhabs), establishing "Trust".
*   **Status**:
    *   [x] Custom Solar Calculation Core (No black-box dependencies)
    *   [x] High-Latitude Fallback Logic (Verified for Oslo/London)
    *   [x] FastAPI Backend (`GET /times`)

## 🧠 Phase 2: The Brain - "AI Accountability Core" (NEXT)
**Objective**: Create the AI agent that uses the Time Engine to structure the user's day.
**Innovation Factor**: The AI doesn't just "remind"; it *optimizes* flow. It uses prayer windows as "Pomodoro" anchors for Deep Work.
*   **Tasks**:
    *   [ ] **Context Engine**: Build a module that accepts "User Goals" (e.g., "Finish coding by 5 PM") and "Prayer Times" to generate a schedule.
    *   [ ] **The "Barakah" Algorithm**: Logic to suggest work blocks. (e.g., "Fajr is at 5 AM. High energy block recommended from 6 AM - 8 AM").
    *   [ ] **LLM Integration**: Connect the API to an LLM (Gemini/OpenAI) to generate personalized motivational prompts based on the *current* prayer window.

## 📱 Phase 3: The Body - "Cross-Platform Application"
**Objective**: A unified interface for Mobile (iOS/Android) and Web.
**Strategy**: "Unified Native"- **Technology**: React Native (Expo). This allows us to write ONE codebase and deploy to both Apple and Android.
- **Why Expo?**: It simplifies the "build" process using EAS (Expo Application Services). We don't need a Mac to build the iOS app initially; the cloud does it.

### Step-by-Step Deployment Process

#### 1. Development (The Code)
Instead of HTML/CSS, we use React Native components (`<View>`, `<Text>`). We can reuse the logic from our current `app.js` (fetching API, calculating times).

#### 2. The Build (EAS Build)
We use **EAS Build** to turn our code into binary files:
-   **Android**: Generates an `.aab` (Android App Bundle).
-   **iOS**: Generates an `.ipa` file.

#### 3. Store Submission
**Google Play Store (Android):**
-   **Cost**: $25 (One-time fee).
-   **Process**: Create Developer Account -> Create App Listing -> Upload `.aab` -> Fill Content Rating -> Submit for Review (approx. 3-7 days).

**Apple App Store (iOS):**
-   **Cost**: $99 / year.
-   **Process**: Create Apple Developer Account -> Register App ID -> Create Listing in App Store Connect -> Upload build via Transporter -> Submit for Review (strict guidelines, approx. 1-3 days).

### Innovator Visa Strategy (Mobile)
To satisfy the "Innovation" criteria for the visa, the mobile app must not just be a prayer time app. It must feature:
1.  **The "Barakah" Algorithm**: The AI scheduling feature must be prominent.
2.  **Context Awareness**: Using GPS and Motion sensors (which mobile gives us access to) to detect "Deep Work" states.
.
*   Single codebase for iOS, Android, and Web.
*   Native Notifications for Prayer Alerts.
*   **Tasks**:
    *   [ ] **MVP UI**: Simple dashboard showing "Current Loop" (Current prayer window + Current Task).
    *   [ ] **Notifications**: Intelligent, context-aware pushes. Not just "Adhan", but "Maghrib is in 30 mins. Wrap up your meeting to pray on time."
    *   [ ] **State Management**: Syncing local user state with the AI constraints.

## 🇬🇧 Phase 4: Business & Visa Strategy (The "Endorsement" Layer)
**Objective**: Demonstrate Innovation, Viability, and Scalability.
*   **Viability**:
    *   [ ] **Tech Stack Documentation**: Professional architectural diagrams.
    *   [ ] **Data Privacy**: GDPR compliance (Crucial for UK/EU).
*   **Scalability**:
    *   [ ] **SaaS Architecture**: Dockerize the API for cloud deployment (AWS/Azure).
    *   [ ] **User Growth**: Plan for "Community Challenges" feature.
*   **Innovation**:
    *   [ ] **Whitepaper**: "The Intersection of Faith and Flow State: An AI Approach."

---

## 🚀 Immediate Next Steps (Technical)
1.  **AI Integration**: Create a new endpoint `POST /schedule` that takes tasks + location and returns a "Faith-Optimized Schedule".
2.  **Prototype Frontend**: Build a simple web/mobile interface to demonstrate the "Accountability" loop.
