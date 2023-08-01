import re
import subprocess
import threading
from datetime import datetime
import PySimpleGUI as sg
import acp_cmd

def getLayoutName() -> str:
    return 'Main'

def getLayout() -> list:
    layout = [
        [sg.Text("ADB commands:")],
        [sg.Button(key='btnAdbKeycode_POWER', button_text='Power'),
         sg.Button(key='btnAdbKeycode_SLEEP', button_text='Suspend'),
         sg.Button(key='btnAdbKeycode_WAKEUP', button_text='Resume'),
         sg.Text("|"), 
         sg.Button(key='btnADB_REBOOT_P', button_text='Shutdown'),
         sg.Text("|"),
         sg.Button(key='btnADB_REBOOT', button_text='Reboot'),
         sg.Button(key='btnADB_REBOOT_BL', button_text='Reboot Bootloader')],
        [sg.Button(key='btnADB_ROOT', button_text='Root'),
         sg.Button(key='btnADB_UNROOT', button_text='Unroot'),
         sg.Text("|"),
         sg.Button(key='btnADB_REMOUNT', button_text='Remount'),
         sg.Button(key='btnADB_DISABLE_VERITY', button_text='Disable-verity'),
         sg.Text("|"),
         sg.Button(key='btnScreenShot', button_text='Screenshot')],
        [sg.Text("Set SELinux"),
         sg.Button(key='btnSetenforce_0', button_text='Permissive (0)'),
         sg.Button(key='btnSetenforce_1', button_text='Enforcing (1)'),
         sg.Text("|"),
         sg.Button(key='btnRestartServices', button_text='Restart Services'),
         sg.Button(key='btnFactoryReset', button_text='Factory Reset'), sg.Text("*Need ROOT first")],
        [sg.HorizontalSeparator()],
        [sg.Text("Fastboot commands:")],
        [sg.Button(key='btnFB_REBOOT', button_text='Reboot'),
         sg.Button(key='btnFB_REBOOT_BL', button_text='Reboot Bootloader')],
        [sg.HorizontalSeparator()],
        [sg.Text("Key codes:")],
        [sg.Button(size=(5,1), key='btnAdbKeycode_BACK', button_text='◀'),
         sg.Button(size=(5,1), key='btnAdbKeycode_HOME', button_text='●'),
         sg.Button(size=(5,1), key='btnAdbKeycode_APP_SWITCH', button_text='◼'),
         sg.Button(size=(5,1), key='btnAdbKeycode_MENU', button_text='≡')],
        [sg.Button(size=(5,1), key='btnAdbKeycode_PAGE_UP', button_text='PgUp'),
         sg.Button(size=(5,1), key='btnAdbKeycode_DPAD_UP', button_text='↑'),
         sg.Button(size=(5,1), key='btnAdbKeycode_PAGE_DOWN', button_text='PgDn'),
         sg.Button(size=(5,1), key='btnAdbKeycode_VOLUME_UP', button_text='♪+'),
         sg.Button(size=(5,1), key='btnAdbKeycode_VOLUME_MUTE', button_text='♪×')],
        [sg.Button(size=(5,1), key='btnAdbKeycode_DPAD_LEFT', button_text='←'),
         sg.Button(size=(5,1), key='btnAdbKeycode_DPAD_DOWN', button_text='↓'),
         sg.Button(size=(5,1), key='btnAdbKeycode_DPAD_RIGHT', button_text='→'),
         sg.Button(size=(5,1), key='btnAdbKeycode_VOLUME_DOWN', button_text='♪-')],
        [sg.HorizontalSeparator()],
        [sg.Button(key='btnADB_DEVICES', button_text='Check ADB'),
         sg.Button(key='btnFB_DEVICES', button_text='Check Fastboot')],
        [sg.Checkbox(key='chkboxDevice', text='None', disabled=True)]
    ]
    return layout

def getScreenShot(window) -> bool:
    now = datetime.now()
    screencap_file = "screenshot_" + now.strftime("%Y%m%d_%H%M%S") + ".png"
    fp = open(screencap_file, "a+")
    try:
        subprocess.check_call('adb exec-out screencap -p', stdout=fp, timeout=30)
    except subprocess.TimeoutExpired:
        window['statusText'].update('Screenshot Timeout !')
    fp.close()
    return True

def processEvent(window, event) -> bool:
    rc = False

    if re.match('btnAdbKeycode_([ -~]+)', event):
        dontcare, keycode = event.split('code_', maxsplit=1)
        acp_cmd.adbCmd(5, "shell input keyevent " + keycode)
        rc = True
    ## ADB commands
    elif event == 'btnADB_ROOT':
        tAdbRoot = threading.Thread(target=acp_cmd.adbRootCheck, args=(window))
        tAdbRoot.start()
        rc = True
    elif event == 'btnADB_UNROOT':
        acp_cmd.adbCmd(5, "unroot")
        rc = True
    elif event == 'btnADB_REMOUNT':
        acp_cmd.adbCmd(5, "remount")
        rc = True
    elif event == 'btnADB_REBOOT':
        acp_cmd.adbCmd(10, "reboot")
        rc = True
    elif event == 'btnADB_REBOOT_BL':
        acp_cmd.adbCmd(10, "reboot bootloader")
        rc = True
    elif event == 'btnADB_REBOOT_P':
        acp_cmd.adbCmd(10, "shell reboot -p")
        rc = True
    elif event == 'btnADB_DISABLE_VERITY':
        acp_cmd.adbCmd(5, "disable-verity")
        rc = True
    elif event == 'btnScreenShot':
        getScreenShot(window)
        rc = True
    elif event == 'btnSetenforce_0':
        acp_cmd.adbCmd(5, "shell setenforce 0")
        rc = True
    elif event == 'btnSetenforce_1':
        acp_cmd.adbCmd(5, "shell setenforce 1")
        rc = True
    elif event == 'btnFactoryReset':
        acp_cmd.adbCmd(10, "shell am broadcast -p \"android\" --receiver-foreground -a android.intent.action.FACTORY_RESET", donotprintcmd=True)
        rc = True
    elif event == 'btnRestartServices':
        acp_cmd.adbCmd(10, "shell stop", blocking=True, donotprintcmd=True)
        acp_cmd.adbCmd(10, "shell start", blocking=True, donotprintcmd=True)
        rc = True
    # Fastboot commands
    elif event == 'btnFB_REBOOT':
        acp_cmd.fastbootCmd(10, "reboot")
        rc = True
    elif event == 'btnFB_REBOOT_BL':
        acp_cmd.fastbootCmd(10, "reboot bootloader")
        rc = True
    ## Check devices
    elif event == 'btnADB_DEVICES':
        window['chkboxDevice'].update(text='None', disabled=True)
        cmd = "adb devices"
        stdoutdata = subprocess.getoutput(cmd)
        for line in stdoutdata.splitlines():
            if line[0] == '*':
                pass
            elif line == 'List of devices attached':
                pass
            else:
                strSerial, strDevStatus = line.split(maxsplit=1)
                if strDevStatus == 'device':
                    window['chkboxDevice'].update(text=strSerial, disabled=False)
        rc = True
    elif event == 'btnFB_DEVICES':
        window['chkboxDevice'].update(text='None', disabled=True)
        cmd = "fastboot devices"
        stdoutdata = subprocess.getoutput(cmd)
        for line in stdoutdata.splitlines():
            if line[0] == '*':
                pass
            elif line == 'List of devices attached':
                pass
            else:
                strSerial, strDevStatus = line.split(maxsplit=1)
                if strDevStatus == 'fastboot':
                    window['chkboxDevice'].update(text=strSerial, disabled=False)
        rc = True

    return rc
