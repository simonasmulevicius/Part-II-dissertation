import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from testing_libraries.drawing.boxcharts import *
from testing_libraries.util.conversion import *
from testing_libraries.bashterminal.commands import *

# 0. Constants
CLIENT_URL = "https://10.2.2.101:7777/" 

payload_sizes          = [ 10,    100,    1024,   10240 ,  102400 ,  1048576,  10485760,  104857600,  1073741824,  4294967295]
payload_sizes_in_bytes = ['10B', '100B', '1KiB', '10KiB', '100KiB', '1MiB',   '10MiB',   '100MiB',   '1GiB',      '4GiB']


# fig, (ax1, ax2, ax3) = plt.subplots(3)
# ax1.plot(payload_sizes, delays)
# ax2.plot(payload_sizes, requests)
# ax3.plot(payload_sizes, throughputs)

# ax1.set(xlabel='Payload size', ylabel='total_delay_ms')
# ax1.grid()
# ax2.set(xlabel='Payload size', ylabel='requests_per_second')
# ax2.grid()
# ax3.set(xlabel='Payload size', ylabel='throughput_KB_per_second')
# ax3.grid()




# # TEST - GSO impact 
# measurements_with_gso    = perform_group_of_measurements([], CLIENT_URL)
# measurements_without_gso = perform_group_of_measurements(["--no-udp-gso"], CLIENT_URL)

# print(payload_sizes)
# print(measurements_with_gso['throughputs'])

# print(payload_sizes)
# print(measurements_without_gso['throughputs'])

# fig, ax = plt.subplots(1)
# ax.plot(payload_sizes, measurements_with_gso['throughputs'],    label='With GSO')
# ax.plot(payload_sizes, measurements_without_gso['throughputs'], label='No GSO')
# ax.set(xlabel='Payload size', ylabel='throughput_KB_per_second')
# ax.grid()

# fig.savefig("test.png")
# plt.xscale("log")
# plt.title('GSO impact on throughput')

# # From https://stackoverflow.com/questions/22263807/how-is-order-of-items-in-matplotlib-legend-determined
# handles, labels = ax.get_legend_handles_labels()
# labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
# ax.legend(handles, labels)

# plt.show()



# ---------------------------------------------------------
# # TEST START 
# ---------------------------------------------------------
# Precondition: server 
# 1. Perform measurements
set_MTU(9000, False)
measurements_baseline  = perform_group_of_h2load_measurements(["taskset", "-c", "1", "ip", "netns", "exec", "mr_client"], [], CLIENT_URL)
# measurements_baseline = {}
# measurements_baseline['throughputs'] = [[0.0791015625, 11.7, 12.3], [26.96, 27.17, 26.3], [163.33, 169.9, 166.29], [1525.76, 1464.32, 1198.08], [10608.64, 10342.4, 10536.96], [46970.88, 43827.2, 53534.72], [82094.08, 87603.2, 82964.48], [31.22, 30.34, 30.66], [30.28, 31.28, 29.61], [30.16, 30.0, 30.16]]

# set_MTU(9000, False)
# measurements_improved  = perform_group_of_h2load_measurements(["taskset", "-c", "1", "ip", "netns", "exec", "mr_client"], [], CLIENT_URL)
measurements_improved = {}
measurements_improved['throughputs'] = [[10.51, 12.71, 12.29], [26.74, 26.25, 25.87], [165.11, 162.17, 170.82], [1495.04, 1505.28, 1484.8], [10403.84, 10547.2, 10475.52], [49274.88, 48138.24, 50933.76], [94289.92, 92282.88, 97525.76], [31.03, 30.35, 30.82], [30.7, 30.39, 31.23], [30.74, 31.19, 32.23]]

print("payload_sizes: "                       , payload_sizes)
print("measurements_baseline['throughputs']: ", measurements_baseline['throughputs'])
print("measurements_improved['throughputs']: ", measurements_improved['throughputs'])

# 2. Draw measurements
draw_boxplot_2seq(payload_sizes_in_bytes,
             measurements_baseline['throughputs'], 
             measurements_improved['throughputs'],
             'MTU = 1280',
             'MTU = 1500',
             'Throughput, KBytes/second', 
             'Throughput when packets go via machine B (A1-to-B-to-A2) using different MTUs')

# draw_boxplot_2seq(payload_sizes_in_bytes,
#              measurements_on_same_cores['delays'], 
#              measurements_on_different_cores['delays'],
#              'Client and server on the same core',
#              'Client and server on different cores',
#              'Delay, ms',
#              'Time required to transfer a file when packets go via machine B (A1-to-B-to-A2)')

# draw_boxplot_2seq(payload_sizes_in_bytes,
#              measurements_on_same_cores['requests'], 
#              measurements_on_different_cores['requests'],
#              'Client and server on the same core',
#              'Client and server on different cores',
#              'Requests per second, (number of requests)/s',
#              'Requests per second when packets go via machine B (A1-to-B-to-A2)')

# ---------------------------------------------------------
# # TEST END
# ---------------------------------------------------------
