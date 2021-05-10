#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>

#define TEXT_LENGTH 1000000

double run_naive_implementation(){
    printf(" ----------TEST 1--------------  \n");
    // Time measurements according to: 
    // https://www.tutorialspoint.com/how-to-measure-time-taken-by-a-function-in-c
    
    
    uint8_t dest[3*TEXT_LENGTH];
    size_t plaintextlen = TEXT_LENGTH;
    size_t taglen = TEXT_LENGTH;
    clock_t timestamp_start;
    clock_t timestamp_end;
    
    timestamp_start = clock();
    for (size_t i=0; i<taglen; i++){
        dest[plaintextlen+i] = 0;
    }
    timestamp_end = clock();
    
    printf(" Test ran for %ld steps          \n", timestamp_end - timestamp_start);
    printf(" Test ran for %f miliseconds     \n", 
        ((double) (timestamp_end - timestamp_start)*1000)/CLOCKS_PER_SEC);
    printf(" ------------------------------  \n");
    
    return ((double) (timestamp_end - timestamp_start)*1000)/CLOCKS_PER_SEC;
}

double run_improved_implementation(){
    printf(" ----------TEST 2--------------  \n");
    // Time measurements according to: 
    // https://www.tutorialspoint.com/how-to-measure-time-taken-by-a-function-in-c
    
    uint8_t dest[3*TEXT_LENGTH];
    size_t plaintextlen = TEXT_LENGTH;
    size_t taglen = TEXT_LENGTH;
    clock_t timestamp_start;
    clock_t timestamp_end;
    
    timestamp_start = clock();
    memset(dest+plaintextlen,0,taglen);
    timestamp_end = clock();
    
    printf(" Test ran for %ld steps          \n", timestamp_end - timestamp_start);
    printf(" Test ran for %f miliseconds     \n", 
        ((double) (timestamp_end - timestamp_start)*1000)/CLOCKS_PER_SEC);
    printf(" ------------------------------  \n");
    
    return ((double) (timestamp_end - timestamp_start)*1000)/CLOCKS_PER_SEC;
}



int main()
{
    printf("Running comparison tests\n");
    

    // for (size_t i=0; i<taglen; i++){
    //     printf("dest[%lu] = %d\n", plaintextlen+i, dest[plaintextlen+i]);
    // } 

    int number_of_experiments = 1000;
    double list_miliseconds_to_complete_naive[number_of_experiments];
    double list_miliseconds_to_complete_improved[number_of_experiments];
    
    // 1. Run experiments
    for (int i=0; i<number_of_experiments; i++){
        list_miliseconds_to_complete_naive[i] = run_naive_implementation();
    }
    
    for (int i=0; i<number_of_experiments; i++){
        list_miliseconds_to_complete_improved[i] = run_improved_implementation();
    }

    // 2. Report results
    double avg_milisecond_to_complete_naive = 0.0;
    for (int i=0; i<number_of_experiments; i++){
        avg_milisecond_to_complete_naive+=list_miliseconds_to_complete_naive[i];
    }
    avg_milisecond_to_complete_naive = avg_milisecond_to_complete_naive/number_of_experiments;
    
    
    double avg_squared_distance_naive = 0.0;
    for (int i=0; i<number_of_experiments; i++){
        double distance = avg_milisecond_to_complete_naive - list_miliseconds_to_complete_naive[i];
        avg_squared_distance_naive += distance*distance;
    }
    double standard_deviation_naive = sqrt(avg_squared_distance_naive/(number_of_experiments-1));
    
    
    
    double avg_milisecond_to_complete_improved = 0;
    for (int i=0; i<number_of_experiments; i++){
        avg_milisecond_to_complete_improved+=list_miliseconds_to_complete_improved[i];
    }
    avg_milisecond_to_complete_improved = avg_milisecond_to_complete_improved/number_of_experiments;
    
    double avg_squared_distance_improved = 0.0;
    for (int i=0; i<number_of_experiments; i++){
        double distance = avg_milisecond_to_complete_improved - list_miliseconds_to_complete_improved[i];
        avg_squared_distance_improved += distance*distance;
    }
    double standard_deviation_improved = sqrt(avg_squared_distance_improved/(number_of_experiments-1));
    
    
    
    
    printf("Naive    implementation took: %f miliseconds on average (stdev: %f) \n", avg_milisecond_to_complete_naive, standard_deviation_naive);
    printf("Improved implementation took: %f miliseconds on average (stdev: %f) \n", avg_milisecond_to_complete_improved, standard_deviation_improved);
    
    
    // for (size_t i=0; i<taglen; i++){
    //     printf("dest[%lu] = %d\n", plaintextlen+i, dest[plaintextlen+i]);
    // } 
    
    

    return 0;
}

