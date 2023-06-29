from sqlalchemy import Column, String, Boolean, Date, Integer
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Base(DeclarativeBase):
    pass


# храним состояние о юзере, чтобы восстановить в случае отключения бота
class State(Base):
    __tablename__ = "states"
    
    tg_id = Column("tg_id", String(12), primary_key=True)
    state = Column("state", String(60))


# храним состояние о юзере, чтобы восстановить в случае отключения бота
class UserPostLike(Base):
    __tablename__ = "user_post_like"
    
    tg_id = Column("tg_id", String(12), primary_key=True)
    post_message_id = Column("post_message_id", String(14), primary_key=True)


class Points(Base):
    __tablename__ = "points"
    
    tg_id = Column("tg_id", String(12), primary_key=True)
    score = Column("score", Integer)
