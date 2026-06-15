from sqlalchemy import Column, Integer, String, Date
from database import Base


class TransaksiModel(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    produk = Column(String, nullable=False, index=True)
    kategori = Column(String, nullable=False)
    jumlah = Column(Integer, nullable=False)
    harga = Column(Integer, nullable=False)
    tanggal = Column(Date, nullable=False)  # Tipe Date (bukan String)
