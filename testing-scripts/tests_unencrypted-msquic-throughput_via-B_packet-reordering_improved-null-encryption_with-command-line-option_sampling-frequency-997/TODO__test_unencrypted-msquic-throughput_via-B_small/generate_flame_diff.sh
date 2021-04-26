flame_graph_folder="/root/evaluation/FlameGraph"

test_name_1="sampling-frequency_997__payload-size_1000000000__delay-ms-10__loss-rate-0-percent__experiment-number_1"
test_name_2="sampling-frequency_997__payload-size_1000000000__delay-ms-10__loss-rate-0.1-percent__experiment-number_1"




"${flame_graph_folder}/difffolded.pl" "./results/${test_name_1}/out.folded" "./results/${test_name_2}/out.folded" | ${flame_graph_folder}/flamegraph.pl > ./diff_${test_name_2}_minus_${test_name_1}.svg