from fastapi import FastAPI, Request, Response

from src.clients.dathost_client import DathostClient
from src.db.db_manager import DbManager
from src.routes.csgo_server import CsgoServerRouter
from src.routes.dathost_webhooks import DathostWebhookRouter


class HTTPServer:

    def __init__(self, dathost_client: DathostClient, db_manager: DbManager):
        self._dathost_client = dathost_client
        self._db_manager = db_manager

        app = FastAPI()
        csgo_server_router = CsgoServerRouter(dathost_client, db_manager)
        dathost_webhook_router = DathostWebhookRouter(dathost_client, db_manager)

        app.include_router(csgo_server_router.router)
        app.include_router(dathost_webhook_router.router)
        app.router.add_api_route('/ping/', self.ping)

        self._app = app

    @property
    def app(self):
        return self._app

    async def ping(self, _: Request):
        await self._db_manager.healthcheck()
        return Response(status_code=200)
