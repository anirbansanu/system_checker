# filename = system_diagnostics.py

import psutil
import wmi
import subprocess

class SystemDiagnostics:
    def __init__(self):
        self.diagnostics = {}

    def check_overheating(self):
        c = wmi.WMI()
        temperatures = c.Win32_Temperature()
        if temperatures:
            temp_list = [temp.CurrentTemperature for temp in temperatures]
            # Convert temperature from Kelvin to Celsius
            return [round((temp / 10) - 273.15, 2) for temp in temp_list if temp is not None]
        return None

    def check_battery(self):
        c = wmi.WMI()
        battery_info = c.Win32_Battery()
        if battery_info:
            battery = battery_info[0]
            return {
                'Charge': battery.EstimatedChargeRemaining,
                'Status': battery.Status,
                'Design Capacity': battery.DesignCapacity,
                'Full Charge Capacity': battery.FullChargeCapacity
            }
        return None

    def check_hard_drive(self):
        try:
            result = subprocess.run(['wmic', 'diskdrive', 'get', 'Status'], capture_output=True, text=True)
            return result.stdout.splitlines()[1:]  # Skip header line
        except Exception as e:
            return str(e)

    def check_ram(self):
        memory_info = psutil.virtual_memory()
        return {
            'Total': memory_info.total,
            'Available': memory_info.available,
            'Used': memory_info.used,
            'Percentage': memory_info.percent
        }

    def check_network_performance(self):
        net_io = psutil.net_io_counters()
        return {
            'Bytes Sent': net_io.bytes_sent,
            'Bytes Received': net_io.bytes_recv,
            'Packets Sent': net_io.packets_sent,
            'Packets Received': net_io.packets_recv,
            'Errors Sent': net_io.errout,
            'Errors Received': net_io.errin
        }

    def run_diagnostics(self):
        self.diagnostics = {
            'Overheating': self.check_overheating(),
            'Battery': self.check_battery(),
            'Hard Drive': self.check_hard_drive(),
            'RAM': self.check_ram(),
            'Network Performance': self.check_network_performance(),
        }
        return self.diagnostics
