# Changelog

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-22

### Added
- Initial project skeleton: FastAPI backend + React/Vite frontend
- Dictionary Coverage Checker workflow:
  - Backend: `POST /api/dictionary/lookup`, `GET /api/dictionary/misses`, `POST /api/dictionary/seed`
  - SQLite models: `DictionaryEntry`, `DictionaryMiss`
  - Service: canonical lookup, alias resolution (DB + static map), miss deduplication
  - Frontend: search page with kind selector, three-state result display, miss list with filtering
  - Tests: 20+ backend pytest tests, 2 frontend component test suites
- Docker Compose with backend, frontend, persistent volume
- README with architecture, API reference, quick start
- MIT License
- portfolio.json manifest

### Security
- Demo mode localhost-only binding
- No hardcoded credentials
- CORS restricted to localhost origins

### Infrastructure
- Backend Dockerfile (non-root user, healthcheck)
- Frontend Dockerfile (nginx, multi-stage build)
- GitHub Actions CI workflow (backend tests, frontend build/test, Docker builds)