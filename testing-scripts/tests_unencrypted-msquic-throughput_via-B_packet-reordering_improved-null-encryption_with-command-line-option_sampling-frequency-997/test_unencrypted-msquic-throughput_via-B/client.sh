#!/bin/bash
source env.sh

flame_graph_folder="/root/evaluation/FlameGraph"
msquic_folder="/root/evaluation/msquic_folder/msquic/artifacts/bin/linux/x64_Debug_openssl"

number_of_experiments=1

for delay_ms in 0 #0.01 0.1 1 10 
do
    for probability_of_reordering in 0 #0.0001 0.001 0.01 0.1 1 
    do
        for payload_size in 1000000 #10000000 100000000 1000000000
        do
            for clients_requests in 1 # 10 
            do
                group_experiment_description="payload-size_${payload_size}____delay-ms_${delay_ms}____loss-rate-percent_${probability_of_loss}____clients-requests_${clients_requests}"
                experiment_group_folder="./results/${group_experiment_description}"
                mkdir "${experiment_group_folder}"

                # TODO make use of clients_requests
                for experiment_number in $(seq $number_of_experiments); do
                    # Set bidirectional loss rate and delay
                    printf " ------------------------------------ \n\n"
                    ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth2 root netem delay ${delay_ms}ms reorder ${probability_of_reordering}% 0%)"
                    ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth3 root netem delay ${delay_ms}ms reorder ${probability_of_reordering}% 0%; tc qdisc; printf 'DONE\n')"

                    
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

                    printf "1.1 Run throughput test\n"
                    command=( 'taskset -c 1 ip netns exec mr_client "${msquic_folder}/secnetperf" -TestName:Throughput -target:10.2.2.101 -encrypt:0 "-upload:${payload_size}" -stats:1' )
                    printf "1.1.1 Running command: ${command[@]}\n"
                    command_output=$( taskset -c 1 ip netns exec mr_client "${msquic_folder}/secnetperf" -TestName:Throughput -target:10.2.2.101 -encrypt:0 "-upload:${payload_size}" -stats:1 | tee "${individual_experiment_folder}/result.txt" )


                    # printf "${command_output}"  | tee "./results/${individual_experiment_description}/output-log.txt"

                    # printf "1.2 Generate FlameGraph\n"

                    # perf script | "${flame_graph_folder}/stackcollapse-perf.pl" > ${experiment_folder}/out.perf-folded
                    # "${flame_graph_folder}/flamegraph.pl" ${experiment_folder}/out.perf-folded > ${experiment_folder}/perf-kernel.svg

                    
                    # printf "1.3 Prepare for FlameGraph difference\n"
                    # ${flame_graph_folder}/stackcollapse-perf.pl "${experiment_folder}/out.stacks" >  "${experiment_folder}/out.folded"
                    # ${flame_graph_folder}/flamegraph.pl "${experiment_folder}/out.folded" > ${experiment_folder}/${individual_experiment_description}.svg



                    # ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth2 root netem delay ${delay_ms}ms reorder 0% 0%)"
                    # ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth3 root netem delay ${delay_ms}ms reorder 0% 0%; tc qdisc; printf 'DONE\n')"

                    # individual_experiment_description_0_percent_packet_reordering="sampling-frequency_${sampling_frequency}__payload-size_${payload_size}__MTU-1252-bytes__delay-ms-${delay_ms}__loss-rate-0-percent__experiment-number_${experiment_number}"
                    
                    # printf "1.4 Running experiment with 0%% packet reordering\n"


                    # printf "2.1 Run throughput test\n"
                    # printf " Running command:\n"
                    # perf record -F "${sampling_frequency}" --cpu=1 --call-graph dwarf taskset -c 1 ip netns exec mr_client  "${msquic_folder}/src/h2load"  --npn-list h3 "https://10.2.2.101:7777/${payload_size}"
                    # # printf "Command output: ${command_output}"
                

                    # printf "2.2 Generate FlameGraph\n"
                    # perf script > "${experiment_folder}/out_0_percent_packet_reordering.stacks"
                    
                    # printf "2.3 Prepare for FlameGraph difference\n"
                    # ${flame_graph_folder}/stackcollapse-perf.pl "${experiment_folder}/out_0_percent_packet_reordering.stacks" >  "${experiment_folder}/out_0_percent_packet_reordering.folded"
                    # ${flame_graph_folder}/flamegraph.pl "${experiment_folder}/out_0_percent_packet_reordering.folded" > ${experiment_folder}/${individual_experiment_description_0_percent_packet_reordering}.svg



                    # printf "3.1 Generate FlameGraph difference\n"
                    # ${flame_graph_folder}/difffolded.pl "${experiment_folder}/out_0_percent_packet_reordering.folded" "${experiment_folder}/out.folded" | ${flame_graph_folder}/flamegraph.pl > ${experiment_folder}/difference_loss-rate-${probability_of_reordering}-percent_vs_loss-rate-0-percent_.svg
                    # ${flame_graph_folder}/difffolded.pl "${experiment_folder}/out.folded" "${experiment_folder}/out_0_percent_packet_reordering.folded" | ${flame_graph_folder}/flamegraph.pl > ${experiment_folder}/difference_loss-rate-0-percent_vs_loss-rate-${probability_of_reordering}-percent_.svg

                    printf " ------------------------------------ \n"
                    printf "\n\n\n\n"
                done
            done
        done
    done
done
