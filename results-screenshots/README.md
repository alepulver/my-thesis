# Generate images from experiments

This is a simple server to show the resulting canvas at the end of each stage, with a script to collect screenshots of them. These canvas representations are independent of the generated results table, serving as a cross-check tool.

To create the images, follow these steps:

- The server must be running (`python server.py results.json`) and the "images" directory must exist
- Run the command `casperjs download.coffee`
- In case it fails, you can try `coffee -c download.coffee` and `casperjs download.js`
- Wait a few hours, it's slow :(

Note that the timeline uses matrix transformations, so the serialized stage was missing some information and didn't look good. That's why they were excluded.
