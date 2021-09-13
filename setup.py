#!/usr/bin/env python3

# setup.py

# Docs: https://www.geeksforgeeks.org/using-cx_freeze-python/

from cx_Freeze import setup, Executable

includes = []
excludes = ['Tkinter']
packages = ['pystray', 'psutil', 'PIL']
includeFiles = ['plot-icon.png', 'pssuspend64.exe']

setup(
	name = "Madmax Win Pause",
	version = "0.1",
	author = "unsocial-bleach",
	options = {
		'build_exe': {
			'includes': includes,
			'excludes': excludes,
			'packages': packages,
			'include_files': includeFiles,
		}
	},
	description = "A systray tool to pause/resume current Chia plotting operations from madMAx43v3r/chia-plotter",
	executables = [Executable("madmax-win-pause.py")]
)
