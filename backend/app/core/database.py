"""
Database configuration and session management.
Handles SQLAlchemy setup, connection pooling, and session lifecycle.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import asyncio

from app.core.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Database URL and engine configuration
DATABASE_URL = settings.DATABASE_URL

# Engine configuration based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30
        },
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # PostgreSQL/MySQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG
    )

# Session configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


async def create_tables() -> None:
    """
    Create all database tables.
    Safe to call multiple times.
    """
    try:
        # Import all models to ensure they're registered
        from app.models import booking, contact
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


async def drop_tables() -> None:
    """
    Drop all database tables.
    Use with caution - only for testing/development.
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
        
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def reset_database() -> None:
    """
    Reset database by dropping and recreating all tables.
    Use only in development/testing.
    """
    if not settings.DEBUG:
        raise RuntimeError("Database reset is only allowed in debug mode")
    
    try:
        asyncio.run(drop_tables())
        asyncio.run(create_tables())
        logger.info("Database reset completed")
        
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise


class DatabaseManager:
    """
    Database management utility class.
    Provides high-level database operations.
    """
    
    def __init__(self):
        self.engine = engine
        self.session = SessionLocal
    
    def health_check(self) -> bool:
        """
        Check database connectivity.
        
        Returns:
            bool: True if database is accessible
        """
        try:
            with self.session() as session:
                session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def get_table_info(self) -> dict:
        """
        Get information about database tables.
        
        Returns:
            dict: Table information
        """
        try:
            inspector = engine.dialect.get_table_names(engine.connect())
            return {
                "tables": inspector,
                "engine": str(engine.url),
                "driver": engine.dialect.name
            }
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            return {}
    
    def backup_database(self, backup_path: str) -> bool:
        """
        Create database backup (SQLite only).
        
        Args:
            backup_path: Path for backup file
            
        Returns:
            bool: True if backup successful
        """
        if not DATABASE_URL.startswith("sqlite"):
            logger.warning("Backup only supported for SQLite databases")
            return False
        
        try:
            import shutil
            import os
            
            # Extract database file path from URL
            db_path = DATABASE_URL.replace("sqlite:///", "")
            
            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_path)
                logger.info(f"Database backed up to {backup_path}")
                return True
            else:
                logger.error(f"Database file not found: {db_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()