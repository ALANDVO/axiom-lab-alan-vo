# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

dictionary-coverage-checker

## Roadmap

### dictionary-coverage-checker — Dictionary Coverage Checker

Status: done

Acceptance:
- Public page at /dictionary accepts skill/role/industry term input
- Returns canonical hit, alias hit, or miss with correct classification
- Misses recorded in deduplicated table with request count and timestamps
- Backend API: POST /api/dictionary/lookup, GET /api/dictionary/misses
- Frontend: search input, result display with three-state classification, submit-to-list on miss
- Tests: backend lookup logic, miss recording, frontend search flow

Implementation: `backend/app/api/dictionary.py`, `backend/app/services/dictionary.py`, `backend/app/models/dictionary.py`, `frontend/src/components/DictionarySearch.tsx`, `frontend/src/components/MissList.tsx`, `frontend/src/pages/DictionaryPage.tsx`, `frontend/src/hooks/useDictionaryLookup.ts`, `frontend/src/hooks/useMisses.ts`, `frontend/src/api/client.ts`, `frontend/src/types/api.ts`

Tests: `backend/tests/test_dictionary.py`, `frontend/src/components/DictionarySearch.test.tsx`, `frontend/src/components/MissList.test.tsx`

### candidate-profile-redesign — Candidate Profile Redesign

Status: planned

Acceptance:
- Single-page profile replacing 8-tab structure
- Unified autosave editing pattern across sections
- Profile completeness indicator visible at glance
- Sections: Profile, Contacts, Location, Skills, Experience, Education, Screening, Settings

### anonymous-tracking-aggregation — Anonymous Application Tracking Aggregation

Status: planned

Acceptance:
- Opt-in per-job sharing of anonymized application process data
- K-anonymity floor (N≥5) before showing aggregates
- Aggregate display: tracker count, stage timing buckets, outcome distribution
- Backend aggregation API, frontend job posting integration

### job-board-source-management — Job Board Source Management

Status: planned

Acceptance:
- YAML-based source catalog for ATS providers
- CLI/API to validate board liveness before adding
- Provider adapter pattern for extensibility

