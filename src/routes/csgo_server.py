import uuid
from typing import Optional

from aiologger.loggers.json import JsonLogger
from fastapi import APIRouter, Response

from config import MATCH_ROUTING_KEY, MATCH_ROUTS_PREFIX
from src.api.schemas import (CreateMatchResponseSchema, CreateMatchSchema,
                             MatchDataSchema)
from src.clients.dathost_client import DathostClient
from src.db.db_manager import DbManager

logger = JsonLogger.with_default_handlers()


class CsgoServerRouter:

    def __init__(self, dathost_client: DathostClient, db_manager: DbManager):
        self._dathost_client = dathost_client
        self._db_manager = db_manager

        router = APIRouter(prefix=MATCH_ROUTS_PREFIX)
        router.add_api_route(MATCH_ROUTING_KEY, self._start_match, methods=['POST'])
        router.add_api_route(MATCH_ROUTING_KEY, self._match_data, methods=['GET'])
        self._router = router

    async def _start_match(self, match_settings: CreateMatchSchema, response: Response) -> CreateMatchResponseSchema:
        try:
            new_server = await self._dathost_client.create_new_server_from_copy()
            secret_key = uuid.uuid4()
            new_match = await self._dathost_client.create_and_setup_match(new_server, match_settings, secret_key)
            match = await self._db_manager.create_match(new_server, match_settings, secret_key, new_match.id_)

            return CreateMatchResponseSchema(match=MatchDataSchema(**dict(match)))
        except Exception:
            await logger.exception('Got exception on server create')
            response.status_code = 500
            return CreateMatchResponseSchema(
                status='error',
                error='Error on creating match',
            )

    async def _match_data(self, match_id: str, response: Response) -> Optional[MatchDataSchema]:
        if match := await self._db_manager.get_match(match_id):
            return MatchDataSchema(**match.__dict__)
        else:
            response.status_code = 404
            return None

    @property
    def router(self):
        return self._router
