import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# import sys
# from pathlib import Path
#
# sys.path.append(str(Path(__file__).parent.parent))

from ..main import app, get_db

from ..database import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    future=True
)

AsyncTestingSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    # Создание рабочей среды (до и после тестов)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    # Создание новой сессии для каждого теста
    session = AsyncTestingSessionLocal()

    try:
        return session
    finally:

        #Откатываем изменения
        await session.rollback()
        await session.close()


@pytest.fixture
async def client(db_session):


    print(f'db_session_type: {type(db_session)}')
    # для одмены депенденси функции
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from httpx import ASGITransport
    transport = ASGITransport(app=app)

    test_client = AsyncClient(transport=transport, base_url="http://testserver")

    return test_client




@pytest.fixture(autouse=True)
async def clean(client):
    yield
    app.dependency_overrides.clear()
    await client.aclose()