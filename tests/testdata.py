import uuid

from config import MATCH_END_WEBHOOK, ROUND_END_WEBHOOK
from src.common.schemas import (CreatedServerSchema, CreateMatchRequestSchema,
                                MatchDataSchema, MatchDathostSchema)

SERVER_ID = 'dc1cfc0c-5bfe-4cb2-9fdc-98680935d940'

MATCH1_ID = '477a6924-6ef2-47fc-8cb2-ed03f17abef9'
MATCH1_SECRET = uuid.UUID('67fbd589-276a-4fb8-b647-bc262af5514b')

MATCH2_ID = '9e12b826-431e-4d61-b93d-3eeee42bb294'
MATCH2_SECRET = uuid.UUID('8d6d525a-421e-497c-afe6-398494ebc3b2')

DATHOST_GAME_SERVER_IP = '222.222.222.222'
DATHOST_GAME_SERVER_PROT = '2222'
DATHOST_GAME_SERVER_HOST = F'{DATHOST_GAME_SERVER_IP}:{DATHOST_GAME_SERVER_PROT}'
CSGO_MAP = 'de_dust2'
CSGO_MAX_ROUNDS = 15

PLAYER1 = 'STEAM8:13213'
PLAYER2 = 'STEAM4:11231'
PLAYER3 = 'STEAM5:74364'
PLAYER4 = 'STEAM2:55555'

TEAM1_NAME = 'navi'
TEAM1_ROSTER = [PLAYER1, PLAYER2]
TEAM2_NAME = 'faze'
TEAM2_ROSTER = [PLAYER3, PLAYER4]


NEW_DATHOST_SERVER = CreatedServerSchema(id=SERVER_ID, host=DATHOST_GAME_SERVER_HOST)
NEW_MATCH_SETTINGS = CreateMatchRequestSchema(
    max_rounds=CSGO_MAX_ROUNDS,
    map=CSGO_MAP,
    team1_roster=TEAM1_ROSTER,
    team1_name=TEAM1_NAME,
    team2_roster=TEAM2_ROSTER,
    team2_name=TEAM2_NAME,
)

SERIALIZED_DATHOST_MATCH_SETTINGS = {
    'enable_knife_round': 'true',
    'enable_pause': 'true',
    'enable_playwin': 'false',
    'enable_ready': 'true',
    'game_server_id': SERVER_ID,
    'map': CSGO_MAP,
    'match_end_webhook_url': MATCH_END_WEBHOOK,
    'message_prefix': 'CSBANGER',
    'playwin_result_webhook_url': '',
    'round_end_webhook_url': ROUND_END_WEBHOOK,
    'team1_name': TEAM1_NAME,
    'team1_steam_ids': TEAM1_ROSTER,
    'team2_name': TEAM2_NAME,
    'team2_steam_ids': TEAM2_ROSTER,
    'webhook_authorization_header': MATCH1_SECRET
}

MATCH1_RESPONSE_DATA = MatchDataSchema(
    id=MATCH1_ID,
    server_id=SERVER_ID,
    server_host=DATHOST_GAME_SERVER_HOST,
    max_rounds=CSGO_MAX_ROUNDS,
    map=CSGO_MAP,
    team1_roster=TEAM1_ROSTER,
    team1_name=TEAM1_NAME,
    team1_score=0,
    team2_roster=TEAM2_ROSTER,
    team2_name=TEAM2_NAME,
    team2_score=0,
)

CREATE_MATCH_DATA = CreateMatchRequestSchema(
    max_rounds=CSGO_MAX_ROUNDS,
    map=CSGO_MAP,
    team1_roster=TEAM1_ROSTER,
    team1_name=TEAM1_NAME,
    team2_roster=TEAM2_ROSTER,
    team2_name=TEAM2_NAME,
)

MATCH_CREATED_DATHOST_RESPONSE = MatchDathostSchema(
    id=MATCH1_ID,
    server_id=SERVER_ID,
    map=CSGO_MAP,
    connect_time=300,
    warmup_time=300,
    team1_start_ct=True,
    team1_steam_ids=TEAM1_ROSTER,
    team1_coaches=[],
    team1_name=TEAM1_NAME,
    team1_flag='',
    team2_start_ct=False,
    team2_steam_ids=TEAM2_ROSTER,
    team2_coaches=[],
    team2_name=TEAM2_NAME,
    team2_flag='',
    spectator_steam_ids=[],
    wait_for_coaches=False,
    wait_for_spectators=False,
    round_end_webhook_url=ROUND_END_WEBHOOK,
    match_end_webhook_url=MATCH_END_WEBHOOK,
    started=True,
    finished=False,
    cancel_reason='',
    rounds_played=0,
    team1_stats=[],
    team2_stats=[],
    player_stats=[],
    enable_knife_round=True,
    enable_pause=True,
    enable_playwin=False,
    playwin_result_webhook_url='',
    playwin_result='',
    ready_min_players=10,
    enable_tech_pause=True,
    message_prefix='CSBANGER',
)
