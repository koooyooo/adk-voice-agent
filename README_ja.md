# adk-voice-agent

[English](README.md) | 日本語

黙らない汎用音声チャット（Google ADK + `gemini-3.8-live`）。Google Developers Blog の記事 [Step-by-step guide: Build a voice agent that never goes silent using ADK](https://developers.googleblog.com/step-by-step-guide-build-a-voice-agent-that-never-goes-silent-using-adk/) の手法を実装している。設計は [docs/voice-agent-dd.md](docs/voice-agent-dd.md)。

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

## サンプルのツールについて

`voice_agent/tools/samples.py` の調べ物ツールは**模擬**である。実際には何も検索せず、遅いバックエンドを再現するために `asyncio.sleep` で約13秒（検索 4秒 → 読む 5秒 → まとめる 4秒）待つだけ。13秒は[元記事](https://developers.googleblog.com/step-by-step-guide-build-a-voice-agent-that-never-goes-silent-using-adk/)の例（13秒かかるクエリ）に合わせた値で、エージェントが最後に話す答えはモデル自身の知識による。

このプロジェクトで確かめているのは、遅いツールの実行中も会話を続ける手法であり、調べ物の質ではない。

計測結果の改善前の値（最初の発話まで約14.6秒）は、作った13秒の待ちからそのまま決まる。意味があるのは、ストリーミング型ではツールの長さに関係なく約2秒で話し始める点である。

## ライセンス

[MIT](LICENSE)
