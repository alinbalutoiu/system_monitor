from system_monitor.agents.agent_model import Agent_Model


class wmi_dsk(Agent_Model):
    def getDiskReads(self):
        self.update_status()
        return self.disk.DiskReadsPerSec

    def getDiskWrites(self):
        self.update_status()
        return self.disk.DiskWritesPerSec

    def update_status(self):
        self.disk = self.conn.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1]

    def setData(self):
        self.data['DiskReadsPersec'] = self.getDiskReads()
        self.data['DiskWritesPersec'] = self.getDiskWrites()

    def setAgentName(self):
        self.agent_name = 'Disk Agent ' + self.hostname

# disk = conn.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1] ->
# -> in order to select total disk writes and read
# disk = conn.query("SELECT DiskReadsPerSec, DiskWritesPerSec
#                    FROM Win32_PerfRawData_PerfDisk_PhysicalDisk")
