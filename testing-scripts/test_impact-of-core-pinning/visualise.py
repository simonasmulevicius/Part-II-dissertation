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
import json



number_of_experiments=10



# Using writing functionality from https://www.programiz.com/python-programming/writing-csv-files
with open('summary_of_results.csv', 'w', newline='') as summary_of_results_file:
    results_writer = csv.writer(summary_of_results_file, delimiter=',')
    results_writer.writerow(["number_of_experiments:", number_of_experiments])
    results_writer.writerow(["delay_ms", "probability_of_loss_percentage", "payload_size", "clients_requests",      
        "min_receiver_throughput_megabits_per_second", "max_receiver_throughput_megabits_per_second", "avg_receiver_throughput_megabits_per_second", "stdev_receiver_throughput_megabits_per_second",
        "min_completion_time_in_miliseconds"         , "max_completion_time_in_miliseconds"         , "avg_completion_time_in_miliseconds"         , "stdev_completion_time_in_miliseconds",
        "min_lost_percent"                           , "max_lost_percent"                           , "avg_lost_percent"                           , "stdev_lost_percent",
        "min_emitted_bytes"                          , "max_emitted_bytes"                          , "avg_emitted_bytes"                          , "stdev_emitted_bytes" 
        ])

    # 1. Extract data
    for delay_ms in [0]: #0 1 10 100
        for probability_of_loss_percentage in [0]: #0.0001 0.001 0.01 0.1 1 
            for payload_size in [1000000, 10000000, 100000000, 1000000000]: #1000000, 10000000, 100000000, 1000000000
                for clients_requests in [1]: #1, 10

                    group_experiment_description=("payload-size_" + str(payload_size) + 
                        "____delay-ms_" + str(delay_ms) + 
                        "____loss-rate-percent_" + str(probability_of_loss_percentage) +
                        "____clients-requests_" + str(clients_requests))
                    experiment_group_folder="./results/" + group_experiment_description
                    print("experiment_group_folder: ", experiment_group_folder)

                    list_receiver_throughput_megabits_per_second = []
                    list_completion_time_in_miliseconds = []
                    list_lost_percent = []
                    list_emitted_bytes=[]

                    

                    for experiment_number in range(1,number_of_experiments+1):
                        print("----")
                        print ("  experiment_number              : ", experiment_number)
                        print ("  payload_size                   : ", payload_size)
                        print ("  probability_of_loss_percentage : ", probability_of_loss_percentage)
                        print ("  delay-ms                       : ", delay_ms)
                        print ("  clients_requests               : ", clients_requests)
                        
                        individual_experiment_folder= str(experiment_group_folder) + "/" + str(experiment_number)


                        # File reading functionality is written according instructions from:
                        # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
                        # https://realpython.com/read-write-files-python/
                        with open(individual_experiment_folder+'/result.json') as results_file:
                            experiment_data = json.load(results_file)
                            experiment_summary = experiment_data['end']['sum']

                            receiver_throughput_megabits_per_second = float(experiment_summary['bits_per_second'])/1000000
                            list_receiver_throughput_megabits_per_second.append(receiver_throughput_megabits_per_second)

                            completion_time_in_miliseconds = float(experiment_summary['seconds'])*1000
                            list_completion_time_in_miliseconds.append(completion_time_in_miliseconds)

                            lost_percent = float(experiment_summary['lost_percent'])
                            list_lost_percent.append(lost_percent)

                            emitted_bytes = float(experiment_summary['bytes'])
                            list_emitted_bytes.append(emitted_bytes)

                            print("    completion_time_in_miliseconds          : ", float(completion_time_in_miliseconds))
                            print("    receiver_throughput_megabits_per_second : ", float(receiver_throughput_megabits_per_second))
                            print("    lost_percent                            : ", float(lost_percent))
                            print("    emitted_bytes                           : ", float(emitted_bytes))


                    #1.1 Summarise data
                    min_receiver_throughput_megabits_per_second   = max(list_receiver_throughput_megabits_per_second)  
                    max_receiver_throughput_megabits_per_second   = min(list_receiver_throughput_megabits_per_second)   
                    avg_receiver_throughput_megabits_per_second   = mean(list_receiver_throughput_megabits_per_second)  
                    stdev_receiver_throughput_megabits_per_second = stdev(list_receiver_throughput_megabits_per_second)  


                    min_completion_time_in_miliseconds   = max(list_completion_time_in_miliseconds)  
                    max_completion_time_in_miliseconds   = min(list_completion_time_in_miliseconds)   
                    avg_completion_time_in_miliseconds   = mean(list_completion_time_in_miliseconds)  
                    stdev_completion_time_in_miliseconds = stdev(list_completion_time_in_miliseconds)  

                    min_lost_percent   = max(list_lost_percent)  
                    max_lost_percent   = min(list_lost_percent)   
                    avg_lost_percent   = mean(list_lost_percent)  
                    stdev_lost_percent = stdev(list_lost_percent)  


                    min_emitted_bytes   = max(list_emitted_bytes)  
                    max_emitted_bytes   = min(list_emitted_bytes)   
                    avg_emitted_bytes   = mean(list_emitted_bytes)  
                    stdev_emitted_bytes = stdev(list_emitted_bytes)  

                    #1.2 Write summarised data
                    results_writer.writerow([delay_ms, probability_of_loss_percentage, payload_size, clients_requests,
                        min_receiver_throughput_megabits_per_second, max_receiver_throughput_megabits_per_second, avg_receiver_throughput_megabits_per_second, stdev_receiver_throughput_megabits_per_second,
                        min_completion_time_in_miliseconds         , max_completion_time_in_miliseconds         , avg_completion_time_in_miliseconds         , stdev_completion_time_in_miliseconds,
                        min_lost_percent                           , max_lost_percent                           , avg_lost_percent                           , stdev_lost_percent,
                        min_emitted_bytes                          , max_emitted_bytes                          , avg_emitted_bytes                          , stdev_emitted_bytes             ])