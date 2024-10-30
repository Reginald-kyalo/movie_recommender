#!/usr/bin/python3
"""Defines hbnb command intepreter"""
import cmd
import re
import os
import pandas as pd
import ast
import json
from shlex import split
from datetime import datetime
from models.base_model import BaseModel
from models.movie import Movie
from models.credits import Credit
from models.movie_content_based import MovieContentBased
from models.movie_vectors import MovieVector
from models import storage


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl

def parse_json_field(field):
    """Convert a JSON-like string to a list of dictionaries.
    """
    if pd.isna(field) or field.strip() == "":
        return []  # Handle missing or empty fields
    return ast.literal_eval(field)

class Command(cmd.Cmd):
    """Sets up commands in command intepreter

    Args:
        prompt (str): prompt string stdout
        __classes (list): classes available
    """
    prompt = "(hbnb) "
    __classes = ['Movie',
                 'MovieContentBased'
                 'MovieVector'
                 'Credit']

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

def do_load(self, arg):
    # Parse arguments and ensure valid input
    args = parse(arg)
    if len(args) == 0:
        print("Include correct file path.")
        return  # Exit if no valid file path is provided

    csv_path = args[0]
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        df_cleaned = df.drop_duplicates().dropna()
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Determine which file is being loaded based on the filename
    path = csv_path.split('_')

    # Handling movies.csv
    if path[-1] == "movie.csv":
        for _, row in df_cleaned.iterrows():
            try:
                movie = Movie(
                    id=int(row['id']),
                    title=row['title'],
                    budget=int(row['budget']),
                    homepage=row['homepage'],
                    original_language=row['original_language'],
                    original_title=row['original_title'],
                    overview=row['overview'],
                    popularity=float(row['popularity']),
                    release_date=datetime.strptime(row['release_date'], "%Y-%m-%d"),
                    revenue=int(row['revenue']),
                    runtime=int(row['runtime']),
                    status=row['status'],
                    tagline=row['tagline'],
                    vote_average=float(row['vote_average']),
                    vote_count=int(row['vote_count']),
                    # Store list-like data as JSON strings
                    genres=str(parse_json_field(row['genres'])),
                    keywords=str(parse_json_field(row['keywords'])),
                    production_companies=str(parse_json_field(row['production_companies'])),
                    production_countries=str(parse_json_field(row['production_countries'])),
                    spoken_languages=str(parse_json_field(row['spoken_languages']))
                )
                movie.save()  # Save to the database
            except Exception as e:
                print(f"Error processing movie {row['title']}: {e}")

    # Handling credits.csv
    elif path[-1] == "credits.csv":
        for _, row in df_cleaned.iterrows():
            try:
                # Parse cast and crew JSON fields as text
                cast_text = json.dumps(parse_json_field(row['cast']))  # Convert to JSON string
                crew_text = json.dumps(parse_json_field(row['crew']))  # Convert to JSON string

                # Create a Credit object and save it to the database
                credit = Credit(
                    movie_id=int(row['movie_id']),
                    title=row['title'],
                    cast=cast_text,
                    crew=crew_text
                )
                credit.save()

            except Exception as e:
                print(f"Error processing credits for movie ID {row['movie_id']}: {e}")

    else:
        print("Unsupported file type. Please provide either 'movie.csv' or 'credits.csv'.")


    def do_show(self, arg):
        """prints string representation of instance
        based on class name
        Ex: (hbnb) show BaseModel
        """
        model_name = model_id = ""
        args = parse(arg)
        objs = storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return
        else:
            model_name = args[0]
        if model_name not in Command.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        else:
            model_id = args[1]
        if "{}.{}".format(model_name, model_id) not in objs:
            print("** no instance found **")
            return
        else:
            print(objs["{}.{}".format(model_name, model_id)])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        save changes to JSON file
        """
        line = parse(arg)
        model_name = model_id = ""
        objs = storage.all()

        if len(line) >= 1:
            model_name = line[0]
        else:
            print("** class name missing **")
            return
        if model_name not in Command.__classes:
            print("** class doesn't exist **")
            return
        if len(line) >= 2:
            model_id = line[1]
        else:
            print("** instance id missing **")
            return
        if "{}.{}".format(model_name, model_id) not in objs:
            print("** no instance found **")
            return
        else:
            del objs["{}.{}".format(model_name, model_id)]
            storage.save()

    def do_all(self, arg):
        """prints all string representation of all instances
        based or not on the class name
        Ex: $ all BaseModel or $ all
        """
        args = parse(arg)
        objs = storage.all().values()
        list = []

        if args and args[0] not in Command.__classes:
            print("** class doesn't exist **")
        else:
            for obj in objs:
                if args and args[0] == obj.__class__.__name__:
                    list.append(obj.__str__())
                elif not args:
                    list.append(obj.__str__())

            print(list)

    def do_update(self, arg):
        """adds or updates attribute to an instance
        saves changes to JSON file
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        model_name = model_id = attr_name = attr_val = ''
        args = parse(arg)
        objs = storage.all()

        if args:
            model_name = args[0]
        else:
            print("** class name missing **")
            return
        if model_name not in Command.__classes:
            print("** class doesn't exist **")
            return
        if len(args) >= 2:
            model_id = args[1]
        else:
            print("** instance id missing **")
            return
        if "{}.{}".format(model_name, model_id) not in objs.keys():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        my_obj = objs["{}.{}".format(model_name, model_id)]

        if len(args) == 4:
            attr_name = args[2]
            attr_val = args[3]
            if attr_name in my_obj.__class__.__dict__.keys():
                valtype = type(my_obj.__class__.dict__[attr_name])
                my_obj.__dict__[attr_name] = valtype(attr_val.strip("\""))
            else:
                my_obj.__dict__[attr_name] = attr_val.strip("\"")
        elif type(eval(args[2])) == dict:
            for k, v in eval(args[2]).items():
                if (k in my_obj.__class__.__dict__.keys() and
                        type(my_obj.__class__.__dict__[k]) in
                        {str, int, float}):
                    valtype = type(my_obj.__class__.__dict__[k])
                    my_obj.__dict__[k] = valtype(v)
                else:
                    my_obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_EOF(self, line):
        """command to exit program"""
        return True

    def do_quit(self, line):
        """command to exit program"""
        return True

    def emptyline(self):
        """defaults to doing nothing if no command provided"""
        pass


if __name__ == '__main__':
    Command().cmdloop()