import os
from src.game_profiles.registry import load_profile
from src.rl.reward import compute_reward


def test_default_profile():
    profile = load_profile()
    assert profile.__class__.__name__ == "PokemonProfile"


def test_env_profile_switch():
    prev = os.environ.get("GAME_PROFILE")
    os.environ["GAME_PROFILE"] = "zelda"
    try:
        profile = load_profile()
        assert profile.__class__.__name__ == "ZeldaProfile"
        assert profile.get_reward({}, {}) == 0.0
    finally:
        if prev is None:
            os.environ.pop("GAME_PROFILE", None)
        else:
            os.environ["GAME_PROFILE"] = prev


def test_zelda_reward_noop(capsys):
    prev = os.environ.get("GAME_PROFILE")
    os.environ["GAME_PROFILE"] = "zelda"
    try:
        profile = load_profile()
        profile.get_reward({}, {})
        out = capsys.readouterr().out
        assert "Zelda reward stub" in out
    finally:
        if prev is None:
            os.environ.pop("GAME_PROFILE", None)
        else:
            os.environ["GAME_PROFILE"] = prev


def test_compute_reward_delegates():
    prev_env = os.environ.get("GAME_PROFILE")
    os.environ["GAME_PROFILE"] = "zelda"
    try:
        assert compute_reward({}, {}) == 0.0
        os.environ["GAME_PROFILE"] = "pokemon"
        prev = {"badges": 0, "in_battle": True}
        curr = {"badges": 1, "in_battle": False, "battle_result": "win"}
        assert compute_reward(prev, curr) == 15.0
    finally:
        if prev_env is None:
            os.environ.pop("GAME_PROFILE", None)
        else:
            os.environ["GAME_PROFILE"] = prev_env
