import time
import thread

from system_monitor.agents import agent as ag
from system_monitor import conf
from sys import platform as _platform


def Windows_Client():  # Get all the details about the system using WMI
    # How to initiate an agent:
    # -> use the name of the agent, currently available agents:
    # CPU, RAM, DISK, NET
    # For the name please start with RAM, CPU, NET, DISK and add a custom name
    # after that in order to identify the agent in the database
    # -> and the mode, currently available:
    # use 1 for used CPU or Memory, Disk reads/sec, Network sent bytes
    # use 2 for free CPU or Memory, Disk writes/sec, Network received bytes
    thread.start_new_thread(ag.Agent, ("RAM used", 1))
    thread.start_new_thread(ag.Agent, ("CPU used", 1))
    thread.start_new_thread(ag.Agent, ("NET sent bytes", 1))
    thread.start_new_thread(ag.Agent, ("DISK read ops", 1))

    sample_no = 1
    while (True):
        # sample_no represents the number of entries that have been inserted
        # into the database since the script started
        print 'Sample number: %s' % sample_no
        sample_no = sample_no + 1
        time.sleep(conf.update_interval)

# checks to see if the program is being run directly or it's being imported
if __name__ == "__main__":
    # Determine the OS of the node and select the specific monitor function
    if _platform == "linux" or _platform == "linux2":
        print 'Linux not supported yet'
    elif _platform == "darwin":
        print 'MacOS not suppoert yet'
    elif _platform == "win32":
        Windows_Client()
