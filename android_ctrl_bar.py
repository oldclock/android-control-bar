#
# Android control bar
#

import configparser
import subprocess
import threading
import PySimpleGUI as sg

EXEC_ADB_DEFAULT = str('adb.exe')
mExecAdbPath = EXEC_ADB_DEFAULT
mExecAdbPathVerified = bool(False)
EXEC_FASTBOOT_DEFAULT = str('fastboot.exe')
mExecFastbootPath = EXEC_FASTBOOT_DEFAULT
mExecFastbootPathVerified = bool(False)

# Functions
def cmdExec(timeout_sec: int, cmd: str) -> bytes:
    rc = True
    try:
        stdoutdata = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        #print("Command TIMEOUT !!!")
        window['statusText'].update(window['statusText'].get() + 'Timeout !')
        rc = False
    except subprocess.CalledProcessError as e:
        print(e.output)
        window['statusText'].update(window['statusText'].get() + 'Error: ' + e.output)
        rc = False
    if rc == True:
        window['statusText'].update(window['statusText'].get() + ' done')
        return stdoutdata
    else:
        return "ERROR"

def adbCmd(timeout_sec: int, command: str) -> bool:
    global mExecAdbPath, mExecAdbPathVerified
    rc = True
    if timeout_sec < 1:
        print("Arg timeout_sec must >= 1")
        return False
    if mExecAdbPathVerified == False:
        window['statusText'].update('ADB path not verified')
        if verifyAdbPath(mExecAdbPath) == True:
            mExecAdbPathVerified = True
        else:
            return False

    window['statusText'].update('Processing command: adb ' + command)
    tCmd = threading.Thread(target=cmdExec, args=(timeout_sec, mExecAdbPath + " " + command))
    tCmd.start()
    return rc

def fastbootCmd(timeout_sec: int, command: str) -> bool:
    global mExecFastbootPath, mExecFastbootPathVerified
    rc = True
    if timeout_sec < 1:
        print("Arg timeout_sec must >= 1")
        return False
    if mExecFastbootPathVerified == False:
        window['statusText'].update('Fastboot path not verified')
        if verifyFastbootPath(mExecFastbootPath) == True:
            mExecFastbootPathVerified = True
        else:
            return False

    window['statusText'].update('Processing command: fastboot ' + command)
    tCmd = threading.Thread(target=cmdExec, args=(timeout_sec, mExecFastbootPath + " " + command))
    tCmd.start()
    return rc

def verifyAdbPath(path: str) -> bool:
    rc = False
    window['statusText'].update('Processing command: adb --version')
    adbVersion = cmdExec(10, path + " --version").decode('latin1')
    if adbVersion[:20] == "Android Debug Bridge":
        rc = True
        window['statusCheckExec'].update(window['statusCheckExec'].get() + adbVersion + '\n')
    return rc

def verifyFastbootPath(path: str) -> bool:
    rc = False
    window['statusText'].update('Processing command: fastboot --version')
    fastbootVersion = cmdExec(10, path + " --version").decode('latin1')
    if fastbootVersion[:8] == "fastboot":
        rc = True
        window['statusCheckExec'].update(window['statusCheckExec'].get() + fastbootVersion + '\n')
    return rc

def checkExecutable() -> bool:
    rc = True
    global mExecAdbPath, mExecAdbPathVerified, mExecFastbootPath, mExecFastbootPathVerified
    window['statusCheckExec'].update('')

    tmpAdbPath = window['inputAdbPath'].get()
    if tmpAdbPath[-7:].casefold() == "adb.exe":
        window['statusCheckExec'].update(window['statusCheckExec'].get() + '\nUse user input ADB Path\n')
        if verifyAdbPath(tmpAdbPath) == True:
            mExecAdbPath = tmpAdbPath
            mExecAdbPathVerified = True
            if 'host_settings' not in config:
                config['host_settings'] = {}
            config['host_settings']['ADB'] = mExecAdbPath
            with open('local_config.ini', 'w') as configfile:
                config.write(configfile)
    else:
        window['inputAdbPath'].update('')
        window['statusCheckExec'].update(window['statusCheckExec'].get() + '\nUse system ADB Path\n')
        mExecAdbPath = EXEC_ADB_DEFAULT
        if 'host_settings' in config:
            if 'ADB' in config['host_settings']:
                config['host_settings']['ADB'] = EXEC_ADB_DEFAULT
                with open('local_config.ini', 'w') as configfile:
                    config.write(configfile)
        if verifyAdbPath(EXEC_ADB_DEFAULT) == True:
            mExecAdbPathVerified = True

    tmpFastbootPath = window['inputFastbootPath'].get()
    if tmpFastbootPath[-12:].casefold() == "fastboot.exe":
        window['statusCheckExec'].update(window['statusCheckExec'].get() + '\nUse user input Fastboot Path\n')
        if verifyFastbootPath(tmpFastbootPath) == True:
            mExecFastbootPath = tmpFastbootPath
            mExecFastbootPathVerified = True
            if 'host_settings' not in config:
                config['host_settings'] = {}
            config['host_settings']['Fastboot'] = mExecFastbootPath
            with open('local_config.ini', 'w') as configfile:
                config.write(configfile)
    else:
        window['inputFastbootPath'].update('')
        window['statusCheckExec'].update(window['statusCheckExec'].get() + '\nUse system Fastboot Path\n')
        mExecFastbootPath = EXEC_FASTBOOT_DEFAULT
        if 'host_settings' in config:
            if 'Fastboot' in config['host_settings']:
                config['host_settings']['Fastboot'] = EXEC_FASTBOOT_DEFAULT
                with open('local_config.ini', 'w') as configfile:
                    config.write(configfile)
        if verifyFastbootPath(mExecFastbootPath) == True:
            mExecFastbootPathVerified = True

    return rc

# Define the window's contents
layout = [ [sg.Text("ADB commands:")],
           [sg.Button(key='btnSLEEP', button_text='Suspend'),
            sg.Button(key='btnWAKEUP', button_text='Resume'),
            sg.Button(key='btnREBOOT', button_text='Reboot'),
            sg.Button(key='btnREBOOT_BL', button_text='Reboot Bootloader')],
           [sg.Button(key='btnADB_ROOT', button_text='Root'),
            sg.Button(key='btnADB_UNROOT', button_text='Unroot'),
            sg.Button(key='btnADB_REMOUNT', button_text='Remount'),
            sg.Button(key='btnDISABLE_VERITY', button_text='Disable-verity')],
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
           [sg.Checkbox(key='chkboxDevice', text='None', disabled=True)]
         ]

layoutTabFilePush = [ [sg.Text("Source:", size=(6,1)), sg.Input(key='inputPushFileSource'), sg.FileBrowse()],
                      [sg.Text("Target:", size=(6,1)), sg.Input(key='inputPushTarget', default_text='/sdcard/')],
                      [sg.Button(size=(10,1), key='btnPushFile', button_text='Push File')]
                    ]

layoutConfig = [ [sg.Checkbox(key='chkboxAlwaysOnTop', text='Always on Top', default=True, enable_events=True)],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Executable path:")],
                 [sg.Text("ADB:", size=(8,1)), sg.Input(key='inputAdbPath'), sg.FileBrowse()],
                 [sg.Text("Fastboot:", size=(8,1)), sg.Input(key='inputFastbootPath'), sg.FileBrowse()],
                 [sg.Button(key='btnExecSave', button_text='Check and Save')],
                 [sg.Text(key='statusCheckExec', expand_x=True, expand_y=True)]
               ]

tabgroupMain = [ [sg.TabGroup([[sg.Tab('Main', layout),
                                sg.Tab('File Push', layoutTabFilePush),
                                sg.Tab('Configuration', layoutConfig)]])],
                 [sg.Text("Status:"), sg.Text(key='statusText')]
               ]

# Create the window
window = sg.Window('Android Control Bar', tabgroupMain, keep_on_top = True, finalize=True)

# Create configuration handler
config = configparser.ConfigParser()
config.read('local_config.ini')
if 'host_settings' in config:
    if 'always_on_top' in config['host_settings']:
        if config['host_settings']['always_on_top'] == 'true':
            window.keep_on_top_set()
            window['chkboxAlwaysOnTop'].update(True)
        else:
            window.keep_on_top_clear()
            window['chkboxAlwaysOnTop'].update(False)

    if 'ADB' in config['host_settings']:
        tmpAdbPath = config['host_settings']['ADB']
        if tmpAdbPath[-7:].casefold() == "adb.exe":
            #window['statusCheckExec'].update(window['statusCheckExec'].get() + '\nUse user input ADB Path\n')
            if verifyAdbPath(tmpAdbPath) == True:
                mExecAdbPath = tmpAdbPath
                mExecAdbPathVerified = True
                window['inputAdbPath'].update(mExecAdbPath)

    if 'Fastboot' in config['host_settings']:
        tmpFastbootPath = config['host_settings']['Fastboot']
        if tmpFastbootPath[-12:].casefold() == "fastboot.exe":
            #window['statusCheckExec'].update(window['statusCheckExec'].get() + '\nUse user input Fastboot Path\n')
            if verifyFastbootPath(tmpFastbootPath) == True:
                mExecFastbootPath = tmpFastbootPath
                mExecFastbootPathVerified = True
                window['inputFastbootPath'].update(mExecFastbootPath)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    #
    # Tab: Main
    #
    ## Key codes
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
    ## ADB commands
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
    ## Check devices
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
    # 
    # Tab: Push file to device
    #
    elif event == 'btnPushFile':
        adbCmd(10, "push \"" + window['inputPushFileSource'].get() + "\" \"" + window['inputPushTarget'].get() + "\"")
    #
    # Tab: Settings
    #
    elif event == 'chkboxAlwaysOnTop':
        if 'host_settings' not in config:
            config['host_settings'] = {}
        if window['chkboxAlwaysOnTop'].get() == True:
            window.keep_on_top_set()
            config['host_settings']['always_on_top'] = 'true'
        else:
            window.keep_on_top_clear()
            config['host_settings']['always_on_top'] = 'false'
        with open('local_config.ini', 'w') as configfile:
            config.write(configfile)
    elif event == 'btnExecSave':
        checkExecutable()

# Finish up by removing from the screen
window.close()
