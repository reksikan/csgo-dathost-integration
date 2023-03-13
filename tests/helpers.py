import uuid
from typing import List

from testdata import (
    MATCH1_ID,
    MATCH2_ID,
    MATCH1_SECRET,
    MATCH2_SECRET,
    SERVER_ID,
    CSGO_MAP,
    DATHOST_GAME_SERVER_HOST,
    PLAYER1,
    PLAYER2,
    PLAYER3,
    PLAYER4,
    TEAM1_NAME,
    TEAM2_NAME, CSGO_MAX_ROUNDS
)

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
