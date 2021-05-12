with open('./payload-size_1000000000____delay-ms_0____loss-rate-percent_0____clients-requests_1/1/result.txt') as results_file:
    file_contents = results_file.read()
    print(file_contents)