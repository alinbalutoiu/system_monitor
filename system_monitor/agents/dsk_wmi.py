import wmi
conn = wmi.WMI()

disk = conn.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1]    # in order to select total disk writes and read
# disk = conn.query("SELECT DiskReadsPerSec, DiskWritesPerSec FROM Win32_PerfRawData_PerfDisk_PhysicalDisk")

class wmi_dsk:

    def getDiskReads(self):
        disk = conn.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1]
        return disk.DiskReadsPerSec

    def getDiskWrites(self):
        disk = conn.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1]
        return disk.DiskWritesPerSec