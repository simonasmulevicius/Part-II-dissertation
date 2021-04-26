#!/bin/bash
source env.sh

flame_graph_folder="/root/evaluation/FlameGraph"
nghttp2_folder="/root/evaluation/unencrypted_stack/nghttp2"
sampling_frequency=997

number_of_experiments=1



printf "CORRECT!\n"



for delay_ms in 10 #0.01 0.1 1 10 # 1 # 10 100 
do
    for probability_of_reordering in 0.1 # 0.01 0.1  # 0.1 # 0.1 1 # 0 0.0001 0.001 0.01 0.1 1 
    do
        for payload_size in 100000000 # 10000000 100000000 1000000000
        do
            for experiment_number in $(seq $number_of_experiments); do
                # Set bidirectional loss rate and delay
                ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth2 root netem delay ${delay_ms}ms reorder ${probability_of_reordering}% 0%)"
                ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth3 root netem delay ${delay_ms}ms reorder ${probability_of_reordering}% 0%; tc qdisc; printf 'DONE\n')"


                individual_experiment_description="sampling-frequency_${sampling_frequency}__payload-size_${payload_size}__MTU-1252-bytes__delay-ms-${delay_ms}__loss-rate-${probability_of_reordering}-percent__experiment-number_${experiment_number}"
                
                printf "Running experiment\n"
                printf "  experiment_number         : ${experiment_number}\n"
                printf "  payload_size              : ${payload_size}\n"
                printf "  probability_of_reordering : ${probability_of_reordering}\n"
                printf "  delay-ms                  : ${delay_ms}\n"

                printf "1.1 Run throughput test\n"
                command=( perf record -F "${sampling_frequency}" --cpu=1 --call-graph dwarf taskset -c 1 ip netns exec mr_client  "${nghttp2_folder}/src/h2load"  --npn-list h3 "https://10.2.2.101:7777/${payload_size}" )

                printf "1.1.1 Running command: ${command[@]}\n"
                          perf record -F "${sampling_frequency}" --cpu=1 --call-graph dwarf taskset -c 1 ip netns exec mr_client  "${nghttp2_folder}/src/h2load"  --npn-list h3 "https://10.2.2.101:7777/${payload_size}"

                # printf "Command output: ${command_output}"
            

                experiment_folder="./results/${individual_experiment_description}"
                mkdir "${experiment_folder}"
                # printf "${command_output}"  | tee "./results/${individual_experiment_description}/output-log.txt"

                printf "1.2 Generate FlameGraph"
                perf script > "${experiment_folder}/out.stacks"
                
                
                printf "1.3 Prepare for FlameGraph difference\n"
                ${flame_graph_folder}/stackcollapse-perf.pl "${experiment_folder}/out.stacks" >  "${experiment_folder}/out.folded"
                ${flame_graph_folder}/flamegraph.pl "${experiment_folder}/out.folded" > ${experiment_folder}/${individual_experiment_description}.svg





                ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth2 root netem delay ${delay_ms}ms reorder 0% 0%)"
                ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth3 root netem delay ${delay_ms}ms reorder 0% 0%; tc qdisc; printf 'DONE\n')"

                individual_experiment_description_0_percent_packet_reordering="sampling-frequency_${sampling_frequency}__payload-size_${payload_size}__MTU-1252-bytes__delay-ms-${delay_ms}__loss-rate-0-percent__experiment-number_${experiment_number}"
                
                printf "1.4 Running experiment with 0%% packet reordering\n"


                printf "2.1 Run throughput test\n"
                printf " Running command:\n"
                perf record -F "${sampling_frequency}" --cpu=1 --call-graph dwarf taskset -c 1 ip netns exec mr_client  "${nghttp2_folder}/src/h2load" --npn-list h3 "https://10.2.2.101:7777/${payload_size}"
                # printf "Command output: ${command_output}"
            

                printf "2.2 Generate FlameGraph\n"
                perf script > "${experiment_folder}/out_0_percent_packet_reordering.stacks"
                
                printf "2.3 Prepare for FlameGraph difference\n"
                ${flame_graph_folder}/stackcollapse-perf.pl "${experiment_folder}/out_0_percent_packet_reordering.stacks" >  "${experiment_folder}/out_0_percent_packet_reordering.folded"
                ${flame_graph_folder}/flamegraph.pl "${experiment_folder}/out_0_percent_packet_reordering.folded" > ${experiment_folder}/${individual_experiment_description_0_percent_packet_reordering}.svg



                printf "3.1 Generate FlameGraph difference\n"
                ${flame_graph_folder}/difffolded.pl "${experiment_folder}/out_0_percent_packet_reordering.folded" "${experiment_folder}/out.folded" | ${flame_graph_folder}/flamegraph.pl > ${experiment_folder}/difference_loss-rate-${probability_of_reordering}-percent_vs_loss-rate-0-percent_.svg
                ${flame_graph_folder}/difffolded.pl "${experiment_folder}/out.folded" "${experiment_folder}/out_0_percent_packet_reordering.folded" | ${flame_graph_folder}/flamegraph.pl > ${experiment_folder}/difference_loss-rate-0-percent_vs_loss-rate-${probability_of_reordering}-percent_.svg

                printf "\n\n\n\n"
            done
        done
    done
done
