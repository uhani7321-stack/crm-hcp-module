from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Default to Postgres, but allow sqlite fallback for easier local testing if postgres is not running
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://crm_user:crm_password@localhost/crm_db")

try:
    engine = create_engine(DATABASE_URL)
    engine.connect()
except Exception as e:
    # Fallback to SQLite
    print(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")
    DATABASE_URL = "sqlite:///./crm.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
