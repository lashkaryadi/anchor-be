from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import Base, engine, SessionLocal
from app.seed import seed_all
from app.routers import dashboard, employees, teams, interventions, analytics, careers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()
    yield
    # Shutdown: nothing to clean up


settings = get_settings()

app = FastAPI(
    title="Anchor API",
    description="Predictive Flight Risk Platform for Employee Retention",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(employees.router)
app.include_router(teams.router)
app.include_router(interventions.router)
app.include_router(analytics.router)
app.include_router(careers.router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "Anchor API"}
