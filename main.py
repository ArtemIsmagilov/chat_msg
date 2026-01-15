from typing import Annotated

from fastapi import FastAPI, Query, status, HTTPException

from schema import ChatIn, ChatMessagesResponse, MessageIn
from crud import insert_chat, select_chat_with_msgs, insert_msg_in_chat, remove_chat
from logger import logger


app = FastAPI()


@app.get(
    "/chats/{id}", status_code=status.HTTP_200_OK, response_model=ChatMessagesResponse
)
async def get_chat_with_messages(
    id: int,
    limit: Annotated[int, Query(ge=20, le=100)] = 20,
):
    logger.info(f"get chat with messages {id=} {limit=}")
    result = select_chat_with_msgs(id, limit)
    if result is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    return ChatMessagesResponse.model_validate(result)


@app.post("/chats", status_code=status.HTTP_200_OK)
async def create_chat(chat: ChatIn):
    logger.info(f"create chat {chat.title=}")
    insert_chat(chat.title.strip())


@app.post("/chats/{id}/messages", status_code=status.HTTP_200_OK)
async def create_msg(id: int, msg: MessageIn):
    logger.info(f"create msg {id=} {msg.text=}")
    result = insert_msg_in_chat(id, msg.text)
    if result is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@app.delete("/chats/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(id: int):
    logger.info(f"delete chat {id=}")
    remove_chat(id)
