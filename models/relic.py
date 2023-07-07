from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from sqlalchemy.orm import declarative_base

# from models.level import level
Base = declarative_base()


class relic(Base):

    __tablename__ = 'relic'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    multiplier = Column(Integer)
    level_req = Column(Integer)
    price = Column(Integer)
    # def __str__(self):
    #     return f"{self.tg_id}"

RELICS_NAME = {
    'stone_cross': 'Каменный крест',
    'iron_cross': 'Стальной крест'
}
