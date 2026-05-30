from sqlalchemy import Column, Integer, String
from database import Base

# Membuat struktur tabel bernama 'transaksi'
class TransaksiModel(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    produk = Column(String, index=True)
    kategori = Column(String)
    jumlah = Column(Integer)
    harga = Column(Integer)
    tanggal = Column(String)