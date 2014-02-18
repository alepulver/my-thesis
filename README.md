# Thesis Project

## Introduction

...

## Installation

The latest version of Kivy (1.8.0) supports Python 3.3, and we prefer it over 2.7. To ease portability, the following instructions use the `pyenv` Python version manager. It can coexist with any system Python installations without interference.

```
# Install pyenv from github
# https://github.com/yyuu/pyenv#installation

# For Ubuntu, these dev libs are required for building Python
sudo apt-get install libreadline-dev libbz2-dev zlib1g-dev libssl-dev

# And these for pygame
sudo apt-get install mercurial ffmpeg \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev

# Install Python 3.3 locally for the current user
pyenv install 3.3.4
pyenv shell 3.3.4
pip install cython

# Install latest pygame from their repository
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python setup.py install

# Install kivy
pip install kivy
```

## TODO

- Color buttons
- Show popup if circle isn't closed
- Add line width (or draw circles at each position)
- Save positions to file
- Add exit button or terminate when complete
