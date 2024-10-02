# filename = system_info_base.py

from abc import ABC, abstractmethod

class SystemInfo(ABC):
    @abstractmethod
    def get_info(self):
        pass

    def get_cpu_info(self):
        raise NotImplementedError

    def get_memory_info(self):
        raise NotImplementedError

    def get_disk_info(self):
        raise NotImplementedError

    def get_os_info(self):
        raise NotImplementedError

    def get_network_info(self):
        raise NotImplementedError
