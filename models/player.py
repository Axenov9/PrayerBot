from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from sqlalchemy.orm import declarative_base

# from models.level import level
Base = declarative_base()


class player(Base):
    # Уровни церквей, их привилегии
    __tablename__ = 'player'

    # Параметры церквей
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    chat_id = Column(Integer)
    player_level = Column(Integer)
    purse = Column(Integer)
    last_pray = Column(Integer)
    name = Column(String)

    # def __str__(self):
    #     return f"{self.tg_id}"
