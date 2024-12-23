#!/usr/bin/env python3
import platform
import psutil
from tabulate import tabulate
import os
from datetime import datetime

def get_size(bytes):
    """
    Convert bytes to human readable format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def get_system_info():
    """
    Get basic system information
    """
    return {
        "OS": f"{platform.system()} {platform.release()}",
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Hostname": platform.node()
    }

def get_cpu_info():
    """
    Get CPU information
    """
    cpu_freq = psutil.cpu_freq()
    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{cpu_freq.max:.2f}Mhz" if cpu_freq else "N/A",
        "Current Frequency": f"{cpu_freq.current:.2f}Mhz" if cpu_freq else "N/A",
        "CPU Usage": f"{psutil.cpu_percent()}%"
    }
    
    # Add per-core usage
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_info[f"Core {i} Usage"] = f"{percentage}%"
    
    return cpu_info

def get_memory_info():
    """
    Get RAM information
    """
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        "Total Memory": get_size(svmem.total),
        "Available Memory": get_size(svmem.available),
        "Used Memory": get_size(svmem.used),
        "Memory Usage": f"{svmem.percent}%",
        "Total Swap": get_size(swap.total),
        "Free Swap": get_size(swap.free),
        "Used Swap": get_size(swap.used),
        "Swap Usage": f"{swap.percent}%"
    }

def get_disk_info():
    """
    Get storage information
    """
    disk_info = {}
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info[f"Device {partition.device}"] = {
                "Mountpoint": partition.mountpoint,
                "File System": partition.fstype,
                "Total Size": get_size(partition_usage.total),
                "Used": get_size(partition_usage.used),
                "Free": get_size(partition_usage.free),
                "Usage": f"{partition_usage.percent}%"
            }
        except Exception:
            continue
            
    return disk_info

def try_get_gpu_info():
    """
    Attempt to get GPU information if available
    """
    try:
        import GPUtil
        gpu_info = {}
        gpus = GPUtil.getGPUs()
        for i, gpu in enumerate(gpus):
            gpu_info[f"GPU {i}"] = {
                "Name": gpu.name,
                "ID": gpu.id,
                "Load": f"{gpu.load*100}%",
                "Free Memory": f"{gpu.memoryFree}MB",
                "Used Memory": f"{gpu.memoryUsed}MB",
                "Total Memory": f"{gpu.memoryTotal}MB",
                "Temperature": f"{gpu.temperature} °C",
                "UUID": gpu.uuid
            }
        return gpu_info
    except ImportError:
        return {"Status": "GPU information unavailable - GPUtil module not installed or supported"}
    except Exception as e:
        return {"Error": f"Failed to get GPU information: {str(e)}"}

def main():
    """
    Main function to gather and display all hardware information
    """
    print("\n=== Hardware Diagnostic Tool ===")
    print(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get all information
    system_info = get_system_info()
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    gpu_info = try_get_gpu_info()
    
    # Display System Information
    print("\n--- System Information ---")
    print(tabulate([[k, v] for k, v in system_info.items()], 
                  headers=['Property', 'Value'], 
                  tablefmt='grid'))
    
    # Display CPU Information
    print("\n--- CPU Information ---")
    print(tabulate([[k, v] for k, v in cpu_info.items()],
                  headers=['Property', 'Value'],
                  tablefmt='grid'))
    
    # Display Memory Information
    print("\n--- Memory Information ---")
    print(tabulate([[k, v] for k, v in memory_info.items()],
                  headers=['Property', 'Value'],
                  tablefmt='grid'))
    
    # Display Disk Information
    print("\n--- Disk Information ---")
    for disk, info in disk_info.items():
        print(f"\n{disk}:")
        print(tabulate([[k, v] for k, v in info.items()],
                      headers=['Property', 'Value'],
                      tablefmt='grid'))
    
    # Display GPU Information
    print("\n--- GPU Information ---")
    if isinstance(gpu_info, dict) and len(gpu_info) == 1 and ("Status" in gpu_info or "Error" in gpu_info):
        # Handle the case where GPU info is unavailable or there was an error
        key = "Status" if "Status" in gpu_info else "Error"
        print(gpu_info[key])
    else:
        for gpu, info in gpu_info.items():
            print(f"\n{gpu}:")
            print(tabulate([[k, v] for k, v in info.items()],
                          headers=['Property', 'Value'],
                          tablefmt='grid'))

if __name__ == "__main__":
    main()