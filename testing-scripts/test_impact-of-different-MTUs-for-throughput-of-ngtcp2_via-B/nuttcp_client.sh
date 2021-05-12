#!/bin/bash
source env.sh


number_of_experiments=10


# Instructions how to run nuttcp for high-throughput UDP links were taken from:
# https://fasterdata.es.net/performance-testing/network-troubleshooting-tools/nuttcp/

echo "MTU=1280"
for experiment_number in $(seq $number_of_experiments); do
    experiment_output=$( taskset -c 1 ip netns exec mr_client nuttcp -l1228 -T10 -u -w4m -Ru  -fparse 10.2.2.101 )
    echo ${experiment_output} > "./mtu_1280/${experiment_number}"
done

echo "MTU=1500"
for experiment_number in $(seq $number_of_experiments); do
    experiment_output=$( taskset -c 1 ip netns exec mr_client nuttcp -l1448 -T10 -u -w4m -Ru  -fparse 10.2.2.101 )
    echo ${experiment_output} > "./mtu_1500/${experiment_number}"
done

echo "MTU=9000"
for experiment_number in $(seq $number_of_experiments); do
    experiment_output=$( taskset -c 1 ip netns exec mr_client nuttcp -l8948 -T10 -u -w4m -Ru  -fparse 10.2.2.101 )
    echo ${experiment_output} > "./mtu_9000/${experiment_number}"
done
