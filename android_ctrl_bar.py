#
# Android control bar
#

import configparser
import importlib
import os
import threading
import PySimpleGUI as sg
from platform import version as platform_version
from platform import python_version as platform_python_version

from version import __version__
import acp_cmd
import acp_tab_main
import acp_tab_config
import acp_tab_custom_buttons
import acp_tab_file_app

#
# Feature flags
#
ENABLE_FEATURE_CUSTOM_BUTTONS =     True
ENABLE_FEATURE_FILE_APP =           True

#
# Define the window's contents
#
layoutTabs = [[sg.Tab(acp_tab_main.getLayoutName(), acp_tab_main.getLayout(), expand_x=True)]]

if ENABLE_FEATURE_CUSTOM_BUTTONS == True:
    layoutTabs += [[sg.Tab(acp_tab_custom_buttons.getLayoutName(), acp_tab_custom_buttons.getLayout())]]

if ENABLE_FEATURE_FILE_APP == True:
    layoutTabs += [[sg.Tab(acp_tab_file_app.getLayoutName(), acp_tab_file_app.getLayout())]]

layoutTabs += [[sg.Tab(acp_tab_config.getLayoutName(), acp_tab_config.getLayout())]]

tabgroupMain = [
    [sg.TabGroup(layoutTabs, tab_location='topleft')],
    [sg.Button(key='btnDown_ADB_ROOT', button_text='⚙ Root'),
     sg.Button(key='btnDown_AdbKeycode_POWER', button_text='⏯ Power'),
     sg.Button(key='btnDown_AdbKeycode_SLEEP', button_text='⏸ Suspend'),
     sg.Button(key='btnDown_AdbKeycode_WAKEUP', button_text='▶ Resume'),
     sg.Button(key='btnDown_ADB_REBOOT', button_text='♻ Reboot'),
     sg.Button(key='btnDown_ADB_REBOOT_P', button_text='❌ Shutdown')],
    [sg.Text("Status:"), sg.Text(key='statusText')]
]

#
# Main start
#

# Create the window
window = sg.Window('Android Control Panel', tabgroupMain, keep_on_top = True, finalize=True)
# Get OS version
# platform_version().split('.')[2]
window['textHostVersion'].update('Windows ' + platform_version() + ', Python ' + platform_python_version())

# Create configuration handler
config = configparser.ConfigParser()

# Init command module
acp_cmd.setWindow(window)

# Init config
acp_tab_config.loadConfig(window, config)

# load custom button text to layout
if ENABLE_FEATURE_CUSTOM_BUTTONS == True:
    acp_tab_custom_buttons.loadCustButton(window, config)

# Splash screen handle (for pyinstaller)
if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()

#
# Main loop: display and interact with the Window using an Event Loop
#
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    #
    # Always bottom buttons
    #
    elif event == 'btnDown_ADB_ROOT':
        tAdbRoot = threading.Thread(target=acp_cmd.adbRootCheck, args=(window))
        tAdbRoot.start()
    elif event == 'btnDown_AdbKeycode_POWER':
        acp_cmd.adbCmd(5, "shell input keyevent POWER")
    elif event == 'btnDown_AdbKeycode_SLEEP':
        acp_cmd.adbCmd(5, "shell input keyevent SLEEP")
    elif event == 'btnDown_AdbKeycode_WAKEUP':
        acp_cmd.adbCmd(5, "shell input keyevent WAKEUP")
    elif event == 'btnDown_ADB_REBOOT':
        acp_cmd.adbCmd(10, "reboot")
    elif event == 'btnDown_ADB_REBOOT_P':
        acp_cmd.adbCmd(10, "shell reboot -p")

    #
    # Tab: Main
    #
    elif acp_tab_main.processEvent(window, event) == True:
        pass

    #
    # Tab: Configurations
    #
    elif acp_tab_config.processEvent(window, event, config) == True:
        pass

    #
    # Tab: Push file to device, install apps
    #
    elif ENABLE_FEATURE_FILE_APP == True and acp_tab_file_app.processEvent(window, event, values) == True:
        pass

    #
    # Tab: Custom Buttons
    #
    elif ENABLE_FEATURE_CUSTOM_BUTTONS == True and acp_tab_custom_buttons.processEvent(window, event, values, config) == True:
        pass

    else:
        window['statusText'].update('Unhandled event: ' + event)

# Finish up by removing from the screen
window.close()
