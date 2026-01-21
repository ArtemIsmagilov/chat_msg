from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from valkey.asyncio import Valkey
from fastapi import FastAPI, Query, status, HTTPException, Response, Depends

from jobs import worker, sleeper
from schema import ChatIn, ChatMessagesOut, MessageIn
from crud import insert_chat, select_chat_with_msgs, insert_msg_in_chat, remove_chat
from logger import logger
from cache import get_chat_with_msgs, set_chat_with_msgs
from utils import get_session, get_cache

app = FastAPI()


@app.get("/chats/{id}", status_code=status.HTTP_200_OK, response_model=ChatMessagesOut)
async def get_chat_with_messages(
    s: Annotated[AsyncSession, Depends(get_session)],
    c: Annotated[Valkey, Depends(get_cache)],
    id: int,
    limit: Annotated[int, Query(ge=20, le=100)] = 20,
):
    logger.info(f"get chat with messages {id=} {limit=}")
    if (result := await get_chat_with_msgs(c, id, limit)) is not None:
        return ChatMessagesOut.model_validate_json(result)
    if (result := await select_chat_with_msgs(s, id, limit)) is not None:
        await set_chat_with_msgs(c, id, limit, result)
        return ChatMessagesOut.model_validate(result)
    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@app.post("/chats", status_code=status.HTTP_200_OK)
async def create_chat(s: Annotated[AsyncSession, Depends(get_session)], chat: ChatIn):
    logger.info(f"create chat {chat.title=}")
    await insert_chat(s, chat.title.strip())
    return Response(status_code=status.HTTP_200_OK)


@app.post("/chats/{id}/messages", status_code=status.HTTP_200_OK)
async def create_msg(
    s: Annotated[AsyncSession, Depends(get_session)], id: int, msg: MessageIn
):
    logger.info(f"create msg {id=} {msg.text=}")
    result = await insert_msg_in_chat(s, id, msg.text)
    if result is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_200_OK)


@app.delete("/chats/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(s: Annotated[AsyncSession, Depends(get_session)], id: int):
    logger.info(f"delete chat {id=}")
    await remove_chat(s, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/task_sleep", status_code=status.HTTP_200_OK)
async def task_sleep(time: int):
    logger.info(f"task sleep {time=}")
    async with worker:
        await sleeper.enqueue(time)
    return Response(status_code=status.HTTP_200_OK)
