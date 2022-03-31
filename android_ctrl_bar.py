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

# Define the window's contents
layout = [ [sg.Text("Device:")],
           [sg.Button(size=(7,1), key='btnWAKEUP', button_text='Resume'),
            sg.Button(size=(7,1), key='btnSLEEP', button_text='Suspend'),
            sg.Button(size=(7,1), key='btnREBOOT', button_text='Reboot')],
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
           [sg.Text("ADB commands:")],
           [sg.Button(size=(7,1), key='btnADB_ROOT', button_text='root'),
            sg.Button(size=(7,1), key='btnADB_UNROOT', button_text='unroot'),
            sg.Button(size=(7,1), key='btnADB_REMOUNT', button_text='remount')],
           [sg.Button(size=(12,1), key='btnDEVICES', button_text='Check device')],
           [sg.Checkbox(key='chkboxDevice', text='')],
           [sg.Text("Status: "), sg.Text(size=(25,1), key='statusText')],
         ]

# Create the window
window = sg.Window('Android Control Bar', layout, keep_on_top = True)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    # Handle button events
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
        adbCmd(5, "reboot")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'btnDEVICES':
        window['chkboxDevice'].update(text='')
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
                    window['chkboxDevice'].update(text=strSerial)

# Finish up by removing from the screen
window.close()
