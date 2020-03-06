import sys
import os

apg_folder = sys.argv[2]

def run():
    _file = None
    line = None
    with open(sys.argv[1], 'r') as f:
        while True:
            line = f.readline()
            if not line: break
            if line[0] == '>' and 'linkage group' in line:
                if _file != None and file_name != None and apg_obj != None: 
                    _file.close()               

                linkage_group = line.split('linkage group')[1].split(' ')[1].replace(',', '')
                apg_obj, file_name = get_apg_file_data(apg_folder, linkage_group)
                if apg_obj == None: continue
                write_chunks(f, apg_obj, file_name)
                seq_verification(file_name, apg_obj)

def write_chunks(fasta_file, apg_obj, file_name):
    with open(file_name, '+w') as f:
        for obj in apg_obj.objects:
            chunk = get_chunk(fasta_file, obj.start_pos, obj.end_pos)           
            if not obj.is_gap:
                f.write(obj.fasta_name() + chunk + '\n')

def get_chunk(fasta_file, start, end):
    data = ''
    init_start = start
    while (end - start) > 0:
        data += fasta_file.read(end - start).replace('\n', '')
        start = len(data) + init_start
    return data

def get_apg_file_data(apg_folder, linkage_group):  
    file_path = apg_folder + '\\' + 'chr' + linkage_group + '.agp'
    if not os.path.isfile(file_path):
        print("Cannot find apg file: " + file_path)
        return None, None
    else:
        print("Processing apg file: " + file_path)

    apg_obj = read_apg_file(file_path)
    file_name = sys.argv[2] + 'chr' + linkage_group + '.fasta'
    return apg_obj, file_name

def read_apg_file(filename):
    apg_file = open(filename, 'r')
    objs = APGObjects()
    for line in apg_file:
        if line[0] != '#':
            parts = line.split("\t")
            obj = APGObject(parts[0], int(parts[1]), int(parts[2]), int(parts[3]), parts[4])
            if obj.type == 'N' or obj.type == 'U':
                obj.gap_obj = GapObject(int(parts[5]), parts[6], parts[7] == 'yes', parts[8])
                obj.is_gap = True
            else:
                obj.component_obj = ComponentObject(parts[5], parts[6], parts[7], parts[8])
                obj.is_gap = False
            objs.objects.append(obj)        
    return objs

def seq_verification(filename, apg_object):
    verified = True
    with open(filename) as f:
        seqs = f.read().split('>')
        i = 1
        for obj in apg_object.objects:
            if obj.is_gap: continue
            lines = seqs[i].split('\n')
            contents_list = lines[1:len(lines)]
            contents = ''
            apg_len = obj.end_pos - obj.start_pos
            i+=1
            verified = verified and (apg_len == len(contents.join(contents_list).replace('\n', '')))

    if verified:
        print ("Sequence for " + filename + " was proccessed correctly")
    else:
        print ("Error: Sequence for " + filename + " was not processed correctly")

class APGObjects:
    def __init__(self):
        self.objects = []
        self.current_obj = 0
        self.char_num = 0
        self.seq_num = 0

    def get_obj(self):
        return self.objects[self.current_obj]

class APGObject:
    def __init__(self, obj, start_pos, end_pos, part_number, _type):
        self.object = obj
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.part_number = part_number
        self.type = _type
        self.is_gap = True
        self.component_obj = None
        self.gap_obj = None
    
    def fasta_name(self):
        return '>' + self.component_obj.id_ + '\n'

class ComponentObject:
    def __init__(self, id_, start_pos, end_pos, orientation):
        self.id_ = id_
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.orientation = orientation

class GapObject:
    def __init__(self, length, _type, linkage, linkage_evidence):
        self.length = length
        self.type = _type
        self.linkage = linkage
        self.linkage_evidence = linkage_evidence

run()