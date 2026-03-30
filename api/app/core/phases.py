# =============================================================
# phases.py — Faze natjecanja (konačni automat)
# =============================================================
# Tri faze određene usporedbom trenutnog vremena s rokovima:
#   OPEN           — prije prelim_deadline
#   PRELIM_PASSED  — između prelim i final roka
#   CLOSED         — nakon final_deadline
#
# Korištenje u service layeru:
#   phase = get_competition_phase(competition)
#   if phase != Phase.OPEN: raise AppError(...)
# =============================================================

from datetime import datetime, timezone
from enum import Enum

from app.models.competition import Competition


class Phase(str, Enum):
    OPEN = "open"
    PRELIM_PASSED = "prelim_passed"
    CLOSED = "closed"


def get_competition_phase(competition: Competition) -> Phase:
    """Odredi fazu natjecanja prema trenutnom vremenu."""
    now = datetime.now(timezone.utc)
    if now < competition.prelim_deadline:
        return Phase.OPEN
    if now < competition.final_deadline:
        return Phase.PRELIM_PASSED
    return Phase.CLOSED
