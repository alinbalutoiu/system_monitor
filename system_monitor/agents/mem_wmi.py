import wmi


class wmi_mem:
    def __init__(self, mode):
        self.mode = mode
        self.conn = wmi.WMI()

    def getFreeMemory(self):
        self.update_status()
        freeRam = self.os.FreePhysicalMemory
        return (int(freeRam)/1024)

    def getUsedMemory(self):
        return self.getTotalMemory() - self.getFreeMemory()

    def getTotalMemory(self):
        self.update_status()
        totalRam = self.os.TotalVisibleMemorySize
        return (int(totalRam)/1024)

    def update_status(self):
        self.os = self.conn.win32_OperatingSystem()[0]

    def get_data(self):
        if self.mode == 1:
            return self.getUsedMemory()
        elif self.mode == 2:
            return self.getFreeMemory()
