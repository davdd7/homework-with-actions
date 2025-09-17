from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL, echo=True)

# noinspection PyTypeChecker
async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
