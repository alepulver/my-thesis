# Results analysis

The subjects' data can be accessed through the appropriate URL, but as it's not always fetched properly I recommend using `links`. Otherwise the database dump can be obtained with [db-tools](https://github.com/meteor-london/db-tools) in BJSON (Binary JSON) and converted to regular (plain text) JSON.

A script for analysis of the quantity and "completeness" of experiments is available as `generate_stats.py`. To get the data as a CSV, use `generate_results.py`. 

...

## TODO

- Add shown button order in timeline (chronological vs unsorted)
- Add 'superposition' percentage variable
- Add space usage percentage
- Make timestamps relative to start of stage
- Return dates and handle them from R with "lubridate"
- Use HDF5 to export: http://en.wikipedia.org/wiki/Hierarchical_Data_Format
- ...

## Links

- [Export from server](https://gist.github.com/olizilla/5209369)
- [Import from server](https://gist.github.com/IslamMagdy/5519514)
- [neuro-circles-json-to-csv](https://github.com/chudichudichudi/neuro-circles-json-to-csv)
- http://pythontesting.net/framework/nose/nose-fixture-reference/