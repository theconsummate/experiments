# use with python3.5 and above
# run with the command: python3 -m gpu.gpumonitor
# the reason is some wacky classpath issue

import subprocess
import pickle
import argparse
from threading import Timer
from datetime import datetime

from email_util.send_email import send
import sys
# result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE)

# this function checks if stats for all the specified number of gpus are below the input thresholds.
def parse_command_output(num_gpu = 4, mem_threshold = 0.1, util_threshold = 0.1):
    result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)
    mem, uti = None, None
    def check_property(property, threshold):
        i = 0
        for stat in stats:
            if stat[property] < threshold:
                i += 1
        if i >= num_gpu:
            return True
        return False
    
    lines = result.stdout.decode("utf-8").split("\n")

    line_nos = [8, 11, 14, 17]
    stats = []
    for i in line_nos:
        stats.append(parse_single_line(lines[i]))
    
    if mem_threshold:
        mem = check_property("memory", mem_threshold)

    
    if util_threshold:
        uti = check_property("util", mem_threshold)
    
    print("mem: " + str(mem) + ", uti: " + str(uti))
    if mem or uti:
        send("gpu is free", "mem: " + str(mem) + ", uti: " + str(uti), "email_util/config.json")
        # send one email and exit
        sys.exit()
    t = Timer(get_secs(), parse_command_output)
    t.start()

def parse_single_line(line):
    args = line.split("|")
    stats = {}
    memory = args[2].strip().replace("MiB", "")
    used, total = [int(x.strip()) for x in memory.split("/")]
    util = args[3].replace("Default", "").replace("%", "").strip()
    return {"memory": used/total, "util": int(util)/100}


def get_secs():
    # x=datetime.today()
    # y=x.replace(day=x.day+1, hour=6, minute=0, second=0, microsecond=0)
    # delta_t=y-x
    # secs=delta_t.seconds+1
    # # secs = x.hour -11
    # return secs
    # check every 5 mins
    return 300

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--gpu',type=int, help='number of gpus to watch')
    args.add_argument('--mem',type=float, help='memory threshold')
    args.add_argument('--util',type=float, help='gpu util threshold')
    arguments = args.parse_args()

    # print(result.stdout)
    # dump the output for offline debugging
    # outfile = open("output.pickle",'wb')
    # pickle.dump(result, outfile, pickle.HIGHEST_PROTOCOL)
    # outfile.close()

    # read input file
    # infile = open("output.pickle", "rb")
    # result = pickle.load(infile)
    # infile.close()

    print(parse_command_output(num_gpu= arguments.gpu, mem_threshold=arguments.mem, util_threshold=arguments.util))
    # subject, message, path to config file
    # send("gpu stats", "something", "email_util/config.json")
    t = Timer(get_secs(), parse_command_output)
    t.start()