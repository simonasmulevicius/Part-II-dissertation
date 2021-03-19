from testing_libraries.bashterminal.commands import *

set_MTU_server(9000, True)
run_command_in_terminal(["taskset", "-c", "0", "iperf3", "-s"])