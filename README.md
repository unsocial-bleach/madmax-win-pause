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
* See fully-packaged release. 

## Other Notes
* The [madMAx43v3r/chia-plotter](https://github.com/madMAx43v3r/chia-plotter) executable file must be named `chia-plotter`.
* This tool is only useful on Windows. Use `kill -SIGSTOP <pid>` and `kill -SIGCONT <pid>` on *NIX systems.
