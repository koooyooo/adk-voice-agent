# adk-voice-agent

English | [日本語](README_ja.md)

A general-purpose voice chat agent that never goes silent, built with Google ADK and `gemini-3.8-live`. See the design document (Japanese) at [docs/voice-agent-dd.md](docs/voice-agent-dd.md).

## Getting started

```sh
cp .env.example .env   # fill in GEMINI_API_KEY if it is not already set in your shell
uv run adk web
```

Open http://localhost:8000 in Chrome, select `voice_agent`, and press the call (phone) button.

In other browsers such as Firefox, microphone audio may not be captured and the waveform stays flat.

## Before / after comparison

```sh
RESEARCH_MODE=blocking uv run adk web   # before: silent for ~13 seconds while researching
uv run adk web                          # after: narrates progress while researching
```

Ask something like "Can you look up ..." to feel the difference.

## About the sample tools

The research tool in `voice_agent/tools/samples.py` is a **mock**. It does not search anything: it only waits about 13 seconds with `asyncio.sleep` (search 4s → read 5s → summarize 4s) to simulate a slow backend, matching the 13-second query in the original article. The answer the agent gives afterwards comes from the model's own knowledge.

This project verifies the technique of staying conversational while a slow tool runs, not the quality of the research itself.

When reading the measurements, note that the "before" time (about 14.6s to the first words) follows directly from the 13-second simulated wait. The meaningful result is that, with the streaming tool, the agent starts talking in about 2 seconds regardless of how long the tool takes.

## License

[MIT](LICENSE)
