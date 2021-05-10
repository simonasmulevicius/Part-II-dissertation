import json
import statistics
import csv

# 1. Read JSON
with open('h2load_results.txt') as h2load_results_file:
    results_output_JSON = json.load(h2load_results_file)
    # print(results_output_JSON)


    # 2. Compute variation for each payload group for each core individually

    payload_sizes = results_output_JSON["payload_sizes"]
    measurements_on_same_cores_throughputs = results_output_JSON["measurements_on_same_cores_throughputs"]
    measurements_on_different_cores_throughputs = results_output_JSON["measurements_on_different_cores_throughputs"]

    # print(measurements_on_same_cores_throughputs)
    throughput_stdevs_on_same_cores = [statistics.stdev(list_of_througput) for list_of_througput in measurements_on_same_cores_throughputs]
    print(throughput_stdevs_on_same_cores)
    throughput_stdevs_on_different_cores = [statistics.stdev(list_of_througput) for list_of_througput in measurements_on_different_cores_throughputs]
    print(throughput_stdevs_on_different_cores)
    

    # 3. Visualise the results
    # Using writing functionality from https://www.programiz.com/python-programming/writing-csv-files
    with open('throughput_stdevs.csv', 'w', newline='') as summary_of_results_file:
        results_writer = csv.writer(summary_of_results_file, delimiter=',')
        
        results_writer.writerow(["payload_sizes_in_bytes"] + payload_sizes)
        results_writer.writerow(["throughput_stdevs_on_same_cores"] + throughput_stdevs_on_same_cores)
        results_writer.writerow(["throughput_stdevs_on_different_cores"] + throughput_stdevs_on_different_cores)
