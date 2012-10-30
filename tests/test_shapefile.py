'''
Created on Oct 25, 2012

@author: ray
'''
import os
import unittest
from libeller import shapesort


class ShapefileTest(unittest.TestCase):

    def test_sort(self):

        source = './input/test_shapefile.shp'
        target = './output/sorted_shapefile.shp'

        shapesort.shapesort(source,
                            target,
                            'test_shapefile',
                            [('scalerank', 'asc'), ],
                            overwrite=True
                            )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
