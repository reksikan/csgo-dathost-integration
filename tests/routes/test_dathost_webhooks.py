import pytest
from helpers import create_matches_in_db, get_test_http_self_client
from testdata import MATCH1_SECRET, MATCH_DATHOST_DATA

from clients.fake_dathost_client import FakeDathostClient
from config import (MATCH_END_WEBHOOK_ROUTING_KEY,
                    ROUND_END_WEBHOOK_ROUTING_KEY, WEBHOOK_ROUTS_PREFIX)
from src.common.schemas import MatchDathostSchema
from src.db.db_manager import DbManager
from src.db.models import Match


@pytest.mark.parametrize(
    'dathost_request, secret_key, awaited_status_code',
    (
        (MATCH_DATHOST_DATA, str(MATCH1_SECRET), 200, ),
        (MATCH_DATHOST_DATA, 'imposter-key', 401, ),
    )
)
async def test_round_end_webhook(
    isolate_db_manager: DbManager,
    dathost_request: MatchDathostSchema,
    secret_key: str,
    awaited_status_code: int
):
    fake_dathost_client = FakeDathostClient()
    client = await get_test_http_self_client(isolate_db_manager, fake_dathost_client)

    _ = await create_matches_in_db(isolate_db_manager)

    response = await client.post(
        WEBHOOK_ROUTS_PREFIX + ROUND_END_WEBHOOK_ROUTING_KEY,
        headers={'Authorization': str(secret_key)},
        json=dathost_request.dict()
    )

    assert response.status_code == awaited_status_code
    if response.status_code == 200:
        match = await isolate_db_manager.get_match(MATCH_DATHOST_DATA.id)
        assert match.team1_score == MATCH_DATHOST_DATA.team1_stats['score']
        assert match.team2_score == MATCH_DATHOST_DATA.team2_stats['score']


@pytest.mark.parametrize(
    'dathost_request, secret_key, awaited_status_code',
    (
        (MATCH_DATHOST_DATA, str(MATCH1_SECRET), 200, ),
        (MATCH_DATHOST_DATA, 'imposter-key', 401, ),
    )
)
async def test_match_end_webhook(
    isolate_db_manager: DbManager,
    dathost_request: MatchDathostSchema,
    secret_key: str,
    awaited_status_code: int
):
    fake_dathost_client = FakeDathostClient()
    client = await get_test_http_self_client(isolate_db_manager, fake_dathost_client)

    _ = await create_matches_in_db(isolate_db_manager)

    response = await client.post(
        WEBHOOK_ROUTS_PREFIX + MATCH_END_WEBHOOK_ROUTING_KEY,
        headers={'Authorization': str(secret_key)},
        json=dathost_request.dict()
    )

    assert response.status_code == awaited_status_code
    if response.status_code == 200:
        match = await isolate_db_manager.get_match(MATCH_DATHOST_DATA.id)
        assert match.status == Match.Status.finished
