from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Lokasi file database SQLite
DATABASE_URL = "sqlite:///./toko.db"

# Engine penghubung ke database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Sesi untuk operasi database (Insert, Select, Update, Delete)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk mendefinisikan model / tabel database
Base = declarative_base()


def get_db():
    """Dependency untuk mendapatkan sesi database di setiap request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
