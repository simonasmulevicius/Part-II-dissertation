#!/bin/bash

ngtcp2_folder="/root/evaluation/unencrypted_stack/ngtcp2"
printf "ngtcp2_folder: ${ngtcp2_folder}\n"

printf "Running the following command:\n"
printf "taskset -c 0 ip netns exec mr_server ${ngtcp2_folder}/examples/server -q --max-dyn-length 4g  -P  10.2.2.101 7777  ${ngtcp2_folder}/examples/server.key ${ngtcp2_folder}/examples/server.cert\n"
        taskset -c 0 ip netns exec mr_server ${ngtcp2_folder}/examples/server -q --max-dyn-length 4g  -P  10.2.2.101 7777  ${ngtcp2_folder}/examples/server.key ${ngtcp2_folder}/examples/server.cert

