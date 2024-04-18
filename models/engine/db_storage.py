#!/usr/bin/python3
"""Defines the DBStorage class."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


class DBStorage:
    """Represents the database storage engine."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                       .format(getenv('HBNB_MYSQL_USER'),
                                               getenv('HBNB_MYSQL_PWD'),
                                               getenv('HBNB_MYSQL_HOST'),
                                               getenv('HBNB_MYSQL_DB'),
                                               pool_pre_ping=True))
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for cls in Base.__subclasses__():
                query = self.__session.query(cls).all()
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
