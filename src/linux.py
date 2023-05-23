import psutil
from datetime import datetime
from utils import byte_to_gigabyte


class LinuxHealth:
    formatLog = "{time}: CPU:{cpu}%, RAM:{{{ram}}}%"

    def __init__(self):
        pass

    def checkCPU(self):
        return psutil.cpu_percent()

    def checkRAM(self):
        percent = psutil.virtual_memory().percent
        used = psutil.virtual_memory().used
        total = psutil.virtual_memory().total
        return [used, percent, total]

    def checkDisk():
        pass

    def checkHealth(self):
        cpu = self.checkCPU()
        ram = self.checkRAM()
        log = self.formatLog.format(
            time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            cpu=cpu,
            ram="{} GB ({}%) of {} GB".format(
                byte_to_gigabyte(ram[0]), ram[1], byte_to_gigabyte(ram[2])
            ),
        )

        return {"log": log, "cpu": cpu, "ram": ram}
