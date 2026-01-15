from datetime import datetime

from sqlalchemy import create_engine, desc, select, func, delete
import sqlalchemy
from models import Base, Chat, Message
from settings import DB_URL
from utils import get_session


def init_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)


def select_chat_with_msgs(id: int, limit: int):
    with get_session() as s:
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
        return s.scalar(stmt)


def insert_chat(title: str):
    with get_session() as s:
        s.add(Chat(title=title, created_at=datetime.now()))
        s.commit()


def insert_msg_in_chat(id: int, text: str):
    with get_session() as s:
        s.add(Message(chat_id=id, text=text, created_at=datetime.now()))
        try:
            s.commit()
        except sqlalchemy.exc.IntegrityError:
            return False
        else:
            return True


def remove_chat(id: int):
    with get_session() as s:
        s.execute(delete(Chat).where(Chat.id == id))
        s.commit()
