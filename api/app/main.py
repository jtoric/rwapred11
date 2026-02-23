# =============================================================
# main.py — Ulazna točka FastAPI aplikacije
# =============================================================
# Ovo je "naivna" verzija: sve na jednom mjestu.
# U sljedećem commitu ćemo refaktorirati u app factory pattern
# i razdvojiti routere, konfiguraciju i error handling.
#
# Pokretanje:
#   cd api
#   uvicorn app.main:app --reload
#
# --reload znači: svaki put kad spremimo datoteku,
# uvicorn automatski restarta server (samo za development!).
# =============================================================

from fastapi import FastAPI

# Kreiramo FastAPI instancu.
# title i description se prikazuju u Swagger UI (/docs).
# version koristimo i u /version endpointu.
app = FastAPI(
    title="Powerlifting Registrations API",
    version="0.1.0",
    description="Sustav za prijavu natjecatelja na powerlifting natjecanja",
)


@app.get("/health", tags=["health"])
def health():
    """
    Health check endpoint.

    Najjednostavniji mogući endpoint koji potvrđuje:
    - da se aplikacija podiže
    - da routing radi
    - (kasnije) da baza odgovara

    U produkciji se koristi kao liveness/readiness probe
    (npr. Railway/Kubernetes periodički poziva ovaj endpoint).
    """
    return {"status": "ok"}


@app.get("/version", tags=["health"])
def version():
    """
    Vraća verziju API-ja.

    Korisno za debugging — kad netko prijavi bug,
    pitamo "koja verzija?" i znamo što gledamo.
    app.version čita iz FastAPI konstruktora iznad.
    """
    return {"version": app.version}
