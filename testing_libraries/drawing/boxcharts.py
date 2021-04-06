import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from io import StringIO


# def draw_2seq_1par():

# x_ticks        = MTUs
# measurements_A = sender_bitrates
# measurements_B = receiver_bitrates
# measurements_C = receiver_losses

# print(x_ticks)
# print(measurements_A)
# print(measurements_B)
# print(measurements_C)

# fig, ax = plt.subplots()
# ax.plot(MTUs, measurements_A, label='Sender bitrate')
# ax.plot(MTUs, measurements_B, label='Receiver bitrate')
# ax.set(xlabel='MTUs, Bytes' , ylabel='UDP throughput, Bytes/second')
# ax.grid()

# # Chart example taken from:
# # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
# ax_losses = ax.twinx()
# colour = 'tab:red'
# ax_losses.set_ylabel('Proportion of lost datagrams at the receiver side, %', color=colour) 
# ax_losses.plot(MTUs, measurements_C, color=colour)
# ax_losses.tick_params(axis='y', labelcolor=colour)
# fig.tight_layout()  

# plot_title = 'Iperf3 UDP throughput using different MTUs (localhost)'
# fig.savefig(plot_title + ".png")
# plt.xscale("log")
# plt.title(plot_title)

# # # From https://stackoverflow.com/questions/22263807/how-is-order-of-items-in-matplotlib-legend-determined
# handles, labels = ax.get_legend_handles_labels()
# labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
# ax.legend(handles, labels)

# plt.show()



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
    plot_title = title_of_plot
    fig.savefig(plot_title + ".png")
    plt.title(plot_title)
    plt.show()



def draw_line_chart_with_double_y_yxis(
        xaxis_ticks, 
        data_sequences_for_left_y_axis, 
        data_sequences_for_right_y_axis, 
        data_xlabel,
        data_yLlabel,
        data_yRlabel, 
        plot_title):
    fig, ax = plt.subplots()
    for data_sequence in data_sequences_for_left_y_axis:
        ax.plot(xaxis_ticks, data_sequence["measurements"], label=data_sequence["label"])
    ax.set(xlabel=data_xlabel, ylabel=data_yLlabel)
    ax.grid()

    if len(data_sequences_for_right_y_axis) > 0:
    # Chart example taken from:
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
        ax_losses = ax.twinx()
        colour = 'tab:red'
        ax_losses.set_ylabel(data_yRlabel, color=colour) 

        for data_sequence in data_sequences_for_right_y_axis:
            # TODO add more colours for other measurements
            ax_losses.plot(xaxis_ticks, data_sequence["measurements"], label=data_sequence["label"], color=colour)
        ax_losses.tick_params(axis='y', labelcolor=colour)
        fig.tight_layout()  

    fig.savefig(plot_title + ".png")
    plt.xscale("log")
    plt.title(plot_title)

    # # From https://stackoverflow.com/questions/22263807/how-is-order-of-items-in-matplotlib-legend-determined
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(handles, labels)

    plt.show()