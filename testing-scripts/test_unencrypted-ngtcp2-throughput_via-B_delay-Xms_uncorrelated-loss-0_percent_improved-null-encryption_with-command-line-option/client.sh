#!/bin/bash
source env.sh

flame_graph_folder="/root/evaluation/FlameGraph"
nghttp2_folder="/root/evaluation/unencrypted_stack/nghttp2"
number_of_experiments=10 #10

for delay_ms in 0 0.1 1 10 100 #1 10 # 100
do
    for probability_of_loss in  0 #0.0001 0.001 0.01 0.1 1 
    do
        for payload_size in 1000000 1000000000 #10000000 100000000 1000000000
        do
            for clients_requests in 1 # 
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
                    command=(        'taskset -c 1 ip netns exec mr_client  "${nghttp2_folder}/src/h2load" --requests "${clients_requests}" --clients "${clients_requests}"  -P  --npn-list h3 "https://10.2.2.101:7777/${payload_size}"' )
                   
                    printf "   1.1.1 Running command: '${command[@]}' \n"
                    command_output=$( taskset -c 1 ip netns exec mr_client  "${nghttp2_folder}/src/h2load" --requests "${clients_requests}" --clients "${clients_requests}"  -P  --npn-list h3 "https://10.2.2.101:7777/${payload_size}"  | tee "${individual_experiment_folder}/result.txt" )
                    

                    printf "  --------------------------------\n"
                    printf "  2 Analyse output"
                    printf "    command_output : \n"
                    printf " %s \n" "${command_output}"
                    printf "  --------------------------------\n"

                    printf "  2.1 Extract relevant fields \n"
                    relevant_fields=$( grep "finished in" "${individual_experiment_folder}/result.txt" )
                    printf "    relevant_fields : $relevant_fields \n"

                    relevant_fields_string=($relevant_fields)
                    completion_time_string=$( echo ${relevant_fields_string[2]} | tr -d ',' )
                    requests_per_second=$( echo ${relevant_fields_string[3]} | tr -d ',' )
                    throughput_string=$( echo ${relevant_fields_string[5]} | tr -d ',' )

                    # printf "    completion_time_string        : [${completion_time_string}] \n"
                    # printf "          time abbreviation: %s \n" "${completion_time_string:(-2)}"


                    completion_time_ms=${completion_time_string::-2}
                    if [ "${completion_time_string:(-2)}" != "ms" ] 
                    then
                        echo "EXTRA ATTENTION!!!!"
                        echo " completion_time_ms: ${completion_time_string::-1} x 1000 (ms)"
                        completion_time_ms=$(bc -l <<<"${completion_time_string::-1}*1000")
                    fi



                    if [ "${throughput_string:(-4)}" == "GB/s" ] 
                    then
                        throughput_megabytes_per_second=$(bc -l <<<"${throughput_string::(-4)}*1024*1024*1024/1000/1000")
                    
                    elif [ "${throughput_string:(-4)}" == "MB/s" ] 
                    then
                        throughput_megabytes_per_second=$(bc -l <<<"${throughput_string::(-4)}*1024*1024/1000/1000")
                    elif [ "${throughput_string:(-4)}" == "kB/s" ] || [ "${throughput_string:(-4)}" == "KB/s" ]
                    then
                        throughput_megabytes_per_second=$(bc -l <<<"${throughput_string::(-4)}*1024/1000/1000")
                    else
                        # B/s
                        throughput_megabytes_per_second=$(bc -l <<<"${throughput_string::(-3)}/1000/1000")
                    fi

                    printf "    completion_time_ms              : [${completion_time_ms}] (ms)\n"
                    printf "    requests_per_second             : [${requests_per_second}] \n"
                    printf "    throughput_megabytes_per_second : [${throughput_megabytes_per_second}] (MBytes/s) \n"

                    echo "${completion_time_ms}" > "${individual_experiment_folder}/completion_time_ms.txt"
                    echo "${requests_per_second}" > "${individual_experiment_folder}/requests_per_second.txt"
                    echo "${throughput_megabytes_per_second}" > "${individual_experiment_folder}/throughput_megabytes_per_second.txt"


                    printf "  --------------------------------\n"
                    printf "\n\n\n"
                done
            done
        done
    done
done
