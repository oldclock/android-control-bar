#
# Android control bar
#

import configparser
import os
import re
import subprocess
import threading
from datetime import datetime
import PySimpleGUI as sg

from version import __version__

EXEC_ADB_DEFAULT = str('adb.exe')
mExecAdbPath = EXEC_ADB_DEFAULT
mExecAdbPathVerified = bool(False)
EXEC_FASTBOOT_DEFAULT = str('fastboot.exe')
mExecFastbootPath = EXEC_FASTBOOT_DEFAULT
mExecFastbootPathVerified = bool(False)

# Functions
def cmdExec(timeout_sec: int, cmd: str) -> bytes:
    rc = True
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        stdoutdata = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout_sec, startupinfo=startupinfo)
    except subprocess.TimeoutExpired:
        #print("Command TIMEOUT !!!")
        window['statusText'].update(window['statusText'].get() + ' Timeout !')
        rc = False
        bytesRcError = bytes('command timeout', 'latin1')
    except subprocess.CalledProcessError as e:
        #print(e.output)
        window['statusText'].update(window['statusText'].get() + ' Error !')
        rc = False
        bytesRcError = e.output
    if rc == True:
        window['statusText'].update(window['statusText'].get() + ' Done')
        return stdoutdata
    else:
        return bytesRcError

def adbCmd(timeout_sec: int, command: str, blocking=False, donotprintcmd=False) -> bool:
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

    if donotprintcmd == True:
        window['statusText'].update('Processing adb command ...')
    else:
        window['statusText'].update('Processing command: adb ' + command)

    if blocking == True:
        cmdExec(timeout_sec, mExecAdbPath + " " + command)
    else:
        tCmd = threading.Thread(target=cmdExec, args=(timeout_sec, mExecAdbPath + " " + command))
        tCmd.start()
    return rc

def fastbootCmd(timeout_sec: int, command: str, blocking=False, donotprintcmd=False) -> bool:
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

    if donotprintcmd == True:
        window['statusText'].update('Processing fastboot command ... ')
    else:
        window['statusText'].update('Processing command: fastboot ' + command)

    if blocking == True:
        cmdExec(timeout_sec, mExecFastbootPath + " " + command)
    else:
        tCmd = threading.Thread(target=cmdExec, args=(timeout_sec, mExecFastbootPath + " " + command))
        tCmd.start()
    return rc

def installApk(source: str) -> bool:
    if source[-4:].casefold() == ".apk":
        rc = adbCmd(20, "install -r -g " + source)
    else:
        window['statusText'].update('Invalid APK source path')
        rc = False
    return rc

def verifyAdbPath(path: str) -> bool:
    rc = False
    window['statusText'].update('Processing command: adb --version')
    adbVersion = cmdExec(10, path + " --version").decode('latin1')
    if adbVersion[:20] == "Android Debug Bridge":
        rc = True
        window['statusCheckExec'].update(adbVersion + '\n', append=True)
    return rc

def verifyFastbootPath(path: str) -> bool:
    rc = False
    window['statusText'].update('Processing command: fastboot --version')
    fastbootVersion = cmdExec(10, path + " --version").decode('latin1')
    if fastbootVersion[:8] == "fastboot":
        rc = True
        window['statusCheckExec'].update(fastbootVersion + '\n', append=True)
    return rc

def checkExecutable() -> bool:
    rc = True
    global config, mExecAdbPath, mExecAdbPathVerified, mExecFastbootPath, mExecFastbootPathVerified
    window['statusCheckExec'].update('')

    tmpAdbPath = window['inputAdbPath'].get()
    if tmpAdbPath[-7:].casefold() == "adb.exe":
        window['statusCheckExec'].update('Use user input ADB Path\n', append=True)
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
        window['statusCheckExec'].update('Use system ADB Path\n', append=True)
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
        window['statusCheckExec'].update('Use user input Fastboot Path\n', append=True)
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
        window['statusCheckExec'].update('Use system Fastboot Path\n', append=True)
        mExecFastbootPath = EXEC_FASTBOOT_DEFAULT
        if 'host_settings' in config:
            if 'Fastboot' in config['host_settings']:
                config['host_settings']['Fastboot'] = EXEC_FASTBOOT_DEFAULT
                with open('local_config.ini', 'w') as configfile:
                    config.write(configfile)
        if verifyFastbootPath(mExecFastbootPath) == True:
            mExecFastbootPathVerified = True

    return rc

def loadConfig():
    global config, mExecAdbPath, mExecAdbPathVerified, mExecFastbootPath, mExecFastbootPathVerified
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
                window['statusCheckExec'].update('Use user input ADB Path\n', append=True)
                if verifyAdbPath(tmpAdbPath) == True:
                    mExecAdbPath = tmpAdbPath
                    mExecAdbPathVerified = True
                    window['inputAdbPath'].update(mExecAdbPath)

        if 'Fastboot' in config['host_settings']:
            tmpFastbootPath = config['host_settings']['Fastboot']
            if tmpFastbootPath[-12:].casefold() == "fastboot.exe":
                window['statusCheckExec'].update('Use user input Fastboot Path\n', append=True)
                if verifyFastbootPath(tmpFastbootPath) == True:
                    mExecFastbootPath = tmpFastbootPath
                    mExecFastbootPathVerified = True
                    window['inputFastbootPath'].update(mExecFastbootPath)

def loadCustButton():
    if 'custom_button' in config:
        for i in [1, 2, 3, 4]:
            for j in [1, 2, 3, 4]:
                currentBtnName = 'btnCust_'+ str(i) + '_' + str(j)
                if currentBtnName in config['custom_button'] and config['custom_button'][currentBtnName] == 'true':
                    window[currentBtnName].update(text=(config['custom_button'][currentBtnName + '_text']))

def execCustButton(btnName: str):
    if 'custom_button' in config:
        if btnName in config['custom_button'] and config['custom_button'][btnName] == 'true':
            if btnName+'_type' in config['custom_button']:
                if config['custom_button'][btnName+'_type'] == 'adb':
                    if btnName+'_cmd' in config['custom_button']:
                        window['statusCustBtn'].update('')
                        window['statusText'].update('Processing command ...')
                        outputExec = cmdExec(20, "adb " + config['custom_button'][btnName+'_cmd']).decode('latin1')
                        window['statusCustBtn'].update(outputExec + '\n', append=True)
                    else:
                        window['statusText'].update('No command defined for this button')
                elif config['custom_button'][btnName+'_type'] == 'fastboot':
                    if btnName+'_cmd' in config['custom_button']:
                        window['statusCustBtn'].update('')
                        window['statusText'].update('Processing command ...')
                        outputExec = cmdExec(20, "fastboot " + config['custom_button'][btnName+'_cmd']).decode('latin1')
                        window['statusCustBtn'].update(outputExec + '\n', append=True)
                    else:
                        window['statusText'].update('No command defined for this button')
                else:
                    window['statusText'].update('Invalid command type')
            else:
                window['statusText'].update('No type defined for this button')
        else:
            window['statusText'].update('Button not enabled')
    else:
        window['statusText'].update('No custom button setting')

def getScreenShot() -> bool:
    now = datetime.now()
    screencap_file = "screenshot_" + now.strftime("%Y%m%d_%H%M%S") + ".png"
    fp = open(screencap_file, "a+")
    try:
        subprocess.check_call('adb exec-out screencap -p', stdout=fp, timeout=20)
    except subprocess.TimeoutExpired:
        window['statusText'].update('Screenshot Timeout !')
    fp.close()
    return True

# Define the window's contents
layout = [ [sg.Text("ADB commands:")],
           [sg.Button(key='btnSLEEP', button_text='Suspend'),
            sg.Button(key='btnWAKEUP', button_text='Resume'),
            sg.Button(key='btnREBOOT', button_text='Reboot'),
            sg.Button(key='btnREBOOT_BL', button_text='Reboot Bootloader')],
           [sg.Button(key='btnADB_ROOT', button_text='Root'),
            sg.Button(key='btnADB_UNROOT', button_text='Unroot'),
            sg.Button(key='btnADB_REMOUNT', button_text='Remount'),
            sg.Button(key='btnDISABLE_VERITY', button_text='Disable-verity'),
            sg.Button(key='btnScreenShot', button_text='Screenshot')],
           [sg.HorizontalSeparator()],
           [sg.Text("Fastboot commands:")],
           [sg.Button(key='btnFB_REBOOT', button_text='Reboot'),
            sg.Button(key='btnFB_REBOOT_BL', button_text='Reboot Bootloader')],
           [sg.HorizontalSeparator()],
           [sg.Text("Key codes:")],
           [sg.Button(size=(5,1), key='btnBACK', button_text='◀'),
            sg.Button(size=(5,1), key='btnHOME', button_text='●'),
            sg.Button(size=(5,1), key='btnAPP_SWITCH', button_text='◼'),
            sg.Button(size=(5,1), key='btnVOLUME_MUTE', button_text='♪×')],
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

layoutCustBtn = [ [sg.Button(size=(12,2), key='btnCust_1_1', button_text='Button 1-1'),
                   sg.Button(size=(12,2), key='btnCust_1_2', button_text='Button 1-2'),
                   sg.Button(size=(12,2), key='btnCust_1_3', button_text='Button 1-3'),
                   sg.Button(size=(12,2), key='btnCust_1_4', button_text='Button 1-4')],
                  [sg.Button(size=(12,2), key='btnCust_2_1', button_text='Button 2-1'),
                   sg.Button(size=(12,2), key='btnCust_2_2', button_text='Button 2-2'),
                   sg.Button(size=(12,2), key='btnCust_2_3', button_text='Button 2-3'),
                   sg.Button(size=(12,2), key='btnCust_2_4', button_text='Button 2-4')],
                  [sg.Button(size=(12,2), key='btnCust_3_1', button_text='Button 3-1'),
                   sg.Button(size=(12,2), key='btnCust_3_2', button_text='Button 3-2'),
                   sg.Button(size=(12,2), key='btnCust_3_3', button_text='Button 3-3'),
                   sg.Button(size=(12,2), key='btnCust_3_4', button_text='Button 3-4')],
                  [sg.Button(size=(12,2), key='btnCust_4_1', button_text='Button 4-1'),
                   sg.Button(size=(12,2), key='btnCust_4_2', button_text='Button 4-2'),
                   sg.Button(size=(12,2), key='btnCust_4_3', button_text='Button 4-3'),
                   sg.Button(size=(12,2), key='btnCust_4_4', button_text='Button 4-4')],
                  [sg.Multiline(key='statusCustBtn', size=(64, 9))],
                ]

layoutTabFilePush = [ [sg.Text("Source:", size=(8,1)), sg.Input(key='inputPushFileSource'), sg.FileBrowse()],
                      [sg.Text("Target:", size=(8,1)), sg.Input(key='inputPushTarget', default_text='/sdcard/')],
                      [sg.Button(size=(10,1), key='btnPushFile', button_text='Push File')],
                      [sg.HorizontalSeparator()],
                      [sg.Text("APK:", size=(8,1)), sg.Input(key='inputApkSource'), sg.FileBrowse()],
                      [sg.Button(size=(10,1), key='btnInstallApk', button_text='Install')]
                    ]

layoutConfig = [ [sg.Checkbox(key='chkboxAlwaysOnTop', text='Always on Top', default=True, enable_events=True)],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Executable path:")],
                 [sg.Text("ADB:", size=(8,1)), sg.Input(key='inputAdbPath'), sg.FileBrowse()],
                 [sg.Text("Fastboot:", size=(8,1)), sg.Input(key='inputFastbootPath'), sg.FileBrowse()],
                 [sg.Button(key='btnExecSave', button_text='Check and Save')],
                 [sg.Multiline(key='statusCheckExec', size=(64, 10))],
                 [sg.Text("Version: " + __version__)]
               ]

layoutImages = [
    [sg.Text("Folder:", size=(8,1)), sg.Input(key='inputImageFolderPath'), sg.FolderBrowse()],
    [sg.Button(key='btnShowImage', button_text='Show images')],
    [sg.HorizontalSeparator()],
    [sg.Image(size=(120, 60), key='imageT1', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT2', visible=False, enable_events=True),
     sg.Image(size=(120, 60), key='imageT3', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT4', visible=False, enable_events=True)],
    [sg.Image(size=(120, 60), key='imageT5', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT6', visible=False, enable_events=True),
     sg.Image(size=(120, 60), key='imageT7', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT8', visible=False, enable_events=True)],
    [sg.Image(size=(120, 60), key='imageT9', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT10', visible=False, enable_events=True),
     sg.Image(size=(120, 60), key='imageT11', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT12', visible=False, enable_events=True)],
    [sg.Image(size=(120, 60), key='imageT13', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT14', visible=False, enable_events=True),
     sg.Image(size=(120, 60), key='imageT15', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT16', visible=False, enable_events=True)],
    [sg.Image(size=(120, 60), key='imageT17', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT18', visible=False, enable_events=True),
     sg.Image(size=(120, 60), key='imageT19', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT20', visible=False, enable_events=True)],
    [sg.Image(size=(120, 60), key='imageT21', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT22', visible=False, enable_events=True),
     sg.Image(size=(120, 60), key='imageT23', visible=False, enable_events=True), sg.Image(size=(120, 60), key='imageT24', visible=False, enable_events=True)],
]

tabgroupMain = [ [sg.TabGroup([[sg.Tab('Main', layout),
                                sg.Tab('Custom Button', layoutCustBtn),
                                sg.Tab('Show Images', layoutImages),
                                sg.Tab('Push File/APK', layoutTabFilePush),
                                sg.Tab('Configuration', layoutConfig)]])],
                 [sg.Text("Status:"), sg.Text(key='statusText')]
               ]

# Create the window
window = sg.Window('Android Control Bar', tabgroupMain, keep_on_top = True, finalize=True)

# Create configuration handler
config = configparser.ConfigParser()
loadConfig()

# load custom button text to layout
loadCustButton()

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
    elif event == 'btnVOLUME_MUTE':
        adbCmd(5, "shell input keyevent VOLUME_MUTE")
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
    elif event == 'btnScreenShot':
        getScreenShot()
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
        for line in stdoutdata.splitlines():
            if line[0] == '*':
                pass
            elif line == 'List of devices attached':
                pass
            else:
                strSerial, strDevStatus = line.split(maxsplit=1)
                if strDevStatus == 'device':
                    window['chkboxDevice'].update(text=strSerial, disabled=False)
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
    #
    # Tab: Push file to device
    #
    elif event == 'btnPushFile':
        adbCmd(10, "push \"" + window['inputPushFileSource'].get() + "\" \"" + window['inputPushTarget'].get() + "\"")
    elif event == 'btnInstallApk':
        installApk(window['inputApkSource'].get())
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
    #
    # Tab: Show image
    #
    elif event == 'btnShowImage':
        folderName = values['inputImageFolderPath'] or '.'
        print(folderName)
        window['statusText'].update('Loading images ... ')
        i = 1
        for file in os.listdir(folderName):
            if i > 24:
                break
            if file.endswith(".png") or file.endswith(".jpg"):
                fileFullPath = os.path.join(folderName, file)
                window['imageT' + str(i)].update(source=fileFullPath, subsample=40, visible=True)
                print(fileFullPath)
                i = i + 1
        window['statusText'].update('Loading images ... Done')

    #TODO: get path and name from image element
    # elif re.match('imageT[0-9][0-9]', event):
    #     imagePath = window[event].Source
    #     print(str(imagePath))
    #     imageFolder = os.path.dirname(str(imagePath))
    #     imageFilename = os.path.basename(str(imagePath))
    #     print(imageFolder + ' XXX ' + imageFilename)

    #
    # Custom Buttons
    #
    elif re.match('btnCust_[1-4]_[1-4]', event):
        execCustButton(event)

    else:
        window['statusText'].update('Unhandled event: ' + event)

# Finish up by removing from the screen
window.close()
