"""
Menjalankan Katalog Service di mesin lokal tanpa Docker.

    python scripts/dev_up.py                       # port 8001
    python scripts/dev_up.py --data-dir data/dev   # pilih folder SQLite

Tekan Ctrl+C untuk menghentikan layanan.
"""
import argparse
import os
import subprocess
import sys
import time

DISK = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.dirname(DISK)
sys.path.insert(0, AKAR)
sys.path.insert(0, os.path.join(AKAR, "tests"))

from base import URL, butuh_layanan  # noqa: E402

LAYANAN = [
    ("katalog", "katalog-service/app.py", 8001),
]


def main():
    p = argparse.ArgumentParser(description="Jalankan Katalog Service secara lokal")
    p.add_argument("--data-dir", default=os.path.join(AKAR, "data", "dev"))
    p.add_argument("--tanpa-tunggu", action="store_true")
    arg = p.parse_args()

    os.makedirs(arg.data_dir, exist_ok=True)
    lingkungan = os.environ.copy()
    lingkungan.update({"DATA_DIR": arg.data_dir, "PYTHONPATH": AKAR, "PYTHONUNBUFFERED": "1"})

    proses = []
    print(f"DATA_DIR = {arg.data_dir}")
    for nama, berkas, port in LAYANAN:
        if not os.path.exists(os.path.join(AKAR, berkas)):
            continue
        log = open(os.path.join(arg.data_dir, f"{nama}.log"), "w", encoding="utf-8")
        proses.append((nama, subprocess.Popen(
            [sys.executable, os.path.join(AKAR, berkas)],
            cwd=AKAR, env=lingkungan, stdout=log, stderr=subprocess.STDOUT), log))
        print(f"  - {nama:10s} http://127.0.0.1:{port}  (log: {arg.data_dir}/{nama}.log)")

    if not arg.tanpa_tunggu:
        for nama, _, _ in proses:
            for _ in range(40):
                if butuh_layanan(URL[nama], 0.5):
                    break
                time.sleep(0.25)

    print("\nSeed data : python seed/seed_data.py")
    print("Tes       : python tests/run_tests.py --tanpa-boot")
    try:
        while True:
            time.sleep(1)
            if all(pr.poll() is not None for _, pr, _ in proses):
                print("Proses berhenti.")
                break
    except KeyboardInterrupt:
        print("\nMenghentikan layanan...")
    finally:
        for _, pr, log in proses:
            if pr.poll() is None:
                pr.terminate()
                try:
                    pr.wait(timeout=6)
                except subprocess.TimeoutExpired:
                    pr.kill()
            log.close()


if __name__ == "__main__":
    main()
