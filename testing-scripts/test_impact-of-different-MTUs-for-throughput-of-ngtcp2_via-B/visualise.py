import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from io import StringIO

# Increase the font size according to https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
plt.rc('font', size=11)          


throughputs_mtu_1280 = []
for i in range(1,11):
    experiment_output_array = open("./mtu_1280/" + str(i), "r").read().split()
    experiment_output_fields = [ key_value_pair for key_value_pair in experiment_output_array if key_value_pair.startswith("rate_Mbps=") ]
    
    assert(len(experiment_output_fields) == 1)

    experiment_throughput_Mbps = float(experiment_output_fields[0].replace("rate_Mbps=", ""))
    # print(experiment_throughput_Mbps) 
    throughputs_mtu_1280.append(experiment_throughput_Mbps)


throughputs_mtu_1500 = []
for i in range(1,11):
    experiment_output_array = open("./mtu_1500/" + str(i), "r").read().split()
    experiment_output_fields = [ key_value_pair for key_value_pair in experiment_output_array if key_value_pair.startswith("rate_Mbps=") ]
    
    assert(len(experiment_output_fields) == 1)

    experiment_throughput_Mbps = float(experiment_output_fields[0].replace("rate_Mbps=", ""))
    # print(experiment_throughput_Mbps) 
    throughputs_mtu_1500.append(experiment_throughput_Mbps)

throughputs_mtu_9000 = []
for i in range(1,11):
    experiment_output_array = open("./mtu_9000/" + str(i), "r").read().split()
    experiment_output_fields = [ key_value_pair for key_value_pair in experiment_output_array if key_value_pair.startswith("rate_Mbps=") ]
    
    assert(len(experiment_output_fields) == 1)

    experiment_throughput_Mbps = float(experiment_output_fields[0].replace("rate_Mbps=", ""))
    # print(experiment_throughput_Mbps) 
    throughputs_mtu_9000.append(experiment_throughput_Mbps)

assert(len(throughputs_mtu_1500) == len(throughputs_mtu_1280))
assert(len(throughputs_mtu_1500) == len(throughputs_mtu_9000))

print(throughputs_mtu_1280)
print(throughputs_mtu_1500)
print(throughputs_mtu_9000)


# Box plotter
# The code of this function is taken from: https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
def draw_boxplot_2seq(xaxis_ticks, data_seq1, data_seq2, label1, label2, x_axis_label, y_axis_label, title_of_plot):
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

    ax.set(xlabel=x_axis_label, ylabel=y_axis_label)
    fig.savefig(title_of_plot + ".png")
    plt.title(title_of_plot)

    plt.show()

# Box plotter
# The code of this function is taken from: https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
def draw_boxplot_3seq(xaxis_ticks, data_seq1, data_seq2, data_seq3, label1, label2, label3, x_axis_label, y_axis_label, title_of_plot):
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
    box_plot3 = plt.boxplot(data_seq3, positions=np.array(range(len(data_seq2)))*2.0, sym='', widths=0.6)

    # colors are from http://colorbrewer2.org/
    set_box_color(box_plot1, '#1a9641') 
    set_box_color(box_plot2, '#a6d96a')
    set_box_color(box_plot3, '#d7191c')
    
    # draw temporary lines and use them to create a legend
    plt.plot([], c='#1a9641', label=label1)
    plt.plot([], c='#a6d96a', label=label2)
    plt.plot([], c='#d7191c', label=label3)
    plt.legend()

    plt.xticks(range(0, len(ticks) * 2, 2), ticks)
    plt.xlim(-2, len(ticks)*2)

    ax.set(xlabel=x_axis_label, ylabel=y_axis_label)
    fig.savefig(title_of_plot + ".png")
    plt.title(title_of_plot)

    plt.show()


draw_boxplot_3seq([1280, 1500, 9000], [throughputs_mtu_1280, [], []], [[], throughputs_mtu_1500, []], [[], [], throughputs_mtu_9000], "using MTU of 1280 bytes", "using MTU of 1500 bytes", "using MTU of 9000 bytes", 'MTUs, Bytes', 'UDP throughput, Mbits/second', 'nuttcp UDP throughput using different MTUs \n (packets travel via the intermediate machine) \n')