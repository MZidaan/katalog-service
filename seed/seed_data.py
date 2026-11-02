"""
Mengisi Katalog Service dengan data contoh dari seed/data/katalog.json.

    python seed/seed_data.py
    python seed/seed_data.py --url http://127.0.0.1:8001

Skrip idempoten: kategori dicocokkan lewat nama, produk lewat SKU.
"""
import argparse
import json
import os
import sys

import requests

DISK = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.dirname(DISK)
sys.path.insert(0, AKAR)

from common.jwtutil import buat_token  # noqa: E402

BATAS = 15


def baca(nama):
    with open(os.path.join(DISK, "data", nama), encoding="utf-8") as f:
        return json.load(f)


def kepala_admin(secret):
    token = buat_token({"sub": "1", "email": "admin@contoh.test", "nama": "Administrator Toko",
                        "peran": "admin"}, secret)
    return {"Authorization": "Bearer " + token, "Content-Type": "application/json"}


def pastikan_kategori(url, h, daftar):
    peta = {}
    for k in daftar:
        r = requests.post(url + "/kategori", json=k, headers=h, timeout=BATAS)
        if r.status_code in (200, 201):
            peta[k["nama"]] = r.json()["data"]["id"]
            print(f"  - kategori dibuat: {k['nama']}")
            continue
        for item in requests.get(url + "/kategori", timeout=BATAS).json()["data"]:
            if item["nama"].lower() == k["nama"].lower():
                peta[k["nama"]] = item["id"]
                break
        print(f"  - kategori sudah ada: {k['nama']}")
    return peta


def pastikan_produk(url, h, daftar, peta):
    ada = {p["sku"] for p in requests.get(url + "/produk", params={"batas": 100, "aktif": "semua"},
                                          timeout=BATAS).json()["data"]}
    baru = 0
    for p in daftar:
        if p["sku"] in ada:
            continue
        muatan = {"sku": p["sku"], "nama": p["nama"], "harga": p["harga"], "stok": p["stok"],
                  "kategori_id": peta.get(p["kategori"]),
                  "deskripsi": f"Produk contoh kategori {p['kategori']}"}
        r = requests.post(url + "/produk", json=muatan, headers=h, timeout=BATAS)
        if r.status_code == 201:
            baru += 1
        else:
            print(f"    ! gagal membuat {p['sku']}: {r.text[:120]}")
    print(f"  - produk: {baru} baru, {len(daftar) - baru} sudah ada")


def main():
    p = argparse.ArgumentParser(description="Isi data contoh katalog")
    p.add_argument("--url", default=os.environ.get("KATALOG_URL", "http://127.0.0.1:8001"))
    p.add_argument("--secret", default=os.environ.get("JWT_SECRET",
                                                      "dev-secret-jangan-dipakai-di-produksi"))
    arg = p.parse_args()

    try:
        requests.get(arg.url + "/health", timeout=3).raise_for_status()
    except requests.RequestException:
        print(f"Katalog Service belum hidup di {arg.url}. Jalankan dulu: python scripts/dev_up.py")
        return 1

    h = kepala_admin(arg.secret)
    data = baca("katalog.json")
    print("Mengisi kategori...")
    peta = pastikan_kategori(arg.url, h, data["kategori"])
    print("Mengisi produk...")
    pastikan_produk(arg.url, h, data["produk"], peta)
    print("Selesai.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
