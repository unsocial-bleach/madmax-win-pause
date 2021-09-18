# madmax-win-pause
A systray tool to pause/resume current Chia plotting operations from [madMAx43v3r/chia-plotter](https://github.com/madMAx43v3r/chia-plotter)

## Dependencies
* Microsoft's sysinternal's "PsSuspend"
	* v1.07 is already downloaded in the repo for your convencience. Otherwise, it must be downloaded from [their website for free.](https://docs.microsoft.com/en-us/sysinternals/downloads/pssuspend)
* Various Python libraries, installed via `python3 -m pip install -r requirements.txt`.

## Source/Acknowledgements
* Using PsSuspend to pause MadMax: https://www.reddit.com/r/chia/comments/njev0c/windows_automatically_pause_plotters_when_you/
* Pausing on Linux: https://www.reddit.com/r/chia/comments/ojfn5j/is_it_possible_to_pause_plotting/h51aj6o

## How to Install
* See fully-packaged release executable.

### How to Build
Building this package to a .exe file is done with the following command:
`python -m PyInstaller --noconfirm --onefile --console --clean --add-data "plot-icon.png;." --add-data "pssuspend64.exe;."  "madmax-win-pause.py"`

## Other Notes
* The [madMAx43v3r/chia-plotter](https://github.com/madMAx43v3r/chia-plotter) executable file must be named `chia-plotter`.
* This tool is only useful on Windows. Use `kill -SIGSTOP <pid>` and `kill -SIGCONT <pid>` on *NIX systems.

## Donations
I know this isn't a complicated tool or anything, but feel free to share a couple mojos.
* **Bitcoin:** 1E6mm66QU4DeF9NBGKqWBPnbGNPg3Uwf8u
* **Monero:** 43hK7YNKQvvZNrAGaisdYT61v7gUAvyQqL1m8uoD66VGc8MFmoHoWWq5EiHKGeQPWBJa29JbL45dE7L3ViaXMuaB9sUAfEM
* **Litecoin:** LKi9UzDNTRpXh8TmDaETE1K1a3jqdXedDG
* **Chia:** xch15qrjf3z5m3pv3f3kxpv8fazmutfz2jghlheju25tuncvzj8xhcdq74kzlj
