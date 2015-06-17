# Results analysis

This program parses the stored information in the database and outputs several CSV files for table-based analysis.

## Usage

The subjects' data can be accessed through the appropriate URL, but as it's not always fetched properly I recommend using `links`.
Otherwise the database dump can be obtained with [db-tools](https://github.com/meteor-london/db-tools) in BJSON (Binary JSON) and converted to regular (plain text) JSON.

If the JSON files are in the `input/` directory, for instance, run `python runner.py input/*.json` and it will put the
output files inside `output/` (if it doesn't already exist). The tests can be run with `nosetests`.

## Links

- [Export from server](https://gist.github.com/olizilla/5209369)
- [Import from server](https://gist.github.com/IslamMagdy/5519514)
- [neuro-circles-json-to-csv](https://github.com/chudichudichudi/neuro-circles-json-to-csv)
- [Nose tests reference](http://pythontesting.net/framework/nose/nose-fixture-reference/)