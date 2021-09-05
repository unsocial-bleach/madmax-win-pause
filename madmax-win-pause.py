#!/usr/bin/env python3


import os
import subprocess
import psutil

from PIL import Image
import pystray

targetProcName = 'chia_plot.exe'
pssuspendFilePath = 'pssuspend64.exe' # assume in same directory as Python file; can specify a full path here if desired

store = {
	'tray_icon': None,
	'last_action': None,
}

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

def doActionOnProcess(action:str, pid:int):
	"""
	Either pauses or resumes a given instance.

	:param action: either 'pause' or 'resume'
	:param pid: target chia_plot PID
	"""

	print(f"Performing '{action}' action on PID {pid}.")

	store['last_action'] = action

	if action == 'resume':
		textBack = subprocess.check_output([pssuspendFilePath, '/accepteula', '-r', str(int(pid))])
	elif action == 'pause':
		textBack = subprocess.check_output([pssuspendFilePath, '/accepteula', str(int(pid))])
	else:
		print(f"Invalid action: '{action}'")
		return

	print(f"Ran Command, and got this output: {textBack}")

def doActionOnAllProcesses(action:str):
	"""
	Either pauses or resumes all instances.
	
	:param action: passed through to `doActionOnProcess(action, ...)`
	"""

	procList = find_procs_by_name('chia_plot.exe')
	for proc in procList:
		doActionOnProcess(action, proc.pid)

def getStatusText(icon=None) -> str:
	if store['last_action']:
		return "Last Action: " + store['last_action'].title()
	else:
		return "No Action Yet"

def initSysTray():
	img = Image.open("plot-icon.png") # Get it? The icon is a picture of a plot for a tool about plotting.

	menu = pystray.Menu(
		pystray.MenuItem("MadMax Pause Tool", enabled=False, action=lambda: None),
		pystray.MenuItem(getStatusText, enabled=False, action=lambda: None),
		pystray.MenuItem("Pause All Instances", lambda: doActionOnAllProcesses('pause')),
		pystray.MenuItem("Resume All Instances", lambda: doActionOnAllProcesses('resume')),
		pystray.MenuItem('Quit This Tool', lambda: store['tray_icon'].stop()),
	)

	store['tray_icon'] = pystray.Icon("MadMax Pause Tool", img, "MadMax Pause Tool", menu)
	store['tray_icon'].run()

if __name__ == '__main__':
	print("Starting...")
	initSysTray()
