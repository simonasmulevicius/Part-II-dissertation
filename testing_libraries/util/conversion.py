import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from io import StringIO

def split_string_into_array_of_words(string):
    raw_words = string.split(" ")
    words = [word for word in raw_words if word != '']
    # print(words)
    return words

def convert_bitrate_to_bytes_per_second(bitrate, bitrate_units):
    # print("bitrate:",bitrate)
    converted_bitrate_in_bytes = bitrate/8
    if(bitrate_units == "Kbits/sec"):
        converted_bitrate_in_bytes = converted_bitrate_in_bytes*1024
    elif(bitrate_units == "Mbits/sec"):
        converted_bitrate_in_bytes = converted_bitrate_in_bytes*1024*1024
    elif(bitrate_units == "Gbits/sec"):
        converted_bitrate_in_bytes = converted_bitrate_in_bytes*1024*1024*1024
    # print("converted bitrate (Bytes/sec):", converted_bitrate_in_bytes)
    
    return converted_bitrate_in_bytes