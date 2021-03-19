import subprocess
from io import StringIO
import numpy as np

from testing_libraries.drawing.boxcharts import *
from testing_libraries.util.conversion import *
from testing_libraries.bashterminal.commands import *

# -------------------
# Option 1 - original 

# MTUs = [576, 600, 700, 800, 900, 1000, 
#         1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 
#         2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000]
MTUs = [1300, 1400, 1500]
localhost_measurements = perform_group_of_perf3_measurements(MTUs, "127.0.0.1", True)

MTUs = localhost_measurements["valid_MTUs"]
sender_bitrates = localhost_measurements["sender_bitrates"]
receiver_bitrates = localhost_measurements["receiver_bitrates"]
receiver_losses = localhost_measurements["receiver_losses"]

# Option 2 - old test
# sender_bitrates   = [458.0, 524.0, 763.0]
# receiver_bitrates = [458.0, 524.0, 763.0]
# receiver_losses   = [0.0, 0.0, 0.0]

MTUs_kB = [mtu/1000 for mtu in MTUs]
print(MTUs_kB)
print(sender_bitrates)
print(receiver_bitrates)
print(receiver_losses)


draw_line_chart_with_double_y_yxis( MTUs_kB, 
    [{  "measurements": sender_bitrates, "label": 'Sender bitrate'}, {  "measurements": receiver_bitrates, "label": 'Receiver bitrate'}],
    [{  "measurements": receiver_losses, "label": 'TODO'}],
    'MTUs, kBytes',
    'UDP throughput, Bytes/second',
    'Proportion of lost datagrams at the receiver side, %',
    'Iperf3 UDP throughput using different MTUs (localhost)'
    )