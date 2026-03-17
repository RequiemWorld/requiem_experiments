import os
import psutil

process = psutil.Process(os.getpid())
print(process.cpu_affinity())