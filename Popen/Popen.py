import threading
import subprocess
import shlex
from timeit import default_timer as timer

# Alexander Zhu, May 2018
# Python 3.6.5

# This method for simultaenous popen() to use threading and a barrier object to enable
# simultaneous release of all initialized threads

# This code can be modified to demonstrate sequental execution by setting the first argument in
# the Barrier call to "1" and commenting out the loop statement that joins the threads together.
# You can note by doing this that sequential execution is slightly faster than multi-threaded
# execution, which is a logical outcome given that multi-threaded execution competes with processing
# power.

commands = ['sleep 3', 'ls -l /', 'find /', 'sleep 4', 'find /usr', 'date', 'sleep 5', 'uptime']
listLen = len(commands)
# Barrier objects only work with a finite number of threads, which is appropriate for the problem
b = threading.Barrier(listLen, timeout = 5)
threads = []
# append execution times in a global variable
results = [0.0] * listLen


def simuPopen(cmd, index):
    global results
    # Barrier Object with call to wait(); when "n" wait calls are made all threads that called wait()
    # will execute at the same time
    b.wait()
    start = timer()
    p = subprocess.Popen(cmd, stdout = None)
    while p.poll() == None: # polling
        time.sleep(0.0001)
    results[index] = (timer() - start)
    return p.poll()


if __name__ == "__main__":

    # main loop; init threads w/ target of simuPopen and start all.

    for i in range(listLen):
        t = threading.Thread(target = simuPopen, args = (shlex.split(commands[i]), i))
        threads.append(t)
        threads[-1].start()

    #join threads back together to continue main loop execution
    for i in range(listLen):
        threads[i].join()

    print(results)
    # Results as calculated with built-in functions
    print("Total elapsed Time: ", sum(results))
    print("Average elapsed Time: ", sum(results)/len(results))
    print("Max elapsed Time: ", max(results))
    print("Min elapsed Time:", min(results))