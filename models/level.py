from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class level(Base):
    # Уровни церквей, их привелегии
    __tablename__ = 'level'

    # Параметры церквей
    id = Column(Integer, primary_key=True)
    cost = Column(Integer)
    income = Column(Integer)

    def __str__(self):
        return self.name
