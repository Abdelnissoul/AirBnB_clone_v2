#!/usr/bin/python3
"""This defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse_arguments(arg_string):
    """make the arguments parsing input"""
    curly_braces = re.search(r"\{(.*?)\}", arg_string)
    brackets = re.search(r"\[(.*?)\]", arg_string)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg_string)]
        else:
            lexer = split(arg_string[:brackets.span()[0]])
            result_list = [i.strip(",") for i in lexer]
            result_list.append(brackets.group())
            return result_list
    else:
        lexer = split(arg_string[:curly_braces.span()[0]])
        result_list = [i.strip(",") for i in lexer]
        result_list.append(curly_braces.group())
        return result_list


class HBNBCommand(cmd.Cmd):
    """ the HolbertonBnB command. attr(s).

    Attributes:
        prompt : The command defined as a string
    """

    prompt = "(hbnb) "
    __valid_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """passing and receiving an empty line."""
        pass

    def default(self, arg_string):
        """setting defazult for invalid input."""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg_string)
        if match is not None:
            arg_list = [
                arg_string[:match.span()[0]],
                arg_string[match.span()[1]:]
                ]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                command = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(arg_list[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg_string))
        return False

    def do_quit(self, arg_string):
        """Quitting the program if true"""
        return True

    def do_EOF(self, arg_string):
        """Exiting the program."""
        print("")
        return True

    def do_create(self, arg_string):
    """Create a new instance of a class"""
    arg_list = parse_arguments(arg_string)
    if not arg_list:
        print("** class name missing **")
        return

    class_name = arg_list[0]
    if class_name not in self.__valid_classes:
        print("** class doesn't exist **")
        return

    kwargs = {}
    for pair in arg_list[1:]:
        if '=' in pair:
            key, value = pair.split('=')
            if value.startswith('"') and value.endswith('"'):
                # String value
                value = value[1:-1].replace('_', ' ')
            elif '.' in value:
                # Float value
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                # Integer value
                try:
                    value = int(value)
                except ValueError:
                    continue
            kwargs[key] = value

    new_instance = eval(class_name)(**kwargs)
    new_instance.save()
    print(new_instance.id)


    def do_show(self, arg_string):
        """showing the information about one case"""
        arg_list = parse_arguments(arg_string)
        obj_dct = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__valid_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dct:
            print("** no instance found **")
        else:
            print(obj_dct["{}.{}".format(arg_list[0], arg_list[1])])

    def do_destroy(self, arg_string):
        """Destroying the case"""
        arg_list = parse_arguments(arg_string)
        obj_dct = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__valid_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dct.keys():
            print("** no instance found **")
        else:
            del obj_dct["{}[[O.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def do_all(self, arg_string):
        """showing all the cases of a class."""
        arg_list = parse_arguments(arg_string)
        if len(arg_list) > 0 and \
                arg_list[0] not in HBNBCommand.__valid_classes:

            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_count(self, arg_string):
        """Counting the cases of a class."""
        arg_list = parse_arguments(arg_string)
        count = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg_string):
        """Updating one case"""
        arg_list = parse_arguments(arg_string)
        obj_dct = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.__valid_classes:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dct.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
            obj = obj_dct["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = val_type(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dct["{}.{}".format(arg_list[0], arg_list[1])]
            for k, v in eval(arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = val_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
