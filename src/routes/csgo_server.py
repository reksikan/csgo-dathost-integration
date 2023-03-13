import uuid
from typing import Optional

from aiologger.loggers.json import JsonLogger
from fastapi import APIRouter, Response, status

from config import MATCH_ROUTING_KEY, MATCH_ROUTS_PREFIX
from src.clients.dathost_client import DathostClient
from src.common.schemas import (CreateMatchRequestSchema,
                                CreateMatchResponseSchema, MatchDataSchema)
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

    async def _start_match(
        self,
        match_settings: CreateMatchRequestSchema,
        response: Response
    ) -> CreateMatchResponseSchema:
        try:
            new_server = await self._dathost_client.create_new_server_from_copy()
            secret_key = uuid.uuid4()
            new_match = await self._dathost_client.create_and_setup_match(new_server, match_settings, secret_key)
            match = await self._db_manager.create_match(new_server, match_settings, secret_key, new_match.id)

            return CreateMatchResponseSchema(match=MatchDataSchema(**match.__dict__))
        except Exception as ex:
            raise ex
            await logger.exception('Got exception on server create')
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return CreateMatchResponseSchema(
                status='error',
                error='Error on creating match',
            )

    async def _match_data(self, match_id: str, response: Response) -> Optional[MatchDataSchema]:
        match = await self._db_manager.get_match(match_id)
        if match:
            return MatchDataSchema(**match.__dict__)
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return None

    @property
    def router(self):
        return self._router
