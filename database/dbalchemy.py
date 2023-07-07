from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.dbcore import Base

from settings import config
from models.player import player
from models.level import level
from models.admin import admin
from models.relic import relic


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(**kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):

    def __init__(self):
        # pass
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)

        self._session = session()

        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def player_by_tgandchat(self, tg_id, chat_id):

        result = self._session.query(player).filter_by(tg_id=tg_id, chat_id=chat_id).all()
        self.close()
        try:
            return result[0]
        except:
            return False

    def level_by_id(self, id):
        result = self._session.query(level).filter_by(id=id).all()
        # print(result[0].income)
        self.close()

        return result[0]

    def update_player_inf(self, id, purse, level, last_pray, relics):
        self._session.query(player).filter_by(id=id).update(
            {"purse": purse, "player_level": level, "last_pray": last_pray, "relics": relics}, synchronize_session='fetch')
        self._session.commit()
        self.close()

    def add_new_player(self, tg_id, chat_id, name):
        newplayer = player(
            tg_id=tg_id,
            chat_id=chat_id,
            player_level=1,
            purse=0,
            last_pray=0,
            name=name,
            relics=' '
        )
        self._session.add(newplayer)
        self._session.commit()
        self.close()

    def add_new_admin(self, tg_id, name, parent_level):
        newadmin = admin(
            tg_id=tg_id,
            name=name,
            level=parent_level + 1
        )
        self._session.add(newadmin)
        self._session.commit()
        self.close()

    def is_admin(self, tg_id):
        if self._session.query(admin).filter_by(tg_id=tg_id).all():
            return True
        else:
            return False

    def admin_by_tgid(self, tg_id):
        result = self._session.query(admin).filter_by(tg_id=tg_id).all()
        self.close()
        return result[0]

    def relic_by_id(self, id):
        result = self._session.query(relic).filter_by(id=id).all()
        self.close()
        return result[0]

    def relics_by_player(self, player):
        result = []
        if player.relics:
            for relic_id in player.relics.split():
                res = self._session.query(relic).filter_by(id=relic_id).all()[0]
                result.append(res)
            self.close()
            return result
        else:
            return False

    def relic_multiplier_by_player(self, player):
        multiplier = 1
        if player.relics:
            for relic_id in player.relics.split():
                res = self._session.query(relic).filter_by(id=relic_id).all()[0]
                multiplier += res.multiplier
            self.close()
        return round(multiplier, 1)


    def all_relics(self):
        result = self._session.query(relic).all()
        self.close()
        return result
    def close(self):
        self._session.close()
