import unittest
from nose.tools import assert_equals
import layouts
import data_loader
import pyx


class LayoutTest(unittest.TestCase):
    def test_rectangular(self):
        clusters = data_loader.DataLoader("examples/tables", "examples/clusters").results
        layoutObj = layouts.RectangularLayout(2, 2)

        canvas = pyx.canvas.canvas()
        layoutObj.draw(clusters['present_past_future'], canvas)
        canvas.writePDFfile("output/rectangular_layout")

    def test_rectangular2(self):
        clusters = data_loader.DataLoader("input/tables", "input/clusters").results
        layoutObj = layouts.RectangularLayout(20, 20)

        canvas = pyx.canvas.canvas()
        layoutObj.draw(clusters['present_past_future'], canvas)
        canvas.writePDFfile("output/rectangular_layout2")