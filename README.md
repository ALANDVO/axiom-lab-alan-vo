# freehire — Open-Source Search Engine for Job Seekers

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


**Alan Vo | AI & Machine Learning**

freehire is an open-source job search engine that pulls jobs directly from company career pages (Lever, Greenhouse, Ashby, BambooHR, etc.) rather than from scraped aggregators. It provides transparent, deduplicated job listings with AI/ML-powered enrichment for skills, roles, and industries — all built on open dictionaries that anyone can help improve.

## Problem & Approach

Job seekers face fragmented listings across hundreds of company career sites. Existing aggregators scrape from each other, creating duplicates, stale data, and no visibility into what skills/roles a given market actually demands.

**freehire's approach:**
- **Direct ingestion** from 180+ ATS adapters (Lever, Greenhouse, Ashby, Workday, BambooHR, etc.)
- **Dict-only enrichment** — skills, roles, industries resolved against curated dictionaries; unknown terms emit nothing (never hallucinate)
- **Dictionary coverage checker** — public transparency surface showing exactly what freehire recognizes, with community-driven gap reporting
- **Candidate tracking** — users track applications privately; opt-in anonymized aggregation powers crowdsourced process signals per job

**Intended user:** Job seekers who want comprehensive, deduplicated listings with trustworthy skill/role metadata, and engineers who want to extend an open job search infrastructure.

## AI/ML Evaluation

freehire uses deterministic dictionary-based enrichment (no LLM required for core functionality). LLM explanations are opt-in, advisory-only, and grounded in actual dictionary entries.

**Reproducible evaluation:**
```bash
# Backend tests (includes dictionary lookup logic tests)
cd backend && PYTHONPATH=. python -m pytest tests/ -v

# Dictionary coverage baseline (seeded entries)
python -c "
from app.services.dictionary import seed_dictionary, lookup_term, DictionaryKind
from app.core.database import SessionLocal
db = SessionLocal()
seed_dictionary(db)
for kind in DictionaryKind:
    entries = db.query(__import__('app.models.dictionary', fromlist=['DictionaryEntry']).DictionaryEntry).filter(
        __import__('app.models.dictionary', fromlist=['DictionaryEntry']).DictionaryEntry.kind == kind.value
    ).count()
    print(f'{kind.value}: {entries} entries')
"
```

**Baseline (seeded):**
- Skills: 20 entries (+ aliases)
- Roles: 10 entries (+ aliases)
- Industries: 10 entries (+ aliases)

**Failure cases (expected misses):**
- Emerging terms: "quantum-computing", "prompt-engineering", "rust", "zig"
- Niche aliases: "kube" → kubernetes (covered), "k8s" → kubernetes (covered)
- Ambiguous abbreviations: "ml" → machine-learning (covered), "ai" → artificial-intelligence (covered)

## Features

### Dictionary Coverage Checker (`/dictionary`)
Public page to look up any skill, role, or industry term. Three possible answers:
1. **Canonical hit** — term is a canonical dictionary entry (shows slug + display label)
2. **Alias hit** — term resolves to a different canonical (e.g., `k8s` → `kubernetes`, shows what it resolves to)
3. **Miss** — term not recognized; recorded in deduplicated miss table for maintainer review

### Job Search & Enrichment (planned)
- Search across all ingested company boards
- Filter by skill, role, industry, location, seniority
- Dict-only enrichment badges on each listing

### Candidate Profile & Tracking (planned)
- Unified single-page profile (replaces 8-tab legacy design)
- Application tracking with calendar sync
- Opt-in anonymized sharing for crowdsourced process signals

## Quick Start

### Prerequisites
- Python 3.12+
- Node 24+
- Docker (optional, for containerized run)

### Local Development

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` (frontend proxies `/api` to backend on `127.0.0.1:8000`).

### Docker Compose
```bash
docker compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### Testing

**Backend:**
```bash
cd backend
PYTHONPATH=. python -m pytest tests/ -v
```

**Frontend:**
```bash
cd frontend
npm run test
```

## Architecture

```mermaid
graph TB
    subgraph Client
        FE[React + Vite Frontend]
    end
    
    subgraph Server
        API[FastAPI Backend]
        DB[(SQLite)]
    end
    
    subgraph Ingestion
        ADAPTERS[ATS Adapters\n(Lever, Greenhouse, Ashby...)]
        DICT[Dictionaries\n(Skills, Roles, Industries)]
    end
    
    FE -->|REST API| API
    API --> DB
    ADAPTERS --> DB
    DICT --> API
```

## API Reference

### Dictionary Coverage

**POST** `/api/dictionary/lookup`
```json
{ "kind": "skill", "term": "k8s" }
```
Response:
```json
{
  "result_type": "alias",
  "kind": "skill",
  "term": "k8s",
  "canonical_slug": "kubernetes",
  "display_label": "Kubernetes",
  "resolved_to": "kubernetes"
}
```

**GET** `/api/dictionary/misses?kind=skill&limit=50`
Returns paginated list of recorded misses for admin review.

**POST** `/api/dictionary/seed`
Idempotent seed of baseline dictionary entries.

### Health
**GET** `/health` → `{ "status": "ok", "app": "freehire", "version": "1.0.0" }`

## Security Limitations

- **Demo mode** binds to localhost only; refuses to start in production without explicit configuration
- **No authentication implemented yet** — OIDC/Keycloak integration planned
- **SQLite** for development; PostgreSQL recommended for production
- **No rate limiting** on public endpoints (dictionary lookup, miss submission)
- **LLM keys** server-side only; never exposed to client

## Provider Configuration

| Provider | Adapter | Config Variables |
|----------|---------|------------------|
| OpenAI-compatible (OpenRouter, LiteLLM, Ollama) | `httpx` | `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL` |
| Anthropic | `httpx` | `LLM_API_KEY`, `LLM_MODEL` |
| Gemini | `httpx` | `LLM_API_KEY`, `LLM_MODEL` |

All LLM usage is opt-in, advisory, and grounded in actual dictionary records.

## SSO/SAML Setup (Planned)

Keycloak realm import provided for:
- OIDC authorization code flow with PKCE
- SAML 2.0 identity provider brokering
- Role mapping: `viewer`, `operator`, `admin`

## License

MIT © Alan Vo <alanvo@gmail.com>