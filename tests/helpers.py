import uuid
from typing import List

from testdata import (CSGO_MAP, DATHOST_GAME_SERVER_HOST, PLAYER1, PLAYER2,
                      PLAYER3, PLAYER4, TEAM1_NAME, TEAM2_NAME)

from src.db.db_manager import DbManager
from src.db.models import Match


async def create_matches_in_db(db_manager: DbManager) -> List[str]:
    match1_id = str(uuid.uuid4())
    match1 = Match(
        id=match1_id,
        secret_key=uuid.uuid4(),
        server_id=str(uuid.uuid4()),
        server_host=DATHOST_GAME_SERVER_HOST,
        selected_map=CSGO_MAP,
        max_rounds=15,
        team1_name=TEAM1_NAME,
        team1_roster=[PLAYER1, PLAYER2],
        team2_name=TEAM2_NAME,
        team2_roster=[PLAYER3, PLAYER4],
    )

    match2_id = str(uuid.uuid4())
    match2 = Match(
        id=match2_id,
        secret_key=uuid.uuid4(),
        server_id=str(uuid.uuid4()),
        server_host=DATHOST_GAME_SERVER_HOST,
        selected_map=CSGO_MAP,
        max_rounds=15,
        team1_name=TEAM1_NAME,
        team1_roster=[PLAYER1, PLAYER2],
        team2_name=TEAM2_NAME,
        team2_roster=[PLAYER3, PLAYER4],
    )
    async with db_manager.session() as session:
        session.add(match1)
        session.add(match2)
        await session.commit()
        return [match1_id, match2_id]
