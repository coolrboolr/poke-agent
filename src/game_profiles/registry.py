from __future__ import annotations

import os

from .base import GameProfile
from .pokemon import PokemonProfile
from .zelda import ZeldaProfile


_PROFILES = {
    "pokemon": PokemonProfile,
    "zelda": ZeldaProfile,
}


def load_profile(game_id: str | None = None) -> GameProfile:
    """Instantiate a profile by id or environment variable."""
    game_id = (game_id or os.getenv("GAME_PROFILE", "pokemon")).lower()
    cls = _PROFILES.get(game_id, PokemonProfile)
    return cls()
