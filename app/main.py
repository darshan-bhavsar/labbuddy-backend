from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .config import settings
from .database import engine, Base
from .routers import auth_simple, hospitals, patients, report, tests, requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass


app = FastAPI(
    title=settings.app_name,
    description="Pathology Lab Management System - MVP",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_simple.router, prefix="/api/v1")
app.include_router(requests.router, prefix="/api/v1")
app.include_router(hospitals.router, prefix="/api/v1")
app.include_router(patients.router, prefix="/api/v1")
app.include_router(report.router, prefix="/api/v1")
app.include_router(tests.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "LabBuddy API - Pathology Lab Management System",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "labbuddy-api"}


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )