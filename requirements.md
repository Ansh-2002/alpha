# Alpha Platform — Full-Stack Engineer Project

## Overview
This document outlines the requirements for building a "vertical slice" of the Alpha Platform that demonstrates your ability to:

1. Model and implement a data structure for Campaigns, Companies, and People with context snippets from agent runs
2. Implement a Deep Research Agent that—given a person’s name & email—does iterative Google-style searches, extracts structured insights, and writes them back to the DB
3. Develop dual interfaces (API/CLI and web UI) for running and monitoring the agent


## Core Requirements

### Data Model
The application should implement the following data structure:

#### Campaigns
```sql
CREATE TABLE campaigns (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### Companies
```sql
CREATE TABLE companies (
  id UUID PRIMARY KEY,
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  name TEXT,
  domain TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### People
```sql
CREATE TABLE people (
  id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  full_name TEXT,
  email TEXT UNIQUE,
  title TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### Context Snippets
```sql
CREATE TABLE context_snippets (
  id UUID PRIMARY KEY,
  entity_type TEXT CHECK (entity_type IN ('company','person')),
  entity_id UUID NOT NULL,
  snippet_type TEXT DEFAULT 'research',
  payload JSONB NOT NULL, -- agent's formatted JSON
  source_urls JSONB NOT NULL, -- array of strings
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### Search Logs
```sql
CREATE TABLE search_logs (
  id UUID PRIMARY KEY,
  context_snippet_id UUID REFERENCES context_snippets(id) ON DELETE CASCADE,
  iteration INT,
  query TEXT,
  top_results JSONB, -- urls + snippets
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### End-to-End Flow

| Step | Description | Requirements |
|------|-------------|-------------|
| A. Seed Data | On first boot, the app seeds 1 Campaign → 1 Company → 2 People | Use migration or seed script |
| B. Trigger Agent | User clicks "Run Research" in UI or hits POST `/enrich/{person_id}` | Accept Person ID; enqueue job |
| C. Agent Loop | Agent performs up to 3 search iterations until it finds all required fields | Use a real search API or a clearly pluggable mock; record every query & top 3 result links |
| D. Persist Results | Final JSON saved in `context_snippets`; raw searches in `search_logs` | Must link back to `company_id` (and optionally `person_id`) |
| E. Stream Progress | Frontend receives status via WebSocket or SSE and updates a progress bar / log console | Fallback to long-polling only if necessary (with explanation) |
| F. Display | After completion, UI shows the structured insight JSON and human-readable card under the Company | Data must be pulled from DB, not agent memory |

#### Required Fields for Agent to Find
- company_value_prop
- product_names
- pricing_model
- key_competitors
- company_domain

## Technical Requirements

### Backend & Infrastructure
- **Language:** Python
- **Framework:** FastAPI
- **Async job queue:** RQ
- **Deployment:** Docker Compose to spin up DB, queue, and app with one command
- **API Documentation:** OpenAPI/Swagger auto-generated and committed

### Deep Research Agent
- Modular class/function design that can be swapped to real SerpAPI with one environment variable
- Re-planning logic: if any required field is missing → new query crafted (basic heuristics acceptable)
- All extracted text must be cleaned & deduplicated
- Final payload must be validated against a JSON Schema before persisting

### Frontend
- Lightweight stack (React + Vite)
- Implementation flow: People List → Research Button → Progress → Results Card
- Real-time updates via WebSocket/SSE; fallback to polling every 3 seconds only if WebSocket is unsupported
- Simple styling with CSS or Tailwind (no complex styling libraries required)

### Testing
- **Unit tests:**
  - JSON schema validator
  - Parsing email → domain
  - Agent re-planning edge case (no competitors found)
- **Integration test:** Spin up a test DB, seed a Person, hit `/enrich`, wait, assert snippet saved

### Observability
- Console logs with person_id, iteration, and query string
- Optional: `/healthz` endpoint & basic Prometheus metrics

## Deliverables

| Item | Requirements |
|------|-------------|
| Repository | Public or private link with readable commit history (approximately 5-15 commits) |
| ERD Diagram | PNG or Markdown Mermaid format, checked into repository root |
| README | ≤1,000 words covering: quick-start instructions, how to trigger enrichment via API & UI, how to swap between mock & real search, and future work notes (scaling, auth, other agents) |
| API Collection | Postman/Insomnia Collection with at least GET `/people`, POST `/enrich/{id}`, GET `/snippets/{company_id}` |
| Tests | All tests passing; coverage badge optional |