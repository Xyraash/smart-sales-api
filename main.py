from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import models
from database import engine, get_db

# Membuat tabel otomatis di database SQLite saat aplikasi menyala
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart-Sales Analytics API + Database")

@app.get("/")
def home():
    return {"pesan": "API dengan Database SQLite & Pandas siap digunakan!"}

# --- ENDPOINT 1: INPUT DATA BARU KE DATABASE ---
@app.post("/api/v1/transaksi")
def tambah_transaksi(produk: str, kategori: str, jumlah: int, harga: int, tanggal: str, db: Session = Depends(get_db)):
    # 1. Bungkus data inputan menjadi objek model database
    data_baru = models.TransaksiModel(
        produk=produk, kategori=kategori, jumlah=jumlah, harga=harga, tanggal=tanggal
    )
    # 2. Simpan ke database SQLite
    db.add(data_baru)
    db.commit()
    db.refresh(data_baru)
    return {"status": "Sukses", "pesan": f"Transaksi {produk} berhasil disimpan ke database!"}

# --- ENDPOINT 2: ANALISIS DATA LANGSUNG DARI DATABASE ---
@app.get("/api/v1/analytics")
def ambil_analisis_dari_db(db: Session = Depends(get_db)):
    # 1. Ambil seluruh data dari database SQLite
    semua_data = db.query(models.TransaksiModel).all()
    
    if not semua_data:
        return {"status": "Kosong", "pesan": "Belum ada data di database. Isi data dulu lewat POST!"}

    # 2. Ubah data database menjadi List of Dictionary agar bisa dibaca Pandas
    data_list = []
    for item in semua_data:
        data_list.append({
            "jumlah": item.jumlah,
            "harga": item.harga
        })

    # 3. Masukkan ke Pandas DataFrame untuk dihitung otomatis
    df = pd.DataFrame(data_list)
    df["total_bayar"] = df["jumlah"] * df["harga"]
    
    total_omzet = int(df["total_bayar"].sum())
    total_transaksi = len(df)

    return {
        "sumber_data": "Database SQLite Real-time",
        "data_summary": {
            "total_omzet_idr": total_omzet,
            "total_transaksi_tercatat": total_transaksi
        }
    }