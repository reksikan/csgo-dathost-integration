import uuid
from typing import Any, Dict, Optional, Tuple

from aiohttp import BasicAuth
from aiohttp.client import ClientSession
from aiologger.loggers.json import JsonLogger

from config import (DATHOST_LOGIN, DATHOST_PASSWORD, DATHOST_URL,
                    SOURCE_SERVER_ID, STEAM_TOKEN)
from src.common.helpers import startgame_settings
from src.common.schemas import (CreatedServerSchema, CreateMatchRequestSchema,
                                MatchDathostSchema)

logger = JsonLogger.with_default_handlers()


class DathostException(Exception):
    pass


class DathostClient:

    def __init__(self):
        self._dathost_auth = BasicAuth(DATHOST_LOGIN, DATHOST_PASSWORD)

    async def _make_http_dathost_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        awaited_result_code: Tuple[int] = (200, 201),
    ) -> Dict[str, Any]:
        async with ClientSession as client:
            await logger.info(f'Making http request to dathost with {path=} {method=} {params=} {data=}')
            async with client.request(
                method=method,
                url=DATHOST_URL + path,
                params=params or {},
                json_serialize=data or {},
                auth=self._dathost_auth,
            ) as response:
                if response.status not in awaited_result_code:
                    raise DathostException(f'Error on http request {path=} {method=}')

                content = await response.json()
                logger.info(f'Got response for {path=} {method=} {content=}')
                return content

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
            id=copied_server['id'],
            host=copied_server['ip'] + ':' + str(copied_server['ports']['game']),
        )

    async def _create_match_on_server(
        self,
        server: CreatedServerSchema,
        match: CreateMatchRequestSchema,
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
        match: CreateMatchRequestSchema,
        secret_key: uuid.UUID,
    ):
        new_match = await self._create_match_on_server(server, match, secret_key)
        await self._set_up_new_match(server.id, max_rounds=match.max_rounds)
        return new_match
