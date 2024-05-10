// /filespace/k/ksekar2/ece752/gem5/util/m5/src/abi/x86/
#include <iostream>
//#include <pthread.h>
#include <thread>
#include <stdio.h>

#define GEM5 1

/* #ifdef GEM5
#include "m5op.h"
#endif */
using namespace std;

const int XDIM = 512;
const int YDIM = 512;

struct __attribute__((packed)) pd_fs_trigger {
    int32_t data1;
    int32_t data2;
};

struct __attribute__((packed)) pd_fs_non_trigger {
    int32_t data1;
    char padding[64]; //To make it go to the next cache line
    int32_t data2;
};

pd_fs_trigger PD_FS_DATA_STRUCT;

//pd_fs_non_trigger PD_FS_DATA_STRUCT;

void thread_function_1(){
    for(int i = 0; i < 10000; i++){
        PD_FS_DATA_STRUCT.data1 += 1;
    }
}


void thread_function_2(){
    for(int i = 0; i < 10000; i++){
        PD_FS_DATA_STRUCT.data2 += 1;
    }
}


int main(int argc, char *argv[]) {

   printf("Memory footprint = %f MB\n", (float)(XDIM*YDIM*sizeof(float))/(1024*1024));
   printf("Number of Cores available = %d", thread::hardware_concurrency());
   //unsigned cpus = thread::hardware_concurrency();
   unsigned cpus = 2;
   //unsigned cpus = 1;
   printf("\nRunning on %d cores", cpus);

   thread **threads = new thread*[cpus];
   //pthread_t threads[NUM_THREADS];
   int rc;
   long t;

   threads[0] = new thread(thread_function_1);
   printf("\nThread 1 Created");
   thread_function_2();
   printf("\nThread 2 Created");

   cout << "\nWaiting for other threads to complete" << endl;

   for (t = 0; t < cpus - 1; t++) {
       //pthread_join(threads[t], NULL);
       threads[t]->join();
   }
   delete[] threads;
   cout << "\nValidating..." << flush;
   printf("End of Toy False Sharer \n");

   printf("\nData 1 = %d", PD_FS_DATA_STRUCT.data1);
   printf("\nData 2 = %d", PD_FS_DATA_STRUCT.data2);
   //printf("\nPadding = %d", PD_FS_DATA_STRUCT.padding);
   printf("\n");
   return 0;
}