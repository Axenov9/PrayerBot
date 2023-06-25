from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class admin(Base):

    __tablename__ = 'admin'

    # Параметры церквей
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    name = Column(String)
    level = Column(Integer)

    # def __str__(self):
    #     return self.tg_id
