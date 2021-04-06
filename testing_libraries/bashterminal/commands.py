import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from io import StringIO

from testing_libraries.drawing.boxcharts import *
from testing_libraries.util.conversion import *

NUMBER_OF_REPEATED_EXPERIMENTS = 3

def run_command_in_terminal(parameters):
    command_output = subprocess.run(parameters, stdout=subprocess.PIPE, text=True).stdout
    return command_output    

def set_MTU(mtu, use_localhost=True):
    mtu = str(mtu)
    print("Using MTU:", mtu, "bytes")
    if use_localhost:
        run_command_in_terminal(["taskset", "-c", "1", "ifconfig", "lo", "mtu", mtu])
    else:
        run_command_in_terminal(["taskset", "-c", "1", "ip", "netns", "exec", "mr_client", "ifconfig", "eth2", "mtu", mtu])
    

def set_MTU_server(mtu, use_localhost=True):
    mtu = str(mtu)
    print("Using MTU:", mtu, "bytes")
    if use_localhost:
        run_command_in_terminal(["taskset", "-c", "0", "ifconfig", "lo", "mtu", mtu])
    else:
        run_command_in_terminal(["taskset", "-c", "0", "ip", "netns", "exec", "mr_server", "ifconfig", "eth3", "mtu", mtu])

def perform_perf3_measurement(MTU, url_string, use_localhost=True):
    set_MTU(MTU, use_localhost)
    if(use_localhost):
        command_output = run_command_in_terminal(["taskset", "-c", "1", "iperf3", "-c", url_string, "--udp", "-b", "0"])
    else:
        command_output = run_command_in_terminal(["taskset", "-c", "1", "ip", "netns", "exec", "mr_client", "iperf3", "-c", url_string, "--udp", "-b", "0"])
    # print("command_output:[", command_output, "]")
    
    output_lines = command_output.splitlines()
    if "unable to connect to server" in command_output or len(output_lines) < 16:
        return

    # # TODO include samples into the graph
    # for line in output_lines[3:13]:
    #     words = split_string_into_array_of_words(line)

    sender_line          = output_lines[15]
    sender_words         = split_string_into_array_of_words(sender_line)
    sender_bitrate_units = sender_words[-6]
    sender_bitrate       = convert_bitrate_to_bytes_per_second(float(sender_words[-7]), sender_bitrate_units)

    receiver_line          = output_lines[16]
    receiver_words         = split_string_into_array_of_words(receiver_line)
    receiver_bitrate_units = receiver_words[-6]
    receiver_bitrate       = convert_bitrate_to_bytes_per_second(float(receiver_words[-7]), receiver_bitrate_units)
    receiver_proportion_of_losses = float(receiver_words[-2].replace("(", "").replace(")", "").replace("%", ""))

    print("sender_bitrate_bytes_per_second  : ",   sender_bitrate)
    print("receiver_bitrate_bytes_per_second: ", receiver_bitrate) 
    print("receiver_proportion_of_losses    : ", receiver_proportion_of_losses) 

    return {"sender_bitrate_bytes_per_second"  :   sender_bitrate,
            "receiver_bitrate_bytes_per_second": receiver_bitrate,
            "receiver_proportion_of_losses"    : receiver_proportion_of_losses}

def perform_group_of_perf3_measurements(MTUs, url_string, use_localhost):
    # valid_MTUs        = []
    sender_bitrates   = []
    receiver_bitrates = []
    receiver_losses   = []

    for MTU in MTUs:
        # valid_MTUs.append(MTU)
        repeated_sender_bitrates   = []
        repeated_receiver_bitrates = []
        repeated_receiver_losses   = []
        
        for _ in range(NUMBER_OF_REPEATED_EXPERIMENTS):
            measurement_result = perform_perf3_measurement(MTU, url_string, use_localhost)
            if measurement_result is not None:                
                repeated_sender_bitrates.append(measurement_result["sender_bitrate_bytes_per_second"])
                repeated_receiver_bitrates.append(measurement_result["receiver_bitrate_bytes_per_second"])
                repeated_receiver_losses.append(measurement_result["receiver_proportion_of_losses"])
        
        sender_bitrates.append(repeated_sender_bitrates)
        receiver_bitrates.append(repeated_receiver_bitrates)
        receiver_losses.append(repeated_receiver_losses)

    return {"valid_MTUs"       : MTUs, 
            "sender_bitrates"  : sender_bitrates, 
            "receiver_bitrates": receiver_bitrates, 
            "receiver_losses"  : receiver_losses}

def perform_h2load_measurement(parameters):
    print("parameters: ", parameters)
    command_output = run_command_in_terminal(parameters)
    print("command_output:")
    print(command_output)

    total_delay_ms           = 0
    requests_per_second      = 0
    throughput_KB_per_second = 0

    output_lines = StringIO(command_output)
    for line in output_lines:
        if "finished in" in line:
            print(line)
            measurements = line.replace('finished in ', '').replace('\n', '').replace(' ', '').split(',')
            # print(measurements)

            if "us" == measurements[0][-2:]:
                total_delay_ms       = float(measurements[0].replace('us', ''))/1000.0
            elif "ms" == measurements[0][-2:]:
                total_delay_ms       = float(measurements[0].replace('ms', ''))
            elif "s" == measurements[0][-1:]:
                total_delay_ms       = float(measurements[0].replace('s', ''))*1000
            requests_per_second      = float(measurements[1].replace('req/s', ''))

            
            if measurements[2][-4].isdigit() and "B/s" == measurements[2][-3:]:
                throughput_KB_per_second =  float(measurements[2][:-3])/1024
            else:
                assert (not any(symbol.isdigit() for symbol in measurements[2][-4:]))
                throughput_KB_per_second = float(measurements[2][:-4])

                if "kB/s" == measurements[2][-4:] or "KB/s" == measurements[2][-4:]:
                    throughput_KB_per_second *= 1
                elif "MB/s" == measurements[2][-4:]:
                    throughput_KB_per_second *= 1024
                elif "GB/s" == measurements[2][-4:]:
                    throughput_KB_per_second *= 1024*1024
            
            print(total_delay_ms, "ms")
            print(requests_per_second, "req/s")
            print(throughput_KB_per_second, "KB/s")

            return ({"total_delay_ms": total_delay_ms,
                    "requests_per_second": requests_per_second, 
                    "throughput_KB_per_second": throughput_KB_per_second})

def perform_group_of_h2load_measurements(parameter_list_prefix, parameter_list_suffix, baseURL, payload_sizes):
    delays      = []
    requests    = []
    throughputs = []

    for payload_size in payload_sizes:
        url = baseURL + str(payload_size)
        print(url)

        parameters = parameter_list_prefix.copy()
        parameters.extend(["../nghttp2/src/h2load", "--npn-list", "h3", url])
        parameters.extend(parameter_list_suffix)
        print("parameters: ", parameters)
        
        repeated_delays      = []
        repeated_requests    = []
        repeated_throughputs = []
        
        for _ in range(NUMBER_OF_REPEATED_EXPERIMENTS):
            measurements = perform_h2load_measurement(parameters)
            repeated_delays.append(measurements['total_delay_ms'])
            repeated_requests.append(measurements['requests_per_second'])
            repeated_throughputs.append(measurements['throughput_KB_per_second'])

        delays.append(repeated_delays)
        requests.append(repeated_requests)
        throughputs.append(repeated_throughputs)

    print(delays)

    return ({"delays": delays,
        "requests": requests, 
        "throughputs": throughputs})