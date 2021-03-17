import subprocess
from io import StringIO
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def run_command_in_terminal(parameters):
    command_output = subprocess.run(parameters, stdout=subprocess.PIPE, text=True).stdout
    print("command_output:")
    print(command_output)
    return command_output


NGTCP2_RELATIVE_LOCATION = "../../../ngtcp2/"

run_command_in_terminal(["taskset", "-c", "0", "ip", "netns", "exec", "mr_server", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server", 
                        "--htdocs", NGTCP2_RELATIVE_LOCATION + "/examples/servers_folder", 
                        "-q", 
                        "--max-dyn-length=4g", 
                        "--max-udp-payload-size=1500", 
                        "10.2.2.101", "7777", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server.key", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server.cert"])


