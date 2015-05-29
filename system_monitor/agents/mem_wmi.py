import wmi
conn = wmi.WMI()
os = conn.win32_OperatingSystem()[0]

class wmi_mem:
    def getFreeMemory(self):
        os = conn.win32_OperatingSystem()[0]
        freeRam = os.FreePhysicalMemory
        freeRam = (int(freeRam)/1024)
        return freeRam

    def getUsedMemory(self):
        return getTotalMemory() - getFreeMemory()

    def getTotalMemory(self):
        totalRam = os.TotalVisibleMemorySize
        totalRam = (int(totalRam)/1024)
        return totalRam