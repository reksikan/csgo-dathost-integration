import subprocess
import uuid

from sqlalchemy import text, select, update
from aiologger.loggers.json import JsonLogger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import _AsyncSessionContextManager

from .models import Match
from src.api.schemas import CreateMatchSchema, CreatedServerSchema

logger = JsonLogger.with_default_handlers()


class DbManager:

    def __init__(self, async_engine: AsyncEngine):
        self._async_engine = async_engine
        self._async_session = async_sessionmaker(
            self._async_engine,
            expire_on_commit=False,
        )

    async def healthcheck(self) -> bool:
        try:
            async with self.session() as session:
                await session.execute(text('CREATE TEMPORARY TABLE test (testclmn TEXT) ON COMMIT DROP;'))
                return True
        except Exception:
            logger.exception('Database healthcheck failed')
            return False

    def session(self) -> _AsyncSessionContextManager[AsyncSession]:
        return self._async_session.begin()

    async def create_match(
        self,
        server: CreatedServerSchema,
        create_match: CreateMatchSchema,
        secret_key: uuid.UUID,
        match_id: str,
    ) -> Match:
        async with self.session() as session:
            match = Match(
                id=match_id,
                secret_key=secret_key,
                server_id=server.id_,
                server_host=server.host,
                selected_map=create_match.map,
                max_rounds=create_match.max_rounds,
                team1_name=create_match.team1_name,
                team1_roster=create_match.team1_roster,
                team2_name=create_match.team2_name,
                team2_roster=create_match.team2_roster,
            )
            session.add(match)
            return match

    async def end_match(
        self,
        match_id: str,
    ) -> None:
        async with self.session() as session:
            await session.execute(
                update(Match)
                .where(Match.id == match_id)
                .values(status=Match.Status.finished)
            )

    async def update_score(
        self,
        match_id: str,
        team1_score: int,
        team2_score: int,
    ) -> None:
        async with self.session() as session:
            await session.execute(
                update(Match)
                .where(Match.id == match_id)
                .values(
                    team1_score=team1_score,
                    team2_score=team2_score,
                )
            )

    async def get_match(self, match_id: str) -> Match:
        async with self.session() as session:
            return await session.scalar(
                select(Match)
                .where(Match.id == match_id)
            )


def create_db_manager(
    connection_url: str,
    need_migrations: bool = True
) -> DbManager:
    engine = create_async_engine(connection_url)
    if need_migrations:
        subprocess.run(
            'alembic upgrade head',
            check=True,
            shell=True
        )
    return DbManager(engine)
