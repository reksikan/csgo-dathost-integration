import datetime
import time

from fastapi import FastAPI
from typing import Optional
import requests

from config import SOURCE_SERVER_ID, API_LOGIN, API_PASSWORD, SERVER_HOST, SERVER_PORT

app = FastAPI()


@app.post('/startgame/')
async def startgame(
        selected_map: str,
        max_rounds: int,
        players1: Optional[str],
        players2: Optional[str],
        team1: str,
        team2: str
):
    try:
        # Create game server
        copied_server = requests.post(
            f'https://dathost.net/api/0.1/game-servers/{SOURCE_SERVER_ID}/duplicate',
            auth=(API_LOGIN, API_PASSWORD)
        ).json()
        print(copied_server)

        # Create match
        match = requests.post(
            f'https://dathost.net/api/0.1/matches',
            data={
                "enable_knife_round": "true",
                "enable_pause": "true",
                "enable_playwin": "false",
                "enable_ready": "true",
                "game_server_id": copied_server['id'],
                "map": selected_map,
                "match_end_webhook_url": f'{SERVER_HOST}:{SERVER_PORT}/endgame/',
                "message_prefix": "CSBANGER",
                "playwin_result_webhook_url": f'{SERVER_HOST}:{SERVER_PORT}/endgame/',
                "round_end_webhook_url": "https://webhook.site/158356bd-dcc4-46d6-9903-4d5b85e0935c",
                "team1_name": team1,
                "team1_steam_ids": players1,
                "team2_name": team2,
                "team2_steam_ids": players2,
            },
            auth=(API_LOGIN, API_PASSWORD)
        ).json()
        print(match)
        requests.post(
            f'https://dathost.net/api/0.1/game-servers/{SOURCE_SERVER_ID}/console',
            data={'line': f'mp_maxrounds {max_rounds}'},
            auth=(API_LOGIN, API_PASSWORD)
        )

        response_data = {
            'ip': copied_server['ip'] + ':' + copied_server['ports']['game'],
            'start_time': datetime.datetime.now(),
            'match': match
        }
        return response_data

    except Exception as ex:
        print(ex)
        return {
            'status': 'Error',
            'Error': ex
            }


@app.get('/endgame/')
async def endgame(**kwargs):
    # Logic after end match

    time.sleep(10)
    requests.delete(
        f'https://dathost.net/api/0.1/game-servers/{kwargs["game_server_id"]}',
        auth=(API_LOGIN, API_PASSWORD)
    )
    return {'status': 'OK'}
