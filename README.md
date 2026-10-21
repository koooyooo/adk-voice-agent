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

## License

[MIT](LICENSE)
