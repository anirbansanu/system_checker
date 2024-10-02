# filename = system_diagnostics.py

import psutil
import subprocess
import wmi

class SystemDiagnostics:
    def __init__(self):
        self.diagnostics = {}

    def check_overheating(self):
        try:
            c = wmi.WMI()
            processors = c.Win32_Processor()
            if processors:
                # Get temperature from Win32_Processor
                temp_list = [proc.LoadPercentage for proc in processors]  # Load percentage as a proxy for temperature
                return {'Load Percentage': temp_list}
            return {"Error": "No processor data available."}
        except Exception as e:
            return {"Error retrieving temperature": str(e)}

    def check_battery(self):
        try:
            c = wmi.WMI()
            battery_info = c.Win32_Battery()
            if battery_info:
                battery = battery_info[0]
                return {
                    'Charge': battery.EstimatedChargeRemaining,
                    'Status': battery.Status,
                    'Design Capacity': battery.DesignCapacity if battery.DesignCapacity is not None else 'N/A',
                    'Full Charge Capacity': battery.FullChargeCapacity if battery.FullChargeCapacity is not None else 'N/A'
                }
            return {"Error": "No battery information found."}
        except Exception as e:
            return {"Error": str(e)}

    def check_hard_drive(self):
        try:
            result = subprocess.Popen(['wmic', 'diskdrive', 'get', 'DeviceID,Status,Model'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            lines = stdout.decode().strip().split('\n')[1:]  # Skip header
            hard_drive_info = {}
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:  # Ensure there are enough parts to unpack
                    device_id = parts[0]
                    status = parts[1]
                    model = " ".join(parts[2:])
                    hard_drive_info[device_id] = {
                        'Status': status,
                        'Model': model
                    }
            return hard_drive_info or {"Error": "No hard drive information found."}
        except Exception as e:
            return {"Error": str(e)}

    def check_ram(self):
        memory_info = psutil.virtual_memory()
        return {
            'Total (MB)': round(memory_info.total / (1024 * 1024), 2),  # Convert to MB and round to 2 decimal places
            'Available (MB)': round(memory_info.available / (1024 * 1024), 2),  # Convert to MB and round to 2 decimal places
            'Used (MB)': round(memory_info.used / (1024 * 1024), 2),  # Convert to MB and round to 2 decimal places
            'Percentage': memory_info.percent
        }

    def check_network_performance(self):
        net_io = psutil.net_io_counters()
        return {
            'Bytes Sent': net_io.bytes_sent,
            'Bytes Received': net_io.bytes_recv,
            'Mega Bytes Sent (MB)': round(net_io.bytes_sent / (1024 * 1024),2),   # Convert to MB
            'Mega Bytes Received (MB)': round(net_io.bytes_recv / (1024 * 1024),2),   # Convert to MB
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
