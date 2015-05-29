from system_monitor.controller import controller
from system_monitor.agents import agent
from system_monitor.db import api
from system_monitor import constants as ct
import time

# Get all the details about the system using WMI
def Windows_Client():
    import system_monitor.agents.mem_wmi
    memory_agent = system_monitor.agents.mem_wmi.wmi_mem()

    import system_monitor.agents.cpu_wmi
    cpu_agent = system_monitor.agents.cpu_wmi.wmi_cpu()

    import system_monitor.agents.net_wmi
    net_agent = system_monitor.agents.net_wmi.wmi_net()

    import system_monitor.agents.dsk_wmi
    dsk_agent = system_monitor.agents.dsk_wmi.wmi_dsk()
    
    ag = agent.SystemMonitorAgentRPCAPI()

    # try to add the agents if the database doesn't contain them already
    ag.call(api.add_agent,"Memory Agent")
    ag.call(api.add_agent,"CPU Agent")
    ag.call(api.add_agent,"Network Agent")
    ag.call(api.add_agent,"Disk Agent")

    sample_no = 1
    while (True) :
        # sample_no represents the number of entries that have been inserted 
        # into the database since the script started
        print 'Sample number: %s' % sample_no
        time.sleep(ct.update_interval)
        sample_no = sample_no + 1

        # Agent IDs:
        # 1 - Memory Agent
        # 2 - CPU Agent
        # 3 - Network Agent
        # 4 - Disk Agent

        # add details about Free Memory in the database using the Memory Agent
        ag.call(api.add_status,1,memory_agent.getFreeMemory()) 

        # add details about Used CPU in the database using the CPU Agent
        ag.call(api.add_status,2,cpu_agent.getUsedCPU())

        # add details about all the traffic sent out by all NICs in
        # the database using Network Agent
        ag.call(api.add_status,3,net_agent.getBytesSentPerSec())

        # add details about rate of read operations on the disk using Disk Agent
        ag.call(api.add_status,4,dsk_agent.getDiskReads())
        
    # get the statistics for each agent at the end
    # ag.call(api.get_stats,1)
    # ag.call(api.get_stats,2)
    # ag.call(api.get_stats,3)
    # ag.call(api.get_stats,4)


from sys import platform as _platform

# Determine the OS of the node and select the monitor function specific for the OS
if _platform == "linux" or _platform == "linux2":
    print 'Linux not supported yet'
elif _platform == "darwin":
    print 'MacOS not suppoert yet'
elif _platform == "win32":
    Windows_Client()