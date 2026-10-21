# adk-voice-agent

[English](README.md) | 日本語

黙らない汎用音声チャット（Google ADK + `gemini-3.8-live`）。設計は [docs/voice-agent-dd.md](docs/voice-agent-dd.md)。

## 起動

```sh
cp .env.example .env   # GEMINI_API_KEY がシェルで未設定なら記入する
uv run adk web
```

Chrome で http://localhost:8000 を開き、`voice_agent` を選んで通話（受話器）ボタンを押す。

Firefox などではマイクの音声が取り込まれず、波形が動かないことがある。

## 改善前との比較

```sh
RESEARCH_MODE=blocking uv run adk web   # 改善前: 調べ物の間 約13秒 黙る
uv run adk web                          # 改善後: 進捗を話しながら調べる
```

「〇〇について調べて」と頼むと差を体感できる。

## ライセンス

[MIT](LICENSE)
