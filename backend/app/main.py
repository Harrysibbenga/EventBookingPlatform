"""
FastAPI application entry point for Event Booking Platform.
Handles application initialization, middleware setup, and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.api.routes import bookings, contact, health
from app.core.config import get_settings
from app.core.database import create_tables
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Event Booking Platform API")
    await create_tables()
    logger.info("Database tables created/verified")
    yield
    # Shutdown
    logger.info("Shutting down Event Booking Platform API")


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="Event Booking Platform API",
        description="A comprehensive API for event booking and management",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add middleware
    setup_middleware(app)
    
    # Include routers
    setup_routes(app)
    
    return app


def setup_middleware(app: FastAPI) -> None:
    """Configure application middleware."""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware (security)
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS
        )


def setup_routes(app: FastAPI) -> None:
    """Configure application routes."""
    
    # API routes
    app.include_router(
        health.router,
        prefix=settings.API_PREFIX,
        tags=["Health"]
    )
    
    app.include_router(
        bookings.router,
        prefix=settings.API_PREFIX,
        tags=["Bookings"]
    )
    
    app.include_router(
        contact.router,
        prefix=settings.API_PREFIX,
        tags=["Contact"]
    )


# Create application instance
app = create_application()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Event Booking Platform API",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "health": f"{settings.API_PREFIX}/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )