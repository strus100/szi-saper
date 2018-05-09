import json
class Parser:
    def parse_data(self, file_name):
        to_return = []
        file = open(file_name, "r")
        for line in file:
            str = line.rstrip()
            str2 = str.split(",")
            to_return.insert(len(to_return), str2)
        
        return to_return

    def parse_tree(self, file_name):
        file = open(file_name, "r")
        json_str = file.read()
        tree = json.loads(json_str)
        return tree
