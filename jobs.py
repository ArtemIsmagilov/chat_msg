import asyncio

from streaq import Worker

from settings import CH_URL

worker = Worker(CH_URL)


@worker.task()
async def sleeper(time: int):
    await asyncio.sleep(time)
    return time
