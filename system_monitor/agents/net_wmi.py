import wmi


class wmi_net:
    def __init__(self, mode):
        self.mode = mode
        self.conn = wmi.WMI()

    # computing the sum of total bytes sent by all network adapters
    def getBytesSentPerSec(self):
        self.update_status()
        bytesSent = 0
        for i in self.netw:
            bytesSent = bytesSent + int(i.BytesSentPersec)
        return bytesSent

    def getBytesReceivedPerSec(self):
        self.update_status()
        bytesReceived = 0
        for i in self.netw:
            bytesReceived = bytesReceived + int(i.BytesReceivedPersec)
        return bytesReceived

    def update_status(self):
        self.netw = self.conn.query("SELECT BytesSentPersec, BytesReceivedPersec, CurrentBandwidth \
                                     FROM Win32_PerfRawData_Tcpip_NetworkInterface")

    def get_data(self):
        if self.mode == 1:
            return self.getBytesSentPerSec()
        elif self.mode == 2:
            return self.getBytesReceivedPerSec()
