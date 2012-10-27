'''
Created on Oct 25, 2012

@author: ray
'''
import unittest
from osgeo import ogr
from libeller import shapesort


class ShapefileTest(unittest.TestCase):

    def test_read(self):
        source_dataset = './input/test_read_shapefile.shp'
        target_dataset = './output/test_shape.shp'

        def cmpfunc(left, right):
            if left["ScaleRank"] < right["ScaleRank"]:
                return -1
            elif left["ScaleRank"] > right["ScaleRank"]:
                return 1
            else:
                lt_geom_area = left.geometry().GetArea()
                rt_geom_area = right.geometry().GetArea()
                if lt_geom_area < rt_geom_area:
                    return -1
                elif lt_geom_area > rt_geom_area:
                    return 1
                else:
                    return 0

        shapesort.shapesort(source_dataset, target_dataset, cmp_func=cmpfunc)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
