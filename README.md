---
title: Evoloki Superki
emoji: 🔥
colorFrom: pink
colorTo: purple
sdk: docker
pinned: false
---
# EvoLoki SuperKI

An experimental Python project exploring AI-agent orchestration, model-provider APIs, local Ollama workers, task dispatch, and learning/knowledge components.

## Project map

- `freedom_bridge/` contains the modular core, worker, task-dispatch, and knowledge components.
- `SuperKI_Genesis.py` and `SuperKI_MiniServer.py` are experimental entry-point code.
- `Dockerfile` contains the current container setup.

This repository includes prototype and legacy components. The README is an orientation guide, not a claim that every module is production-ready or works end to end. Review dependencies, configuration, and code before running it.

## Privacy and credentials

Some code configures external model providers as well as a local Ollama worker. Depending on configuration, prompts or other input may be sent to those providers. Use your own review before configuring a provider, keep credentials in environment variables, and never commit real keys.

## Research topics and search terms

This prototype includes **self-learning and knowledge components**, **AI agent evolution experiments**, **LLM orchestration**, and persistent-memory experiments. These are research topics, not evidence of validated autonomous self-improvement; review the code to assess what is implemented.
## Related public experiments

- [AIO-Core-Alpha](https://github.com/Loki-Der-Wahnsinn/AIO-Core-Alpha) — experimental Python companion and worker-node project.
- [FreedomAI](https://github.com/Loki-Der-Wahnsinn/FreedomAI) — small Python team-orchestration prototype.

## License

No license is currently provided. Public visibility allows you to view this repository; it does not grant permission to reuse, modify, or distribute its contents.