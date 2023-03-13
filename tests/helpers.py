from typing import List

from httpx import AsyncClient
from testdata import (CSGO_MAP, CSGO_MAX_ROUNDS, DATHOST_GAME_SERVER_HOST,
                      MATCH1_ID, MATCH1_SECRET, MATCH2_ID, MATCH2_SECRET,
                      PLAYER1, PLAYER2, PLAYER3, PLAYER4, SERVER_ID,
                      TEAM1_NAME, TEAM2_NAME)

from config import SERVER_HOST, SERVER_PORT
from src.api.http_server import HTTPServer
from src.clients.dathost_client import DathostClient
from src.db.db_manager import DbManager
from src.db.models import Match


async def create_matches_in_db(db_manager: DbManager) -> List[str]:
    match1 = Match(
        id=MATCH1_ID,
        secret_key=MATCH1_SECRET,
        server_id=SERVER_ID,
        server_host=DATHOST_GAME_SERVER_HOST,
        map=CSGO_MAP,
        max_rounds=CSGO_MAX_ROUNDS,
        team1_name=TEAM1_NAME,
        team1_roster=[PLAYER1, PLAYER2],
        team2_name=TEAM2_NAME,
        team2_roster=[PLAYER3, PLAYER4],
    )

    match2 = Match(
        id=MATCH2_ID,
        secret_key=MATCH2_SECRET,
        server_id=SERVER_ID,
        server_host=DATHOST_GAME_SERVER_HOST,
        map=CSGO_MAP,
        max_rounds=CSGO_MAX_ROUNDS,
        team1_name=TEAM1_NAME,
        team1_roster=[PLAYER1, PLAYER2],
        team2_name=TEAM2_NAME,
        team2_roster=[PLAYER3, PLAYER4],
    )
    async with db_manager.session() as session:
        session.add(match1)
        session.add(match2)
        await session.commit()
        return [MATCH1_ID, MATCH2_ID]


async def get_test_http_self_client(db_manager: DbManager, dathost_client: DathostClient) -> AsyncClient:
    app = HTTPServer(db_manager=db_manager, dathost_client=dathost_client).app
    return AsyncClient(app=app, base_url=f'http://{SERVER_HOST}:{SERVER_PORT}')
