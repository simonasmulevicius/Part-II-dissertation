from testing_libraries.bashterminal.commands import *

# set_MTU_server(9000, False)
run_command_in_terminal(["taskset", "-c", "0", "ip", "netns", "exec", "mr_server", "iperf3", "-s"])