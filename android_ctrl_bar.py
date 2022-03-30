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
layout = [ [sg.Text("Press button")],
           [sg.Button('Back'), sg.Button('Home'), sg.Button('Apps')],
           [sg.Text("Status: "), sg.Text(size=(40,1), key='statusText')],
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
    elif event == 'Back':
        window['statusText'].update('Input ' + event + ", executing... ")
        adbCmd(5, "shell input keyevent BACK")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'Home':
        window['statusText'].update('Input ' + event + ", executing... ")
        adbCmd(5, "shell input keyevent HOME")
        window['statusText'].update('Input ' + event + ", done")
    elif event == 'Apps':
        window['statusText'].update('Input ' + event + ", executing... ")
        adbCmd(5, "shell input keyevent APP_SWITCH")
        window['statusText'].update('Input ' + event + ", done")

# Finish up by removing from the screen
window.close()
