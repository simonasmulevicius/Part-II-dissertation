#!/bin/bash
stringZ="[SUM]   0.00-0.00   sec  1.53 MBytes  3.74 Gbits/sec                  receiver"
echo ${stringZ:36:6}
echo ${stringZ:42:10}