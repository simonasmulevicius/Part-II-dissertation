taskset -c 1 ip netns exec mr_client iperf3 -c 10.2.2.101 --udp -b 0 -l 65507

taskset -c 1 ip netns exec mr_client iperf3 -c 10.2.2.101 --udp -b 0 -l 1470