from system_monitor.agents.agent_model import Agent_Model


class wmi_net(Agent_Model):
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
        self.netw = self.conn.query("SELECT BytesSentPersec, BytesReceivedPersec \
                                     FROM Win32_PerfRawData_Tcpip_NetworkInterface")

    def setData(self):
        self.data['NetBytesSentPersec'] = self.getBytesSentPerSec()
        self.data['NetBytesReceivedPersec'] = self.getBytesReceivedPerSec()

    def setAgentName(self):
        self.agent_name = 'Net Agent ' + self.hostname
