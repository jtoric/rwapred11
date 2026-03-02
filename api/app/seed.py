# =============================================================
# seed.py — Inicijalni podaci za razvoj i testiranje
# =============================================================
# Kreira admin korisnika, demo klub i club usera.
#
# Pokretanje (iz api/ direktorija):
#   python -m app.seed
#
# Zašto seed?
#   - Nakon "alembic upgrade head" imamo prazne tablice
#   - Za razvoj trebamo barem admin login i jedan klub
#   - Za testiranje auth/ownership logike (predavanje 3-4)
#
# Idempotentnost:
#   Skripta provjerava postoji li već zapis s istim emailom/imenom.
#   Ako postoji — preskače. Sigurno je pokrenuti višestruko.
#
# NAPOMENA: koristimo bcrypt direktno (ne passlib) jer passlib
#   ima problem kompatibilnosti s novijim bcrypt>=4.1.
#   Zajednički utility za password dolazi u predavanju 3.
# =============================================================

import asyncio
import logging

import bcrypt as _bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, engine
from app.models.club import Club
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Seed podaci ------------------------------------------------
# U produkciji ovi podaci NE BI postojali ovdje (posebno lozinke).
# Ovo je ISKLJUČIVO za development okruženje.
ADMIN_EMAIL = "admin@pl.local"
ADMIN_PASSWORD = "admin123"

DEMO_CLUB_NAME = "Behemot"
DEMO_CLUB_CITY = "Zadar"

CLUB_USER_EMAIL = "klub@pl.local"
CLUB_USER_PASSWORD = "klub123"


async def seed(session: AsyncSession) -> None:
    """
    Kreira inicijalne podatke ako ne postoje.

    Redoslijed je bitan:
      1. Klub (jer user treba club_id)
      2. Admin user (nema club_id)
      3. Club user (ima club_id)
    """

    # -- 1. Demo klub --
    result = await session.execute(select(Club).where(Club.name == DEMO_CLUB_NAME))
    club = result.scalar_one_or_none()

    if club is None:
        club = Club(name=DEMO_CLUB_NAME, city=DEMO_CLUB_CITY)
        session.add(club)
        # flush šalje INSERT u bazu (ali ne commitira) tako da
        # club.id bude dostupan za club usera u koraku 3.
        await session.flush()
        logger.info("Kreiran klub: %s (id=%s)", club.name, club.id)
    else:
        logger.info("Klub '%s' već postoji — preskačem.", club.name)

    # -- 2. Admin user --
    result = await session.execute(select(User).where(User.email == ADMIN_EMAIL))
    admin = result.scalar_one_or_none()

    if admin is None:
        admin = User(
            email=ADMIN_EMAIL,
            password_hash=_bcrypt.hashpw(ADMIN_PASSWORD.encode(), _bcrypt.gensalt()).decode(),
            role="admin",
            club_id=None,  # admin ne pripada nijednom klubu
        )
        session.add(admin)
        logger.info("Kreiran admin: %s", admin.email)
    else:
        logger.info("Admin '%s' već postoji — preskačem.", admin.email)

    # -- 3. Club user (za demo klub) --
    result = await session.execute(select(User).where(User.email == CLUB_USER_EMAIL))
    club_user = result.scalar_one_or_none()

    if club_user is None:
        club_user = User(
            email=CLUB_USER_EMAIL,
            password_hash=_bcrypt.hashpw(CLUB_USER_PASSWORD.encode(), _bcrypt.gensalt()).decode(),
            role="club",
            club_id=club.id,
        )
        session.add(club_user)
        logger.info("Kreiran club user: %s (club=%s)", club_user.email, club.name)
    else:
        logger.info("Club user '%s' već postoji — preskačem.", club_user.email)

    # Commit svih promjena odjednom (atomarno).
    await session.commit()
    logger.info("Seed završen uspješno!")


async def main() -> None:
    """Entry point — otvara sesiju, pokreće seed, zatvara engine."""
    async with AsyncSessionLocal() as session:
        await seed(session)
    # Čisto zatvaranje svih konekcija u poolu.
    await engine.dispose()


# Omogućuje pokretanje sa: python -m app.seed
if __name__ == "__main__":
    asyncio.run(main())

