# Global Interpreter Lock (GIL)
It is a mutex (Mutually Exculsive) or a lock that allows only one thread to hold control of the Python interpreter at one time.

## Benefits
The main benefit for GIL is because of **memory management**. In Python, how they decide whether to release memory for a given variable is by counting the number of reference. When the reference count reach `0`, the memory will be released. In order to prevent race conditions, GIL is used, so that multiple threads wont be able to increase or decrease the count simultaneously, if not it will cause memory leak or incorrectly release of memory for an object that still exist.