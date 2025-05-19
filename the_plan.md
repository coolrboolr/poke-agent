# Implementation Roadmap

This document tracks development from bootstrap through advanced features. Only merge functional code and document all work in pull requests.

## Milestones

### M0: Repo Bootstrap, CI, Docker
- **Goals:**
  - Establish repository structure and GitHub Actions CI
  - Dockerfile and Docker Compose to run the agent
  - Placeholder unit test passes in CI
- **Deliverables:** Docker setup, CI pipeline, minimal test
- **Latency Budget:** N/A (infrastructure only)
- **Testing:** `pytest` runs with zero or simple tests

### M1: Emulator Connectivity
- **Goals:**
  - Connect to the Pokémon emulator process
  - Send basic input commands and capture screen frames
- **Deliverables:** Emulator client module with I/O
- **Latency Budget:** Frame capture + input dispatch under 5ms
- **Testing:** Integration tests using a mocked emulator interface

### M2: Perception Module
- **Goals:**
  - Screen differencing, OCR for text boxes, sprite detection
- **Deliverables:** Perception utilities returning structured observations
- **Latency Budget:** <= 4ms per frame
- **Testing:** Unit tests with sample frames

### M3: Memory and Knowledge Module
- **Goals:**
  - Maintain recent state history and game knowledge
- **Deliverables:** Memory store with query/update API
- **Latency Budget:** <= 1ms per query
- **Testing:** Unit tests covering updates and lookups

### M4: Reflex Lane
- **Goals:**
  - Implement the fast reaction layer for immediate responses
- **Deliverables:** Reflex policies and action dispatcher
- **Latency Budget:** <= 2ms per decision
- **Testing:** Policy unit tests and simulated frame loops

### M5: Tactical Lane
- **Goals:**
  - Handle battle strategy and in-map logic
- **Deliverables:** Tactical planner integrated with memory
- **Latency Budget:** <= 3ms per decision
- **Testing:** Tactical scenarios via unit tests

### M6: Strategic Lane and Arbiter
- **Goals:**
  - Long-term planning and arbitration between lanes
- **Deliverables:** Strategic planner, arbiter logic with priority rules
- **Latency Budget:** Strategic decisions may span multiple frames but should not block the main loop
- **Testing:** Arbiter unit tests verifying priority routing

### M7: RL Critic and Twitch Polish
- **Goals:**
  - Implement reinforcement learning critic and finalize Twitch integration
- **Deliverables:** RL feedback loop, stable streaming pipeline
- **Latency Budget:** RL updates run asynchronously; streaming must remain <16ms per frame
- **Testing:** RL unit tests with mock rewards; streaming soak tests

## Rules
- Only merge functional code—no half-completed modules on `main`.
- Every contribution must have associated tests and CI must pass.
- Document significant design decisions in pull requests referencing this plan.
- Use `.env` or Compose secrets for sensitive data like ROM paths and Twitch keys.
- Maintain logs for every perception, decision, and action to aid debugging and research.

This roadmap should guide development through each milestone. Refer back before starting new work.
