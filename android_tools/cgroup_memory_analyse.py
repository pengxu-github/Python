import multiprocessing
import subprocess
import matplotlib.pyplot as plt

adb_device = 'adb -s 192.168.1.24:50240 shell cat '
MEMORY_USED = "/sys/fs/cgroup/memory/memory.usage_in_bytes"
MEMORY_TOTAL = "/sys/fs/cgroup/memory/memory.limit_in_bytes"
MEMORY_STAT = "/sys/fs/cgroup/memory/memory.stat"
command_total = adb_device + MEMORY_TOTAL
command_used = adb_device + MEMORY_USED

PAGE_SIZE = 1024 * 1024
step = 2  # seconds between each time tick


def get_memory_stat():
    cache_size = ""
    shmem_size = ""
    mem_stat = subprocess.Popen(adb_device + MEMORY_STAT, shell=True, stdout=subprocess.PIPE)
    for line in mem_stat.stdout:
        b_line = line.rstrip().decode()
        # print(b_line)
        if b_line.find("total_cache") != -1:
            cache_size = b_line.split(' ', 2)[1]
        elif b_line.find("total_shmem") != -1:
            shmem_size = b_line.split(' ', 2)[1]
    return int(cache_size) / PAGE_SIZE, int(shmem_size) / PAGE_SIZE


def get_node_num(cmd):
    memory_get = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return int(memory_get.stdout.readline().rstrip().decode()) / PAGE_SIZE


def get_memory_and_draw():
    i = 0
    listx = []
    list_available = []
    list_cache = []
    plt.title("memory info")
    plt.xlabel('time')
    plt.ylabel('memory(M)')
    plt.ylim(0, total)
    plt.legend(['memory used', 'memory cache', 'memory share'], bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
    plt.ion()
    while True:
        listx.append(i)
        used = get_node_num(command_used)
        cache, shmem = get_memory_stat()
        actual_cache = cache - shmem
        available = total - used + actual_cache
        print("actual_cache={}, available={}".format(actual_cache, available))
        list_available.append(available)
        list_cache.append(actual_cache)

        plt.plot(listx, list_available, linestyle='-', label='memory share', color='blue')
        plt.plot(listx, list_cache, linestyle='-', label='memory cache', color='red')
        # plt.show()
        i += step
        plt.pause(step)


if __name__ == '__main__':
    total = get_node_num(command_total)
    get_memory_and_draw()
    print("cpu count: %d" % multiprocessing.cpu_count())
