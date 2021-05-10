#!/bin/bash
source env.sh

number_of_experiments=10 #
draw_a_diagram=0
ngtcp2_servers_folder="/root/evaluation/unencrypted_stack/ngtcp2/examples/servers_folder"


for delay_ms in 0 #1 10 100
do
    for probability_of_loss in 0 #0.0001 0.001 0.01 0.1 1 
    do
        for payload_size in 1000000 10000000 100000000 1000000000 #1000000 10000000 100000000 1000000000
        do
            for clients_requests in 1 # 1 10 
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


                    additional_parameters_for_drawing=""
                    if [ ${draw_a_diagram} == 1 ] 
                    then
                        additional_parameters_for_drawing="--interval 0.1"
                    fi

                    printf "  1.1 Run throughput test\n"
                    command=(        'taskset -c 1 ip netns exec mr_client /root/evaluation/iperf/src/iperf3 -c 10.2.2.101 --udp -b 0 --bytes "${payload_size}" --parallel "${clients_requests}" --json ${additional_parameters_for_drawing}' )
                                        
                    printf "   1.1.1 Running command: '${command[@]}' \n"
                    command_output=$( taskset -c 1 ip netns exec mr_client /root/evaluation/iperf/src/iperf3 -c 10.2.2.101 --udp -b 0 --bytes "${payload_size}" --parallel "${clients_requests}" --json  ${additional_parameters_for_drawing} > "${individual_experiment_folder}/result.json" )
                   


                done
            done
        done
    done
done
