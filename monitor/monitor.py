import os
import subprocess
import time
from typing import Union
from configparser import ConfigParser
import psutil
import win32gui
from win32.lib import win32con

CONFIGFILE = 'config.ini'
if not os.path.exists(CONFIGFILE):
    win32gui.MessageBox(0, "找不到配置文件", "提醒", win32con.MB_OK)
    exit()
config = ConfigParser()
config.read(CONFIGFILE)
back_exe = config.get('backend', 'path')
back_name = config.get('backend', 'name')
front_exe = config.get('frontend', 'path')
front_name = config.get('frontend', 'name')
if not os.path.exists(back_exe[1:-1]):
    win32gui.MessageBox(0, "后端程序配置文件错误", "提醒", win32con.MB_OK)
    exit()
if not os.path.exists(front_exe[1:-1]):
    win32gui.MessageBox(0, "前端程序配置文件错误", "提醒", win32con.MB_OK)
    exit()

front = subprocess.Popen(front_exe, shell=True)
back = subprocess.Popen(back_exe, shell=True)
# front = os.system(front_exe)
# back = os.system(back_exe)
ProList = []


def main():
    for proc in psutil.process_iter():
        try:
            ProList.append(proc.name)
        except psutil.NoSuchProcess:
            pass

    status = True
    if front_name in ProList:
        print('')
        print("Server is running...")
        print('')
    else:
        os.system('taskkill /f /im %s' % back_name)
        # os.system('taskkill /f /pid %s' % back_pid)
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
            return True
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
            return True
    return False


if __name__ == "__main__":
    back_status = check_back()
    while back_status is False:
        back_status = check_back()
    front_status = check_front()
    while front_status is False:
        front_status = check_front()
    while main():
        time.sleep(2)
