# Python version

This one uses a Python library that supports Windows, Linux, Mac and multitouch devices (Android, etc).
See the [Kivy website](http://kivy.org/#home) and [these slides](http://slid.es/baptistelagarde/kivy-python-for-android/fullscreen#/).

## Install

The latest version of Kivy (1.8.0) supports Python 3.3, and we prefer it over 2.7.
To ease portability, the following instructions use the `pyenv` Python version manager.
It can coexist with any system Python installations without interference.

```
# Install pyenv from github
# https://github.com/yyuu/pyenv#installation

# For Ubuntu, these dev libs are required for building Python
sudo apt-get install libreadline-dev libbz2-dev zlib1g-dev libssl-dev

# Install Python 3.3 locally for the current user
pyenv install 3.3.4
pyenv shell 3.3.4
pip install cython

# Install latest pygame from their repository
# (ignoring python3* packages, as we've built a custom version)
# http://www.pygame.org/wiki/CompileUbuntu?parent=index

# Install kivy
pip install kivy
```

## Run

```
cd python-circles
python main.py
```

## Android package

...

## TODO

- Add popup messages for information
- Color buttons
- Show popup if circle isn't closed
- Check that circle is closed or at least near
- Workflow: 3 buttons (past, etc) then color picker, no undo
- Save positions to file
- Add exit button or terminate when complete
- Circle detection