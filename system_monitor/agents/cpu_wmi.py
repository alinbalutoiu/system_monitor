import wmi
conn = wmi.WMI()

cpu = conn.win32_Processor()[0]

class wmi_cpu:
    def getUsedCPU(self):
        cpu = conn.win32_Processor()[0]
        return cpu.LoadPercentage

    def getFreeCPU(self):
        return 100 - int(getUsedCPU())

    def getNumberCoresCPU(self):
        return cpu.NumberOfCores
