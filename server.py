from system_monitor.controller import controller
from system_monitor.agents import agent
from system_monitor.db import api as dbapi
from system_monitor import constants

controller.SystemMonitorControllerAPI().accept()
