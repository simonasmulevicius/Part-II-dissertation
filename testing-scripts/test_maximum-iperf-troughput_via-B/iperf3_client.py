import subprocess
from io import StringIO
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from testing_libraries.drawing.boxcharts import *
from testing_libraries.util.conversion import *
from testing_libraries.bashterminal.commands import *

# -------------------
# Option 1 - original 

# MTUs = [500, 750, 800, 900, 1000, 
#         1100, 1200, 1300, 1400, 1500, 1600, 1750, 1800, 1900, 
#         2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
MTUs = [1280, 1500, 9000]

measurement_results = perform_group_of_perf3_measurements(MTUs, "10.2.2.101", False)
MTUs = measurement_results["valid_MTUs"]
sender_bitrates = measurement_results["sender_bitrates"]
receiver_bitrates = measurement_results["receiver_bitrates"]
receiver_losses = measurement_results["receiver_losses"]

measurements_A = sender_bitrates
measurements_B = receiver_bitrates
measurements_C = receiver_losses

# -------------------
# Option 2 - old short (localhost)
# measurements_A = [458.0, 524.0, 763.0]
# measurements_B = [458.0, 524.0, 763.0]
# measurements_C = [0.0, 0.0, 0.0]

# -------------------
# Option 3.1 - old long (localhost)
# MTUs = [100, 200, 400, 500, 750, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1750, 1800, 1900, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000]
# measurements_A = [8270643.2, 24772608.0, 58195968.0, 74842112.0, 115212288.0, 123076608.0, 142270791.68, 161061273.6, 175825223.68, 193273528.32, 209379655.68, 226827960.32, 244276264.96, 261724569.6, 279172874.24, 285883760.64, 297963356.16, 315411660.8, 476472934.4, 621428080.64, 759672340.48, 897916600.32, 1042871746.56, 1099243192.32, 1209301729.28, 1307280670.72, 1422707916.8, 1503238553.6, 1610612736.0, 1717986918.4, 1785095782.4, 1892469964.8, 1798517555.2, 1838782873.6, 1905891737.6, 1986422374.4, 1999844147.2, 2120640102.4, 2187748966.4, 2241436057.6, 2281701376.0, 2362232012.8, 2389075558.4, 2375653785.6, 2483027968.0, 2496449740.8, 2590402150.4, 2684354560.0]
# measurements_B = [8087142.4, 24641536.0, 58195968.0, 74711040.0, 115212288.0, 122814464.0, 142270791.68, 161061273.6, 175825223.68, 193273528.32, 209379655.68, 226827960.32, 244276264.96, 260382392.32, 277830696.96, 284541583.36, 297963356.16, 314069483.52, 475130757.12, 620085903.36, 756987985.92, 895232245.76, 1041529569.28, 1092532305.92, 1205275197.44, 1300569784.32, 1422707916.8, 1489816780.8, 1597190963.2, 1717986918.4, 1785095782.4, 1892469964.8, 1785095782.4, 1825361100.8, 1892469964.8, 1973000601.6, 1986422374.4, 2107218329.6, 2160905420.8, 2214592512.0, 2268279603.2, 2335388467.2, 2375653785.6, 2348810240.0, 2456184422.4, 2496449740.8, 2576980377.6, 2670932787.2]
# measurements_C = [2.2, 0.2, 0.17, 0.14, 0.064, 0.22, 0.19, 0.2, 0.26, 0.18, 0.1, 0.14, 0.24, 0.57, 0.19, 0.45, 0.23, 0.23, 0.28, 0.27, 0.26, 0.22, 0.14, 0.56, 0.38, 0.5, 0.58, 0.5, 0.44, 0.4, 0.43, 0.33, 0.76, 0.79, 0.77, 0.64, 0.78, 0.7, 0.72, 0.82, 0.72, 0.77, 0.65, 0.87, 0.99, 0.48, 0.44, 0.72]

# -------------------
# Option 3.2 - old long (A1-B-A2)
# MTUs = [100, 200, 400, 500, 750, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1750, 1800, 1900, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
# measurements_A = [21626880.0, 65404928.0, 153008209.92, 187904819.2, 255013683.2, 276488519.68, 314069483.52, 352992624.64, 385204879.36, 418759311.36, 454998097.92, 496605593.6, 526133493.76, 566398812.16, 386547056.64, 402653184.0, 418759311.36, 445602856.96, 677799526.4, 571767521.28, 677799526.4, 820070318.08, 950261514.24, 652298158.08, 732828794.88]
# measurements_B = [19267584.0, 56492032.0, 127401984.0, 162403450.88, 222801428.48, 240249733.12, 275146342.4, 307358597.12, 336886497.28, 362387865.6, 395942297.6, 433523261.44, 456340275.2, 492579061.76, 374467461.12, 390573588.48, 406679715.84, 432181084.16, 664377753.6, 532844380.16, 634849853.44, 781147176.96, 766383226.88, 636192030.72, 714038312.96]
# measurements_C = [11.0, 14.0, 15.0, 14.0, 13.0, 13.0, 12.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 3.1, 3.0, 3.0, 3.1, 2.0, 6.8, 6.3, 4.6, 19.0, 2.6, 2.6]



print(MTUs_kB)
print(measurements_A)
print(measurements_B)
print(measurements_C)


MTUs_kB = [mtu/1000 for mtu in MTUs]
draw_boxplot_2seq(MTUs_kB, sender_bitrates, receiver_bitrates, 
    "Sender bitrate", "Receiver bitrate", 'MTUs, kBytes', 
    'UDP throughput, Bytes/second', 'Iperf3 UDP throughput using different MTUs (A1-B-A2)')


# draw_line_chart_with_double_y_yxis(
#     MTUs_kB, 
#     [{  "measurements": measurements_A, "label": 'Sender bitrate'}, {  "measurements": measurements_B, "label": 'Receiver bitrate'}],
#     [{  "measurements": measurements_C, "label": 'TODO'}],
#     'MTUs, kBytes',
#     'UDP throughput, Bytes/second',
#     'Proportion of lost datagrams at the receiver side, %',
#     'Iperf3 UDP throughput using different MTUs (A1-B-A2)'
#     )