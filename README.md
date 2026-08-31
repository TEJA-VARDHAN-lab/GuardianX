# 🛡️ GuardianX

### Detect. Analyze. Respond.

> Turning surveillance cameras into intelligent emergency sensors.

GuardianX is an AI-powered emergency detection and incident management platform built to help teams detect dangerous situations, understand what is happening, and coordinate a response from one place.

The project combines computer vision, backend services, real-time camera processing, incident workflows, and an operations dashboard into one system.

---

## 🚀 What I've Built So Far

GuardianX is an active work in progress. The current build includes:

- 🎥 **Camera intelligence** — camera registration, health monitoring, streaming, and processing pipelines
- 🧠 **AI detection pipeline** — YOLOv8-based detection with specialized emergency detectors
- 🔥 **Emergency detection** — fire, flood, landslide, weapon, and accident-oriented detection/rules
- 🚨 **Incident management** — incident creation, status transitions, severity handling, and response workflow logic
- 🗺️ **Tactical map** — live operational view using Leaflet for incident/camera location context
- 📊 **Operations dashboard** — incident statistics, active alerts, resolved incidents, and system visibility
- 🤖 **AI assistant layer** — backend support for operational/incident queries
- 📡 **Real-time communication** — WebSocket and camera-stream routes for live updates
- 📱 **Response integration** — Telegram configuration for operational notifications
- 🗄️ **Database layer** — SQLAlchemy + SQLite with Alembic migrations
- 🐳 **Container-ready stack** — project structure prepared for Docker-based deployment

---

## 🧠 Architecture

```text
                         ┌─────────────────────┐
                         │     React / UI       │
                         │  Dashboard + Maps    │
                         └──────────┬──────────┘
                                    │
                             HTTP / WebSocket
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │     Backend API     │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        ┌───────────┐         ┌────────────┐       ┌────────────┐
        │ Camera /  │         │ Incident   │       │ AI / Rules │
        │ Streaming │         │ Management │       │   Engine   │
        └─────┬─────┘         └─────┬──────┘       └─────┬──────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │  SQLAlchemy / DB    │
                         │   SQLite (current)  │
                         └─────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Telegram / Response │
                         └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- React
- TypeScript
- Interactive tactical map with Leaflet

### Backend
- Python
- FastAPI
- Pydantic / pydantic-settings
- SQLAlchemy
- Alembic
- WebSockets

### AI / Computer Vision
- YOLOv8
- OpenCV
- Custom emergency detectors and rule engines
- Ollama / LLM integration groundwork

### Data & Infrastructure
- SQLite (current development database)
- Docker
- Python virtual environment
- Environment-based configuration via `.env`

### Integrations
- Telegram Bot API configuration

---

## 🔐 Authentication & Security

Authentication is part of the next security layer of the platform rather than a completed feature in the current build.

The backend already has configuration support for application secrets and the dependency stack includes JWT/authentication packages, but the current API does **not yet implement a complete user login → token → authorization flow**.

Planned direction:

```text
GitHub / OAuth Login
        ↓
User Identity
        ↓
Secure Session / JWT
        ↓
Protected FastAPI Routes
        ↓
Role-based permissions
```

The goal is to support secure operator access without exposing incident, camera, or response operations to unauthenticated users.

---

## 📁 Project Structure

```text
aI/
backend/
  app/
    ai/              # detection + inference + emergency rules
    api/             # FastAPI routes
    camera/          # camera registry and workers
    core/            # application configuration
    db/              # database/session setup
    models/          # SQLAlchemy models
    repositories/    # database access layer
    schemas/         # API schemas
    services/        # business logic
frontend/            # React / TypeScript application
server.js            # legacy/simple server implementation
```

---

## 🚨 Emergency Detection Pipeline

The current backend is organized around a modular detection workflow rather than one monolithic model.

```text
Camera Feed
    ↓
Frame Capture
    ↓
AI / CV Inference
    ↓
Detection
    ↓
Emergency Mapping
    ↓
Rule / Hybrid Engine
    ↓
Incident Creation
    ↓
Dashboard + Response Workflow
```

This structure makes it possible to add or tune individual emergency detectors without rebuilding the entire system.

---

## 🗺️ Tactical Operations View

GuardianX includes a tactical-map direction for connecting camera/incident data to real locations. The project has already introduced a Leaflet-based tactical map and backend updates around that operational view.

---

## 📈 Current Development Status

### ✅ Built

- Core FastAPI backend
- Camera registry and camera workers
- Camera health and streaming routes
- AI inference pipeline
- Emergency-specific detection modules
- Incident management workflow
- Dashboard statistics and operational routes
- WebSocket endpoint
- Tactical map integration
- SQLite + SQLAlchemy data layer
- Telegram configuration

### 🔨 In Progress / Next

- GitHub OAuth authentication
- Secure JWT/session lifecycle
- Role-based access control
- Protected API and WebSocket authorization
- Production database/deployment hardening
- Expanded real-world emergency detection evaluation

---

## 🧪 Project Status

> **🚧 Under active development**

GuardianX is currently an evolving prototype/MVP. The architecture is being built toward a more production-ready emergency operations platform, with security, reliability, and deployment hardening still ahead.

---

## 📌 Milestones So Far

- **Initial commit** — project foundation
- **Incident manager + database structure** — core incident workflow groundwork
- **Fire detection threshold/rule updates** — tuned emergency detection behavior
- **Leaflet tactical map** — added operational geographic visualization
- **Backend + tactical map updates** — expanded the integrated operations flow

---

## 🎯 Vision

GuardianX is being built around one idea:

> **Detect earlier. Understand faster. Respond smarter.**

Instead of treating cameras as passive video sources, the goal is to turn them into an intelligent sensing layer for emergency operations.

---

## 👨‍💻 Author

**Rushabh**

Building GuardianX step by step — from computer vision and incident intelligence to secure, real-time emergency operations.

---

⭐ If you're interested in AI, computer vision, intelligent systems, or emergency technology, follow the project as it evolves.
