# use with python3.5 and above
# run with the command: python3 -m gpu.gpumonitor
# the reason is some wacky classpath issue

import subprocess
import pickle

from email_util.send_email import send
# result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE)


if __name__ == '__main__':
    result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)

    # print(result.stdout)
    # dump the output for offline debugging
    pickle.dump(result, open("output.pickle", 'rb'), pickle.HIGHEST_PROTOCOL)
    # subject, message, path to config file
    # send("gpu stats", "something", "email_util/config.json")