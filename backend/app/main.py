from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import campaigns, companies, people, enrichment
from app.database import engine
from app.models import Base

app = FastAPI(
    title="Alpha Platform API",
    description="Deep Research Agent Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Alpha Platform API"}

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(people.router, prefix="/api/people", tags=["people"])
app.include_router(enrichment.router, prefix="/api", tags=["enrichment"])