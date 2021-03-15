print("Plotter")
import subprocess
from io import StringIO
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# 0. Constants
NUMBER_OF_REPEATED_EXPERIMENTS = 3


# payload_sizes          = [10,     100,   1024,  10240 , 102400 ]#, 1048576, 10485760, 104857600, 1073741824, 4294967295]
# payload_sizes_in_bytes = ['10B', '100B', '1KB', '10KB', '100KB']#,  '1MB',   '10MB',   '100MB',      '1GB',      '4GB']

payload_sizes          = [10240] #,  102400, 1048576, 10485760] #, 104857600] #, 1073741824, 4294967295]
payload_sizes_in_bytes = ['10KB'] #, '100KB',  '1MB',   '10MB'] #,   '100MB'] #,      '1GB',      '4GB']

# payload_sizes          = [   10,    100,  1024,  10240,  102400, 1048576, 10485760, 104857600, 1073741824, 4294967295]
# payload_sizes_in_bytes = ['10B', '100B', '1KB', '10KB', '100KB',   '1MB',   '10MB',   '100MB',       '1GB',     '4GB']


def perform_measurement(parameters):
    print("parameters: ", parameters)
    command_output = subprocess.run(parameters, stdout=subprocess.PIPE, text=True).stdout
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

def perform_group_of_measurements(parameter_list_prefix, parameter_list_suffix):
    delays      = []
    requests    = []
    throughputs = []

    for payload_size in payload_sizes:
        url = "https://10.2.2.101:7777/" + str(payload_size)
        print(url)

        parameters = parameter_list_prefix.copy()
        parameters.extend(["../../../nghttp2/src/h2load", "--npn-list", "h3", url])
        parameters.extend(parameter_list_suffix)
        print("parameters: ", parameters)
        
        repeated_delays      = []
        repeated_requests    = []
        repeated_throughputs = []
        
        for _ in range(NUMBER_OF_REPEATED_EXPERIMENTS):
            measurements = perform_measurement(parameters)
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




# Box plotter
# The code of this function is taken from: https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
def draw_boxplot_2seq(xaxis_ticks, data_seq1, data_seq2, label1, label2, y_axis_label, title_of_plot):
    ticks = xaxis_ticks

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)

    # plt.figure()
    fig, ax = plt.subplots(1)

    box_plot1 = plt.boxplot(data_seq1, positions=np.array(range(len(data_seq1)))*2.0, sym='', widths=0.6)
    box_plot2 = plt.boxplot(data_seq2, positions=np.array(range(len(data_seq2)))*2.0, sym='', widths=0.6)

    set_box_color(box_plot1, '#D7191C') # colors are from http://colorbrewer2.org/
    set_box_color(box_plot2, '#2C7BB6')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='#D7191C', label=label1)
    plt.plot([], c='#2C7BB6', label=label2)
    plt.legend()

    plt.xticks(range(0, len(ticks) * 2, 2), ticks)
    plt.xlim(-2, len(ticks)*2)

    ax.set(xlabel='Requested file size, Bytes', ylabel=y_axis_label)
    plot_title = title_of_plot
    fig.savefig(plot_title + ".png")
    plt.title(plot_title)
    plt.show()





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
# measurements_with_gso    = perform_group_of_measurements([])
# measurements_without_gso = perform_group_of_measurements(["--no-udp-gso"])

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
# # TEST START - impact of core pinning
# ---------------------------------------------------------
# Precondition: server 
# 1. Perform measurements
measurements_on_same_cores       = perform_group_of_measurements(["taskset", "0x1", "ip", "netns", "exec", "mr_client"], [])
measurements_on_different_cores  = perform_group_of_measurements(["taskset", "0x2", "ip", "netns", "exec", "mr_client"], [])

print(payload_sizes)
print(measurements_on_same_cores['throughputs'])
print(measurements_on_different_cores['throughputs'])

# 2. Draw measurements
draw_boxplot_2seq(payload_sizes_in_bytes,
             measurements_on_same_cores['throughputs'], 
             measurements_on_different_cores['throughputs'],
             'Client and server on the same core',
             'Client and server on different cores',
             'Throughput, KBytes/second', 
             'Throughput when packets go via machine B (A1-to-B-to-A2)')

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









# # OLD Plotter
# measurements_on_same_cores       = perform_group_of_measurements(["taskset", "0x1", "ip", "netns", "exec", "mr_client"], []) #[]
# measurements_on_different_cores  = perform_group_of_measurements(["taskset", "0x2", "ip", "netns", "exec", "mr_client"], []) #[]

# print(payload_sizes)
# print(measurements_on_same_cores['throughputs'])
# print(measurements_on_different_cores['throughputs'])

# fig, ax = plt.subplots(1)
# ax.plot(payload_sizes, measurements_on_same_cores['throughputs'],    label='Client and server on the same core')
# ax.plot(payload_sizes, measurements_on_different_cores['throughputs'],    label='Client and server on different cores')
# ax.set(xlabel='Requested file size, Bytes', ylabel='Throughput, KBytes/second')
# ax.grid()

# plot_title = 'Throughput via node B (A-to-B-to-A)'
# fig.savefig(plot_title + ".png")
# plt.xscale("log")
# plt.title(plot_title)

# # From https://stackoverflow.com/questions/22263807/how-is-order-of-items-in-matplotlib-legend-determined
# handles, labels = ax.get_legend_handles_labels()
# labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
# ax.legend(handles, labels)

# plt.show()