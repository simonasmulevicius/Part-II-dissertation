#!/bin/bash

echo "Running IRQ test..."
service irqbalance start 
taskset -c 1 ip netns exec mr_client nuttcp -l1448 -T60  -u -w4m -Ru -fparse  10.2.2.101 > ./with_IRQ.txt

service irqbalance stop
taskset -c 1 ip netns exec mr_client nuttcp -l1448 -T60  -u -w4m -Ru -fparse  10.2.2.101 > ./without_IRQ.txt

echo "Finnished IRQ test"