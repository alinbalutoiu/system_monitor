import wmi
conn = wmi.WMI()
netw = conn.query("SELECT BytesSentPersec, BytesReceivedPersec, CurrentBandwidth \
                       FROM Win32_PerfRawData_Tcpip_NetworkInterface")

class wmi_net:

    def getBytesSentPerSec(self):
        netw = conn.query("SELECT BytesSentPersec, BytesReceivedPersec, CurrentBandwidth \
                           FROM Win32_PerfRawData_Tcpip_NetworkInterface")
        bytesSent = 0
        for i in netw:
            bytesSent = bytesSent + int(i.BytesSentPersec)
        return bytesSent

    # computing the sum of total bytes sent by all network adapters
    def getBytesReceivedPerSec(self):
        netw = conn.query("SELECT BytesSentPersec, BytesReceivedPersec, CurrentBandwidth \
                           FROM Win32_PerfRawData_Tcpip_NetworkInterface")
        bytesReceived = 0
        for i in netw:
            bytesReceived = bytesReceived + int(i.BytesReceivedPersec)
        return bytesReceived