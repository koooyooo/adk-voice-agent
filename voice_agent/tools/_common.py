"""沈黙しないツールの共通部品。

- ストリーミング型: async generator に `@streaming_tool` を付ける。ADK が非ブロッキングで
  実行し、`yield` のたびに結果をモデルへ送る。
- バックグラウンド型: 普通の coroutine を `background_tool()` で包む。
"""

import asyncio
import functools
import json
import logging
from collections.abc import AsyncGenerator, Awaitable, Callable
from typing import Any

from google.adk.tools import FunctionTool
from google.genai import types

logger = logging.getLogger(__name__)

Scheduling = types.FunctionResponseScheduling

# 実行中のストリーミング型ツールの呼び出し（ツール名 + 引数）。
# ADK は同名ツールの再呼び出しで古いタスクを止めないため、ここで二重起動を防ぐ。
_running: set[str] = set()


def update(data: dict[str, Any], scheduling: Scheduling = Scheduling.WHEN_IDLE) -> types.FunctionResponse:
    """ストリーミング型ツールが yield する 1 回分の結果。伝えるタイミングを指定する。"""
    return types.FunctionResponse(response=data, scheduling=scheduling)


def streaming_tool(func: Callable[..., AsyncGenerator[Any, None]]) -> Callable[..., AsyncGenerator[Any, None]]:
    """二重起動の防止、キャンセル時の後始末、エラーの伝達を付け加える。"""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> AsyncGenerator[Any, None]:
        key = f"{func.__name__}:{json.dumps(kwargs, sort_keys=True, default=str)}"
        if key in _running:
            yield update({"status": "already_running"}, Scheduling.SILENT)
            return
        _running.add(key)
        try:
            async for item in func(*args, **kwargs):
                yield item
        except asyncio.CancelledError:
            logger.info("%s was cancelled", func.__name__)
            raise
        except Exception:
            logger.exception("%s failed", func.__name__)
            yield update({"status": "error"}, Scheduling.INTERRUPT)
        finally:
            _running.discard(key)

    return wrapper


def background_tool(
    func: Callable[..., Awaitable[Any]], scheduling: Scheduling = Scheduling.WHEN_IDLE
) -> FunctionTool:
    """途中経過のない処理を NON_BLOCKING で実行するツールにする。"""
    tool = FunctionTool(func)
    tool.behavior = types.Behavior.NON_BLOCKING
    tool.response_scheduling = scheduling
    return tool


def stop_streaming(function_name: str) -> None:
    """Cancel a running streaming tool. Call this ONLY when the user explicitly asks to cancel or stop it.

    Args:
        function_name: The name of the streaming tool to stop.
    """
    # ADK がこの名前の呼び出しを横取りしてタスクをキャンセルするため、本体は呼ばれない。
