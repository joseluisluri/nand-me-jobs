#!/usr/bin/env python3
from utils import sh, jsony
import mongodb
import time

def do():
    COLLECTION_NAME = 'status'

    # Note:
    # vcgencmd: it's part of RaspberryPi userspace tools. You need to be in group video.

    class System:
        def __init__(self):
            self.processor = sh("cat /proc/cpuinfo | grep model | cut -d':' -f2 | xargs")
            self.cpus = sh("lscpu | grep 'CPU(s):' | awk '{print $2}'")
            self.cpu_mhz = sh("lscpu | grep 'CPU max' | cut -d':' -f2 | xargs | cut -d',' -f1")
            self.os = sh('uname -o')
            self.distro = sh('cat /etc/*-release | awk "NR==2" | cut -c 7- | head -c -2')
            self.kernel = sh('uname -r')
            self.hostname = sh('hostname')
            self.cpu_usage = sh("top -bn 2 | grep '^%Cpu' | awk 'NR==2 {print $2+$4+$6}'")
            self.cpu_temp = sh('expr $(cat /sys/class/thermal/thermal_zone0/temp) / 1000')
            self.gpu_temp = sh('vcgencmd measure_temp | cut -c 6- | head -c -3')
            self.uptime = sh('uptime -p | cut -c 4-')
            self.date = sh("date --rfc-3339=seconds | cut -d'+' -f1")

    class Memory:
        def __init__(self):
            self.hdd_total = sh("df -h | grep root | awk '{print $2}'")
            self.hdd_total_numeric = sh("df | grep root | awk '{print $2}'")
            self.hdd_used = sh("df -h | grep root | awk '{print $3}'")
            self.hdd_used_numeric = sh("df | grep root | awk '{print $3}'")
            self.hdd_avail = sh("df -h | grep root | awk '{print $4}'")
            self.hdd_avail_numeric = sh("df | grep root | awk '{print $4}'")
            self.hdd_usage = sh('echo $(awk "BEGIN { pc=100*' + self.hdd_used_numeric + \
                 '/' + self.hdd_total_numeric + '; i=int(pc); print (pc-i<0.5)?i:i+1 }")')

            self.mem_total = sh("free -h | grep Mem | awk '{print $2}'")
            self.mem_total_numeric = sh("free | grep Mem | awk '{print $2}'")
            self.mem_used = sh("free -h | grep Mem | awk '{print $3}'")
            self.mem_used_numeric = sh("free | grep Mem | awk '{print $3}'")
            self.mem_avail = sh("free -h | grep Mem | awk '{print $7}'")
            self.mem_avail_numeric = sh("free | grep Mem | awk '{print $7}'")
            self.mem_free = sh("free -h | grep Mem | awk '{print $4}'")
            self.mem_free_numeric = sh("free | grep Mem | awk '{print $4}'")
            self.mem_usage = sh('echo $(awk "BEGIN { pc=100*' + self.mem_used_numeric + \
                '/' + self.mem_total_numeric + '; i=int(pc); print (pc-i<0.5)?i:i+1 }")')

            self.swap_total = sh("free -h | grep Swap | awk '{print $2}'")
            self.swap_total_numeric = sh("free | grep Swap | awk '{print $2}'")
            self.swap_used = sh("free -h | grep Swap | awk '{print $3}'")
            self.swap_used_numeric = sh("free | grep Swap | awk '{print $3}'")
            self.swap_free = sh("free -h | grep Swap | awk '{print $4}'")
            self.swap_free_numeric = sh("free | grep Swap | awk '{print $4}'")
            self.swap_usage = sh('echo $(awk "BEGIN { pc=100*' + self.swap_used_numeric + \
                '/' + self.swap_total_numeric + '; i=int(pc); print (pc-i<0.5)?i:i+1 }")')

    try:
        document = jsony(dict(timestamp=time.time(), system=System(), memory=Memory()))
        mongodb.replace(COLLECTION_NAME, document)
        print('Status was updated');
    except Exception as e:
        print(e)

if __name__ == "__main__":
    do()