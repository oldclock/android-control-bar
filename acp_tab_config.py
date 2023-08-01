import PySimpleGUI as sg
import acp_cmd
from version import __version__

def getLayoutName() -> str:
    return 'Configurations'

def getLayout() -> list:
    layout = [
        [sg.Checkbox(key='chkboxAlwaysOnTop', text='Always on Top', default=True, enable_events=True)],
        [sg.HorizontalSeparator()],
        [sg.Text("Android Platform-tools Path", font='Arial 11 bold')],
        [sg.Text("ADB:", size=(8,1)), sg.Input(key='inputAdbPath', size=64), sg.FileBrowse()],
        [sg.Text("Fastboot:", size=(8,1)), sg.Input(key='inputFastbootPath', size=64), sg.FileBrowse()],
        [sg.Button(key='btnExecSave', button_text='Check and Save')],
        [sg.Multiline(key='statusCheckExec', size=(82, 10), horizontal_scroll=True)],
        [sg.Text("Version: " + __version__)],
        [sg.Text(text='', key='textHostVersion')]
    ]
    return layout

def checkExecutable(window, config) -> bool:
    rc = True
    window['statusCheckExec'].update('')

    tmpAdbPath = window['inputAdbPath'].get()
    if tmpAdbPath[-7:].casefold() == "adb.exe":
        window['statusCheckExec'].update('Use user input ADB Path\n', append=True)
        if acp_cmd.verifyAdbPath(tmpAdbPath) == True:
            acp_cmd.setAdbPath(tmpAdbPath)
            acp_cmd.setAdbPathVerified(True)
            if 'host_settings' not in config:
                config['host_settings'] = {}
            config['host_settings']['ADB'] = acp_cmd.getAdbPath()
            with open('local_config.ini', 'w') as configfile:
                config.write(configfile)
    else:
        window['inputAdbPath'].update('')
        window['statusCheckExec'].update('Use system ADB Path\n', append=True)
        acp_cmd.setAdbPath(acp_cmd.getAdbPathDefault())
        if 'host_settings' in config:
            if 'ADB' in config['host_settings']:
                config['host_settings']['ADB'] = acp_cmd.getAdbPathDefault()
                with open('local_config.ini', 'w') as configfile:
                    config.write(configfile)
        if acp_cmd.verifyAdbPath(acp_cmd.getAdbPath()) == True:
            acp_cmd.setAdbPathVerified(True)

    tmpFastbootPath = window['inputFastbootPath'].get()
    if tmpFastbootPath[-12:].casefold() == "fastboot.exe":
        window['statusCheckExec'].update('Use user input Fastboot Path\n', append=True)
        if acp_cmd.verifyFastbootPath(tmpFastbootPath) == True:
            acp_cmd.setFastbootPath(tmpFastbootPath)
            acp_cmd.setFastbootPathVerified(True)
            if 'host_settings' not in config:
                config['host_settings'] = {}
            config['host_settings']['Fastboot'] = acp_cmd.getFastbootPath()
            with open('local_config.ini', 'w') as configfile:
                config.write(configfile)
    else:
        window['inputFastbootPath'].update('')
        window['statusCheckExec'].update('Use system Fastboot Path\n', append=True)
        acp_cmd.setFastbootPath(acp_cmd.getFastbootPathDefault())
        if 'host_settings' in config:
            if 'Fastboot' in config['host_settings']:
                config['host_settings']['Fastboot'] = acp_cmd.getFastbootPathDefault()
                with open('local_config.ini', 'w') as configfile:
                    config.write(configfile)
        if acp_cmd.verifyFastbootPath(acp_cmd.getFastbootPath()) == True:
            acp_cmd.setFastbootPathVerified(True)

    return rc

def loadConfig(window, config):
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
                if acp_cmd.verifyAdbPath(tmpAdbPath) == True:
                    acp_cmd.setAdbPath(tmpAdbPath)
                    acp_cmd.setAdbPathVerified(True)
                    window['inputAdbPath'].update(acp_cmd.getAdbPath())

        if 'Fastboot' in config['host_settings']:
            tmpFastbootPath = config['host_settings']['Fastboot']
            if tmpFastbootPath[-12:].casefold() == "fastboot.exe":
                window['statusCheckExec'].update('Use user input Fastboot Path\n', append=True)
                if acp_cmd.verifyFastbootPath(tmpFastbootPath) == True:
                    acp_cmd.setFastbootPath(tmpFastbootPath)
                    acp_cmd.setFastbootPathVerified(True)
                    window['inputFastbootPath'].update(acp_cmd.getFastbootPath())

def processEvent(window, event, config) -> bool:
    rc = False

    if event == 'chkboxAlwaysOnTop':
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
        rc = True
    elif event == 'btnExecSave':
        checkExecutable(window, config)
        rc = True

    return rc
