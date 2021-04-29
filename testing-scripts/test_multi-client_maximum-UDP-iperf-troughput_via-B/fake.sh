#!/bin/bash


# $1 - receiver_throughput
# $2 - receiver_throughput_units
function convert_throughput_to_MBytes_per_second() {
    return_receiver_throughput_megabytes_per_second="$1"
    if [ "$2" == "Gbits/sec" ] 
    then
        # echo "Units:Gbits/sec?"
        # (1/8*1024*1024*1024/1000/1000) =  134.217728
        return_receiver_throughput_megabytes_per_second=$(bc -l <<<"$1*134.217728")
    elif [ "$2" == "Mbits/sec" ] 
    then
        # echo "Units:Mbits/sec?"
        # (1/8*1024*1024/1000/1000) =  0.131072
        return_receiver_throughput_megabytes_per_second=$(bc -l <<<"$1*0.131072")
    elif [ "$2" == "Kbits/sec" ] || [ "$1" == "kbits/sec" ]
    then
        # echo "Units:Kbits/sec?"
            # (1/8*1024/1000/1000) = 0.000128
        return_receiver_throughput_megabytes_per_second=$(bc -l <<<"$1*0.000128")
    else
        # echo "Units:bits/sec?"
        return_receiver_throughput_megabytes_per_second=$(bc -l <<<"$1/8000000")
    fi
    echo "${return_receiver_throughput_megabytes_per_second}"
}

# Based on: https://www.cyberciti.biz/faq/unix-howto-read-line-by-line-from-file/

# input_file="./delete_me_too.txt"
# while IFS= read -r line
# do
#   echo "${line}" 
# done < "$input_file"


# input_file="./delete_me_too.txt"
# while IFS= read -r line
# do
#     time_slot=$( echo ${line} | awk '{print $1;}'  )
#     receiver_throughput=$( echo "${line}" | awk '{print $2}'  )
#     echo "[$receiver_throughput]"
#     receiver_throughput_units=$( echo "${line}" | awk '{print $3}'  )
#     receiver_throughput=$( convert_throughput_to_MBytes_per_second  ${receiver_throughput} ${receiver_throughput_units} )
#     echo "[$receiver_throughput]"
#     echo $receiver_throughput_units
    
# done < "$input_file"



# input_file="./delete_me_too.txt"
# while IFS= read -r line
# do
#   echo "${line}"  
# done < "$input_file"

cat "./delete_me_too.txt" | awk '{
if ($3 =="Gbits/sec")
	{print $1, $2*1/8*1024*1024*1024/1000/1000}

else if ($3 =="Mbits/sec")
	{print $1, $2*1/8*1024*1024/1000/1000}

else if ($3 =="Kbits/sec")
	{print $1, $2*1/8*1024/1000/1000}

else 
    {print $1, $2*1/8/1000/1000}
}'
