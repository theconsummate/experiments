# use with python3.5 and above
# run with the command: python3 -m gpu.gpumonitor
# the reason is some wacky classpath issue

import subprocess
import pickle
import argparse

from email_util.send_email import send
# result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE)

# this function checks if stats for all the specified number of gpus are below the input thresholds.
def parse_command_output(result, num_gpu = 4, mem_threshold = None, util_threshold = None):
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
    
    return mem, uti

def parse_single_line(line):
    args = line.split("|")
    stats = {}
    memory = args[2].strip().replace("MiB", "")
    used, total = [int(x.strip()) for x in memory.split("/")]
    util = args[3].replace("Default", "").replace("%", "").strip()
    return {"memory": used/total, "util": int(util)/100}

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--gpu',type=int, help='number of gpus to watch')
    args.add_argument('--mem',type=float, help='memory threshold')
    args.add_argument('--util',type=float, help='gpu util threshold')
    arguments = args.parse_args()

    result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)

    # print(result.stdout)
    # dump the output for offline debugging
    # outfile = open("output.pickle",'wb')
    # pickle.dump(result, outfile, pickle.HIGHEST_PROTOCOL)
    # outfile.close()

    # read input file
    # infile = open("output.pickle", "rb")
    # result = pickle.load(infile)
    # infile.close()

    print(parse_command_output(result, num_gpu= arguments.gpu, mem_threshold=arguments.mem, util_threshold=arguments.util))
    # subject, message, path to config file
    # send("gpu stats", "something", "email_util/config.json")