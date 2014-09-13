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
nvm install v0.10.31

# Install meteor
curl https://install.meteor.com/ | sh
```

### Run locally

```
cd myapp
meteor
```

And enter the following url: http://localhost:3000/

Source modifications are reloaded automatically.

### On-line prototype

http://circles-experiment.meteor.com/

### TODO

- Restrict db access
- Allow viewing results graphically (toDataURL)
- Display result summary online with d3/vega/etc
- Add password or token to /reports

#### Ideas

- Check why it works so slow on Firefox
- Deploy to openshift for production
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

#### Import and export data

- [Export from server](https://gist.github.com/olizilla/5209369)
- [Import from server](https://gist.github.com/IslamMagdy/5519514)
- Delete remote database: `meteor deploy ... --delete`

#### Deploy to OpenShift

- https://www.openshift.com/blogs/cloudy-with-a-chance-of-meteorjs
- https://www.openshift.com/blogs/any-version-of-nodejs-you-want-in-the-cloud-openshift-does-it-paas-style
- https://github.com/ramr/nodejs-custom-version-openshift