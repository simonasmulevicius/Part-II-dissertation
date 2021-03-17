import subprocess
from io import StringIO
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def run_command_in_terminal(parameters):
    command_output = subprocess.run(parameters, stdout=subprocess.PIPE, text=True).stdout
    return command_output


def set_MTU(mtu):
    run_command_in_terminal(["ifconfig", "lo", "mtu", mtu])

def split_string_into_array_of_words(string):
    raw_words = string.split(" ")
    words = [word for word in raw_words if word != '']
    # print(words)
    return words


def convert_bitrate_to_bytes_per_second(bitrate, bitrate_units):
    # print("bitrate:",bitrate)
    converted_bitrate_in_bytes = bitrate/8
    if(bitrate_units == "Kbits/sec"):
        converted_bitrate_in_bytes = converted_bitrate_in_bytes*1024
    elif(bitrate_units == "Mbits/sec"):
        converted_bitrate_in_bytes = converted_bitrate_in_bytes*1024*1024
    elif(bitrate_units == "Gbits/sec"):
        converted_bitrate_in_bytes = converted_bitrate_in_bytes*1024*1024*1024
    # print("converted bitrate (Bytes/sec):", converted_bitrate_in_bytes)
    
    return converted_bitrate_in_bytes

assert convert_bitrate_to_bytes_per_second(449, 'Kbits/sec') == 57472
assert convert_bitrate_to_bytes_per_second(449, 'Mbits/sec') == 58851328
assert convert_bitrate_to_bytes_per_second(1.40, 'Gbits/sec') == 187904819.2

def perform_perf3_measurement(mtu):
    print("Using MTU:", str(mtu), "bytes")
    set_MTU(str(mtu))
    command_output = run_command_in_terminal(["taskset", "-c", "1", "iperf3", "-c", "127.0.0.1", "--udp", "-b", "0"])
    print("command_output:")
    print(command_output)
    
    output_lines = command_output.splitlines()
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

    print("sender_bitrate_bytes_per_second  : ",   sender_bitrate,   sender_bitrate_units)
    print("receiver_bitrate_bytes_per_second: ", receiver_bitrate, receiver_bitrate_units) 
    print("receiver_proportion_of_losses : ", receiver_proportion_of_losses) 

    return {"sender_bitrate_bytes_per_second"  : sender_bitrate,
            "receiver_bitrate_bytes_per_second": receiver_bitrate,
            "receiver_proportion_of_losses": receiver_proportion_of_losses}

MTUs = [100, 200, 400, 500, 750, 800, 900, 1000, 
        1100, 1200, 1300, 1400, 1500, 1600, 1750, 1800, 1900, 
        2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 
        10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 
        20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000,
        30000, 31000, 32000 ]
# MTUs = [60000, 80000]

sender_bitrates   = []
receiver_bitrates = []
receiver_losses   = []

for MTU in MTUs:
    measurement_result = perform_perf3_measurement(MTU)
    sender_bitrates.append(measurement_result["sender_bitrate_bytes_per_second"])
    receiver_bitrates.append(measurement_result["receiver_bitrate_bytes_per_second"])
    receiver_losses.append(measurement_result["receiver_proportion_of_losses"])


# Option 1 - original
measurements_A = sender_bitrates
measurements_B = receiver_bitrates
measurements_C = receiver_losses

# Option 2 - fake short
# measurements_A = [458.0, 524.0, 763.0]
# measurements_B = [458.0, 524.0, 763.0]
# measurements_C = [0.0, 0.0, 0.0]

# Option 3 - fake long
# MTUs = [100, 200, 400, 500, 750, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1750, 1800, 1900, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000]
# measurements_A = [8270643.2, 24772608.0, 58195968.0, 74842112.0, 115212288.0, 123076608.0, 142270791.68, 161061273.6, 175825223.68, 193273528.32, 209379655.68, 226827960.32, 244276264.96, 261724569.6, 279172874.24, 285883760.64, 297963356.16, 315411660.8, 476472934.4, 621428080.64, 759672340.48, 897916600.32, 1042871746.56, 1099243192.32, 1209301729.28, 1307280670.72, 1422707916.8, 1503238553.6, 1610612736.0, 1717986918.4, 1785095782.4, 1892469964.8, 1798517555.2, 1838782873.6, 1905891737.6, 1986422374.4, 1999844147.2, 2120640102.4, 2187748966.4, 2241436057.6, 2281701376.0, 2362232012.8, 2389075558.4, 2375653785.6, 2483027968.0, 2496449740.8, 2590402150.4, 2684354560.0]
# measurements_B = [8087142.4, 24641536.0, 58195968.0, 74711040.0, 115212288.0, 122814464.0, 142270791.68, 161061273.6, 175825223.68, 193273528.32, 209379655.68, 226827960.32, 244276264.96, 260382392.32, 277830696.96, 284541583.36, 297963356.16, 314069483.52, 475130757.12, 620085903.36, 756987985.92, 895232245.76, 1041529569.28, 1092532305.92, 1205275197.44, 1300569784.32, 1422707916.8, 1489816780.8, 1597190963.2, 1717986918.4, 1785095782.4, 1892469964.8, 1785095782.4, 1825361100.8, 1892469964.8, 1973000601.6, 1986422374.4, 2107218329.6, 2160905420.8, 2214592512.0, 2268279603.2, 2335388467.2, 2375653785.6, 2348810240.0, 2456184422.4, 2496449740.8, 2576980377.6, 2670932787.2]
# measurements_C = [2.2, 0.2, 0.17, 0.14, 0.064, 0.22, 0.19, 0.2, 0.26, 0.18, 0.1, 0.14, 0.24, 0.57, 0.19, 0.45, 0.23, 0.23, 0.28, 0.27, 0.26, 0.22, 0.14, 0.56, 0.38, 0.5, 0.58, 0.5, 0.44, 0.4, 0.43, 0.33, 0.76, 0.79, 0.77, 0.64, 0.78, 0.7, 0.72, 0.82, 0.72, 0.77, 0.65, 0.87, 0.99, 0.48, 0.44, 0.72]

print(MTUs)
print(measurements_A)
print(measurements_B)
print(measurements_C)

fig, ax = plt.subplots()
ax.plot(MTUs, measurements_A, label='Sender bitrate')
ax.plot(MTUs, measurements_B, label='Receiver bitrate')
ax.set(xlabel='MTUs, Bytes' , ylabel='UDP throughput, Bytes/second')
ax.grid()

# ax_losses.plot(MTUs, measurements_C,    label='receiver_proportion_of_losses')
# ax_losses.set(xlabel='MTUs, UNITS????', ylabel='Proportion of lost datagrams, %')
# ax_losses.grid()


# Chart example taken from:
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
ax_losses = ax.twinx()
colour = 'tab:red'
ax_losses.set_ylabel('Proportion of lost datagrams at the receiver side, %', color=colour) 
ax_losses.plot(MTUs, measurements_C, color=colour)
ax_losses.tick_params(axis='y', labelcolor=colour)
fig.tight_layout()  
# 





plot_title = 'Iperf3 UDP throughput using different MTUs (localhost)'
fig.savefig(plot_title + ".png")
plt.xscale("log")
plt.title(plot_title)




# # From https://stackoverflow.com/questions/22263807/how-is-order-of-items-in-matplotlib-legend-determined
handles, labels = ax.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
ax.legend(handles, labels)

plt.show()


