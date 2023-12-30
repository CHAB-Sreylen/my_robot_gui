import threading
import time

# Define a function that will be executed in a thread
def thread_function(name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(f"Thread {name}: Count {count}")
    print(f"Thread {name} finished")

# Create threads
thread1 = threading.Thread(target=thread_function, args=("Thread 1", 1))  # args are the function arguments
thread2 = threading.Thread(target=thread_function, args=("Thread 2", 2))

# Start threads
thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()

print("Main thread finished")
