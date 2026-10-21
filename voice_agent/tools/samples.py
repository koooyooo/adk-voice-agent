"""模擬のサンプルツール。実際の外部サービスには接続せず、待ち時間だけを再現する。"""

import asyncio
from collections.abc import AsyncGenerator

from ._common import Scheduling, streaming_tool, update

# 調べ物の各段階と所要秒数（合計約13秒）
RESEARCH_STAGES = [("searching", 4.0), ("reading", 5.0), ("summarizing", 4.0)]

RESEARCH_RESULT_NOTE = "Mock research. Answer briefly from your own knowledge."


async def research_topic_blocking(topic: str) -> dict:
    """Research a topic in depth. Takes about 13 seconds.

    Use this when the user asks you to look something up or research a topic.
    Call it only once per request.

    Args:
        topic: The topic to research.
    """
    for _stage, seconds in RESEARCH_STAGES:
        await asyncio.sleep(seconds)
    return {"status": "done", "topic": topic, "note": RESEARCH_RESULT_NOTE}


@streaming_tool
async def research_topic(topic: str) -> AsyncGenerator[dict, None]:
    """Research a topic in depth. Takes about 13 seconds and reports progress while running.

    Use this when the user asks you to look something up or research a topic.
    Call it only once per request; it keeps running in the background and sends
    progress updates and the final result on its own.

    Args:
        topic: The topic to research.
    """
    total = len(RESEARCH_STAGES)
    for step, (stage, seconds) in enumerate(RESEARCH_STAGES, start=1):
        # 話させる進捗は途中の 1 回だけ。残りは履歴に入れるだけにして、しゃべりすぎを防ぐ
        scheduling = Scheduling.WHEN_IDLE if step == 2 else Scheduling.SILENT
        yield update({"status": "in_progress", "stage": stage, "step": step, "total": total}, scheduling)
        await asyncio.sleep(seconds)
    yield update({"status": "done", "topic": topic, "note": RESEARCH_RESULT_NOTE}, Scheduling.WHEN_IDLE)
