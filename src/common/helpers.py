import uuid

from src.api.schemas import CreatedServerSchema, CreateMatchSchema
from config import MATCH_END_WEBHOOK, ROUND_END_WEBHOOK


def startgame_settings(
    server: CreatedServerSchema,
    match: CreateMatchSchema,
    secret_key: uuid.UUID,
):
    return {
        "enable_knife_round": "true",
        "enable_pause": "true",
        "enable_playwin": "false",
        "enable_ready": "true",
        "game_server_id": server.id_,
        "map": match.map,
        "match_end_webhook_url": MATCH_END_WEBHOOK,
        "message_prefix": "CSBANGER",
        "playwin_result_webhook_url": '',
        "round_end_webhook_url": ROUND_END_WEBHOOK,
        "team1_name": match.team1_name,
        "team1_steam_ids": match.team1_roster,
        "team2_name": match.team2_name,
        "team2_steam_ids": match.team2_roster,
        "webhook_authorization_header": secret_key
    }
