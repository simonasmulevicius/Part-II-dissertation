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

run_command_in_terminal(["taskset", "-c", "0", "iperf3", "-s"])