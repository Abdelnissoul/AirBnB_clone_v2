#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represents a storage engine for serializing and deserializing objects.

    Attributes:
        __file_path (str): The path to the JSON file used for storage.
        __objects (dict): A dictionary to store serialized objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Retrieve the dictionary of serialized objects.

        Args:
            cls (class, optional): If specified, filters the result to include
                only objects of the specified class.

        Returns:
            dict: A dictionary containing objects in storage.
        """
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Add a new object to the storage dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize objects to JSON and save to file."""
        serialized_objs = {}
        for key, obj in self.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(serialized_objs, file)

    def reload(self):
        """Deserialize JSON file and reload objects into storage."""
        try:
            with open(self.__file_path, "r") as file:
                data = json.load(file)
                for key, val in data.items():
                    cls_name = val['__class__']
                    del val['__class__']
                    self.__objects[key] = eval(cls_name)(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside."""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects.pop(key, None)
