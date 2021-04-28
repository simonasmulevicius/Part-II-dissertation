#!/bin/bash
source env.sh

number_of_experiments=10

for delay_ms in 0 1 10 100
do
    for probability_of_loss in  0 #0.0001 0.001 0.01 0.1 1 
    do
        for payload_size in 1000000 10000000 100000000 1000000000
        do
            for clients_requests in 1 10 
            do
                group_experiment_description="payload-size_${payload_size}____delay-ms_${delay_ms}____loss-rate-percent_${probability_of_loss}____clients-requests_${clients_requests}"
                experiment_group_folder="./results/${group_experiment_description}"
                mkdir "${experiment_group_folder}"

                for experiment_number in $(seq $number_of_experiments); do
                    # Set bidirectional loss rate and delay
                    ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth2 root netem delay ${delay_ms}ms loss ${probability_of_loss}%)"
                    ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth3 root netem delay ${delay_ms}ms loss ${probability_of_loss}%; tc qdisc; printf 'Remote preparation is DONE\n')"

                    #experiment-number_${experiment_number}
                    printf "\n"
                    printf "  --------------------------------\n"
                    printf "  |     Experiment parameters    |\n"
                    printf "  --------------------------------\n"
                    printf "  experiment_number         : ${experiment_number}\n"
                    printf "  payload_size              : ${payload_size}\n"
                    printf "  probability_of_loss       : ${probability_of_loss}%%\n"
                    printf "  delay-ms                  : ${delay_ms}\n"
                    printf "  clients_requests          : ${clients_requests}\n"
                    printf "  --------------------------------\n"
                    individual_experiment_folder="${experiment_group_folder}/${experiment_number}"
                    mkdir "${individual_experiment_folder}"
                    echo "  individual_experiment_folder: ${individual_experiment_folder}"

                    printf "  1.1 Run throughput test\n"
                    command=(        'taskset -c 1 ip netns exec mr_client iperf3 -c 10.2.2.101 --udp -b 0 --bytes "${payload_size}" --parallel "${clients_requests}"' )
                                      
                    printf "   1.1.1 Running command: '${command[@]}' \n"
                    command_output=$( taskset -c 1 ip netns exec mr_client iperf3 -c 10.2.2.101 --udp -b 0 --bytes "${payload_size}" --parallel "${clients_requests}" | tee "${individual_experiment_folder}/result.txt" )
                    

                    printf "  --------------------------------\n"
                    printf "  2 Analyse output \n"
                    printf "  --------------------------------\n"
                    printf "  2.1 Extract relevant fields \n"
                    printf "  --------------------------------\n"
                    relevant_fields=$( tail -3 "${individual_experiment_folder}/result.txt")
                    echo "${relevant_fields}"
                    printf "  --------------------------------\n"


                    receiver_throughput=$( echo ${relevant_fields:36:6} | tr -d ' ' )
                    receiver_throughput_units=$( echo ${relevant_fields:42:10} | tr -d ' ' )
                    # Xbits/second
                    printf "    receiver_throughput                      : [${receiver_throughput}] \n"
                    printf "    receiver_throughput_units                : [${receiver_throughput_units}] \n"

                    receiver_throughput_megabytes_per_second=receiver_throughput


                    if [ "${receiver_throughput_units}" == "Gbits/sec" ] 
                    then
                        # echo "Units:Gbits/sec?"
                        # (1/8*1024*1024*1024/1000/1000) =  134.217728
                        receiver_throughput_megabytes_per_second=$(bc -l <<<"${receiver_throughput}*134.217728")
                    elif [ "${receiver_throughput_units}" == "Mbits/sec" ] 
                    then
                        # echo "Units:Mbits/sec?"
                        # (1/8*1024*1024/1000/1000) =  0.131072
                        receiver_throughput_megabytes_per_second=$(bc -l <<<"${receiver_throughput}*0.131072")
                    elif [ "${receiver_throughput_units}" == "Kbits/sec" ] || [ "${receiver_throughput_units}" == "kbits/sec" ]
                    then
                        # echo "Units:Kbits/sec?"
                         # (1/8*1024/1000/1000) = 0.000128
                        receiver_throughput_megabytes_per_second=$(bc -l <<<"${receiver_throughput}*0.000128")
                    else
                        # echo "Units:bits/sec?"
                        receiver_throughput_megabytes_per_second=$(bc -l <<<"${receiver_throughput}/8000000")
                    fi

                    printf "    receiver_throughput_megabytes_per_second : [${receiver_throughput_megabytes_per_second}] (megaBytes/s) \n"
                    echo "${receiver_throughput_megabytes_per_second}" > "${individual_experiment_folder}/receiver_throughput_megabytes_per_second.txt"

                    printf "  --------------------------------\n"
                    printf "\n\n\n"
                done
            done
        done
    done
done