import wmi
# import extends as ex

class wmi_cpu():
    def __init__(self, mode):
        self.mode = mode
        self.conn = wmi.WMI()
        self.update_status()
        self.NrCores = self.cpu.NumberOfCores
        
    def getUsedCPU(self):
        self.update_status()
        return self.cpu.LoadPercentage

    def getFreeCPU(self):
        return 100 - int(self.getUsedCPU())

    def getNumberCoresCPU(self):
        return self.NrCores
        
    def update_status(self):
        self.cpu = self.conn.win32_Processor()[0]

    def get_data(self):
        if self.mode == 1:
            return self.getUsedCPU()
        elif self.mode == 2:
            return self.getFreeCPU()
