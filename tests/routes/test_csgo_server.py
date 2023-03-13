from typing import Any, Dict

import pytest
from starlette.testclient import TestClient

from src.api.http_server import HTTPServer
from src.db.db_manager import DbManager
from testdata import MATCH1_ID, MATCH1_RESPONSE_DATA
from tests.clients.fake_dathost_client import FakeDathostClient
from tests.helpers import create_matches_in_db
from config import MATCH_ROUTS_PREFIX, MATCH_ROUTING_KEY

@pytest.mark.parametrize(
    'match_id, awaited_status_code, awaited_content',
    (
        (MATCH1_ID, 200, MATCH1_RESPONSE_DATA.dict()),
        ('ranodm_id', 404, {}),
    )
)
async def test_match_data(
    isolate_db_manager: DbManager,
    match_id: str,
    awaited_status_code: int,
    awaited_content: Dict[str, Any]
):
    fake_dathost_client = FakeDathostClient()
    app = HTTPServer(db_manager=isolate_db_manager, dathost_client=fake_dathost_client).app()
    client = TestClient(app)

    _ = await create_matches_in_db(isolate_db_manager)

    response = client.get(MATCH_ROUTS_PREFIX + MATCH_ROUTING_KEY)

    assert response.status_code == awaited_status_code
    assert response.json() == awaited_content
