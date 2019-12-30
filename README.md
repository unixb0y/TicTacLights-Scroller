# TicTacLights-Scroller

This script lets you display scrolling text on your TicTacLights kit.

It is made for the TicTacLights Nano kit which we soldered @ #36c3 at a workshop of [BlinkenArea](https://www.blinkenarea.org)


Be sure to specify the correct port as the default is specifically set for macOS! In Linux, it will probaby be /dev/ttyUSB0.

>> python3 tictaclights-running.py --help
usage: tictaclights-running.py [-h] -t TEXT [-c {red,green,blue}] [-s SPEED]
                               [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  the text to display
  -c {red,green,blue}, --colour {red,green,blue}
                        the preferred colour
  -s SPEED, --speed SPEED
                        the preferred speed
  -p PORT, --port PORT  the port where your TicTacLights is attached
