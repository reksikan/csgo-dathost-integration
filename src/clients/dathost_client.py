import uuid
from typing import Any, Optional

from aiologger.loggers.json import JsonLogger
from aiohttp import BasicAuth
from aiohttp.client import ClientSession

from src.common.helpers import startgame_settings
from config import (
    DATHOST_LOGIN,
    DATHOST_URL,
    DATHOST_PASSWORD, SOURCE_SERVER_ID, STEAM_TOKEN,
)
from src.api.schemas import CreatedServerSchema, MatchDathostSchema, CreateMatchSchema

logger = JsonLogger.with_default_handlers()


class DathostClient:

    def __init__(self):
        self._dathost_auth = BasicAuth(DATHOST_LOGIN, DATHOST_PASSWORD)

    async def _make_http_dathost_request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> dict:
        async with ClientSession as client:
            await logger.info(f'Making http request to dathost with {path=} {method=} {params=} {data=}')
            async with client.request(
                method=method,
                url=DATHOST_URL + path,
                params=params or {},
                json_serialize=data or {},
                auth=self._dathost_auth,
            ) as response:
                return await response.json()

    async def create_new_server_from_copy(self) -> CreatedServerSchema:
        copied_server = await self._make_http_dathost_request(
            'POST',
            f'/game-servers/{SOURCE_SERVER_ID}/duplicate',
        )
        await self._make_http_dathost_request(
            'PUT',
            f'/game-servers/{copied_server["id"]}',
            data={'csgo_settings.steam_game_server_login_token': STEAM_TOKEN},
        )
        return CreatedServerSchema(
            server_id=copied_server['id'],
            server_host=copied_server['ip'] + ':' + str(copied_server['ports']['game']),
        )

    async def _create_match_on_server(
        self,
        server: CreatedServerSchema,
        match: CreateMatchSchema,
        secret_key: uuid.UUID,
    ) -> MatchDathostSchema:
        return MatchDathostSchema(**await self._make_http_dathost_request(
            method='POST',
            path='/matches',
            data=startgame_settings(server, match, secret_key),
        ))

    async def _set_up_new_match(
        self,
        server_id: str,
        max_rounds: int
    ):
        await self._make_http_dathost_request(
            method='POST',
            path=f'game-servers/{server_id}/console',
            data={'line': f'mp_maxrounds {max_rounds}'},
        )

    async def create_and_setup_match(
        self,
        server: CreatedServerSchema,
        match: CreateMatchSchema,
        secret_key: uuid.UUID,
    ):
        new_match = await self._create_match_on_server(server, match, secret_key)
        await self._set_up_new_match(server.id_, max_rounds=match.max_rounds)
        return new_match