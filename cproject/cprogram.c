#include <stdio.h>
#include "cprogram.h"

// Calling a custom Cython/Python callback
int c_worker_func(void *user_context, int (*cythonCallback)(int percentage, void *user_context))
{
    int response = 1;
    int errNum = 0;
    int i;
    for ( i=0; i<100; i++ ){

        if (cythonCallback( i+1, user_context )) {
            printf( "non-zero exit status from callback, exiting...\n" );
            errNum++;
            break;
        }
        
        // CPU intensive work:
        long long int i;
        long long int j;
        for ( i=0; i<10000000; i++ ) {
            j += i*i + i;
        }
    }
    
    if ( errNum == 0 ) response = 0;
    
    return response;
}

