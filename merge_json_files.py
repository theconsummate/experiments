import sys
import json
# usage python merge_json_files.py fulloutputpath fullpath1 fullpath2 ... 

# f1 = open(sys.argv[1])
# f2 = open(sys.argv[2])

# j1 = json.load(f1)["utts"]
# j2 = json.load(f2)["utts"]

out_utts = {}

for i, file in enumerate(sys.argv[2:]):
    f = open(file)
    j = json.load(f)["utts"]
    for key in j.keys():
        out_utts[key+"_" + i] = j[key]

# for key in j1.keys():
#     out_utts[key+"_1"] = j1[key]

# for key in j2.keys():
#     out_utts[key+"_2"] = j2[key]


f3 = open(sys.argv[1], 'w')
json.dump({"utts":out_utts}, f3, indent=4)
