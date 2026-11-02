"""
Basis bersama untuk tes katalog: klien HTTP tipis, cek kesehatan layanan, dan token admin.
"""
import os
import sys
import uuid

import requests

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AKAR not in sys.path:
    sys.path.insert(0, AKAR)

from common.jwtutil import buat_token  # noqa: E402

SEKRET = os.environ.get("JWT_SECRET", "dev-secret-jangan-dipakai-di-produksi")
TOKEN_LAYANAN = os.environ.get("SERVICE_TOKEN", "token-antar-layanan-dev")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@contoh.test")

URL = {
    "katalog": os.environ.get("KATALOG_URL", "http://127.0.0.1:8001"),
}


def butuh_layanan(basis, detik=1.5):
    """True bila /health layanan menjawab 200 (dipakai skipUnless)."""
    try:
        return requests.get(basis.rstrip("/") + "/health", timeout=detik).status_code == 200
    except requests.RequestException:
        return False


class Jawaban:
    """Pembungkus respons agar tes ringkas: .status_code/.json()/.text/.headers."""

    def __init__(self, respons):
        self._r = respons

    @property
    def status_code(self):
        return self._r.status_code

    @property
    def headers(self):
        return self._r.headers

    @property
    def text(self):
        return self._r.text

    def json(self):
        try:
            return self._r.json()
        except ValueError:
            return {"success": False, "error": {"kode": "BUKAN_JSON", "pesan": self._r.text[:300]}}


def token_admin():
    """Token admin HS256 untuk memanggil endpoint tulis katalog."""
    return buat_token({
        "sub": "1",
        "email": ADMIN_EMAIL,
        "nama": "Administrator Toko",
        "peran": "admin",
    }, SEKRET)


class ApiKlien:
    """Klien HTTP sederhana untuk Katalog Service."""

    def __init__(self, basis, batas=15):
        self.basis = basis.rstrip("/")
        self.batas = batas

    @staticmethod
    def acak(n=8):
        return uuid.uuid4().hex[:n]

    def _header(self, token=None, headers=None, json_=None):
        h = {"Accept": "application/json"}
        if json_ is not None:
            h["Content-Type"] = "application/json"
        if token:
            h["Authorization"] = f"Bearer {token}"
        if headers:
            h.update(headers)
        return h

    def kirim(self, method, path, json=None, params=None, headers=None, token=None):
        url = self.basis + "/" + path.lstrip("/")
        return Jawaban(requests.request(method, url, json=json, params=params,
                                        headers=self._header(token, headers, json),
                                        timeout=self.batas))

    def get_raw(self, path, method="GET", json=None, params=None, headers=None, token=None):
        return self.kirim(method, path, json=json, params=params, headers=headers, token=token)

    def _data(self, jawaban):
        """Kembalikan seluruh body JSON ({success, data, meta}) bila status < 400."""
        body = jawaban.json()
        if jawaban.status_code >= 400 or body.get("success") is False:
            raise AssertionError(f"{self.basis}{jawaban.text[:400]}")
        return body

    def get(self, path, params=None, token=None, headers=None):
        return self._data(self.kirim("GET", path, params=params, token=token, headers=headers))

    def post(self, path, json=None, token=None, headers=None):
        return self._data(self.kirim("POST", path, json=json, token=token, headers=headers))

    def put(self, path, json=None, token=None, headers=None):
        return self._data(self.kirim("PUT", path, json=json, token=token, headers=headers))

    def delete(self, path, token=None, headers=None):
        return self._data(self.kirim("DELETE", path, token=token, headers=headers))

    # ------------------------------------------------------------------- token
    def token_admin(self):
        return {"token": token_admin(), "pengguna": {"id": 1, "email": ADMIN_EMAIL,
                                                     "peran": "admin"}}

    def token_pelanggan(self):
        """Token pengguna biasa, dipakai untuk menguji penolakan endpoint admin."""
        token = buat_token({"sub": "2", "email": "uji@contoh.test", "nama": "Pembeli Uji",
                            "peran": "pelanggan"}, SEKRET)
        return {"token": token, "pengguna": {"id": 2, "email": "uji@contoh.test",
                                             "peran": "pelanggan"}}

    # ------------------------------------------------------- pembantu alur katalog
    def buat_produk(self, stok=10, harga=50000, nama=None, kategori_id=None):
        admin = self.token_admin()
        muatan = {"nama": nama or "Produk Uji " + self.acak(), "harga": harga, "stok": stok}
        if kategori_id:
            muatan["kategori_id"] = kategori_id
        return self.post("/produk", muatan, token=admin["token"])["data"]

    def stok_produk(self, produk_id):
        return self.get(f"/produk/{produk_id}")["data"]
