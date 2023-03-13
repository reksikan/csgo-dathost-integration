from typing import Any, Dict, Optional

import pytest
from testdata import (CREATE_MATCH_DATA, DATHOST_GAME_SERVER_IP,
                      DATHOST_GAME_SERVER_PROT, MATCH1_ID,
                      MATCH1_RESPONSE_DATA, MATCH_DATHOST_DATA, SERVER_ID)

from config import MATCH_ROUTING_KEY, MATCH_ROUTS_PREFIX, SOURCE_SERVER_ID
from src.common.schemas import (CreateMatchRequestSchema,
                                CreateMatchResponseSchema)
from src.db.db_manager import DbManager
from tests.clients.fake_dathost_client import FakeDathostClient
from tests.helpers import create_matches_in_db, get_test_http_self_client


@pytest.mark.parametrize(
    'start_match_settings, awaited_status_code, awaited_content',
    (
        (
            CREATE_MATCH_DATA,
            200,
            CreateMatchResponseSchema(
                status='OK',
                match=MATCH1_RESPONSE_DATA
            ).dict()
        ),
    )
)
async def test_create_match(
    isolate_db_manager: DbManager,
    start_match_settings: CreateMatchRequestSchema,
    awaited_status_code: int,
    awaited_content: Dict[str, Any],
):
    fake_dathost_client = FakeDathostClient()
    fake_dathost_client.response_dict[('POST', f'/game-servers/{SOURCE_SERVER_ID}/duplicate')] = {
        'id': SERVER_ID,
        'ip': DATHOST_GAME_SERVER_IP,
        'ports': {'game': DATHOST_GAME_SERVER_PROT}
    }
    fake_dathost_client.response_dict[('POST', '/matches')] = MATCH_DATHOST_DATA.dict()

    client = await get_test_http_self_client(isolate_db_manager, fake_dathost_client)

    response = await client.post(
        MATCH_ROUTS_PREFIX + MATCH_ROUTING_KEY,
        json=start_match_settings.dict()
    )

    assert response.json() == awaited_content
    assert response.status_code == awaited_status_code


@pytest.mark.parametrize(
    'match_id, awaited_status_code, awaited_content',
    (
        (MATCH1_ID, 200, MATCH1_RESPONSE_DATA.dict()),
        ('random_id', 404, None),
    )
)
async def test_match_data(
    isolate_db_manager: DbManager,
    match_id: str,
    awaited_status_code: int,
    awaited_content: Optional[Dict[str, Any]]
):
    fake_dathost_client = FakeDathostClient()
    _ = await create_matches_in_db(isolate_db_manager)
    client = await get_test_http_self_client(isolate_db_manager, fake_dathost_client)

    response = await client.get(MATCH_ROUTS_PREFIX + MATCH_ROUTING_KEY, params={'match_id': match_id})

    assert response.status_code == awaited_status_code
    assert response.json() == awaited_content
