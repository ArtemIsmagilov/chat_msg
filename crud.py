from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import desc, select, func, delete
import sqlalchemy
from models import Base, Chat, Message
from settings import DB_URL


async def init_db():
    engine = create_async_engine(DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def select_chat_with_msgs(s: AsyncSession, id: int, limit: int):
    cte = (
        select(Message)
        .where(Message.chat_id == id)
        .limit(limit)
        .order_by(desc(Message.created_at))
        .cte()
    )
    sq = (
        select(func.json_agg(cte.table_valued()).label("messages"), Chat)
        .where(Chat.id == id)
        .group_by(Chat.id)
        .subquery()
    )
    stmt = select(func.to_json(sq.table_valued()))
    return await s.scalar(stmt)


async def insert_chat(s: AsyncSession, title: str):
    s.add(Chat(title=title, created_at=datetime.now()))
    await s.commit()


async def insert_msg_in_chat(s: AsyncSession, id: int, text: str):
    s.add(Message(chat_id=id, text=text, created_at=datetime.now()))
    try:
        await s.commit()
    except sqlalchemy.exc.IntegrityError:
        return False
    else:
        return True


async def remove_chat(s: AsyncSession, id: int):
    await s.execute(delete(Chat).where(Chat.id == id))
    await s.commit()
