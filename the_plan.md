# Implementation Roadmap

This document tracks development from bootstrap through advanced features. Only merge functional code and document all work in pull requests.

## Milestones

### M0: Repo Bootstrap, CI, Docker
- **Modules:** `.github/`, `Dockerfile`, `docker-compose.yml`
- **Goals:**
  - Establish repository structure and GitHub Actions CI
  - Dockerfile and Docker Compose to run the agent
  - Placeholder unit test passes in CI
- **Deliverables:** Docker setup, CI pipeline, minimal test
- **Latency Budget:** N/A (infrastructure only)
- **Testing:** `pytest` runs with zero or simple tests

### M1: Emulator Connectivity
- **Modules:** `emulator/`
- **Goals:**
  - Connect to the Pokémon emulator process
  - Send basic input commands and capture screen frames
- **Deliverables:** Emulator client module with I/O
- **Latency Budget:** Frame capture + input dispatch under 5ms
- **Testing:** Integration tests using a mocked emulator interface

### M1.5: Emulator GUI & Streaming
- **Modules:** `emulator/`, `docker-compose.yml`, `frontend/`
- **Goals:**
  - Enable emulator GUI in the container (via X11 forwarding or Xvfb) to capture real emulator frames instead of dummy data
  - Correct handling of the `ENABLE_GUI` flag and default it to `true` for development builds
  - Mount host X11 socket (`/tmp/.X11-unix`) or start `Xvfb` inside the container when no `DISPLAY` is available
  - Validate that `mgba-sdl` launches under `xvfb-run` and confirm process startup via logs
  - Ensure that `logs/frame.jpg` is written with non-black pixel data and refreshed for the front end
- **Deliverables:**
  - Docker Compose updates: change default `ENABLE_GUI` to `true`, propagate `DISPLAY`, add volume mount for `/tmp/.X11-unix`, and document host X setup (e.g., `xhost +local:docker`)
  - Code tweaks in `adapter.py` to emit clear logs for emulator launch, fallback behavior, and frame capture
  - Front-end integration: verify `/frame.jpg` polling and display of captured frames
  - Integration test that, after container startup, `logs/frame.jpg` exists and contains at least one non-zero pixel
- **Testing:**
  - Automated integration test to read `logs/frame.jpg` and assert non-dummy content
  - Manual validation of frame streaming in the web UI

### M2: Perception Module
- **Modules:** `perception/`
- **Goals:**
  - Screen differencing, OCR for text boxes, sprite detection
- **Deliverables:** Perception utilities returning structured observations
- **Latency Budget:** <= 4ms per frame
- **Testing:** Unit tests with sample frames

### M2 Completion Checklist
- [x] Screen differencing detects scene changes
- [x] OCR and HP parsing via HUDParser
- [x] Sprite detector stub with bounding boxes
- [x] PerceptionRunner aggregates modules
- [x] GameState logging throttled to 1/sec
- **Edge Case Handling:** OCR failures log and return ""; warn if no sprites detected for 3 frames

### M3: Memory and Knowledge Module
- **Modules:** `memory/`
- **Goals:**
  - Maintain recent state history and game knowledge
- **Deliverables:** Memory store with query/update API
- **Latency Budget:** <= 1ms per query
- **Testing:** Unit tests covering updates and lookups

### M3 Completion Checklist
- [x] ShortTermMemory buffers 120 frames, tested
- [x] LongTermMemory stores and queries embedded facts
- [x] Scratchpad manages objectives with add/complete logic
- [x] ContextMemory composes all modules and routes updates
- [x] Query latency < 300ms; tested in `test_memory_query.py`
- **Edge Case Handling:** STM overflows drop oldest frames automatically

### M4 Pre-Work Checklist
- [ ] Arbiter interface defined (`arbiter/select_action.py`)
- [ ] Action enums or schemas defined (e.g., `A`, `LEFT`, `RUN`, `SWITCH`)
- [ ] Reflex triggers and interrupt hooks specified
- [ ] Frame timing rules confirmed (reflex every frame, tactical every 0.5s)

### M4: Reflex Lane
- **Modules:** `lanes/reflex/`, `arbiter/`
- **Goals:**
  - Implement the fast reaction layer for immediate responses
- **Deliverables:** Reflex policies and action dispatcher
- **Latency Budget:** <= 2ms per decision
- **Testing:** Policy unit tests and simulated frame loops

### M5: Tactical Lane
- **Modules:** `lanes/tactical/`
- **Goals:**
  - Handle battle strategy and in-map logic
- **Deliverables:** Tactical planner integrated with memory
- **Latency Budget:** <= 3ms per decision
- **Testing:** Tactical scenarios via unit tests

### M6: Strategic Lane and Arbiter
- **Modules:** `lanes/strategic/`, `arbiter/`
- **Goals:**
  - Long-term planning and arbitration between lanes
- **Deliverables:** Strategic planner, arbiter logic with priority rules
- **Latency Budget:** Strategic decisions may span multiple frames but should not block the main loop
- **Testing:** Arbiter unit tests verifying priority routing

### M7: RL Critic and Twitch Polish
- **Modules:** `rl/`
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
