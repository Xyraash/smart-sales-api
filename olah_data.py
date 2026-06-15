"""
Utility: Olah data CSV penjualan dan simpan ke file laporan bersih.

Cara pakai:
    python olah_data.py
    python olah_data.py --input data_lain.csv --output laporan_output.csv
"""

import argparse
import os
import pandas as pd


def baca_dan_validasi(path_csv: str) -> pd.DataFrame:
    """Baca file CSV dan validasi kolom yang dibutuhkan."""
    if not os.path.exists(path_csv):
        raise FileNotFoundError(f"File tidak ditemukan: {path_csv}")

    df = pd.read_csv(path_csv)

    kolom_wajib = {"produk", "kategori", "jumlah", "harga"}
    kolom_hilang = kolom_wajib - set(df.columns)
    if kolom_hilang:
        raise ValueError(f"Kolom berikut tidak ditemukan di CSV: {kolom_hilang}")

    return df


def olah(df: pd.DataFrame) -> dict:
    """Hitung metrik analitik dari DataFrame transaksi."""
    df = df.copy()
    df["total_bayar"] = df["jumlah"] * df["harga"]

    total_omzet = df["total_bayar"].sum()
    total_transaksi = len(df)
    rata_rata = df["total_bayar"].mean()

    per_kategori = (
        df.groupby("kategori")["total_bayar"]
        .sum()
        .sort_values(ascending=False)
    )

    produk_terlaris = (
        df.groupby("produk")["jumlah"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    return {
        "df": df,
        "total_omzet": total_omzet,
        "total_transaksi": total_transaksi,
        "rata_rata": rata_rata,
        "per_kategori": per_kategori,
        "produk_terlaris": produk_terlaris,
    }


def tampilkan_ringkasan(hasil: dict):
    """Cetak ringkasan analitik ke terminal."""
    print("\n========== RINGKASAN PENJUALAN ==========")
    print(f"Total Transaksi   : {hasil['total_transaksi']}")
    print(f"Total Omzet       : Rp {hasil['total_omzet']:,.0f}")
    print(f"Rata-rata Transaksi: Rp {hasil['rata_rata']:,.0f}")

    print("\n--- Omzet per Kategori ---")
    print(hasil["per_kategori"].to_string())

    print("\n--- Top 5 Produk Terlaris (berdasarkan jumlah terjual) ---")
    print(hasil["produk_terlaris"].to_string())
    print("==========================================\n")


def main():
    parser = argparse.ArgumentParser(description="Olah data penjualan dari CSV")
    parser.add_argument("--input", default="penjualan.csv", help="Path file CSV input")
    parser.add_argument("--output", default="laporan_penjualan_clean.csv", help="Path file CSV output")
    args = parser.parse_args()

    print(f"[INFO] Membaca file: {args.input}")
    df = baca_dan_validasi(args.input)

    print("[INFO] Mengolah data...")
    hasil = olah(df)

    tampilkan_ringkasan(hasil)

    hasil["df"].to_csv(args.output, index=False)
    print(f"[Sukses] Laporan bersih disimpan ke: {args.output}")


if __name__ == "__main__":
    main()