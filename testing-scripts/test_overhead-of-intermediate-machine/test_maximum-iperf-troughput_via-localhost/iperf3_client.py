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
# MTUs = [1280, 1500, 9000]
# localhost_measurements = perform_group_of_perf3_measurements(MTUs, "127.0.0.1", True)

# MTUs = localhost_measurements["valid_MTUs"]
# sender_bitrates = localhost_measurements["sender_bitrates"]
# receiver_bitrates = localhost_measurements["receiver_bitrates"]
# receiver_losses = localhost_measurements["receiver_losses"]

# MTUs_kB = [mtu/1000 for mtu in MTUs]
# print(MTUs_kB)
# print(sender_bitrates)
# print(receiver_bitrates)
# print(receiver_losses)


# draw_line_chart_with_double_y_yxis( MTUs_kB, 
#     [{  "measurements": sender_bitrates, "label": 'Sender bitrate'}, {  "measurements": receiver_bitrates, "label": 'Receiver bitrate'}],
#     [{  "measurements": receiver_losses, "label": 'TODO'}],
#     'MTUs, kBytes',
#     'UDP throughput, Bytes/second',
#     'Proportion of lost datagrams at the receiver side, %',
#     'Iperf3 UDP throughput using different MTUs (localhost)'
#     )


MTUs_kB = [1.28, 1.5, 9.0]
sender_bitrates = [[187904819.2, 189246996.48, 187904819.2], [217432719.36, 221459251.2, 230854492.16], [1169036410.88, 1139508510.72, 1175747297.28]]
receiver_bitrates = [[185220464.64, 179851755.52, 179851755.52], [209379655.68, 213406187.52, 229512314.88], [1158298992.64, 1139508510.72, 1175747297.28]]
receiver_losses = [[1.2, 5.0, 4.5], [3.7, 4.1, 0.36], [0.85, 0.01, 0.0013]]



draw_boxplot_2seq(MTUs_kB, sender_bitrates, receiver_bitrates, "Sender bitrate", "Receiver bitrate", 'MTUs, kBytes', 'UDP throughput, Bytes/second', 'Iperf3 UDP throughput using different MTUs (localhost)')