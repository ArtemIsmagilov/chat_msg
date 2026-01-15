from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DB_URL


@contextmanager
def get_session():
    engine = create_engine(DB_URL, echo=True)
    session = sessionmaker(engine, expire_on_commit=False)
    with session() as s:
        yield s
