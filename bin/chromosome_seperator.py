import sys

apg_objects = []

def run():
    read_apg_file(sys.argv[1])

def read_apg_file(filename):
    apg_file = open(filename, 'r')
    for line in apg_file:
        if line[0] != '#':
            parts = line.split("\t")
            obj = APGObject(parts[0], int(parts[1]), int(parts[2]), int(parts[3]), parts[4])
            if obj.type == 'N' or obj.type == 'U':
                obj.properties = GapObject()
            else:
                obj.properties = ComponentObject()

class APGObject:
    def __init__(self, obj, start_pos, end_pos, part_number, type):
        self.object = obj
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.part_number = part_number
        self.type = type
        self.properties = None

class ComponentObject:
    def __init__(self, id_, start_pos, end_pos, orientation):
        self.id = id_
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.orientation = orientation

class GapObject:
    def __init__(self, length, type, linkage, linkage_evidence):
        self.length = 0
        self.type = ""
        self.linkage = False
        self.linkage_evidence = ""

run()