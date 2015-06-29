import unittest
from nose.tools import assert_equals
import layouts
import samplers
import data_loader
import pyx


class LayoutTest(unittest.TestCase):
    def test_rectangular(self):
        clusters = data_loader.DataLoader("examples/tables", "examples/clusters").results
        samplerObj = samplers.StratifiedSampler(clusters['present_past_future'], 5)
        layoutObj = layouts.RectangularLayout()

        canvas = pyx.canvas.canvas()
        layoutObj.draw(samplerObj, canvas)
        canvas.writePDFfile("output/rectangular_layout")

    def test_circular(self):
        clusters = data_loader.DataLoader("examples/tables", "examples/clusters").results
        samplerObj = samplers.SimpleSampler(clusters['present_past_future'], 5)
        layoutObj = layouts.CircularLayout()

        canvas = pyx.canvas.canvas()
        layoutObj.draw(samplerObj, canvas)
        canvas.writePDFfile("output/circular_layout")