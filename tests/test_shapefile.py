'''
Created on Oct 25, 2012

@author: ray
'''
import unittest
from libeller import shapesort


class ShapefileTest(unittest.TestCase):

    def test_read(self):
        source_dataset = './input/test_read_shapefile.shp'
        target_dataset = './output/test_shape.shp'

        shapesort.shapesort(source_dataset, target_dataset,
                            'test_read_shapefile',
                            ('scalerank',),
                            overwrite=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
