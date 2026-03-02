# =============================================================
# user.py — User ORM model
# =============================================================
# Korisnik sustava — može biti admin ili club user.
#
# Role:
#   "admin" — upravlja natjecanjima, vidi sve klubove
#   "club"  — prijavljuje natjecatelje svog kluba
#
# Dizajnerske odluke:
#   - role je String (ne Enum) — jednostavnije za početak,
#     validacija se radi u Pydantic schema sloju
#   - club_id je nullable: admin NEMA klub (club_id = NULL)
#   - email je UNIQUE: sprječava duplicirane loginove i
#     štiti od race conditiona pri registraciji
#   - password_hash: NIKAD ne spremamo lozinku u čistom tekstu!
# =============================================================

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.club import Club


class User(Base):
    """
    Korisnik sustava (admin ili club user).

    Atributi:
        id:            Surrogate primary key.
        email:         Login email (jedinstven u sustavu).
        password_hash: Bcrypt hash lozinke (NIKAD plain text).
        role:          "admin" ili "club".
        club_id:       FK prema klubu (NULL za admine).

    Relacije:
        club: Klub kojem korisnik pripada (None za admine).
              back_populates="users" znači da Club.users pokazuje natrag.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    # Foreign key prema clubs tablici.
    # nullable=True jer admin korisnik ne pripada nijednom klubu.
    club_id: Mapped[int | None] = mapped_column(
        ForeignKey("clubs.id"), nullable=True
    )

    # ORM relationship — omogućuje user.club umjesto ručnog querya.
    club: Mapped[Club | None] = relationship(back_populates="users")

