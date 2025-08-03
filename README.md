# Alpha Platform - Deep Research Agent

A full-stack application that demonstrates automated company research using iterative search and structured data extraction. The platform manages campaigns, companies, and people while running deep research agents to gather competitive intelligence.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd alpha-platform
cp backend/.env.example backend/.env
```

### 2. Start All Services
```bash
docker-compose up -d
```

This launches:
- PostgreSQL database (port 5432)
- Redis queue (port 6379) 
- FastAPI backend (port 8000)
- RQ worker process
- React frontend (port 3000)

### 3. Access the Application
- **Web UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Base**: http://localhost:8000/api

### 4. Trigger Research
The app automatically seeds with sample data. Use the Web UI or API to trigger research on any person.

## 📋 Core Features

### Data Model
- **Campaigns** → **Companies** → **People** → **Context Snippets**
- Polymorphic research results linked to companies/people
- Complete audit trail via search logs

### Deep Research Agent
- **Iterative Search**: Up to 3 search iterations per person
- **Field Extraction**: Finds company_value_prop, product_names, pricing_model, key_competitors, company_domain
- **Re-planning Logic**: Generates new queries if required fields missing
- **Pluggable Search**: Mock provider (default) or real SerpAPI

### Real-time Updates
- Job queue processing with RQ
- Progress updates via polling (WebSocket/SSE ready)
- Live status in web interface

## 🔧 How to Use

### Via Web Interface
1. Navigate to http://localhost:3000
2. View the seeded people list
3. Click "Run Research" on any person
4. Watch real-time progress
5. View structured research results

### Via API

#### Get People
```bash
curl http://localhost:8000/api/people
```

#### Trigger Research
```bash
curl -X POST http://localhost:8000/api/enrich/{person_id}
```

#### Check Job Status
```bash
curl http://localhost:8000/api/job/{job_id}
```

#### Get Research Results
```bash
curl http://localhost:8000/api/companies/{company_id}/snippets
```

## ⚙️ Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/alpha_platform

# Search Provider
USE_REAL_SEARCH=false  # Set to 'true' for real search
SERPAPI_KEY=your_key_here  # Required if USE_REAL_SEARCH=true
```

### Switch to Real Search
1. Get a SerpAPI key from https://serpapi.com
2. Set `USE_REAL_SEARCH=true` in `.env`
3. Set `SERPAPI_KEY=your_key` in `.env`
4. Restart the backend: `docker-compose restart backend worker`

## 🧪 Testing

### Run Tests
```bash
cd backend
pip install -r requirements.txt
pytest
```

### Test Coverage
- Unit tests for JSON schema validation
- Unit tests for email → domain parsing  
- Unit tests for agent re-planning edge cases
- Integration test for full enrichment flow

## 📊 API Collection

Import `api_collection.json` into Postman/Insomnia for pre-configured API requests.

**Key Endpoints:**
- `GET /api/people` - List all people
- `POST /api/enrich/{person_id}` - Trigger research
- `GET /api/companies/{company_id}/snippets` - Get research results

## 📈 Architecture

### Backend Stack
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with PostgreSQL
- **RQ** - Redis-based job queue
- **Alembic** - Database migrations

### Frontend Stack  
- **React** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client

### Infrastructure
- **Docker Compose** - Multi-service orchestration
- **PostgreSQL** - Primary database
- **Redis** - Job queue backend

## 🔍 Research Algorithm

1. **Initialize**: Create context snippet with empty research fields
2. **Iterate**: Up to 3 search rounds per person/company
3. **Query Generation**: 
   - Round 1: "{company} overview"
   - Round 2: "{company} pricing" or "competitors" 
   - Round 3: Target specific missing fields
4. **Extract**: Parse search results for required data
5. **Validate**: Check JSON schema before saving
6. **Store**: Save structured results + source URLs

## 🎯 Future Work

### Scaling
- Horizontal worker scaling with Redis Cluster
- Database read replicas for research queries
- CDN for frontend assets

### Authentication
- User authentication and authorization
- Multi-tenant campaign isolation
- API key management

### Enhanced Agents
- Industry-specific research templates
- Social media data integration
- Financial data enrichment
- Technology stack detection

### Real-time Features
- WebSocket connections for instant updates
- Live collaboration on research campaigns
- Real-time dashboard analytics

## 📝 Development Commands

```bash
# Backend development
cd backend
uvicorn app.main:app --reload

# Run worker
python app/worker.py

# Frontend development  
cd frontend
npm run dev

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Testing
pytest
npm test
```

## 🏗️ Project Structure

```
alpha-platform/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── tests/            # Unit & integration tests
│   ├── alembic/          # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API clients
│   │   └── hooks/        # Custom hooks
│   └── package.json
├── docker-compose.yml    # Multi-service setup
├── api_collection.json   # Postman collection
├── ERD.md               # Database diagram
└── README.md
```

---

**Note**: This implementation prioritizes functionality and demonstrating the full vertical slice. Production deployments would require additional security, monitoring, and scalability considerations.