from src.rl.critic import RLCritic
from src.rl.reward import compute_reward
from src.utils.actions import Action


def test_rl_critic_logs(capsys):
    critic = RLCritic(window=3)
    state = {"badges": 0}
    critic.observe(state, Action.A, 1.0)
    value = critic.estimate_value(state)
    out = capsys.readouterr().out.lower()
    assert "rl" in out
    assert "value estimate" in out
    assert value == 1.0


def test_compute_reward_events(capsys):
    prev = {"badges": 0, "in_battle": True}
    curr = {"badges": 1, "in_battle": False, "battle_result": "win"}
    reward = compute_reward(prev, curr)
    out = capsys.readouterr().out
    assert reward == 15.0
    assert "Badge gained" in out
    assert "Battle win" in out

    prev = curr
    curr = {"fainted": True}
    reward = compute_reward(prev, curr)
    out = capsys.readouterr().out
    assert reward == -10.0
    assert "Penalty" in out

    reward = compute_reward(curr, curr)
    assert reward == -10.0
