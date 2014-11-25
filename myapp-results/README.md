# Results analysis

The subjects' data can be accessed through the appropriate URL, but as it's not always fetched properly I recommend using `links`. Otherwise the database dump can be obtained with [db-tools](https://github.com/meteor-london/db-tools) in BJSON (Binary JSON) and converted to regular (plain text) JSON.

A script for generating reports is available as `runner.py`. The tests can be run with `nosetests`.

## TODO

- Different output with encoded variables for matlab, and table of number -> color
- Use HDF5 to model and export: http://en.wikipedia.org/wiki/Hierarchical_Data_Format

### Variables

- Add 'superposition' percentage variable
- Add space usage percentage
- Return dates and handle them from R with "lubridate"

## Links

- [Export from server](https://gist.github.com/olizilla/5209369)
- [Import from server](https://gist.github.com/IslamMagdy/5519514)
- [neuro-circles-json-to-csv](https://github.com/chudichudichudi/neuro-circles-json-to-csv)
- [Nose tests reference](http://pythontesting.net/framework/nose/nose-fixture-reference/)