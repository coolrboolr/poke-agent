# Poke-Streamer

Poke-Streamer is a real-time agentic framework designed to play Pokémon games autonomously while streaming the gameplay to Twitch. The system is built around modular lanes that emulate different thinking speeds and strategies. An RL-based critic guides long-term improvement. The architecture aims for high observability and low latency, targeting a complete decision cycle under 16ms.

## Architecture Overview

```
+--------------+    +------------------+    +------------------+
|  Emulator    | -> | Perception       | -> | Memory / State   |
+--------------+    +------------------+    +------------------+
        |                    |                    |
        v                    v                    v
+--------------+    +------------------+    +------------------+
| Reflex Lane  |    | Tactical Lane    |    | Strategic Lane   |
+--------------+    +------------------+    +------------------+
        \                    |                    /
         \                   v                   /
          +--------------------------------------+
          |              Arbiter                |
          +--------------------------------------+
                             |
                             v
                      +--------------+
                      | RL Critic    |
                      +--------------+
                             |
                             v
                      +--------------+
                      | Twitch Stream|
                      +--------------+
```

- **Reflex Lane** reacts instantly to in-game events.
- **Tactical Lane** manages battle logic and short-term planning.
- **Strategic Lane** pursues long-term goals and exploration.
- **Arbiter** prioritizes actions from lanes based on urgency and context.
- **RL Critic** observes outcomes to provide rewards and improve policies.

All modules log their perceptions, decisions, and actions through a common logging utility so that developers can trace behavior easily.

## Building and Running with Docker

The project ships with a Docker setup for development and deployment. Ensure you have Docker and Docker Compose installed.

```bash
# Build the base image
docker compose build

# Start the stack with emulator and streaming components
docker compose up
```

The development container exposes a Python environment with required dependencies. ROM paths and Twitch credentials are supplied via environment variables loaded from `.env` or directly through Docker Compose secrets.

## Running Tests

Build the container image and open a shell inside it:

```bash
docker compose build
docker compose run --rm app bash
```

Inside the container run:

```bash
python pytest.py -v
```

This ensures all dependencies are available when executing the test suite.

## Twitch Streaming Setup

Game output is streamed using `ffmpeg` or OBS inside the container. Configure your Twitch stream key in the environment variables:

```bash
TWITCH_STREAM_KEY=your_key_here
```

The streaming script captures frames from the emulator and pushes them to Twitch while the agent sends inputs. Low-latency settings are applied to keep the frame loop under 16ms.

## Developer Practices

- Read `the_plan.md` before contributing. All milestones and rules are defined there.
- Never merge incomplete stubs into `main`.
- All contributions must include tests and pass CI checks.
- Log every perception, decision, and action.
- Maintain performance and observability from the start.

### Logging Example

```python
logger.info("PERCEPT", extra={"frame_id": frame_id, "objects": objects})
logger.info("DECISION", extra={"lane": "tactical", "action": action})
logger.info("ACTION", extra={"input": button_press})
```

## Performance Constraints

The agent operates in a real-time loop targeting less than **16ms** per frame from perception to action. Each lane has its own budget but the combined processing must stay within this limit to maintain sync with the emulator.

## Getting Started

1. Clone the repository.
2. Set up your `.env` file with ROM paths and Twitch keys.
3. Run `docker compose up` to start development.
4. Read `agent.md` to understand lane behavior.

Happy streaming!

## Monitoring & Debugging

The `logs` directory stores runtime data including `loop_metrics.json` which
records average FPS and latency for the main loop. Structured logs appear on
stdout and can be colored when run in a terminal. For deeper inspection, run
`tools/frame_diagnose.py` to subscribe to the frame bus and optionally save
frames for offline review.

