from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient
from testdata import MATCH1_ID, MATCH1_RESPONSE_DATA

from config import (MATCH_ROUTING_KEY, MATCH_ROUTS_PREFIX, SERVER_HOST,
                    SERVER_PORT)
from src.api.http_server import HTTPServer
from src.db.db_manager import DbManager
from tests.clients.fake_dathost_client import FakeDathostClient
from tests.helpers import create_matches_in_db


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

    app = HTTPServer(db_manager=isolate_db_manager, dathost_client=fake_dathost_client).app
    async with AsyncClient(app=app, base_url=f'http://{SERVER_HOST}:{SERVER_PORT}') as client:
        response = await client.get(MATCH_ROUTS_PREFIX + MATCH_ROUTING_KEY, params={'match_id': match_id})

    assert response.status_code == awaited_status_code
    assert response.json() == awaited_content
