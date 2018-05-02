class TxtParser:
    def parse(self, file_name):
        to_return = []
        file = open(file_name, "r")
        for line in file:
            str = line.rstrip()
            str2 = str.split(",")
            to_return.insert(len(to_return), str2)
        
        return to_return
