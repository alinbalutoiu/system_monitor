from system_monitor.agents.agent_model import Agent_Model


class wmi_mem(Agent_Model):
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

    def setData(self):
        self.data['Free RAM'] = self.getFreeMemory()
        self.data['Used RAM'] = self.getUsedMemory()

    def setAgentName(self):
        self.agent_name = 'RAM Agent ' + self.hostname
