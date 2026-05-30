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
        # --- ENDPOINT 3: UPDATE (MENGUBAH DATA TRANSAKSI BERDASARKAN ID) ---
@app.put("/api/v1/transaksi/{transaksi_id}")
def update_transaksi(transaksi_id: int, produk: str, kategori: str, jumlah: int, harga: int, tanggal: str, db: Session = Depends(get_db)):
    # 1. Cari data di database yang ID-nya cocok
    transaksi = db.query(models.TransaksiModel).filter(models.TransaksiModel.id == transaksi_id).first()
    
    # 2. Jika ID tidak ditemukan, keluarkan pesan error 404
    if not transaksi:
        raise HTTPException(status_code=404, detail="Data transaksi tidak ditemukan!")
    
    # 3. Timpa data lama dengan data baru yang diinput user
    transaksi.produk = produk
    transaksi.kategori = kategori
    transaksi.jumlah = jumlah
    transaksi.harga = harga
    transaksi.tanggal = tanggal
    
    # 4. Simpan perubahan ke database
    db.commit()
    db.refresh(transaksi)
    
    return {"status": "Sukses", "pesan": f"Transaksi ID {transaksi_id} berhasil diperbarui!"}


# --- ENDPOINT 4: DELETE (MENGHAPUS DATA TRANSAKSI BERDASARKAN ID) ---
@app.delete("/api/v1/transaksi/{transaksi_id}")
def hapus_transaksi(transaksi_id: int, db: Session = Depends(get_db)):
    # 1. Cari data di database yang ID-nya cocok
    transaksi = db.query(models.TransaksiModel).filter(models.TransaksiModel.id == transaksi_id).first()
    
    # 2. Jika ID tidak ditemukan, keluarkan pesan error 404
    if not transaksi:
        raise HTTPException(status_code=404, detail="Data transaksi tidak ditemukan!")
    
    # 3. Hapus data tersebut dari database
    db.delete(transaksi)
    db.commit()
    
    return {"status": "Sukses", "pesan": f"Transaksi ID {transaksi_id} resmi dihapus dari database!"}

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