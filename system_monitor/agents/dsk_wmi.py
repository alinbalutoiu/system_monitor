import wmi

class wmi_dsk:
    def __init__(self, mode):
        self.mode = mode
        self.conn = wmi.WMI()
        
    def getDiskReads(self):
        self.update_status()
        return self.disk.DiskReadsPerSec

    def getDiskWrites(self):
        self.update_status()
        return self.disk.DiskWritesPerSec

    def update_status(self):
        self.disk = self.conn.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1]

    def get_data(self):
        if self.mode == 1:
            return self.getDiskReads()
        elif self.mode == 2:
            return self.getDiskWrites()

# disk = conn.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1] ->
# -> in order to select total disk writes and read
# disk = conn.query("SELECT DiskReadsPerSec, DiskWritesPerSec 
#                    FROM Win32_PerfRawData_PerfDisk_PhysicalDisk")
