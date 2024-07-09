#!/usr/bin/python3
"""Defines a new storage engine called DBStorage"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """DB Storage Class"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialization method"""

        # make a list of all environment variable values
        env = os.getenv('HBNB_ENV')
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        # construct the database url
        database_url = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(
                user, pwd,
                host, 3306, db
                )

        # create the database engine
        self.__engine = create_engine(
                database_url, pool_pre_ping=True,
                echo=False
                )

        if env == "test":
            # Drop all tables
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query current db for all objects or selected objects"""

        result = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f'{cls.__name__}.{obj.id}'
                result[key] = obj
        else:
            from models.user import User
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review
            for cls in [State, City]:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = f'{cls.__name__}.{obj.id}'
                    result[key] = obj
        return result

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create tables and database sessions"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
                )
        Session = scoped_session(session_factory)
        self.__session = Session()
