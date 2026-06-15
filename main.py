from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from datetime import date
import pandas as pd
import models
from database import engine, get_db

# Membuat tabel otomatis di database SQLite saat aplikasi menyala
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart-Sales Analytics API + Database")


# --- SCHEMA INPUT (Pydantic) untuk validasi data ---
class TransaksiSchema(BaseModel):
    produk: str
    kategori: str
    jumlah: int
    harga: int
    tanggal: date  # Format: YYYY-MM-DD

    @field_validator("produk", "kategori")
    @classmethod
    def tidak_boleh_kosong(cls, v):
        if not v or not v.strip():
            raise ValueError("Tidak boleh kosong")
        return v.strip()

    @field_validator("jumlah")
    @classmethod
    def jumlah_harus_positif(cls, v):
        if v <= 0:
            raise ValueError("Jumlah harus lebih dari 0")
        return v

    @field_validator("harga")
    @classmethod
    def harga_harus_positif(cls, v):
        if v <= 0:
            raise ValueError("Harga harus lebih dari 0")
        return v


# --- ROOT ---
@app.get("/")
def home():
    return {"pesan": "Smart-Sales API siap digunakan!"}


# --- ENDPOINT 1: GET SEMUA TRANSAKSI ---
@app.get("/api/v1/transaksi")
def get_semua_transaksi(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    data = db.query(models.TransaksiModel).offset(skip).limit(limit).all()
    return {
        "status": "Sukses",
        "total": len(data),
        "data": [
            {
                "id": t.id,
                "produk": t.produk,
                "kategori": t.kategori,
                "jumlah": t.jumlah,
                "harga": t.harga,
                "tanggal": str(t.tanggal),
            }
            for t in data
        ],
    }


# --- ENDPOINT 2: GET SATU TRANSAKSI BERDASARKAN ID ---
@app.get("/api/v1/transaksi/{transaksi_id}")
def get_transaksi(transaksi_id: int, db: Session = Depends(get_db)):
    transaksi = db.query(models.TransaksiModel).filter(
        models.TransaksiModel.id == transaksi_id
    ).first()

    if not transaksi:
        raise HTTPException(status_code=404, detail="Data transaksi tidak ditemukan!")

    return {
        "id": transaksi.id,
        "produk": transaksi.produk,
        "kategori": transaksi.kategori,
        "jumlah": transaksi.jumlah,
        "harga": transaksi.harga,
        "tanggal": str(transaksi.tanggal),
    }


# --- ENDPOINT 3: INPUT DATA BARU KE DATABASE ---
@app.post("/api/v1/transaksi", status_code=201)
def tambah_transaksi(body: TransaksiSchema, db: Session = Depends(get_db)):
    data_baru = models.TransaksiModel(
        produk=body.produk,
        kategori=body.kategori,
        jumlah=body.jumlah,
        harga=body.harga,
        tanggal=body.tanggal,
    )
    db.add(data_baru)
    try:
        db.commit()
        db.refresh(data_baru)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Gagal menyimpan data ke database.")

    return {"status": "Sukses", "pesan": f"Transaksi '{body.produk}' berhasil disimpan!", "id": data_baru.id}


# --- ENDPOINT 4: UPDATE DATA TRANSAKSI BERDASARKAN ID ---
@app.put("/api/v1/transaksi/{transaksi_id}")
def update_transaksi(transaksi_id: int, body: TransaksiSchema, db: Session = Depends(get_db)):
    transaksi = db.query(models.TransaksiModel).filter(
        models.TransaksiModel.id == transaksi_id
    ).first()

    if not transaksi:
        raise HTTPException(status_code=404, detail="Data transaksi tidak ditemukan!")

    transaksi.produk = body.produk
    transaksi.kategori = body.kategori
    transaksi.jumlah = body.jumlah
    transaksi.harga = body.harga
    transaksi.tanggal = body.tanggal

    try:
        db.commit()
        db.refresh(transaksi)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Gagal memperbarui data.")

    return {"status": "Sukses", "pesan": f"Transaksi ID {transaksi_id} berhasil diperbarui!"}


# --- ENDPOINT 5: DELETE DATA TRANSAKSI BERDASARKAN ID ---
@app.delete("/api/v1/transaksi/{transaksi_id}")
def hapus_transaksi(transaksi_id: int, db: Session = Depends(get_db)):
    transaksi = db.query(models.TransaksiModel).filter(
        models.TransaksiModel.id == transaksi_id
    ).first()

    if not transaksi:
        raise HTTPException(status_code=404, detail="Data transaksi tidak ditemukan!")

    try:
        db.delete(transaksi)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Gagal menghapus data.")

    return {"status": "Sukses", "pesan": f"Transaksi ID {transaksi_id} berhasil dihapus!"}


# --- ENDPOINT 6: ANALITIK DARI DATABASE ---
@app.get("/api/v1/analytics")
def ambil_analisis(db: Session = Depends(get_db)):
    semua_data = db.query(models.TransaksiModel).all()

    if not semua_data:
        return {"status": "Kosong", "pesan": "Belum ada data di database. Isi data dulu lewat POST!"}

    # Ubah ke Pandas DataFrame
    data_list = [
        {"produk": t.produk, "kategori": t.kategori, "jumlah": t.jumlah, "harga": t.harga}
        for t in semua_data
    ]
    df = pd.DataFrame(data_list)
    df["total_bayar"] = df["jumlah"] * df["harga"]

    total_omzet = int(df["total_bayar"].sum())
    total_transaksi = len(df)
    rata_rata_transaksi = int(df["total_bayar"].mean())

    # Omzet per kategori
    per_kategori = (
        df.groupby("kategori")["total_bayar"]
        .sum()
        .sort_values(ascending=False)
        .astype(int)
        .to_dict()
    )

    # Produk terlaris (berdasarkan jumlah terjual)
    produk_terlaris = (
        df.groupby("produk")["jumlah"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .astype(int)
        .to_dict()
    )

    return {
        "sumber_data": "Database SQLite Real-time",
        "ringkasan": {
            "total_omzet_idr": total_omzet,
            "total_transaksi": total_transaksi,
            "rata_rata_nilai_transaksi_idr": rata_rata_transaksi,
        },
        "omzet_per_kategori": per_kategori,
        "produk_terlaris_top5": produk_terlaris,
    }
