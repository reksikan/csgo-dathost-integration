import pytest

from config import POSTGRES_TEST_URL
from src.db.db_manager import create_db_manager
from src.db.models import Base


@pytest.fixture(scope='function')
async def isolate_db_manager():
    db_manager = create_db_manager(POSTGRES_TEST_URL, need_migrations=False)

    async with db_manager._async_engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)

    yield db_manager

    async with db_manager._async_engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
