# My thesis

## Introduction

Neuroscience experiments for my thesis project.

There is a Python and a Javascript (web, both client and server) version.

## Javascript version

It should work on modern web browsers as well as mobile devices, but the primary target is the web.

The idea is to use [KineticJS](http://kineticjs.com/) for graphics and [Meteor](https://www.meteor.com/) for the server.

One drawback is that widgets and layouts must be either written from scratch, or use additional libraries like:
- [bootstrap](http://getbootstrap.com/) (for HTML+CSS)
- [zebra](http://www.zebkit.com/) (for Canvas)
- [jLayout](http://www.bramstein.com/projects/jlayout/) (generic).

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

...

### TODO

- Ask participant data, use meteor template to switch page
- Save results and allow downloading as CSV, etc

- Save mouse positions and timestamps
- Make buttons and color bar horizontal to save space
- Add message box responding to current mouse position, or tooltip next to the mouse (perhaps outside canvas)

#### Maybe

- Refactor "layout" class for positioning elements
- Check this? https://github.com/HarvardEconCS/turkserver-meteor
- Use lodash/lazy.js instead of underscore, other languages (see gdoc)
- Integrate with mimosa for compilation/require/bower/browserify instead of writing meteorite packages
- Try layout framework like boostrap or gumby for the rest of the page (not canvas)

### References

- Save experiment session graphically
  - [Stage data URL](http://www.html5canvastutorials.com/kineticjs/html5-canvas-stage-data-url-with-kineticjs/)
  - [Replay system for KineticJS](http://nightlycoding.com/index.php/2014/01/replay-system-for-kineticjs-and-html5-canvas/)
- [Dynamic canvas resizing](http://stackoverflow.com/questions/20770247/dynamic-canvas-re-sizing-in-kineticjs)
- [Drag and Drop, resize, move example](http://www.html5canvastutorials.com/labs/html5-canvas-drag-and-drop-resize-and-invert-images/)
- [Rotate example](http://codepen.io/ArtemGr/pen/ociAD)
- [Javascript promises](http://www.html5rocks.com/en/tutorials/es6/promises/)
- [regenerator](http://facebook.github.io/regenerator/) (generator functions for current Javascript)