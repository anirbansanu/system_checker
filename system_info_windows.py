 # filename = system_info_windows.py

import psutil
import wmi
import platform
from system_info_base import SystemInfo

class WindowsSystemInfo(SystemInfo):
    def get_cpu_info(self):
        c = wmi.WMI()
        cpu_info = c.Win32_Processor()[0]
        cpu_name = cpu_info.Name
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_logical = psutil.cpu_count(logical=True)
        return {
            'Name': cpu_name,
            'Physical Cores': cpu_cores,
            'Logical Cores': cpu_logical,
            'Usage': psutil.cpu_percent(interval=1)
        }

    def get_memory_info(self):
        memory_info = psutil.virtual_memory()
        return {
            'Total': memory_info.total,
            'Available': memory_info.available,
            'Used': memory_info.used,
            'Percentage': memory_info.percent
        }

    def get_disk_info(self):
        disk_usage = psutil.disk_usage('/')
        return {
            'Total': disk_usage.total,
            'Used': disk_usage.used,
            'Free': disk_usage.free,
            'Percentage': disk_usage.percent
        }

    def get_os_info(self):
        os_info = platform.uname()
        return {
            'System': os_info.system,
            'Version': os_info.version,
            'Release': os_info.release,
            'Machine': os_info.machine
        }

    def get_network_info(self):
        return psutil.net_if_addrs()

    def get_info(self):
        return {
            'CPU': self.get_cpu_info(),
            'Memory': self.get_memory_info(),
            'Disk': self.get_disk_info(),
            'OS': self.get_os_info(),
            'Network': self.get_network_info()
        }

