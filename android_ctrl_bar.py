#
# Android control bar
#

import subprocess
import time
import PySimpleGUI as sg

# Functions
def adbCmd(timeout_sec: int, command: str) -> bool:
    rc = True
    if timeout_sec < 1:
        print("Arg timeout_sec must >= 1")
        return False
    try:
        cmd = "adb " + command
        stdoutdata = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        print("adb command TIMEOUT !!!")
        rc = False
    except subprocess.CalledProcessError as e:
        print(e.output)
        rc = False
    return rc

def fastbootCmd(timeout_sec: int, command: str) -> bool:
    rc = True
    if timeout_sec < 1:
        print("Arg timeout_sec must >= 1")
        return False
    try:
        cmd = "fastboot " + command
        stdoutdata = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        print("fastboot command TIMEOUT !!!")
        rc = False
    except subprocess.CalledProcessError as e:
        print(e.output)
        rc = False
    return rc

# Define the window's contents
layout = [ [sg.Text("ADB commands:")],
           [sg.Button(key='btnWAKEUP', button_text='Resume'),
            sg.Button(key='btnSLEEP', button_text='Suspend'),
            sg.Button(key='btnREBOOT', button_text='Reboot')],
           [sg.Button(key='btnREBOOT_BL', button_text='Reboot Bootloader'),
            sg.Button(key='btnDISABLE_VERITY', button_text='Disable-verity')],
           [sg.Button(key='btnADB_ROOT', button_text='Root'),
            sg.Button(key='btnADB_UNROOT', button_text='Unroot'),
            sg.Button(key='btnADB_REMOUNT', button_text='Remount')],
           [sg.HorizontalSeparator()],
           [sg.Text("Fastboot commands:")],
           [sg.Button(key='btnFB_REBOOT', button_text='Reboot'),
            sg.Button(key='btnFB_REBOOT_BL', button_text='Reboot Bootloader')],
           [sg.HorizontalSeparator()],
           [sg.Text("Key codes:")],
           [sg.Button(size=(5,1), key='btnBACK', button_text='◀'),
            sg.Button(size=(5,1), key='btnHOME', button_text='●'),
            sg.Button(size=(5,1), key='btnAPP_SWITCH', button_text='◼')],
           [sg.Button(size=(5,1), key='btnPAGE_UP', button_text='PgUp'),
            sg.Button(size=(5,1), key='btnDPAD_UP', button_text='↑'),
            sg.Button(size=(5,1), key='btnPAGE_DOWN', button_text='PgDn'),
            sg.Button(size=(5,1), key='btnVOLUME_UP', button_text='♪+')],
           [sg.Button(size=(5,1), key='btnDPAD_LEFT', button_text='←'),
            sg.Button(size=(5,1), key='btnDPAD_DOWN', button_text='↓'),
            sg.Button(size=(5,1), key='btnDPAD_RIGHT', button_text='→'),
            sg.Button(size=(5,1), key='btnVOLUME_DOWN', button_text='♪-')],
           [sg.HorizontalSeparator()],
           [sg.Button(key='btnADB_DEVICES', button_text='Check ADB'),
            sg.Button(key='btnFB_DEVICES', button_text='Check Fastboot')],
           [sg.Checkbox(key='chkboxDevice', text='None', disabled=True)],
           [sg.HorizontalSeparator()],
           [sg.Text("Source:", size=(6,1)), sg.Input(key='inputPushFileSource'), sg.FileBrowse()],
           [sg.Text("Target:", size=(6,1)), sg.Input(key='inputPushTarget', default_text='/sdcard/')],
           [sg.Button(size=(10,1), key='btnPushFile', button_text='Push File')],
           [sg.HorizontalSeparator()],
           [sg.Text("Status:"), sg.Text(key='statusText')]
         ]

# Create the window
window = sg.Window('Android Control Bar', layout, keep_on_top = True)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    # Key codes
    elif event == 'btnBACK':
        adbCmd(5, "shell input keyevent BACK")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnHOME':
        adbCmd(5, "shell input keyevent HOME")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnAPP_SWITCH':
        adbCmd(5, "shell input keyevent APP_SWITCH")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnPAGE_UP':
        adbCmd(5, "shell input keyevent PAGE_UP")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnPAGE_DOWN':
        adbCmd(5, "shell input keyevent PAGE_DOWN")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnDPAD_UP':
        adbCmd(5, "shell input keyevent DPAD_UP")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnDPAD_DOWN':
        adbCmd(5, "shell input keyevent DPAD_DOWN")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnDPAD_LEFT':
        adbCmd(5, "shell input keyevent DPAD_LEFT")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnDPAD_RIGHT':
        adbCmd(5, "shell input keyevent DPAD_RIGHT")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnVOLUME_UP':
        adbCmd(5, "shell input keyevent VOLUME_UP")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnVOLUME_DOWN':
        adbCmd(5, "shell input keyevent VOLUME_DOWN")
        window['statusText'].update('Input ' + event + ", done")
    # ADB commands
    elif event == 'btnADB_ROOT':
        adbCmd(5, "root")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnADB_UNROOT':
        adbCmd(5, "unroot")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnADB_REMOUNT':
        adbCmd(5, "remount")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnWAKEUP':
        adbCmd(5, "shell input keyevent WAKEUP")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnSLEEP':
        adbCmd(5, "shell input keyevent SLEEP")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnREBOOT':
        adbCmd(10, "reboot")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnREBOOT_BL':
        adbCmd(10, "reboot bootloader")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnDISABLE_VERITY':
        adbCmd(5, "disable-verity")
        window['statusText'].update('Input ' + event + ", done")
    # Fastboot commands
    elif event == 'btnFB_REBOOT':
        fastbootCmd(10, "reboot")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnFB_REBOOT_BL':
        fastbootCmd(10, "reboot bootloader")
        window['statusText'].update('Input ' + event + ", done")
    # Check devices
    elif event == 'btnADB_DEVICES':
        window['chkboxDevice'].update(text='None', disabled=True)
        cmd = "adb devices"
        stdoutdata = subprocess.getoutput(cmd)
        print(stdoutdata)
        for line in stdoutdata.splitlines():
            if line[0] == '*':
                # ignore
                print(line)
            elif line == 'List of devices attached':
                # ignore
                print(line)
            else:
                strSerial, strDevStatus = line.split(maxsplit=1)
                if strDevStatus == 'device':
                    window['chkboxDevice'].update(text=strSerial, disabled=False)
    elif event == 'btnFB_DEVICES':
        window['chkboxDevice'].update(text='None', disabled=True)
        cmd = "fastboot devices"
        stdoutdata = subprocess.getoutput(cmd)
        print(stdoutdata)
        for line in stdoutdata.splitlines():
            if line[0] == '*':
                # ignore
                print(line)
            elif line == 'List of devices attached':
                # ignore
                print(line)
            else:
                strSerial, strDevStatus = line.split(maxsplit=1)
                if strDevStatus == 'fastboot':
                    window['chkboxDevice'].update(text=strSerial, disabled=False)
    # Push file to device
    elif event == 'btnPushFile':
        adbCmd(10, "push \"" + window['inputPushFileSource'].get() + "\" \"" + window['inputPushTarget'].get() + "\"")

# Finish up by removing from the screen
window.close()
