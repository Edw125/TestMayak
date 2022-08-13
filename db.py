import logging

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

_logger = logging.getLogger(__name__)

Base = declarative_base()


class Urls(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)
    xpath = Column(String)


class DBDriver:
    def __init__(self, db_name):
        self._database_url = f'sqlite:///{db_name}'
        self._engine = create_engine(self._database_url)
        self._sm = sessionmaker(bind=self._engine)
        Base.metadata.create_all(self._engine)

    def add_url(self, url: list):
        new_url = Urls(id=url[0], name=url[1], url=url[2], xpath=url[3])
        session = self._sm()

        c = session.query(Urls).filter(Urls.name == url[1]).count()
        if c > 0:
            _logger.warning(
                f"Url '{url[1]}, {url[2]}, {url[3]}' Уже есть в базе данных"
            )
            return False

        session.add(new_url)
        session.commit()
        session.refresh(new_url)
        session.close()
