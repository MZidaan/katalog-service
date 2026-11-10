<<<<<<< HEAD

# Hasil Verifikasi Tiap Arsip

Setiap arsip zip di `releases/` diuji ulang setelah diekstrak ke folder bersih
(`python tests/run_tests.py`, layanan dinyalakan otomatis dan dimatikan kembali).

| Arsip | Isi yang diuji | Jumlah tes | Hasil |
|---|---|---|---|
| `v1-katalog-service.zip` | katalog: CRUD, reserve, komit, rilis, validasi stok | 8 | lulus semua |
| `v2-pelanggan-service.zip` | katalog + pelanggan: JWT, alamat, verifikasi token | 16 | lulus semua |
| `v3-order-service.zip` | + order: keranjang, checkout saga, kompensasi | 24 | lulus semua |
| `v4-pembayaran-service.zip` | + pembayaran: tagihan, simulasi, webhook, laporan | 30 | lulus semua |
| `v5-integrasi-dan-dashboard.zip` | + gateway, dashboard, e2e lewat satu pintu | 39 | lulus semua |

Rinciannya:

```text
v1  Ran  8 tests   OK      (katalog)
v2  Ran 16 tests   OK      (katalog, pelanggan)
v3  Ran 24 tests   OK      (katalog, pelanggan, order)
v4  Ran 30 tests   OK      (katalog, pelanggan, order, pembayaran)
v5  Ran 39 tests   OK      (semua + gateway/e2e)
```

## Bukti alur yang diverifikasi

1. **Reserve stok atomik** — `stok_reserved` naik, `stok` tetap; komit memindahkan
   `stok_reserved` menjadi pengurangan `stok` permanen; rilis mengembalikan keduanya
   dan idempoten.
2. **Kompensasi saga** — checkout dengan hook `simulasi: gagal_pembayaran` menghasilkan
   `502` dengan `detail.kompensasi` berisi `simpan_pesanan` dan `reservasi_stok`;
   `stok_reserved` kembali `0`.
3. **Webhook pembayaran** — simulasi `berhasil` membuat pesanan `DIBAYAR` dan stok
   berkurang permanen; simulasi `gagal` membuat pesanan `DIBATALKAN` dan stok kembali.
4. **Idempotensi tagihan** — dua permintaan inisiasi untuk pesanan yang sama
   mengembalikan `id` yang sama dengan `idempoten: true`.
5. **Proteksi gateway** — endpoint `order`/`pembayaran` tanpa token `401`,
   `/api/*/internal/*` `404`, ringkasan admin untuk peran pelanggan `403`.
6. **Laporan** — ringkasan agregat per status/metode/hari dan ekspor CSV (`;`, BOM UTF-8).

## Reproduksi

```bash
# satu arsip
unzip releases/v3-order-service.zip -d /tmp/uji && cd /tmp/uji/tugas-kelompok
pip install -r katalog-service/requirements.txt
python tests/run_tests.py
```

Lingkungan verifikasi: Python 3.13, Flask 3.1.3, requests 2.34.2, Windows 11,
tanpa Docker (Docker Compose disertakan tetapi tidak dijalankan di lingkungan ini).
=======
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
>>>>>>> 04eda1bd6649056beef7d88be3add86732a7ea72
