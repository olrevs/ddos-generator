import threading

def start_multithreading(thread_count, function, *arguments):
    """Create threads which will perform a specific function.
    
    Argumets:
    thread_count -- count of threads that will be ceated
    function -- the name of function that will be executed by each thread
    arguments -- any number of arguments of the function (such as the IP address of the target; the targets port; fflag for enable / disable source IP spoofing)

    """
    threads = []
    for i in range(0, thread_count):
        threads.append(threading.Thread(target=function, args=arguments))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
