flame_graph_folder="/root/evaluation/FlameGraph"
nghttp2_folder="/root/evaluation/unencrypted_stack/nghttp2"
sampling_frequency=1979
payload_size=1000000000


number_of_experiments=3
for experiment_number in $(seq $number_of_experiments); do
    echo "Running experiment: ${experiment_number}";
    echo "1. Run throughput test"
    echo "perf record -F ${sampling_frequency} --cpu=1 --call-graph dwarf taskset -c 1 ip netns exec mr_client  ${nghttp2_folder}/src/h2load -P --npn-list h3 https://10.2.2.101:7777/1000000000"
          perf record -F ${sampling_frequency} --cpu=1 --call-graph dwarf taskset -c 1 ip netns exec mr_client  ${nghttp2_folder}/src/h2load -P --npn-list h3 https://10.2.2.101:7777/1000000000

    echo "2. Generate FlameGraph"
    perf script | ${flame_graph_folder}/stackcollapse-perf.pl > out.perf-folded
    output_file_name=perf-kernel__sampling-frequency_${sampling_frequency}__payload-size_${payload_size}__MTU-1252-bytes__experiment-number_${experiment_number}
    ${flame_graph_folder}/flamegraph.pl out.perf-folded > ${output_file_name}.svg

done


