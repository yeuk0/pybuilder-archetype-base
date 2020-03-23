# TODO BORRAR
# Se recomienda importar estas variables con:
#   from config import constants as const
# Las variables se declararán en mayúsculas:
# 	DB_USER = 'user'

from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

LOG_FOLDER_PATH = BASE_PATH / 'logs'
TEST_PATH = BASE_PATH / 'tests'
