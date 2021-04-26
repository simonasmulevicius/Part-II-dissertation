#!/bin/bash
source env.sh

flame_graph_folder="/root/evaluation/FlameGraph"
msquic_folder="/root/evaluation/msquic_folder/msquic/artifacts/bin/linux/x64_Debug_openssl"
sampling_frequency=997
number_of_experiments=1


printf " -----------------\n"
# Date formatting taken from: https://www.cyberciti.biz/faq/unix-linux-getting-current-date-in-bash-ksh-shell-script/
date +'%d/%m/%Y'
printf " -----------------\n"


for delay_ms in 10 # 0.01 0.1 1 10 
do
    for probability_of_reordering in 0.1 # 0.0001 0.001 0.01 0.1 1 
    do
        for payload_size in 100000000 # 1000000 10000000 100000000 1000000000
        do
            for experiment_number in $(seq $number_of_experiments); do
                # Set bidirectional loss rate and delay
                printf " ------------------------------------ \n\n"
                ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth2 root netem delay ${delay_ms}ms reorder ${probability_of_reordering}% 0%)"
                ssh user109@172.26.195.184 "( printf ${SSH_PASSWORD} | sudo -S tc qdisc change dev eth3 root netem delay ${delay_ms}ms reorder ${probability_of_reordering}% 0%; tc qdisc; printf 'DONE\n')"


                individual_experiment_description="sampling-frequency_${sampling_frequency}__payload-size_${payload_size}__delay-ms-${delay_ms}__loss-rate-${probability_of_reordering}-percent__experiment-number_${experiment_number}"
                
                printf "\n\n Running experiment\n"
                printf "  experiment_number         : ${experiment_number}\n"
                printf "  payload_size              : ${payload_size}\n"
                printf "  probability_of_reordering : ${probability_of_reordering}\n"
                printf "  delay-ms                  : ${delay_ms}\n"


                # # NOT Using "perf"
                printf "1.1 Run throughput test\n"
                command='( taskset -c 1 ip netns exec mr_client "${msquic_folder}/secnetperf" -TestName:Throughput -target:10.2.2.101 -encrypt:0 "-download:${payload_size}" -stats:1 )'
                printf "1.1.1 Running command: ${command[@]}\n"
                           taskset -c 1 ip netns exec mr_client "${msquic_folder}/secnetperf" -TestName:Throughput -target:10.2.2.101 -encrypt:0 "-download:${payload_size}" -stats:1

            
                # # Using "perf"
                # printf "1.1 Run throughput test\n"
                # command='( perf record -F "${sampling_frequency}" --cpu 1 --call-graph dwarf taskset -c 1 ip netns exec mr_client "${msquic_folder}/secnetperf" -TestName:Throughput -target:10.2.2.101 -encrypt:0 "-download:${payload_size}" -stats:1 )'
                # printf "1.1.1 Running command: ${command[@]}\n"
                #            perf record -F "${sampling_frequency}" --cpu 1 --call-graph dwarf taskset -c 1 ip netns exec mr_client "${msquic_folder}/secnetperf" -TestName:Throughput -target:10.2.2.101 -encrypt:0 "-download:${payload_size}" -stats:1




                # experiment_folder="./results/${individual_experiment_description}"
                # mkdir "${experiment_folder}"
                # # printf "${command_output}"  | tee "./results/${individual_experiment_description}/output-log.txt"


                # printf "1.2 Generate FlameGraph\n"
                # perf script | "${flame_graph_folder}/stackcollapse-perf.pl" > ${experiment_folder}/out.folded
                # "${flame_graph_folder}/flamegraph.pl" ${experiment_folder}/out.folded > ${experiment_folder}/perf-kernel.svg

                

                printf " ------------------------------------ \n"
                printf "\n\n\n\n"
            done
        done
    done
done
