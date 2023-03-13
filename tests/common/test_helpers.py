from src.common.helpers import startgame_settings
from src.db.db_manager import DbManager

from testdata import SERIALIZED_DATHOST_MATCH_SETTINGS, NEW_DATHOST_SERVER, NEW_MATCH_SETTINGS, MATCH1_SECRET


async def test_startgame_settings(isolate_db_manager: DbManager):
    serialized_settings = startgame_settings(NEW_DATHOST_SERVER, NEW_MATCH_SETTINGS, MATCH1_SECRET)
    assert serialized_settings == SERIALIZED_DATHOST_MATCH_SETTINGS
