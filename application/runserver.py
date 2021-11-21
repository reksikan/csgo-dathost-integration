from uvicorn import run

import config

if __name__ == '__main__':
    run('views:app',
        port=config.SERVER_PORT,
        host=config.SERVER_HOST,
        reload=True)

