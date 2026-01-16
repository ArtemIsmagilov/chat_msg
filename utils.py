from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import valkey

from settings import DB_URL, CH_URL


@contextmanager
def get_session():
    engine = create_engine(DB_URL, echo=True)
    session = sessionmaker(engine, expire_on_commit=False)
    with session() as s:
        yield s


@contextmanager
def get_cache():
    yield valkey.from_url(CH_URL)
