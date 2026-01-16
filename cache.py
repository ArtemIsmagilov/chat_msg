import orjson

from utils import get_cache


def get_chat_with_msgs(id: int, limit: int):
    with get_cache() as c:
        return c.get(f"{id}:{limit}")


def set_chat_with_msgs(id: int, limit: int, result: dict):
    with get_cache() as c:
        return c.set(f"{id}:{limit}", orjson.dumps(result))
