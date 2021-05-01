print("Visualising...")


# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np

# 1. Extract data
# Using code and ideas from: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

import os
from os.path import isfile, join
import csv
from statistics import *

# experiment_top_level_folder=os.getcwd()
# print(experiment_top_level_folder)

# onlyfiles = [f for f in os.listdir(experiment_top_level_folder)]
# print(onlyfiles)


number_of_experiments=10



# Using writing functionality from https://www.programiz.com/python-programming/writing-csv-files
with open('summary_of_results.csv', 'w', newline='') as summary_of_results_file:
    results_writer = csv.writer(summary_of_results_file, delimiter=',')
    results_writer.writerow(["number_of_experiments:", number_of_experiments])
    results_writer.writerow(["delay_ms", "probability_of_loss_percentage", "payload_size", "clients_requests", 
        # "min_completion_time_ms",            "max_completion_time_ms",             
        "avg_completion_time_ms",              "stdev_completion_time_ms",

        # "min_requests_per_second",           "max_requests_per_second",            
        # "avg_requests_per_second",           "stdev_requests_per_second",

        #"min_throughput_megabits_per_second", "max_throughput_megabits_per_second", 
        "avg_throughput_megabits_per_second",  "stdev_throughput_megabits_per_second",
        ])

    # 1. Extract data
    for delay_ms in [0]: #1 10 100
        for probability_of_loss_percentage in [0]: #0.0001 0.001 0.01 0.1 1 
            for payload_size in [1000000, 10000000, 100000000, 1000000000]: #1000000000 # 10000000 100000000 1000000000
                for clients_requests in [1, 10]:

                    group_experiment_description=("payload-size_" + str(payload_size) + 
                        "____delay-ms_" + str(delay_ms) + 
                        "____loss-rate-percent_" + str(probability_of_loss_percentage) +
                        "____clients-requests_" + str(clients_requests))
                    experiment_group_folder="./results/" + group_experiment_description
                    print("experiment_group_folder: ", experiment_group_folder)


                    list_completion_time_ms = []
                    list_requests_per_second = []
                    list_throughput_megabits_per_second = []
                    for experiment_number in range(1,number_of_experiments+1):
                        # print("----")
                        # print ("  experiment_number              : ", experiment_number)
                        # print ("  payload_size                   : ", payload_size)
                        # print ("  probability_of_loss_percentage : ", probability_of_loss_percentage)
                        # print ("  delay-ms                       : ", delay_ms)
                        # print ("  clients_requests               : ", clients_requests)
                        
                        individual_experiment_folder= str(experiment_group_folder) + "/" + str(experiment_number)

                        # According to: https://realpython.com/read-write-files-python/
                        with open(individual_experiment_folder+'/completion_time_ms.txt', 'r') as reader:
                            line = reader.readline()
                            completion_time_ms = float(line)

                        with open(individual_experiment_folder+'/requests_per_second.txt', 'r') as reader:
                            line = reader.readline()
                            requests_per_second = float(line)

                        with open(individual_experiment_folder+'/throughput_megabytes_per_second.txt', 'r') as reader:
                            line = reader.readline()
                            throughput_megabits_per_second = float(line)*8
                            
                        print("    completion_time_ms              : ", float(line))
                        print("    requests_per_second             : ", float(requests_per_second))
                        print("    throughput_megabits_per_second : ", float(throughput_megabits_per_second))

                        list_completion_time_ms.append(completion_time_ms)
                        list_requests_per_second.append(requests_per_second)
                        list_throughput_megabits_per_second.append(throughput_megabits_per_second)


                    #1.1 Summarise data
                    max_completion_time_ms = max(list_completion_time_ms)
                    min_completion_time_ms = min(list_completion_time_ms)
                    avg_completion_time_ms = mean(list_completion_time_ms)
                    stdev_completion_time_ms = stdev(list_completion_time_ms)


                    min_requests_per_second = max(list_requests_per_second)             
                    max_requests_per_second = min(list_requests_per_second)             
                    avg_requests_per_second = mean(list_requests_per_second)            
                    stdev_requests_per_second = stdev(list_requests_per_second)


                    min_throughput_megabits_per_second = max(list_throughput_megabits_per_second)  
                    max_throughput_megabits_per_second = min(list_throughput_megabits_per_second)   
                    avg_throughput_megabits_per_second = mean(list_throughput_megabits_per_second)  
                    stdev_throughput_megabits_per_second = stdev(list_throughput_megabits_per_second)  



                    #1.2 Write summarised data
                    results_writer.writerow([delay_ms, probability_of_loss_percentage, payload_size, clients_requests,
                        # min_completion_time_ms,              max_completion_time_ms,              
                        avg_completion_time_ms,              stdev_completion_time_ms,

                        # min_requests_per_second,             max_requests_per_second,             
                        # avg_requests_per_second,             stdev_requests_per_second,

                        # min_throughput_megabits_per_second, max_throughput_megabits_per_second, 
                        avg_throughput_megabits_per_second, stdev_throughput_megabits_per_second])