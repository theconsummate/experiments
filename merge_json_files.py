import sys
import json
# usage python merge_json_files.py fullpath1 fullpath2 fulloutputpath

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

j1 = json.load(f1)["utts"]
j2 = json.load(f2)["utts"]

out_utts = {}

for key in j1.keys():
    out_utts[key+"_1"] = j1[key]

for key in j2.keys():
    out_utts[key+"_2"] = j2[key]


f3 = open(sys.argv[3], 'w')
json.dump({"utts":out_utts}, f3, indent=4)
