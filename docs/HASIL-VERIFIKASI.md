# Hasil Verifikasi

Diuji dengan `python tests/run_tests.py`: layanan dinyalakan memakai `DATA_DIR`
sementara, seluruh tes dijalankan, lalu prosesnya dimatikan lagi.

| Cakupan | Jumlah tes | Hasil |
|---|---|---|
| katalog: CRUD kategori/produk, hak akses, reserve, komit, rilis | 8 | lulus semua |

```text
Ran 8 tests
OK
```

## Yang diperiksa

1. **Reserve stok** - `stok_reserved` naik, `stok` tidak berubah.
2. **Komit** - `stok_reserved` turun dan `stok` berkurang permanen.
3. **Rilis** - stok kembali seperti sebelum reservasi, termasuk saat dipanggil dua kali.
4. **Validasi jumlah** - permintaan melebihi stok tersedia ditolak.
5. **Hak akses** - endpoint tulis menolak permintaan tanpa token admin.

Lingkungan pengujian: Python 3.13, Flask 3.1.3, requests 2.34.2, Windows 11.
