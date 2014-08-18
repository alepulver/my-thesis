# My thesis

## Introduction

Neuroscience experiments for my thesis project.

There is an old Python version, and the current one written in Javascript.

## Javascript version

It should work on modern web browsers as well as mobile devices, but the primary target is the web.

The idea is to use [KineticJS](http://kineticjs.com/) for graphics and [Meteor](https://www.meteor.com/) for the server.

One drawback is that widgets and layouts must be either written from scratch, or use additional libraries like:
- [bootstrap](http://getbootstrap.com/) (for HTML+CSS)
- [zebra](http://www.zebkit.com/) (for Canvas)
- [jLayout](http://www.bramstein.com/projects/jlayout/) (generic)

And even if Wacom tablets aren't natively supported in Javascript, there is an official [Windows/Mac browser plugin](http://www.wacomeng.com/web/WebPluginReleaseNotes.htm), and an unofficial [Linux version](https://github.com/ZaneA/WacomWebPlugin) with partial support.

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
mrt
```

And enter the following url: http://localhost:3000/

Source modifications are reloaded automatically.

### On-line prototype

http://circles-experiment.meteor.com/

### TODO

- Save when moved and resized, and if possible all positions between with timestamps
- Allow directly dragging shapes (automatic selection and move to top when dragstart)
- Allow moving events in timeline

- Restrict db access
- Deploy to openshift for production

#### Tablet / Mobile

- Make anchors larger for tablets, show tooltip always (there is no "mouseover")
- Scale down canvas if screen space is too small, using setScale to avoid changing pixel values; if it doesn't work just use percentage for dimensions

#### Admin panel

- Allow viewing results graphically (toDataURL)
- Add password or token to /reports
- Allow downloading as CSV or any tabulated format
- Maybe displaying online with d3/vega/etc

#### Ideas

- Move buttons and color bar outside canvas (easier and saves space)
- Add message box responding to current mouse position outside canvas
- Refactor widgets in a wrapper and decorator objects
- Check this? https://github.com/HarvardEconCS/turkserver-meteor

### References

- Save experiment session graphically
  - [Stage data URL](http://www.html5canvastutorials.com/kineticjs/html5-canvas-stage-data-url-with-kineticjs/)
  - [Replay system for KineticJS](http://nightlycoding.com/index.php/2014/01/replay-system-for-kineticjs-and-html5-canvas/)
- [Dynamic canvas resizing](http://stackoverflow.com/questions/20770247/dynamic-canvas-re-sizing-in-kineticjs)
- [Drag and Drop, resize, move example](http://www.html5canvastutorials.com/labs/html5-canvas-drag-and-drop-resize-and-invert-images/)
- [Rotate example](http://codepen.io/ArtemGr/pen/ociAD)
- [Javascript promises](http://www.html5rocks.com/en/tutorials/es6/promises/)
- [regenerator](http://facebook.github.io/regenerator/) (generator functions for current Javascript)