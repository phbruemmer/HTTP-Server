import re

def clean_name(function):
    def wrapper(*args):
        name = re.sub('[^A-Za-z0-9]+', '', str(args[0]))
        function(name=name, arguments=args)

    return wrapper