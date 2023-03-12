import uuid

from fastapi import APIRouter, Response
from aiologger.loggers.json import JsonLogger

from config import MATCH_ROUTS_PREFIX, MATCH_ROUTING_KEY
from src.db.db_manager import DbManager
from src.clients.dathost_client import DathostClient
from src.api.schemas import CreateMatchSchema, CreateMatchResponseSchema, MatchDataSchema

logger = JsonLogger.with_default_handlers()


class CsgoServerRouter:

    def __init__(self, dathost_client: DathostClient, db_manager: DbManager):
        self._dathost_client = dathost_client
        self._db_manager = db_manager

        router = APIRouter(prefix=MATCH_ROUTS_PREFIX)
        router.add_api_route(
            MATCH_ROUTING_KEY,
            self._start_match,
            methods=['POST'],
            response_model=CreateMatchResponseSchema
        )
        router.add_api_route(MATCH_ROUTING_KEY, self._match_data, methods=['GET'], response_model=MatchDataSchema)
        self._router = router


    async def _start_match(self, match_settings: CreateMatchSchema) -> Response:
        try:
            new_server = await self._dathost_client.create_new_server_from_copy()
            secret_key = uuid.uuid4()
            new_match = await self._dathost_client.create_and_setup_match(new_server, match_settings, secret_key)
            match = await self._db_manager.create_match(new_server, match_settings, secret_key, new_match.id_)

            return Response(CreateMatchResponseSchema(match=MatchDataSchema(**dict(match))))
        except Exception:
            await logger.exception(f'Got exception on server create')
            return Response(
                content=CreateMatchResponseSchema(
                    status='error',
                    error='Error on creating match',
                ),
                status_code=500,
            )


    async def _match_data(self, match_id: str) -> Response:
        if match := await self._db_manager.get_match(match_id):
            return Response(MatchDataSchema(**dict(match)))
        else:
            return Response(status_code=404)

    @property
    def router(self):
        return self._router
