import uuid

import pytest

from src.api.schemas import CreatedServerSchema, CreateMatchSchema
from src.db.db_manager import DbManager
from src.db.models import Match
from tests.helpers import create_matches_in_db
from tests.testdata import (
    DATHOST_GAME_SERVER_HOST,
    CSGO_MAP,
    PLAYER1,
    PLAYER2,
    PLAYER3,
    PLAYER4,
    TEAM1_NAME,
    TEAM2_NAME, NEW_DATHOST_SERVER, NEW_MATCH_SETTINGS
)


async def test_get_match(isolate_db_manager: DbManager):
    matches = await create_matches_in_db(isolate_db_manager)

    match1 = await isolate_db_manager.get_match(matches[0])
    assert match1

    assert match1.team1_name == TEAM1_NAME
    assert match1.team1_roster == [PLAYER1, PLAYER2]
    assert match1.team2_name == TEAM2_NAME
    assert match1.team2_roster == [PLAYER3, PLAYER4]

    assert match1.selected_map == CSGO_MAP
    assert match1.max_rounds == 15

    assert match1.server_host == DATHOST_GAME_SERVER_HOST




@pytest.mark.parametrize(
    'new_server, new_match, secret_key, match_id',
    (
        (
            NEW_DATHOST_SERVER,
            NEW_MATCH_SETTINGS,
            uuid.uuid4(),
            str(uuid.uuid4()),
        ),
    )
)
async def test_create_match(
    isolate_db_manager: DbManager,
    new_server: CreatedServerSchema,
    new_match: CreateMatchSchema,
    secret_key: uuid.UUID,
    match_id: str
):
    await isolate_db_manager.create_match(new_server, new_match, secret_key, match_id)

    match = await isolate_db_manager.get_match(match_id)
    assert match
    assert match.secret_key == secret_key

    assert match.team1_name == new_match.team1_name
    assert match.team1_roster == new_match.team1_roster
    assert match.team2_name == new_match.team2_name
    assert match.team2_roster == new_match.team2_roster

    assert match.selected_map == new_match.map
    assert match.max_rounds == new_match.max_rounds

    assert match.server_id == new_server.id_
    assert match.server_host == new_server.host



async def test_end_match(isolate_db_manager: DbManager):
    matches = await create_matches_in_db(isolate_db_manager)
    await isolate_db_manager.end_match(matches[0])

    match1 = await isolate_db_manager.get_match(matches[0])
    match2 = await isolate_db_manager.get_match(matches[1])

    assert match1.status == Match.Status.finished
    assert match2.status == Match.Status.in_process


async def test_end_round(isolate_db_manager: DbManager):
    new_team1_score = 0
    new_team2_score = 1
    matches = await create_matches_in_db(isolate_db_manager)
    await isolate_db_manager.update_score(matches[0], new_team1_score, new_team2_score)

    match1 = await isolate_db_manager.get_match(matches[0])

    assert match1.team1_score == new_team1_score
    assert match1.team2_score == new_team2_score