'''
    Triyadhi Surahman
    2014-04-04
    Shutdown Windows if Laptop battery <= X%

    http://stackoverflow.com/questions/6153860/in-python-how-can-i-detect-whether-the-computer-is-on-battery-power
    http://stackoverflow.com/questions/2765405/add-windows-commands-in-python
'''

import ctypes
from ctypes import wintypes

import time
import subprocess

# check every x seconds
waitSeconds = 60
# wait before shutdown (seconds)
waitShutdown = 2
# battery % for shutdown
batteryMinimumPercentage = 10

# define structure for GetSystemPowerStatus()'s SYSTEM_POWER_STATUS
class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]    

# get system power status
def getPowerStatus():
    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)

    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    status = SYSTEM_POWER_STATUS()
    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()

    return status

# call subprocess shutdown
def shutdown(timeout):
    subprocess.call(["shutdown.exe", "-s", "-f", "-t", str(timeout)])

# loop until batteryLifePercentage <= batteryMinimumPercentage
while True:
    batteryLifePercentage = getPowerStatus().BatteryLifePercent
    print("battery %i%%" % batteryLifePercentage)

    if batteryLifePercentage <= batteryMinimumPercentage:
        shutdown(waitShutdown)
        print("shutdown ...")
        break
    
    time.sleep(waitSeconds)
