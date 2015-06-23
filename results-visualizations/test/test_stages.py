import unittest
from nose.tools import assert_equals
import stages
import data_loader
import pyx


class DataLoaderTest(unittest.TestCase):
    def test_generate_figures(self):
        for stage_class in stages.all_stages():
            stage_name = stage_class.stage_name()

            rows = data_loader.DataLoader.read_with_names('examples/tables/{}.csv'.format(stage_name))
            stage_objects = {row['experiment_id']: stage_class(row) for row in rows}
            assert_equals(len(stage_objects), 5)

            canvas = pyx.canvas.canvas()
            stage_objects['36acb0a1-4f13-474e-84c8-a3bf32094014'].draw(canvas)
            canvas.writePDFfile("output/figure_{}".format(stage_name))