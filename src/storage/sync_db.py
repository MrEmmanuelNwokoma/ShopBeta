from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker



class SyncDatabase:
    def __init__(self, db_url: str = "sqlite://my_database.db"):
        self.__engine = create_engine(db_url, echo=False)
        self.__session_maker = sessionmaker(self.__engine, expire_on_commit=False)
    
    @property
    def session_maker(self):
        return self.__session_maker
    
    @contextmanager
    def get_session(self):
        with self.__session_maker as session:
            yield session