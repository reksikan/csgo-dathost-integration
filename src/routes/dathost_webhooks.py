from fastapi import APIRouter, Header, Response

from config import (MATCH_END_WEBHOOK_ROUTING_KEY,
                    ROUND_END_WEBHOOK_ROUTING_KEY, WEBHOOK_ROUTS_PREFIX)
from src.api.schemas import MatchDathostSchema
from src.clients.dathost_client import DathostClient
from src.db.db_manager import DbManager


class DathostWebhookRouter:

    def __init__(
        self,
        dathost_client: DathostClient,
        db_manager: DbManager,
    ):
        self._dathost_client = dathost_client
        self._db_manager = db_manager

        router = APIRouter(prefix=WEBHOOK_ROUTS_PREFIX)
        router.add_api_route(MATCH_END_WEBHOOK_ROUTING_KEY, self._match_ended)
        router.add_api_route(ROUND_END_WEBHOOK_ROUTING_KEY, self._round_ended)
        self._router = router

    async def _match_ended(
        self,
        updated_match: MatchDathostSchema,
        authorization: str = Header(default=''),
    ) -> Response:
        match = await self._db_manager.get_match(updated_match.id_)
        if match and match.secret_key == authorization:
            await self._db_manager.end_match(match.id)
            return Response()
        else:
            Response(status_code=401)

    async def _round_ended(
        self,
        updated_match: MatchDathostSchema,
        authorization: str = Header(default=''),
    ) -> Response:
        match = await self._db_manager.get_match(updated_match.id_)
        if match and match.secret_key == authorization:
            await self._db_manager.update_score(
                match.id,
                team1_score=updated_match.team1_stats['score'],
                team2_score=updated_match.team2_stats['score'],
            )
            return Response()
        else:
            Response(status_code=401)

    @property
    def router(self):
        return self._router
