#!/bin/bash
taskset -c 0 ip netns exec mr_server iperf3 -s