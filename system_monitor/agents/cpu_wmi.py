from agent_model import Agent_Model


class wmi_cpu(Agent_Model):

    def getUsedCPU(self):
        self.update_status()
        return self.cpu.LoadPercentage

    def getFreeCPU(self):
        return 100 - int(self.getUsedCPU())

    def getNumberCoresCPU(self):
        return self.NrCores

    def update_status(self):
        self.cpu = self.conn.win32_Processor()[0]

    def setData(self):
        self.data['Free CPU'] = self.getFreeCPU()
        self.data['Used CPU'] = self.getUsedCPU()
