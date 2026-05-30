from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Smart-Sales Analytics API")

@app.get("/")
def home():
    return {
        "status": "Sukses",
        "pesan": "API Terintegrasi dengan Pandas sudah berjalan!"
    }

# Endpoint Baru: Mengolah data CSV langsung lewat API
@app.get("/api/v1/analytics")
def ambil_analisis_penjualan():
    try:
        # 1. Membaca data penjualan.csv menggunakan Pandas
        df = pd.read_csv("penjualan.csv")
        
        # 2. Melakukan kalkulasi total bayar & omzet
        df["total_bayar"] = df["jumlah"] * df["harga"]
        total_omzet = int(df["total_bayar"].sum()) # diubah ke int agar bisa dikirim via JSON
        total_transaksi = len(df)
        
        # 3. Menghitung rata-rata pembelian
        rata_rata_pembelian = float(df["total_bayar"].mean())
        
        # 4. Mengembalikan hasil olahan Pandas dalam bentuk JSON API
        return {
            "status": "Berhasil",
            "data_summary": {
                "total_omzet_idr": total_omzet,
                "total_transaksi_tercatat": total_transaksi,
                "rata_rata_per_transaksi": rata_rata_pembelian
            }
        }
    except Exception as e:
        return {
            "status": "Error",
            "pesan": f"Gagal mengolah data: {str(e)}"
        }