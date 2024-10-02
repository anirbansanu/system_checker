 # filename = system_info.py

import platform
from system_info_windows import WindowsSystemInfo
from system_info_linux import LinuxSystemInfo

class SystemInfoFactory:
    @staticmethod
    def get_system_info():
        current_os = platform.system()
        if current_os == 'Windows':
            return WindowsSystemInfo()
        elif current_os == 'Linux':
            return LinuxSystemInfo()
        else:
            raise NotImplementedError(f"{current_os} is not supported.")

if __name__ == "__main__":
    system_info = SystemInfoFactory.get_system_info()
    info = system_info.get_info()
    print(info)
