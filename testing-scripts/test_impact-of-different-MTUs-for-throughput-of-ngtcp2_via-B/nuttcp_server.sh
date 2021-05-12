#!/bin/bash
source env.sh

taskset -c 0 ip netns exec mr_server nuttcp -S --nofork