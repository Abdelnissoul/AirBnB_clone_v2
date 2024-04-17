#!/usr/bin/python3
"""This module defines a class for file storage management in the HBNB clone."""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class to manage file storage for HBNB models."""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Retrieve all objects or those of a specific class from storage.

        Args:
            cls (class, optional): If specified, filters the result to include
                only objects of the specified class.

        Returns:
            dict: A dictionary containing objects from storage.
        """
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls)
            if cls and issubclass(cls, BaseModel):
                cls_dict = {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
                return cls_dict
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to storage."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Save the current state of objects to the JSON file."""
        serialized_objects = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Reload objects from the JSON file."""
        try:
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for k, v in obj_dict.items():
                    cls_name = v['__class__']
                    cls_obj = eval(cls_name)(**v)
                    self.__objects[k] = cls_obj
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    def delete(self, obj=None):
        """Delete an object from storage if it exists.

        Args:
            obj (BaseModel, optional): The object to delete.
        """
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in self.__objects:
            del self.__objects[key]
