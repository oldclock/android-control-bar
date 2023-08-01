import re
import PySimpleGUI as sg
import acp_cmd

# Custom button
CUST_BUTTON_ROW_MAX = 4
CUST_BUTTON_COL_MAX = 5

def getLayoutName() -> str:
    return 'Custom Buttons'

def getLayout() -> list:
    layout = [
        [sg.Button(size=(13,2), disabled=True, key='btnCust_' + str(btncust_row) + '_' + str(btncust_col), button_text='Button ' + str(btncust_row) + '-' + str(btncust_col))
            for btncust_col in range(1, CUST_BUTTON_COL_MAX + 1)]
            for btncust_row in range(1, CUST_BUTTON_ROW_MAX + 1)
    ]
    layout += [
        [sg.Multiline(key='statusCustBtn', size=(65, 11), horizontal_scroll=True, font='Consolas')]
    ]
    return layout

def loadCustButton(window, config):
    if 'custom_button' in config:
        for btncust_row in range(1, CUST_BUTTON_ROW_MAX + 1):
            for btncust_col in range(1, CUST_BUTTON_COL_MAX + 1):
                currentBtnName = 'btnCust_'+ str(btncust_row) + '_' + str(btncust_col)
                if currentBtnName in config['custom_button'] and config['custom_button'][currentBtnName] == 'true':
                    window[currentBtnName].update(text=(config['custom_button'][currentBtnName + '_text']), disabled=False)

def execCustButton(window, config, btnName: str):
    if 'custom_button' in config:
        if btnName in config['custom_button'] and config['custom_button'][btnName] == 'true':
            if btnName+'_type' in config['custom_button']:
                if config['custom_button'][btnName+'_type'] == 'adb':
                    if btnName+'_cmd' in config['custom_button']:
                        window['statusCustBtn'].update('')
                        window['statusText'].update('Processing command ...')
                        outputExec = acp_cmd.adbCmdExec(20, config['custom_button'][btnName+'_cmd']).decode('latin1')
                        window['statusCustBtn'].update(outputExec + '\n', append=True)
                    else:
                        window['statusText'].update('No command defined for this button')
                elif config['custom_button'][btnName+'_type'] == 'fastboot':
                    if btnName+'_cmd' in config['custom_button']:
                        window['statusCustBtn'].update('')
                        window['statusText'].update('Processing command ...')
                        outputExec = acp_cmd.fastbootCmdExec(20, config['custom_button'][btnName+'_cmd']).decode('latin1')
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

def processEvent(window, event, values, config) -> bool:
    rc = False

    if re.match('btnCust_[1-' + str(CUST_BUTTON_ROW_MAX) + ']_[1-' + str(CUST_BUTTON_COL_MAX) + ']', event):
        execCustButton(window, config, event)
        rc = True

    return rc
