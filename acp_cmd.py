import subprocess
import threading
import PySimpleGUI as sg

EXEC_ADB_DEFAULT = str('adb.exe')
mExecAdbPath = EXEC_ADB_DEFAULT
mExecAdbPathVerified = bool(False)
EXEC_FASTBOOT_DEFAULT = str('fastboot.exe')
mExecFastbootPath = EXEC_FASTBOOT_DEFAULT
mExecFastbootPathVerified = bool(False)
mWindow = sg.Window('EmptyWindow')

def setWindow(window):
    global mWindow
    mWindow = window

def getAdbPathDefault() -> str:
    return EXEC_ADB_DEFAULT

def setAdbPath(path: str):
    global mExecAdbPath
    mExecAdbPath = path

def getAdbPath() -> str:
    global mExecAdbPath
    return mExecAdbPath

def setAdbPathVerified(verified: bool):
    global mExecAdbPathVerified
    mExecAdbPathVerified = verified

def getFastbootPathDefault() -> str:
    return EXEC_FASTBOOT_DEFAULT

def setFastbootPath(path: str):
    global mExecFastbootPath
    mExecFastbootPath = path

def getFastbootPath() -> str:
    global mExecFastbootPath
    return mExecFastbootPath

def setFastbootPathVerified(verified: bool):
    global mExecFastbootPathVerified
    mExecFastbootPathVerified = verified

def verifyAdbPath(path: str) -> bool:
    rc = False
    mWindow['statusText'].update('Processing command: adb --version')
    adbVersion = cmdExec(10, path + " --version").decode('latin1')
    if adbVersion[:20] == "Android Debug Bridge":
        rc = True
        mWindow['statusCheckExec'].update(adbVersion + '\n', append=True)
    return rc

def verifyFastbootPath(path: str) -> bool:
    rc = False
    mWindow['statusText'].update('Processing command: fastboot --version')
    fastbootVersion = cmdExec(10, path + " --version").decode('latin1')
    if fastbootVersion[:8] == "fastboot":
        rc = True
        mWindow['statusCheckExec'].update(fastbootVersion + '\n', append=True)
    return rc

def cmdExec(timeout_sec: int, cmd: str) -> bytes:
    rc = True
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        stdoutdata = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout_sec, startupinfo=startupinfo)
    except subprocess.TimeoutExpired:
        #print("Command TIMEOUT !!!")
        mWindow['statusText'].update(mWindow['statusText'].get() + ' Timeout !')
        rc = False
        bytesRcError = bytes('command timeout', 'latin1')
    except subprocess.CalledProcessError as e:
        #print(e.output)
        mWindow['statusText'].update(mWindow['statusText'].get() + ' Error !')
        rc = False
        bytesRcError = e.output
    if rc == True:
        mWindow['statusText'].update(mWindow['statusText'].get() + ' Done')
        return stdoutdata
    else:
        return bytesRcError

def adbCmdExec(timeout_sec: int, cmd: str) -> bytes:
    global mExecAdbPath
    return cmdExec(timeout_sec, mExecAdbPath + " " + cmd)

def fastbootCmdExec(timeout_sec: int, cmd: str) -> bytes:
    global mExecFastbootPath
    return cmdExec(timeout_sec, mExecFastbootPath + " " + cmd)

def adbCmd(timeout_sec: int, command: str, blocking=False, donotprintcmd=False) -> bool:
    global mExecAdbPath, mExecAdbPathVerified
    rc = True
    if timeout_sec < 1:
        print("Arg timeout_sec must >= 1")
        return False
    if mExecAdbPathVerified == False:
        mWindow['statusText'].update('ADB path not verified')
        if verifyAdbPath(mExecAdbPath) == True:
            mExecAdbPathVerified = True
        else:
            return False

    if donotprintcmd == True:
        mWindow['statusText'].update('Processing adb command ...')
    else:
        mWindow['statusText'].update('Processing command: adb ' + command)

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
        mWindow['statusText'].update('Fastboot path not verified')
        if verifyFastbootPath(mExecFastbootPath) == True:
            mExecFastbootPathVerified = True
        else:
            return False

    if donotprintcmd == True:
        mWindow['statusText'].update('Processing fastboot command ... ')
    else:
        mWindow['statusText'].update('Processing command: fastboot ' + command)

    if blocking == True:
        cmdExec(timeout_sec, mExecFastbootPath + " " + command)
    else:
        tCmd = threading.Thread(target=cmdExec, args=(timeout_sec, mExecFastbootPath + " " + command))
        tCmd.start()
    return rc

def adbRootCheck(window):
    window['statusText'].update('Processing adb root ...')
    outputExec = adbCmdExec(20, "root").decode('latin1')
    window['statusText'].update('Root result: ' + outputExec.splitlines()[0])
