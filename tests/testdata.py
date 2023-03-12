import uuid

from src.api.schemas import CreateMatchSchema, CreatedServerSchema

DATHOST_GAME_SERVER_HOST = '222.222.222.222:2222'
CSGO_MAP = 'de_dust2'

PLAYER1 = 'STEAM8:13213'
PLAYER2 = 'STEAM4:11231'
PLAYER3 = 'STEAM5:74364'
PLAYER4 = 'STEAM2:55555'

TEAM1_NAME = 'navi'
TEAM2_NAME = 'faze'

NEW_DATHOST_SERVER = CreatedServerSchema(id_=str(uuid.uuid4()), host=DATHOST_GAME_SERVER_HOST)
NEW_MATCH_SETTINGS = CreateMatchSchema(
    max_rounds=15,
    map=CSGO_MAP,
    team1_roster=[PLAYER1, PLAYER2],
    team1_name=TEAM1_NAME,
    team2_roster=[PLAYER3, PLAYER4],
    team2_name=TEAM2_NAME,
)