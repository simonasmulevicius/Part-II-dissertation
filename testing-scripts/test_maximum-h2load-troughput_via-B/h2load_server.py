from testing_libraries.bashterminal.commands import *

NGTCP2_RELATIVE_LOCATION = "../ngtcp2"

set_MTU_server(1458, False)
run_command_in_terminal(["taskset", "-c", "0", "ip", "netns", "exec", "mr_server", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server", 
                        "--htdocs", NGTCP2_RELATIVE_LOCATION + "/examples/servers_folder", 
                        "-q", 
                        "--max-dyn-length=4g", 
                        "--max-udp-payload-size=1458", 
                        "10.2.2.101", "7777", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server.key", 
                        NGTCP2_RELATIVE_LOCATION + "/examples/server.cert"])


