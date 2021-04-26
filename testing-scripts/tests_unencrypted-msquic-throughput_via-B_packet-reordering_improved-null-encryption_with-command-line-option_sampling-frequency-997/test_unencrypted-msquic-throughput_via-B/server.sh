#!/bin/bash

msquic_folder="/root/evaluation/msquic_folder/msquic/artifacts/bin/linux/x64_Debug_openssl"
printf "msquic_folder: ${msquic_folder}\n"

printf "Running the following command:\n"
printf "taskset -c 0 ip netns exec mr_server ${msquic_folder}/secnetperf -bind:10.2.2.101\n"
        taskset -c 0 ip netns exec mr_server ${msquic_folder}/secnetperf -bind:10.2.2.101

