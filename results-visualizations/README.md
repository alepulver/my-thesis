# Results Visualizations

This program takes the output of `results-tables`, and clustering assignments for the stages to generate a visualization.

## Usage

- Install [PyX](http://pyx.sourceforge.net/) (not available through `pip`, must download and run `python setup.py install`)
- Run `python runner.py --tables_dir ... --clusters_dir ...`, with the path to the `individual_stages` (sudirectory) output of `results-tables` and clusters to represent
- The generated files should be in the `output/` directory

## Alternatives

The following software packages were considered in addition to PyX.

- [grid](https://www.stat.auckland.ac.nz/~paul/grid/grid.html): low-level interface used by [ggplot2](http://ggplot2.org/), for R
- [compose](https://github.com/dcjones/Compose.jl): low-level interface used by [gadfly](http://gadflyjl.org/), for Julia
- [Artist](http://matplotlib.org/1.4.0/users/artists.html): objects used by [matplotlib](http://matplotlib.org/)
- [Diagrams](http://projects.haskell.org/diagrams/): promising monadic interface for Haskell
- [cairo](http://cairographics.org/): complex, and doesn't have active high-level interfaces
- LaTeX packages for drawing (like [TikZ](https://www.sharelatex.com/learn/TikZ_package), [Asymptote](http://asymptote.sourceforge.net/)
  and [PSTricks](http://tug.org/PSTricks/main.cgi)) with extensions, but I prefer a general programming language