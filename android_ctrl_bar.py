#
# Android control bar
#

import subprocess
import time
import threading
import PySimpleGUI as sg

# Functions
def cmdExec(timeout_sec: int, cmd: str) -> bool:
    rc = True
    try:
        stdoutdata = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        #print("Oommand TIMEOUT !!!")
        window['statusText'].update('Command timeout: ' + cmd)
        rc = False
    except subprocess.CalledProcessError as e:
        print(e.output)
        window['statusText'].update('Command error: ' + e.output)
        rc = False
    if rc == True:
        window['statusText'].update('Command done: ' + cmd)
    return rc

def adbCmd(timeout_sec: int, command: str) -> bool:
    rc = True
    if timeout_sec < 1:
        print("Arg timeout_sec must >= 1")
        return False
    window['statusText'].update('Processing command: adb ' + command)
    tCmd = threading.Thread(target=cmdExec, args=(timeout_sec, "adb " + command))
    tCmd.start()
    return rc

def fastbootCmd(timeout_sec: int, command: str) -> bool:
    rc = True
    if timeout_sec < 1:
        print("Arg timeout_sec must >= 1")
        return False
    window['statusText'].update('Processing command: fastboot ' + command)
    tCmd = threading.Thread(target=cmdExec, args=(timeout_sec, "fastboot " + command))
    tCmd.start()
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
    elif event == 'btnHOME':
        adbCmd(5, "shell input keyevent HOME")
    elif event == 'btnAPP_SWITCH':
        adbCmd(5, "shell input keyevent APP_SWITCH")
    elif event == 'btnPAGE_UP':
        adbCmd(5, "shell input keyevent PAGE_UP")
    elif event == 'btnPAGE_DOWN':
        adbCmd(5, "shell input keyevent PAGE_DOWN")
    elif event == 'btnDPAD_UP':
        adbCmd(5, "shell input keyevent DPAD_UP")
    elif event == 'btnDPAD_DOWN':
        adbCmd(5, "shell input keyevent DPAD_DOWN")
    elif event == 'btnDPAD_LEFT':
        adbCmd(5, "shell input keyevent DPAD_LEFT")
    elif event == 'btnDPAD_RIGHT':
        adbCmd(5, "shell input keyevent DPAD_RIGHT")
    elif event == 'btnVOLUME_UP':
        adbCmd(5, "shell input keyevent VOLUME_UP")
    elif event == 'btnVOLUME_DOWN':
        adbCmd(5, "shell input keyevent VOLUME_DOWN")
    # ADB commands
    elif event == 'btnADB_ROOT':
        adbCmd(5, "root")
    elif event == 'btnADB_UNROOT':
        adbCmd(5, "unroot")
    elif event == 'btnADB_REMOUNT':
        adbCmd(5, "remount")
    elif event == 'btnWAKEUP':
        adbCmd(5, "shell input keyevent WAKEUP")
    elif event == 'btnSLEEP':
        adbCmd(5, "shell input keyevent SLEEP")
    elif event == 'btnREBOOT':
        adbCmd(10, "reboot")
    elif event == 'btnREBOOT_BL':
        adbCmd(10, "reboot bootloader")
    elif event == 'btnDISABLE_VERITY':
        adbCmd(5, "disable-verity")
    # Fastboot commands
    elif event == 'btnFB_REBOOT':
        fastbootCmd(10, "reboot")
    elif event == 'btnFB_REBOOT_BL':
        fastbootCmd(10, "reboot bootloader")
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
