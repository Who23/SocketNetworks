import socket
import threading
import queue
import subprocess
import sys

host = socket.gethostname()
hostIP = socket.gethostbyname(host)
networkIP = '.'.join(hostIP.split('.')[:3]) + '.'
pinged = 0

#Threading class adjusted from https://www.tutorialspoint.com/python/python_multithreading.htm
class ScannerThread(threading.Thread):
    def __init__(self, threadingID, q, name):
        threading.Thread.__init__(self)
        self.threadingID = threadingID
        self.q = q
        self.name = name

    def run(self):
        global pinged
        while not exitFlag:
            queueLock.acquire()
            if not self.q.empty():
                data = self.q.get()
                queueLock.release()
                #Ping server with IP address
                if subprocess.call(["ping", "-c 1", "-W 50", "{}".format(networkIP + str(data))], shell=False, stdout = subprocess.DEVNULL) == 0:
                    queueLock.acquire()
                    activeIP.append(networkIP + str(data))
                    queueLock.release()
                queueLock.acquire()
                pinged += 1
                queueLock.release()
            else:
                queueLock.release()

exitFlag = False

threadNames = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
work = range(256)
networkQueue = queue.Queue(256)
queueLock = threading.Lock()
threads = []
activeIP = []


queueLock.acquire()
for threadID, threadName in enumerate(threadNames):
    thread = ScannerThread(threadID, networkQueue, threadName)
    thread.start()
    threads.append(thread)
print("Started all threads")
print("Pinging IPs...")

for item in work:
    networkQueue.put(item)
queueLock.release()


while pinged != 256:
    while not networkQueue.empty():
        sys.stdout.write("\u001b[1000D")
        sys.stdout.write("[" + "#"*round(20*pinged/256) + " "*(20 - round(20*pinged/256)) + "]")
    exitFlag = True
    for thread in threads:
        thread.join()
    sys.stdout.write("\u001b[1000D")
    sys.stdout.write("[" + "#"*round(20*pinged/256) + " "*(20 - round(20*pinged/256)) + "]")

print("")
for ip in activeIP:
    try:
        print("{}: {}".format((socket.gethostbyaddr(ip)[0])[:-17], ip))
    except socket.herror:
        print("{}: {}".format("Unknown Host", ip))