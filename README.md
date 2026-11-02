# Katalog Service - Toko Online Mikroservis

Layanan katalog untuk tugas kelompok toko online mikroservis. Menangani kategori,
produk, stok, dan reservasi stok yang dipakai saat checkout.

Ini bagian tahap 1 dari 5. Layanan pelanggan, order, pembayaran, dan API gateway
dikerjakan peserta lain di tahap berikutnya; paket `common/` di sini jadi fondasi
yang dipakai layanan-layanan tersebut.

## Fitur

- Kategori: daftar untuk publik, tambah/ubah/hapus khusus admin.
- Produk: daftar dengan filter `kategori`, `q`, `aktif`, `halaman`, `batas`; detail
  memuat stok tersedia; CRUD khusus admin.
- Stok: penambahan atau pengurangan lewat endpoint admin, ditolak bila hasilnya negatif.
- Reservasi stok: reserve saat checkout, komit saat pembayaran berhasil, rilis saat
  gagal atau kedaluwarsa. Ketiganya atomik dan idempoten.
- Amplop respons seragam `{success, data, error, request_id}` plus header `X-Request-Id`.

## Menjalankan

```bash
python -m venv .venv
. .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r katalog-service/requirements.txt
python scripts/dev_up.py        # http://127.0.0.1:8001
```

Isi data contoh (kategori + produk):

```bash
python seed/seed_data.py
```

Dengan Docker:

```bash
docker compose up --build -d
docker compose ps
docker compose down
```

## Endpoint

| Metode | Path | Akses | Keterangan |
|---|---|---|---|
| GET | `/health` | publik | status layanan |
| GET | `/kategori` | publik | daftar kategori |
| POST | `/kategori` | admin | buat kategori |
| PUT | `/kategori/<id>` | admin | ubah kategori |
| DELETE | `/kategori/<id>` | admin | hapus kategori |
| GET | `/produk` | publik | filter `kategori`, `q`, `aktif`, `halaman`, `batas` |
| GET | `/produk/<id>` | publik | detail + stok tersedia |
| POST | `/produk` | admin | buat produk |
| PUT | `/produk/<id>` | admin | ubah produk |
| DELETE | `/produk/<id>` | admin | nonaktifkan produk |
| POST | `/produk/<id>/stok` | admin | tambah/kurangi stok |
| POST | `/internal/reservasi` | layanan | reserve stok (`order_ref`, `items[]`, `ttl_detik`) |
| GET | `/internal/reservasi/<id>` | layanan | detail reservasi |
| POST | `/internal/reservasi/<id>/komit` | layanan | stok keluar permanen |
| POST | `/internal/reservasi/<id>/rilis` | layanan | kembalikan stok |
| POST | `/internal/reservasi/bersihkan` | layanan | rilis reservasi kedaluwarsa |

Autentikasi admin memakai `Authorization: Bearer <JWT HS256>`; endpoint antar layanan
memakai header `X-Service-Token`.

## Pengujian

```bash
python tests/run_tests.py                # layanan dinyalakan, 8 tes, lalu dimatikan
python tests/run_tests.py -v             # verbose
python tests/run_tests.py --tanpa-boot   # bila layanan sudah jalan
```

## Struktur

```text
common/            config, SQLite, JWT, keamanan, klien HTTP, pabrik aplikasi
katalog-service/   app.py, schema.sql, Dockerfile, requirements.txt
scripts/dev_up.py  jalankan layanan lokal
seed/              data contoh + skrip pengisian
tests/             base.py, run_tests.py, test_katalog.py
docs/              API, distribusi tugas, hasil verifikasi
```

## Catatan

- Reservasi menyimpan `stok_reserved` terpisah dari `stok` sehingga barang yang sedang
  ditahan tidak ikut terjual. TTL-nya diatur `RESERVASI_TTL_DETIK` (bawaan 900 detik)
  dan reservasi kedaluwarsa dirilis lewat `/internal/reservasi/bersihkan`.
- Semua konfigurasi dibaca dari environment variable; contohnya ada di `.env.example`.
