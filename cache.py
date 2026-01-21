import orjson
from valkey.asyncio import Valkey


async def get_chat_with_msgs(c: Valkey, id: int, limit: int):
    return await c.get(f"{id}:{limit}")


async def set_chat_with_msgs(c: Valkey, id: int, limit: int, result: dict):
    return await c.set(f"{id}:{limit}", orjson.dumps(result))
