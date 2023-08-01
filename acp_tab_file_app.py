import PySimpleGUI as sg
import acp_cmd

def getLayoutName() -> str:
    return 'File/App'

def getLayout() -> list:
    layout = [
        [sg.Text("Push file to device", font='Arial 11 bold')],
        [sg.Text("Source:", size=(8,1)), sg.Input(key='inputPushFileSource'), sg.FileBrowse()],
        [sg.Text("Target:", size=(8,1)), sg.Input(key='inputPushTarget', default_text='/sdcard/'),
         sg.Button(size=(10,1), key='btnPushFile', button_text='Push File')],
        [sg.HorizontalSeparator()],
        [sg.Text("Install APK", font='Arial 11 bold')],
        [sg.Text("APK:", size=(8,1)), sg.Input(key='inputApkSource'), sg.FileBrowse(),
         sg.Button(size=(10,1), key='btnInstallApk', button_text='Install')]
    ]
    return layout

def installApk(window, source: str) -> bool:
    if source[-4:].casefold() == ".apk":
        rc = acp_cmd.adbCmd(20, "install -r -g " + source)
    else:
        window['statusText'].update('Invalid APK source path')
        rc = False
    return rc

def processEvent(window, event, values) -> bool:
    rc = False

    if event == 'btnPushFile':
        acp_cmd.adbCmd(10, "push \"" + window['inputPushFileSource'].get() + "\" \"" + window['inputPushTarget'].get() + "\"")
        rc = True
    elif event == 'btnInstallApk':
        installApk(window, window['inputApkSource'].get())
        rc = True

    return rc
