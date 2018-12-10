import sys
import json
# usage python merge_json_files.py fulloutputpath fullpath1 fullpath2 ... 

out_utts = {}

for i, file in enumerate(sys.argv[2:]):
    f = open(file)
    j = json.load(f)["utts"]
    for key in j.keys():
        out_utts[key+"_" + str(i)] = j[key]

f3 = open(sys.argv[1], 'w')
json.dump({"utts":out_utts}, f3, indent=4)
