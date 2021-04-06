from testing_libraries.bashterminal.commands import *

IP_MTU  = 9000
Eth_packet_size             = IP_MTU + 14
max_udp_payload_size        = IP_MTU - 28

set_MTU_server(IP_MTU, True)
run_command_in_terminal(["taskset", "-c", "0", "iperf3", "-s"])