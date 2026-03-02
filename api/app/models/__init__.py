# =============================================================
# models/__init__.py — Registar svih ORM modela
# =============================================================
# Ovdje importiramo Base i sve modele na jedno mjesto.
# Zašto?
#   1. Alembic čita Base.metadata da bi znao koje tablice postoje
#   2. Centralni import — lakše upravljanje modelima
#   3. Osiguravamo da su svi modeli "registrirani" u Base.metadata
#      prije nego Alembic pokuša generirati migraciju
#
# Korištenje:
#   from app.models import Base          # za Alembic env.py
#   from app.models import Club, User    # dolazi u sljedećem commitu
# =============================================================

from app.core.database import Base

__all__ = ["Base"]
