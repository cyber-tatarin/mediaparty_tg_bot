import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker
from root.db import models
from root.logger.config import logger

load_dotenv(find_dotenv())
logger = logger

engine = create_engine(
        f'{os.getenv("DB_ENGINE")}://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}',
        poolclass=pool.QueuePool, pool_size=10, max_overflow=20, pool_pre_ping=True)

Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    # models.UserPostLike.__table__.create(engine)
    models.Points.__table__.create(engine)
    
    # models.Notification.__table__.drop(engine)
    # models.Points.__table__.drop(engine)
    