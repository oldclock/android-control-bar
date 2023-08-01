# Android control bar

A Python GUI (PySimpleGUI) to control Android devices via ADB/Fastboot interface

![Main UI](https://github.com/oldclock/android-control-bar/blob/main/image/for_readme/main_ui.png)

## Dependency

- Python 3
- Packages
  - <code>pip install pysimplegui</code>
- Optional packages
  - <code>pip install psgcompiler</code> (to create standalone EXE file)

## Run (on Windows)

<code>
python android_ctrl_bar.py
</code>

## Create standalone EXE file

<code>
pyinstaller --onefile --windowed --name=android_ctrl_panel --hidden-import=pyi_splash --splash image/splash.png --workpath . --distpath . --specpath . android_ctrl_bar.py
</code>

## TODO

- [x] Local settings file
- [x] Specify ADB/Fastboot path
- [x] Response for adb root success or not
- [ ] ADB/Fastboot command queue
- [x] Separate tabs to different files
- [ ] Multiple device support
- [ ] Monitor device plug/unplug status
- [ ] Drag and drop to push file to device
- [ ] Repeated command
- [ ] Device file browser
