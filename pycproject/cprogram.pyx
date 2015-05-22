cimport cprogram

# good info: http://docs.cython.org/src/tutorial/clibraries.html

# C style callback, must declare "with gil" to acquire the GIL for safety (or use 'with gil:' in code)
# This wraps the Python function, converting it to an object and calling it.
cdef int callback_wrapper( int percentage, void *user_context ) with gil:
    
    if user_context:
        try:
            pyfunc = <object>user_context
            pyfunc( percentage )
        except:
            return 1

    return 0



def wrapper_with_callback_nogil(python_callback_func):
    cdef:
        int status
    
    # run the C function, which uses our cdef'ed callback (C only arguments) and an optional Python callback.
    # Release the GIL to keep from blocking the main thread while doing computation:
    with nogil:
        status = cprogram.c_worker_func( <void *> python_callback_func, callback_wrapper )

    if status != 0:
        raise RuntimeError('c_worker_func failed with exit status = %d\n' % status)


def wrapper_with_callback_gil(python_callback_func):
    cdef:
        int status

    # same as above except without releasing the GIL
    status = cprogram.c_worker_func( <void *> python_callback_func, callback_wrapper )

    if status != 0:
        raise RuntimeError('c_worker_func failed with exit status = %d\n' % status)