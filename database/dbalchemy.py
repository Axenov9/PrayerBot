from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.dbcore import Base

from settings import config
from models.player import player
from models.level import level
from models.admin import admin


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

    def update_player_inf(self, id, purse, level, last_pray):
        self._session.query(player).filter_by(id=id).update(
            {"purse": purse, "player_level": level, "last_pray": last_pray}, synchronize_session='fetch')
        self._session.commit()
        self.close()

    def add_new_player(self, tg_id, chat_id, name):
        newplayer = player(
            tg_id=tg_id,
            chat_id=chat_id,
            player_level=1,
            purse=0,
            last_pray=0,
            name=name
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

    def close(self):
        self._session.close()
