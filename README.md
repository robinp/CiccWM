CiccWM
------

CiccWM aims to be a vmii-like dynamic/iling window manager for Windows,
naviagable using the keyboard with ease.

Requirements
------------
* Python 2.7
* pywin32
* pyHook

Startup
-------

Execute
    python27.exe ciccwm.py

Keys
----

* Alt-Shift Q - quit (at least should)
* Alt-Shift A - adds active window to be managed by CiccWM
* Alt-Shift M - set current column mode to Maxing layout
* Alt-Shift D - set current column mode to Distributing layout
* Alt-Shift R - recalculates layout (should not be needed)
* Alt H/J/K/L - cycle to window left/down/up/right
* Alt-Shift H/J/K/L - shift current window to the respective direction

Status
------

The current implementation is a rough demo showing that things can work.
Deficiencies yet:

* no automatic addition of windows to CiccWM management
* managed windows can't be released
* CiccWM is not notified if a window gets destroyed
* window size query oddities (certain apps seem to not report their true size,
  or not respect the set size commands)
* possibly others

Have fun, contributions are welcome!
