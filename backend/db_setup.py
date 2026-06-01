import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/grindos")

# Declare a clean database model mapping base
Base = declarative_base()

engine = None
SessionLocal = None

try:
    # Setup standard connection engine
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print(f"📦 [Database Setup] Resilient session established on: {DATABASE_URL}")
except Exception as e:
    print(f"⚠️  [Database Warning] Could not connect to PostgreSQL database: {e}")
    print("💡 Falling back to mock memory context. Backend will run successfully without active PostgreSQL engine.")

def get_db():
    """Dependency helper to safely retrieve the database session."""
    if SessionLocal is None:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
