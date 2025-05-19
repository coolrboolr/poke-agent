# Agent Specification

This document defines the behavior and coordination logic of the Poke-Streamer agents.

## Lane Roles

### Reflex Lane
- **Purpose:** Provide immediate reactions to high-priority game events such as button prompts or sudden threats.
- **Personality:** Fast thinker, limited context. Focuses on recent frames only.
- **Examples:** Quickly dismissing pop-up dialogs, reacting to low HP warnings.

### Tactical Lane
- **Purpose:** Handle short-term planning, especially in battles or navigating puzzles.
- **Personality:** Balanced thinker. Considers current game state and recent history.
- **Examples:** Selecting moves in battle, choosing items, navigating routes.

### Strategic Lane
- **Purpose:** Guide long-term objectives like story progression and exploration.
- **Personality:** Slow, deliberate thinker with access to the full knowledge base.
- **Examples:** Deciding which gym to challenge next or when to train.

## Arbiter Logic

The Arbiter receives proposed actions from each lane and selects the one to execute based on priority:
1. Reflex Lane has highest priority for safety-critical responses.
2. Tactical Lane overrides Strategic when in battle or similar scenarios.
3. Strategic Lane provides default behavior when others are idle.

The Arbiter may override lower-priority actions if a higher-priority lane issues a command. All decisions are logged with the selected lane and reasoning.

## RL Critic

- **Reward Design:** Rewards are based on game progress (badges, wins) and penalties for setbacks (faints, time wasted). Dense rewards may come from in-game score or speed.
- **Learning Loop:** Observes states, actions, and outcomes. Updates policies asynchronously so real-time performance is unaffected.
- **Influence:** The critic adjusts policy weights used by the lanes but does not directly command actions.

## Context Memory
- `ContextMemory` composes short-term, long-term and working memory layers.
- Use `update(game_state)` each frame to record state and facts.
- Call `query_context(goal)` to fetch relevant past facts for planning.
- Facts are persisted in `memory_store/` via ChromaDB.

## Model Configuration and Fallbacks

Each lane may load different model sizes depending on available hardware. If a primary model fails or times out, a smaller fallback model is used. Models are loaded once at startup and monitored for latency.

## Logging and Observability

Every perception, decision, and action is logged with timestamps and frame identifiers. Logs are written to stdout and optionally to a file for later analysis. Important metrics (frame time, decision latency) are exported via Prometheus-compatible endpoints so dashboards can track performance.

