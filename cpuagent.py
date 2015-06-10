import system_monitor.agents.cpu_wmi as cpu


if __name__ == "__main__":
    agent = cpu.wmi_cpu()
    agent.start_agent()
