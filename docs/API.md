# Ringkasan API - Katalog Service

Base URL lokal `http://127.0.0.1:8001`. Semua respons memakai amplop:

```json
{ "success": true, "data": { }, "meta": { }, "request_id": "..." }
{ "success": false, "error": { "kode": "VALIDASI_GAGAL", "pesan": "..." }, "request_id": "..." }
```

| Metode | Path | Akses | Keterangan |
|---|---|---|---|
| GET | `/health` | publik | status layanan |
| GET | `/kategori` | publik | daftar kategori |
| POST | `/kategori` | admin | `{ "nama": "...", "deskripsi": "..." }` |
| PUT | `/kategori/<id>` | admin | ubah nama/deskripsi |
| DELETE | `/kategori/<id>` | admin | tolak bila masih dipakai produk |
| GET | `/produk` | publik | filter `kategori`, `q`, `aktif`, `halaman`, `batas` |
| GET | `/produk/<id>` | publik | detail + `stok_tersedia` |
| POST | `/produk` | admin | `sku`, `nama`, `harga`, `stok`, `kategori_id` |
| PUT | `/produk/<id>` | admin | ubah data produk |
| DELETE | `/produk/<id>` | admin | nonaktifkan produk |
| POST | `/produk/<id>/stok` | admin | `{ "tambah": 10 }` atau `{ "tambah": -3 }` |
| POST | `/internal/reservasi` | layanan | `order_ref`, `items[]`, `ttl_detik` |
| GET | `/internal/reservasi/<id>` | layanan | detail reservasi |
| POST | `/internal/reservasi/<id>/komit` | layanan | stok keluar permanen |
| POST | `/internal/reservasi/<id>/rilis` | layanan | kembalikan stok (idempoten) |
| POST | `/internal/reservasi/bersihkan` | layanan | rilis reservasi yang kedaluwarsa |

Contoh:

```bash
curl "http://127.0.0.1:8001/produk?batas=5"

curl -X POST http://127.0.0.1:8001/kategori \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"nama":"Kopi","deskripsi":"Biji kopi dan kopi bubuk"}'

curl -X POST http://127.0.0.1:8001/internal/reservasi \
  -H "X-Service-Token: $SERVICE_TOKEN" -H "Content-Type: application/json" \
  -d '{"order_ref":"ORD-1","items":[{"produk_id":1,"qty":2}],"ttl_detik":900}'
```
