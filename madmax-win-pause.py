#!/usr/bin/env python3


import os, sys
import subprocess
import psutil

from PIL import Image
import pystray

targetProcName = 'chia_plot.exe'
pssuspendFilePath = 'pssuspend64.exe'

store = {
	'tray_icon': None,
	'last_action': None,
	'last_procCount': 0,
}

def resource_path(relative_path):
	"""
	Get absolute path to resource (file).
	Works for dev and for PyInstaller. Required for single-file bundling with PyInstaller exe.

	:source: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
	"""

	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception: # for dev
		#base_path = os.path.abspath(".")
		base_path = os.path.dirname(os.path.realpath(__file__)) # set as the path the current script is in (doesn't matter where the script is run from)

	return os.path.join(base_path, relative_path)

def find_procs_by_name(name):
	"""
	Return a list of processes matching 'name'.
	Each returned element has a `pid` attribute with an int PID.

	:source: https://stackoverflow.com/a/47214426
	"""
	ls = []
	for p in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
		if name == p.info['name'] or \
				p.info['exe'] and os.path.basename(p.info['exe']) == name or \
				p.info['cmdline'] and p.info['cmdline'][0] == name:
			ls.append(p)
	return ls

def setPriority(pid: int, priority: str) -> str:
	proc = psutil.Process(pid)
	pri = psutil.NORMAL_PRIORITY_CLASS
	
	if priority == 'REALTIME_PRIORITY_CLASS':
		pri = psutil.REALTIME_PRIORITY_CLASS
	if priority == 'HIGH_PRIORITY_CLASS':
		pri = psutil.HIGH_PRIORITY_CLASS
	if priority == 'ABOVE_NORMAL_PRIORITY_CLASS':
		pri = psutil.ABOVE_NORMAL_PRIORITY_CLASS
	if priority == 'NORMAL_PRIORITY_CLASS':
		pri = psutil.NORMAL_PRIORITY_CLASS
	if priority == 'BELOW_NORMAL_PRIORITY_CLASS':
		pri = psutil.BELOW_NORMAL_PRIORITY_CLASS
	if priority == 'IDLE_PRIORITY_CLASS':
		pri = psutil.IDLE_PRIORITY_CLASS
	
	try:
		proc.nice(pri)
	except Exception as e:
		return f"Error setting priority for PID {pid}: {e}"
	return f"Set priority for PID {pid}"

def doActionOnProcess(action:str, pid:int):
	"""
	Either pauses or resumes a given instance.

	:param action: either 'pause' or 'resume' or 'priority_XXXX'
	:param pid: target chia_plot PID
	"""

	print(f"Performing '{action}' action on PID {pid}.")

	pssuspendFilePathCmd = resource_path(pssuspendFilePath).replace(' ', '\ ') #'"' + resource_path(pssuspendFilePath) + '"'
	if action == 'resume':
		textBack = subprocess.check_output([pssuspendFilePathCmd, '/accepteula', '-r', str(int(pid))])
	elif action == 'pause':
		textBack = subprocess.check_output([pssuspendFilePathCmd, '/accepteula', str(int(pid))])
	elif action.startswith('priority_'):
		textBack = setPriority(pid, action.replace('priority_',''))
	else:
		print(f"Invalid action: '{action}'")
		return

	print(f"Ran Command, and got this output: {textBack}")

def doActionOnAllProcesses(action:str):
	"""
	Either pauses or resumes all instances.

	:param action: passed through to `doActionOnProcess(action, ...)`
	"""

	procList = find_procs_by_name(targetProcName)
	for proc in procList:
		doActionOnProcess(action, proc.pid)

	store['last_action'] = action
	store['last_procCount'] = len(procList)

def getStatusText(icon=None) -> str:
	if store['last_action']:
		return "Last Action: " + store['last_action'].title() + f" [{store['last_procCount']} instance(s)]"
	else:
		return "No Action Yet"

def initSysTray():
	img = Image.open(resource_path("plot-icon.png")) # Get it? The icon is a picture of a plot for a tool about plotting.

	menu = pystray.Menu(
		pystray.MenuItem("MadMax Pause Tool", enabled=False, action=lambda: None),
		pystray.MenuItem(getStatusText, enabled=False, action=lambda: None),
		pystray.MenuItem("Pause All Instances", lambda: doActionOnAllProcesses('pause')),
		pystray.MenuItem("Resume All Instances", lambda: doActionOnAllProcesses('resume')),
		pystray.MenuItem("Set Plotter CPU Priority",
			pystray.Menu(
				pystray.MenuItem("Select CPU Priority", enabled=False, action=lambda: None),
				pystray.MenuItem("Max Priority (REALTIME)", lambda: doActionOnAllProcesses('priority_REALTIME_PRIORITY_CLASS')),
				pystray.MenuItem("High Priority (HIGH)", lambda: doActionOnAllProcesses('priority_HIGH_PRIORITY_CLASS')),
				pystray.MenuItem("Above Normal Priority (ABOVE_NORMAL)", lambda: doActionOnAllProcesses('priority_ABOVE_NORMAL_PRIORITY_CLASS')),
				pystray.MenuItem("Normal Priority (NORMAL)", lambda: doActionOnAllProcesses('priority_NORMAL_PRIORITY_CLASS')),
				pystray.MenuItem("Below Normal Priority (BELOW_NORMAL)", lambda: doActionOnAllProcesses('priority_BELOW_NORMAL_PRIORITY_CLASS')),
				pystray.MenuItem("Idle Priority (IDLE)", lambda: doActionOnAllProcesses('priority_IDLE_PRIORITY_CLASS'))
			)
		),
		pystray.MenuItem('Quit This Tool', lambda: store['tray_icon'].stop()),
	)

	store['tray_icon'] = pystray.Icon("MadMax Pause Tool", img, "MadMax Pause Tool", menu)
	store['tray_icon'].run()

if __name__ == '__main__':
	print("Starting...")

	# hide the console windown, if applicable (for PyInstaller)
	# https://stackoverflow.com/a/67694576
	import ctypes
	kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
	process_array = (ctypes.c_uint8 * 1)()
	num_processes = kernel32.GetConsoleProcessList(process_array, 1)
	if num_processes < 3: ctypes.WinDLL('user32').ShowWindow(kernel32.GetConsoleWindow(), 0)

	# start the system tray
	initSysTray()
