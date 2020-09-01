# Graphical User Interface for the SDF

A graphical interface to look at the content of a **spcht descriptor file**. Further it provides some basic functionality to test and verify the workings of a created sdf.

**Allows no editing at the moment**

The Interface is build with QT5/PySide2 and runs under Windows/Linux/Mac. I provide simple executables for Windows and Linux. Those are *compiled* with PyInstaller and might have some performance loss, startup for the single files might also be slowed down due the packed nature of the executables.

![main_menu](./README/main_menu.png)

Also works under windows.

![spchtgui_windows](./README/spchtgui_windows.png)

## Installation

1. Satisfy all python requirements from *requirements.txt* `python3 -m pip install -r requirements.txt`
2. Copy the newest Version of the Spcht Descriptor Format Class File into the root of this project, it should reside [here](https://github.com/jpkanter/tiny-efre-lod-tools/blob/Imperator/SpchtDescriptorFormat.py)
3. Run main.py `python3 main.py`

## Requirements

* Python >= 3.5 (earlier Versions might work but not tested)

(Spcht Requirements)

* pymarc >= 4.0.0
* rdflib >= 5.0.0

(GUI)

* PySide2 >= 5.12
* python-dateutils (technically only for one stupid display thing)

