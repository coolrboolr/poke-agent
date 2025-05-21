# Poke-STREAMER Agent Configuration & Roles

This document defines the behavior, structure, and personality of the agents powering the `poke-streamer` system. Each lane operates as an autonomous module within a latency-aware framework. All agents must remain stateless per call and conform to shared developer rules.

## 🎯 Agent Operating Principles

| Principle | Description |
|-----------|-------------|
| 🧠 Modular | Each agent operates within a distinct lane: Reflex, Tactical, Strategic |
| 🪢 Coordinated | The Arbiter resolves all proposals using deterministic priority routing |
| 🔁 Observability | Every decision, trigger, and fallback is logged with timestamps |
| 🚫 No Blocking | All agent operations must return within budget or yield |
| 🧪 Fully Tested | All agent logic must be tested and covered by CI before merging |

## 🧠 Agent Definitions

### Reflex Agent
**Module:** `lanes/reflex/policy.py`
**Latency Target:** ≤ 2ms
**Scope:** Immediate reactions to game stimuli (e.g., text boxes, idle state)

**Behavior:**
- Press `A` to dismiss text boxes
- If idle with no active goal, randomly move to avoid timeouts

**Prompt Format:**
```json
{
  "dialogue_present": true,
  "mode": "idle"
}
```
**Output:** `Action.A`, `Action.UP`, etc. or `None`

### Tactical Agent
**Module:** `lanes/tactical/agent.py`
**Latency Target:** ≤ 5ms
**Scope:** Local logic—battle moves, item use, navigation fixes

**Behavior:**
- Choose battle moves based on type effectiveness
- Heal low HP if potion available
- Unstick if path is blocked

**Prompt Format:**
```json
{
  "battle_state": {
    "enemy_type": "Water",
    "available_moves": [ ... ]
  },
  "last_player_positions": [ ... ]
}
```
**Output:** `Action.USE_MOVE_1`, `Action.USE_POTION`, etc.

### Strategic Agent
**Module:** `lanes/strategic/agent.py`
**Latency Target:** async, non-blocking
**Scope:** Long-term planning based on game knowledge and goals

**Behavior:**
- Set high-level goals (e.g., reach gym, train, acquire item)
- Determine direction/path for active objective
- Trigger re-planning on major events (badge, loss)

**Prompt Format:**
```json
{
  "location": "Route 3",
  "badges": 0,
  "memory": [ ... ]
}
```
**Output:** Movement or objective alignment such as `Action.RIGHT` or `Action.TALK_NPC`

## Arbiter
**Module:** `arbiter/select_action.py`
**Latency Target:** ≤ 1ms
**Scope:** Chooses final action based on lane priorities

**Priority Order:**
1. Reflex
2. Tactical
3. Strategic

**Logging:** Logs all proposed actions and the one selected. Always logs `None` fallback if all lanes are silent.

## RL Critic
**Module:** `rl/critic.py` + `rl/reward.py`
**Latency Target:** async

**Behavior:**
- Receive `(state, action, reward)` each tick
- Log values and learn expected returns
- Optionally update lane priors or inform future arbiter decisions

**Reward Events:**
- +10 badge
- +5 win
- -10 faint or stuck

## 🔧 Configuration

### GameProfile Selector
- Uses `src/game_profiles/` to route perception, reward, and goal heuristics by `GAME_PROFILE`

### Action Enum
- Defined in `utils/actions.py`
- All lanes must return `Action` enums, not strings

### Logging Format
```
[INFO][lane][timestamp] Reason: X → Action: Y
```

### Output Contracts
- Every agent must return `Optional[Action]`
- Agents must be side-effect free and stateless per call
- The Arbiter selects only one action per frame

## Context Memory
`ContextMemory` composes short-term, long-term, and working memory layers. Use `update(game_state)` each frame to record state and facts. Call `query_context(goal)` to fetch relevant past facts for planning. Facts are persisted in `memory_store/` via ChromaDB.

## Model Configuration and Fallbacks
Each lane may load different model sizes depending on available hardware. If a primary model fails or times out, a smaller fallback model is used. Models are loaded once at startup and monitored for latency.

## Logging and Observability
Every perception, decision, and action is logged with timestamps and frame identifiers. Logs are written to stdout and optionally to a file for later analysis. Important metrics (frame time, decision latency) are exported via Prometheus-compatible endpoints so dashboards can track performance.

## 🧪 Agent Testing Rules
- No PR may merge without 100% test coverage in:
  - Reflex: `test_reflex_policy.py`
  - Tactical: `test_tactical_agent.py`
  - Strategic: `test_strategic_agent.py`
  - Arbiter: `test_arbiter.py`
- Use mocks for GameState inputs
- Use `caplog` to test decision traces and log clarity

## 🤖 For Codex Agents
- Do not introduce new agent lanes without updating this file
- Do not bypass arbiter logic to send inputs directly to the emulator
- Always document lane scope, latency, and return schema in PRs
- If introducing async or ML models, isolate behind non-blocking interfaces

This document ensures all agents operate within a stable, explainable, and testable brain architecture. All contributors—human or AI—must refer to it for coordination, arbitration, and agent contract consistency.
