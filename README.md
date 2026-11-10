<<<<<<< HEAD
# Toko Online Mikroservis — Tugas Kelompok

Repositori tugas kelompok berisi **5 arsip zip bertahap**. Setiap arsip adalah versi
sebelumnya ditambah bagian milik peserta berikutnya, sehingga riwayat pekerjaan terlihat
jelas (v1 → v5). Arsip berada di folder `releases/`.

> **Versi ini: tahap 3 dari 5** — Order Service + saga kompensasi.

## Matriks tahap

| Arsip | Isi utama | Pemilik | Status |
|---|---|---|---|
| v1 | Katalog Service | Peserta 1 | ✅ ada |
| v2 | Pelanggan Service | Peserta 2 | ✅ ada |
| v3 | Order Service + saga kompensasi | Peserta 3 | ✅ ada |
| v4 | Pembayaran Service | Peserta 4 | ⬜ belum (menyusul di tahap berikutnya) |
| v5 | API Gateway, dashboard, docker compose, seed, e2e | Peserta 5 | ⬜ belum (menyusul di tahap berikutnya) |

Rincian tiap arsip: [`releases/README.md`](releases/README.md). Hasil uji per tahap:
[`docs/HASIL-VERIFIKASI.md`](docs/HASIL-VERIFIKASI.md). Pohon sumber di akar repositori ini
adalah isi v5 (kondisi akhir).

## Distribusi tugas

Rincian peran dan kontrak antar layanan: [docs/DISTRIBUSI-TUGAS.md](docs/DISTRIBUSI-TUGAS.md).
Alur checkout + kompensasi: [docs/ALUR-SAGA.md](docs/ALUR-SAGA.md).
Ringkasan endpoint: [docs/API.md](docs/API.md).

## Arsitektur

```
                       ┌───────────────────────────┐
   browser / curl ───► │  API Gateway  :8000       │  JWT, proksi, agregasi
   (toko & admin)      │  dashboard / dan /admin   │
                       └───────┬───────────────────┘
             ┌─────────────────┼──────────────────┬──────────────────┐
             ▼                 ▼                  ▼                  ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐
     │ Katalog :8001│  │Pelanggan:8002│  │  Order :8003 │  │Pembayaran :8004│
     │ produk, stok │  │ auth JWT,    │  │ keranjang,   │  │ tagihan,       │
     │ reservasi    │  │ profil,alamat│  │ saga checkout│  │ simulasi,      │
     └──────────────┘  └──────────────┘  └──────────────┘  │ laporan        │
            SQLite            SQLite            SQLite      └────────────────┘
                                                            SQLite
```

Layanan berbicara lewat HTTP + JSON dengan amplop `{success, data, error, request_id}`.
Autentikasi pengguna memakai JWT HS256; autentikasi antar layanan memakai `X-Service-Token`.

## Layanan pada tahap ini

| Layanan | Folder | Alamat |
|---|---|---|
| katalog | `katalog-service/` | http://localhost:8001 |
| pelanggan | `pelanggan-service/` | http://localhost:8002 |
| order | `order-service/` | http://localhost:8003 |
=======
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
>>>>>>> 04eda1bd6649056beef7d88be3add86732a7ea72

## Menjalankan

```bash
<<<<<<< HEAD
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r katalog-service/requirements.txt
python scripts/dev_up.py
python seed/seed_data.py --pesanan 4     # opsional, data contoh
```

### Menjalankan dengan Docker Compose

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```

Akun demo setelah seed: `admin@contoh.test / admin12345`, `siti@contoh.test / rahasia123`.
Dashboard toko: <http://localhost:8000> · Dashboard admin: <http://localhost:8000/admin>.
=======
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
>>>>>>> 04eda1bd6649056beef7d88be3add86732a7ea72

## Pengujian

```bash
<<<<<<< HEAD
python tests/run_tests.py          # menyalakan layanan yang ada, menjalankan semua tes, lalu mematikan
python tests/run_tests.py -v       # verbose
python tests/run_tests.py --tanpa-boot   # bila layanan sudah jalan
```

Tes yang layanannya belum ada akan **dilewati** (bukan gagal) — itu normal untuk arsip tahap awal.

## Struktur berkas pada tahap ini

- `.env.example`
- `.gitignore`
- `common/__init__.py`
- `common/config.py`
- `common/db.py`
- `common/errors.py`
- `common/httpc.py`
- `common/jwtutil.py`
- `common/responses.py`
- `common/security.py`
- `common/service.py`
- `docs/ALUR-SAGA.md`
- `docs/API.md`
- `docs/DISTRIBUSI-TUGAS.md`
- `docs/HASIL-VERIFIKASI.md`
- `katalog-service/Dockerfile`
- `katalog-service/app.py`
- `katalog-service/requirements.txt`
- `katalog-service/schema.sql`
- `order-service/Dockerfile`
- `order-service/app.py`
- `order-service/requirements.txt`
- `order-service/saga.py`
- `order-service/schema.sql`
- `pelanggan-service/Dockerfile`
- `pelanggan-service/app.py`
- `pelanggan-service/requirements.txt`
- `pelanggan-service/schema.sql`
- `scripts/dev_up.py`
- `seed/data/katalog.json`
- `seed/data/pelanggan.json`
- `seed/seed_data.py`
- `tests/base.py`
- `tests/run_tests.py`
- `tests/test_katalog.py`
- `tests/test_order.py`
- `tests/test_pelanggan.py`

## Catatan tahap 3

Order Service + saga kompensasi dikerjakan oleh **Peserta 3**. Detail perubahan ada di
[CHANGELOG.md](CHANGELOG.md). Arsip tahap sebelumnya tetap dapat dijalankan sendiri karena
setiap tahap membawa seluruh kode tahap sebelumnya.
=======
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
>>>>>>> 04eda1bd6649056beef7d88be3add86732a7ea72
