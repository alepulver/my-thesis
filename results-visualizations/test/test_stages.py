import unittest
from nose.tools import assert_equals
import stages
import data_loader
import pyx


class DataLoaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = data_loader.DataLoader("examples/tables", "examples/clusters")
        super(cls)

    def test_present_past_future(self):
        rows = data_loader.DataLoader.read_with_names('examples/tables/present_past_future.csv')
        stage_objects = {row['experiment_id']: stages.PresentPastFuture(row) for row in rows}
        assert_equals(len(stage_objects), 5)

        canvas = pyx.canvas.canvas()
        stage_objects['36acb0a1-4f13-474e-84c8-a3bf32094014'].draw(canvas)
        canvas.writePDFfile("output/present_past_future")

    def test_seasons_of_year(self):
        rows = data_loader.DataLoader.read_with_names('examples/tables/seasons_of_year.csv')
        stage_objects = {row['experiment_id']: stages.SeasonsOfYear(row) for row in rows}
        assert_equals(len(stage_objects), 5)

        canvas = pyx.canvas.canvas()
        stage_objects['36acb0a1-4f13-474e-84c8-a3bf32094014'].draw(canvas)
        canvas.writePDFfile("output/seasons_of_year")

    def test_days_of_week(self):
        rows = data_loader.DataLoader.read_with_names('examples/tables/days_of_week.csv')
        stage_objects = {row['experiment_id']: stages.DaysOfWeek(row) for row in rows}
        assert_equals(len(stage_objects), 5)

        canvas = pyx.canvas.canvas()
        stage_objects['36acb0a1-4f13-474e-84c8-a3bf32094014'].draw(canvas)
        canvas.writePDFfile("output/days_of_week")