import os

import loguru
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

log_file_path = os.path.abspath(os.path.join('root', 'bot.log'))
print(log_file_path)
logger = loguru.logger
logger.add("bot.log", format="{time} {level} {message}", level=os.getenv('LOG_LEVEL'),
           rotation="10 MB", compression="zip")
