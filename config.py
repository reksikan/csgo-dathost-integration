from os import getenv

# Server settings
SERVER_PORT = int(getenv('SERVER_PORT', '8000'))
SERVER_HOST = getenv('SERVER_HOST', '127.0.0.1')

# Routes
MATCH_ROUTS_PREFIX = '/match'
MATCH_ROUTING_KEY = '/create'

WEBHOOK_ROUTS_PREFIX = '/dathost'
MATCH_END_WEBHOOK_ROUTING_KEY = '/match_end/'
ROUND_END_WEBHOOK_ROUTING_KEY = '/round_end/'

MATCH_END_WEBHOOK = f'{SERVER_HOST}:{str(SERVER_PORT)}' + WEBHOOK_ROUTS_PREFIX + MATCH_END_WEBHOOK_ROUTING_KEY
ROUND_END_WEBHOOK = f'{SERVER_HOST}:{str(SERVER_PORT)}' + WEBHOOK_ROUTS_PREFIX + ROUND_END_WEBHOOK_ROUTING_KEY

# Csgo serves
STEAM_TOKEN = getenv('STEAM_TOKEN')
SOURCE_SERVER_ID = '6198112a4b5e144c0d52d0b5'

# Dathost settings
DATHOST_LOGIN = getenv('API_LOGIN', 'Login')
DATHOST_PASSWORD = getenv('API_PASSWORD', 'Password')
DATHOST_URL = 'https://dathost.net/api/0.1'

# Database settings
POSTGRES_HOST = getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = getenv('POSTGRES_PORT', '5432')
POSTGRES_LOGIN = getenv('POSTGRES_LOGIN', 'postgres')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DATABASE = getenv('POSTGRES_DATABASE', 'csgoapi')
POSTGRES_URL = (
    f'postgresql+asyncpg://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'
)

POSTGRES_TEST_DATABASE = getenv('POSTGRES_TEST_DATABASE', 'test_' + POSTGRES_DATABASE)
POSTGRES_TEST_URL = (
    f'postgresql+asyncpg://'
    f'{POSTGRES_LOGIN}:'
    f'{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:'
    f'{POSTGRES_PORT}/'
    f'{POSTGRES_TEST_DATABASE}'
)
