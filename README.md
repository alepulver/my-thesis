# My thesis

## Introduction

Neuroscience experiments for my thesis project.

There is a Python and a Javascript (web, both client and server) version.

## Javascript version

It should work on modern web browsers as well as mobile devices, but the primary target is the web.

The idea is to use [KineticJS](http://kineticjs.com/) for graphics and [Meteor](https://www.meteor.com/) for the server.

### Install

```
# Install NVM (Node Version Manager)
curl https://raw.github.com/creationix/nvm/master/install.sh | sh

# Install Node.js
nvm install v0.11.9

# Install meteor
curl https://install.meteor.com/ | sh

# Install meteorite (package manager)
npm install -g meteorite
```

### Run locally

```
cd myapp
meteor
```

And enter the following url: http://localhost:3000/

Source modifications are reloaded automatically.

### On-line prototype

...

### TODO

- Save experiment session graphically
  - [Stage data URL](http://www.html5canvastutorials.com/kineticjs/html5-canvas-stage-data-url-with-kineticjs/)
  - [Replay system for KineticJS](http://nightlycoding.com/index.php/2014/01/replay-system-for-kineticjs-and-html5-canvas/)
- [Dynamic canvas resizing](http://stackoverflow.com/questions/20770247/dynamic-canvas-re-sizing-in-kineticjs)
- [Drag and Drop, resize, move example](http://www.html5canvastutorials.com/labs/html5-canvas-drag-and-drop-resize-and-invert-images/)
- [Rotate example](http://codepen.io/ArtemGr/pen/ociAD)
- [Javascript promises](http://www.html5rocks.com/en/tutorials/es6/promises/)