from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from valkey.asyncio import Valkey

from settings import DB_URL, CH_URL


async def get_session():
    engine = create_async_engine(DB_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as s:
        yield s


async def get_cache():
    yield Valkey.from_url(CH_URL)
