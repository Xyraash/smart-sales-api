from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Menentukan lokasi database file (Akan otomatis membuat file bernama 'toko.db')
DATABASE_URL = "sqlite:///./toko.db"

# 2. Membuat engine penghubung ke database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Membuat sesi untuk transaksi data (Insert, Select, Update, Delete)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class untuk mendefinisiksan tabel database (Model)
Base = declarative_base()

# Fungsi bantuan untuk mendapatkan sesi database di FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()