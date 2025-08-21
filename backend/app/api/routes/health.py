"""
Health check API routes for monitoring system status.
Provides endpoints for checking application health and dependencies.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
import psutil
import platform

from app.core.database import get_db, db_manager
from app.core.config import get_settings
from app.services.email_service import email_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/health")
settings = get_settings()


@router.get("/")
async def health_check():
    """
    Basic health check endpoint.
    
    Returns simple status to verify the API is running.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Event Booking Platform API",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check with dependency status.
    
    Checks database connectivity, email service, and system resources.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Event Booking Platform API",
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production",
        "dependencies": {}
    }
    
    overall_healthy = True
    
    # Check database connectivity
    try:
        db_healthy = db_manager.health_check()
        health_status["dependencies"]["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "details": db_manager.get_table_info() if db_healthy else "Connection failed"
        }
        if not db_healthy:
            overall_healthy = False
    except Exception as e:
        health_status["dependencies"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        overall_healthy = False
    
    # Check email service
    try:
        email_healthy = await email_service.test_connection()
        health_status["dependencies"]["email"] = {
            "status": "healthy" if email_healthy else "unhealthy",
            "smtp_host": settings.SMTP_HOST,
            "smtp_port": settings.SMTP_PORT
        }
        if not email_healthy:
            overall_healthy = False
    except Exception as e:
        health_status["dependencies"]["email"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        overall_healthy = False
    
    # System resources
    try:
        health_status["system"] = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "platform": platform.platform(),
            "python_version": platform.python_version()
        }
    except Exception as e:
        health_status["system"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Set overall status
    health_status["status"] = "healthy" if overall_healthy else "unhealthy"
    
    # Return appropriate HTTP status code
    if not overall_healthy:
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status


@router.get("/database")
def database_health(db: Session = Depends(get_db)):
    """
    Database-specific health check.
    
    Provides detailed information about database connectivity and status.
    """
    try:
        db_healthy = db_manager.health_check()
        
        if not db_healthy:
            raise HTTPException(
                status_code=503,
                detail={
                    "status": "unhealthy",
                    "message": "Database connection failed"
                }
            )
        
        table_info = db_manager.get_table_info()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": table_info,
            "connection_pool": {
                "size": db_manager.engine.pool.size(),
                "checked_in": db_manager.engine.pool.checkedin(),
                "checked_out": db_manager.engine.pool.checkedout()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@router.get("/email")
async def email_health():
    """
    Email service health check.
    
    Tests SMTP connectivity without sending actual emails.
    """
    try:
        email_healthy = await email_service.test_connection()
        
        if not email_healthy:
            raise HTTPException(
                status_code=503,
                detail={
                    "status": "unhealthy",
                    "message": "Email service connection failed"
                }
            )
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "smtp_config": {
                "host": settings.SMTP_HOST,
                "port": settings.SMTP_PORT,
                "use_tls": settings.SMTP_USE_TLS,
                "from_email": settings.SMTP_FROM_EMAIL
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """
    Application metrics endpoint.
    
    Provides basic metrics about the application usage and performance.
    """
    try:
        # Get database metrics
        from app.models.booking import Booking
        from app.models.contact import Contact
        
        total_bookings = db.query(Booking).count()
        total_contacts = db.query(Contact).count()
        
        # Get recent activity (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_bookings = db.query(Booking).filter(
            Booking.created_at >= yesterday
        ).count()
        recent_contacts = db.query(Contact).filter(
            Contact.created_at >= yesterday
        ).count()
        
        # System metrics
        system_metrics = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            }
        }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "application": {
                "total_bookings": total_bookings,
                "total_contacts": total_contacts,
                "recent_bookings_24h": recent_bookings,
                "recent_contacts_24h": recent_contacts
            },
            "system": system_metrics,
            "uptime_seconds": (datetime.utcnow() - datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            )).total_seconds()
        }
        
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")


@router.get("/readiness")
async def readiness_check(db: Session = Depends(get_db)):
    """
    Kubernetes readiness probe endpoint.
    
    Checks if the application is ready to receive traffic.
    """
    try:
        # Check database
        db_healthy = db_manager.health_check()
        
        # Check email service
        email_healthy = await email_service.test_connection()
        
        if not (db_healthy and email_healthy):
            raise HTTPException(
                status_code=503,
                detail={
                    "ready": False,
                    "database": db_healthy,
                    "email": email_healthy
                }
            )
        
        return {
            "ready": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail={"ready": False, "error": str(e)})


@router.get("/liveness")
def liveness_check():
    """
    Kubernetes liveness probe endpoint.
    
    Simple check to verify the application is alive.
    """
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat()
    }