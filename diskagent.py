import system_monitor.agents.windows.dsk_wmi as disk
from sys import platform as _platform


if __name__ == "__main__":
    if _platform == "linux" or _platform == "linux2":
        print 'Linux not supported yet'
    elif _platform == "darwin":
        print 'MacOS not suppoert yet'
    elif _platform == "win32":
        agent = disk.wmi_dsk()
        agent.start_agent()
