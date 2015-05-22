cdef extern from "cprogram.h":
    # C function declaration.  Note the "nogil" on the end
    int c_worker_func(void *user_context, int (*cythonCallback)(int percentage, void *user_context)) nogil
