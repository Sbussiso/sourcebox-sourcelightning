import psutil
import GPUtil
import os
import platform
import pandas as pd
from datetime import datetime

# Function to get detailed CPU information
def get_detailed_cpu_info():
    cpu_freq = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_stats = psutil.cpu_stats()
    cpu_times = psutil.cpu_times(percpu=False)  # Total CPU times for all cores
    load_avg = os.getloadavg() if hasattr(os, "getloadavg") else (0, 0, 0)
    sensors = psutil.sensors_temperatures()

    cpu_info = {
        "CPU Freq (MHz)": f"{cpu_freq.current:.1f}",
        "Max Freq (MHz)": f"{cpu_freq.max:.1f}",
        "Min Freq (MHz)": f"{cpu_freq.min:.1f}",
        "Physical Cores": cpu_cores,
        "Logical Threads": cpu_threads,
        "Per Core Usage (%)": cpu_percent,
        "Load Avg (1, 5, 15 min)": load_avg,
        "Context Switches": cpu_stats.ctx_switches,
        "Interrupts": cpu_stats.interrupts,
        "System Calls": cpu_stats.syscalls,
        "User Time (s)": f"{cpu_times.user:.2f}",
        "System Time (s)": f"{cpu_times.system:.2f}",
        "Idle Time (s)": f"{cpu_times.idle:.2f}",
        "I/O Wait Time (s)": f"{getattr(cpu_times, 'iowait', 'N/A'):.2f}",
    }

    # Adding CPU temperature if available
    if 'coretemp' in sensors:
        for i, temp in enumerate(sensors['coretemp']):
            cpu_info[f"Core {i+1} Temp (C)"] = f"{temp.current:.1f} °C"

    return pd.DataFrame([cpu_info])

# Function to get detailed memory information
def get_detailed_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    memory_info = {
        "Total Memory (GB)": f"{memory.total / (1024 ** 3):.2f}",
        "Available Memory (GB)": f"{memory.available / (1024 ** 3):.2f}",
        "Used Memory (GB)": f"{memory.used / (1024 ** 3):.2f}",
        "Used Memory (%)": f"{memory.percent:.1f} %",
        "Cache (GB)": f"{memory.cached / (1024 ** 3):.2f}",
        "Buffers (GB)": f"{memory.buffers / (1024 ** 3):.2f}",
        "Active (GB)": f"{memory.active / (1024 ** 3):.2f}",
        "Inactive (GB)": f"{memory.inactive / (1024 ** 3):.2f}",
        "Swap Total (GB)": f"{swap.total / (1024 ** 3):.2f}",
        "Swap Used (GB)": f"{swap.used / (1024 ** 3):.2f}",
        "Swap Free (GB)": f"{swap.free / (1024 ** 3):.2f}",
        "Swap Usage (%)": f"{swap.percent:.1f} %",
    }

    return pd.DataFrame([memory_info])

# Function to get disk usage and IO information
def get_disk_info():
    disk_partitions = psutil.disk_partitions()
    disk_io = psutil.disk_io_counters(perdisk=True)
    disk_info_list = []

    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        io_info = disk_io.get(partition.device.split("/")[-1], None)
        disk_info = {
            "Device": partition.device,
            "Mountpoint": partition.mountpoint,
            "File System": partition.fstype,
            "Total Size (GB)": f"{usage.total / (1024 ** 3):.2f}",
            "Used (%)": f"{usage.percent:.1f}",
            "Read Cnt": io_info.read_count if io_info else "N/A",
            "Write Cnt": io_info.write_count if io_info else "N/A",
            "Read (MB)": f"{io_info.read_bytes / (1024 ** 2):.2f}" if io_info else "N/A",
            "Write (MB)": f"{io_info.write_bytes / (1024 ** 2):.2f}" if io_info else "N/A",
        }
        disk_info_list.append(disk_info)

    return pd.DataFrame(disk_info_list)

# Function to get network information with extended details
def get_network_info():
    net_io = psutil.net_io_counters(pernic=True)
    network_info_list = []

    for interface, io_stats in net_io.items():
        network_info = {
            "Interface": interface,
            "Sent (GB)": f"{io_stats.bytes_sent / (1024 ** 3):.2f}",
            "Recv (GB)": f"{io_stats.bytes_recv / (1024 ** 3):.2f}",
            "Packets Sent": io_stats.packets_sent,
            "Packets Recv": io_stats.packets_recv,
            "Errors In": io_stats.errin,
            "Errors Out": io_stats.errout,
            "Drop In": io_stats.dropin,
            "Drop Out": io_stats.dropout,
        }
        network_info_list.append(network_info)

    return pd.DataFrame(network_info_list)

# Function to get GPU information (if available)
def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        gpu_info_list = []

        for gpu in gpus:
            gpu_info = {
                "GPU Name": gpu.name,
                "Load (%)": f"{gpu.load * 100:.1f}",
                "Mem Free (MB)": f"{gpu.memoryFree:.1f}",
                "Mem Used (MB)": f"{gpu.memoryUsed:.1f}",
                "Total Mem (MB)": f"{gpu.memoryTotal:.1f}",
                "Temp (C)": f"{gpu.temperature:.1f}",
            }
            gpu_info_list.append(gpu_info)

        return pd.DataFrame(gpu_info_list)

    except Exception as e:
        return pd.DataFrame({"Error": ["No GPU detected or GPUtil not working."]})

# Function to display all system info using pandas
def display_system_info():
    os.system('clear' if platform.system() != 'Windows' else 'cls')

    print(f"System Information at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("===== CPU Information =====")
    cpu_info = get_detailed_cpu_info()
    print(cpu_info.to_string(index=False))

    print("\n===== Memory Information =====")
    memory_info = get_detailed_memory_info()
    print(memory_info.to_string(index=False))

    print("\n===== Disk Information =====")
    disk_info = get_disk_info()
    print(disk_info.to_string(index=False))

    print("\n===== Network Information =====")
    network_info = get_network_info()
    print(network_info.to_string(index=False))

    print("\n===== GPU Information =====")
    gpu_info = get_gpu_info()
    print(gpu_info.to_string(index=False))

if __name__ == "__main__":
    display_system_info()
