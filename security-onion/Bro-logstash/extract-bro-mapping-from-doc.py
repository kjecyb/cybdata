import sys

current_file = ""
current_map = []
skip_count = 0

def print_map():
    for tup in current_map:
        print('\t'.join( [ current_file, tup[0], tup[1] ] ) )
#

with open("../../../../Security-Onion-Solutions/security-onion.wiki/Bro-Fields.md") as f:
    for line in f:
        line = line.rstrip()
        if skip_count > 0:
            skip_count -= 1
            continue
        #<==
        if line[0:3] == "###":
            if current_file != "":
                print_map()
            current_file = line[4:]
            current_map = []
            skip_count = 4
            continue
        if line[0:4] == "    ":
            continue
        if len(line) == 0:
            continue
        idx = line.find('=>')
        if idx > 0:
            bro = line[0:idx-1]
            idx2 = line.find('=>', idx +1)
            if idx2 < 0: 
                idx2 = len(line)
            else:
                idx2 = idx2 - 1
            logstash = line[idx+2:idx2]
        else:
            bro = line
            logstash = ""
        current_map.append( (bro, logstash) )
    
