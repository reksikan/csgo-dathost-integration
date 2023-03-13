import uvicorn
from fastapi import FastAPI

from config import POSTGRES_URL, SERVER_HOST, SERVER_PORT
from src.api.http_server import HTTPServer
from src.clients.dathost_client import DathostClient
from src.db.db_manager import create_db_manager


def get_app() -> FastAPI:
    db_manager = create_db_manager(POSTGRES_URL)
    datahost_client = DathostClient()

    http_server = HTTPServer(datahost_client, db_manager)
    return http_server.app


if __name__ == '__main__':
    uvicorn.run(get_app(), host=SERVER_HOST, port=SERVER_PORT)
