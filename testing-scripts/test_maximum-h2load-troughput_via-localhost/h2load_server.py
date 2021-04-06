from testing_libraries.bashterminal.commands import *

NGTCP2_RELATIVE_LOCATION = "../ngtcp2"

IP_MTU  = 1280
Eth_packet_size             = IP_MTU + 14
max_udp_payload_size        = IP_MTU - 28
max_udp_payload_size_string = "--max-udp-payload-size=" + str(max_udp_payload_size)

set_MTU_server(IP_MTU, True)
run_command_in_terminal(["taskset", "-c", "0", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server", 
                        "--htdocs", NGTCP2_RELATIVE_LOCATION + "/examples/servers_folder", 
                        "-q", 
                        "--max-dyn-length=4g", 
                        max_udp_payload_size_string, 
                        "127.0.0.1", "7777", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server.key", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server.cert"])


