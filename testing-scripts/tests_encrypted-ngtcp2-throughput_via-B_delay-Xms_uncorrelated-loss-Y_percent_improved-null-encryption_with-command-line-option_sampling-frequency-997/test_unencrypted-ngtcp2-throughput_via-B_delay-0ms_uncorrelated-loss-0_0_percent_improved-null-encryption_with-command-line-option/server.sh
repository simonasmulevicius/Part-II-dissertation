ngtcp2_folder="/root/evaluation/unencrypted_stack/ngtcp2"
echo "ngtcp2_folder: ${ngtcp2_folder}"

echo "Running the following command:"
echo "taskset -c 0 ip netns exec mr_server ${ngtcp2_folder}/examples/server  -q --max-dyn-length 4g -P 10.2.2.101 7777  ${ngtcp2_folder}/examples/server.key ${ngtcp2_folder}/examples/server.cert"
      taskset -c 0 ip netns exec mr_server ${ngtcp2_folder}/examples/server  -q --max-dyn-length 4g -P 10.2.2.101 7777  ${ngtcp2_folder}/examples/server.key ${ngtcp2_folder}/examples/server.cert
