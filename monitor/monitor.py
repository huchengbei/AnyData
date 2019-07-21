import os
import subprocess
import time
from typing import Union
from configparser import ConfigParser
import psutil

CONFIGFILE = 'config.ini'
config = ConfigParser()
config.read(CONFIGFILE)
back_exe = config.get('backend', 'path')
back_name = config.get('backend', 'name')
front_exe = config.get('frontend', 'path')
front_name = config.get('frontend', 'name')

front = subprocess.Popen(front_exe, shell=True)
back = subprocess.Popen(back_exe, shell=True)
# front = os.system(front_exe)
# back = os.system(back_exe)
ProList = []


def main(front_pid, back_pid):
    for proc in psutil.process_iter():
        try:
            ProList.append(proc.pid)
        except psutil.NoSuchProcess:
            pass

    status = True
    if front_pid in ProList:
        print('')
        print("Server is running...")
        print('')
    else:
        print('Server is not running,Begin to Restart Server...')
        os.system('taskkill /f /pid %s' % back_pid)
        print(time.strftime('%Y-%m-%d %H:%M:%S --%A--%c', time.localtime()))
        status = False
    del ProList[:]
    return status


def check_back():
    proc_list = []
    for proc in psutil.process_iter():
        try:
            proc_list.append({'name': proc.name(), 'pid': proc.pid})
        except psutil.NoSuchProcess:
            pass
    for item in proc_list:
        if back_name == item['name']:
            return item['pid']
    return False


def check_front():
    proc_list = []
    for proc in psutil.process_iter():
        try:
            proc_list.append({'name': proc.name(), 'pid': proc.pid})
        except psutil.NoSuchProcess:
            pass
    for item in proc_list:
        if front_name == item['name']:
            return item['pid']
    return False


if __name__ == "__main__":
    back_pid: Union[int, bool] = check_back()
    while back_pid is False:
        back_pid = check_back()
    front_pid: Union[int, bool] = check_front()
    while front_pid is False:
        front_pid = check_front()
    while main(front_pid, back_pid):
        time.sleep(10)