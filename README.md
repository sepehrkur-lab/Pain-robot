# Pain Robot (MVP)

This repository is an MVP skeleton for the Pain Robot Android app.
- Launcher (Start / Sitting / Exit)
- Rinnegan eyes screen (centered, dark around)
- STT/TTS scaffolding (Android via pyjnius if available)
- AI client (OpenAI wrapper placeholder)
- Local memory (SQLite) for question/answer caching

How to build:
- Option A: Use Buildozer on Ubuntu to create an Android APK.
- Option B: Use GitHub Actions (configure runner for buildozer).

Security note: Do not hard-code API keys in source. Use GitHub Secrets or a backend.
