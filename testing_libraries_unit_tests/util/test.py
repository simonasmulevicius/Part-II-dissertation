from testing_libraries.util.conversion import *

assert convert_bitrate_to_bytes_per_second(449, 'Kbits/sec') == 57472
assert convert_bitrate_to_bytes_per_second(449, 'Mbits/sec') == 58851328
assert convert_bitrate_to_bytes_per_second(1.40, 'Gbits/sec') == 187904819.2
