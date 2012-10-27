# -*- coding:utf-8 -*-
'''
libeller.shapefile

Created on Oct 25, 2012
@author: ray
'''
import os
from osgeo import ogr


def read(filename, *args, **kwargs):
    dataset = ogr.Open(filename, *args, **kwargs)
    if not dataset:
        raise RuntimeError('could not open %s' % filename)

    return dataset


def create(filename):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    if driver is None:
        raise RuntimeError('missing shapefile driver')

    shp = driver.CreateDataSource(filename)
    if shp is None:
        raise RuntimeError('could not create file %s' % filename)

    return shp


def shapesort(source_dataset, target_dataset, key=None, cmp_func=None):

    if os.path.exists(target_dataset):
        raise ValueError('target dataset already exists.')

    source = read(source_dataset)
    target = None

    try:
        for source_layer in source:

            if source_layer.GetFeatureCount() == 0:
                continue

            source_layer_name = source_layer.GetName()
            source_layer_srs = source_layer.GetSpatialRef()
            source_layer_defn = source_layer.GetLayerDefn()

            print source_layer_name
            print source_layer_srs

            source_layer_geomtype = source_layer_defn.GetGeomType()

            feature_list = list(feature for feature in source_layer)
            feature_list.sort(key=key, cmp=cmp_func)

            # create new dataset
            if not target:
                # lazy initialization
                target = create(target_dataset)
            # create layer
            target_layer = target.CreateLayer(source_layer_name,
                                              source_layer_srs,
                                              source_layer_geomtype)
            # create fields
            for field_idx in range(source_layer_defn.GetFieldCount()):
                source_field = source_layer_defn.GetFieldDefn(field_idx)

                field_name = source_field.GetName()
                field_type = source_field.GetType()
                field_width = source_field.GetWidth()
                field_precision = source_field.GetPrecision()

                target_field = ogr.FieldDefn(field_name, field_type)
                target_field.SetWidth(field_width)
                target_field.SetPrecision(field_precision)

                target_layer.CreateField(target_field)

            # populate features
            target_layer_defn = target_layer.GetLayerDefn()
            for feature in feature_list:

                try:
                    target_feature = ogr.Feature(feature_def=target_layer_defn)
                    target_feature.SetFrom(feature, forgiving=False)

                    target_layer.CreateFeature(target_feature)

                finally:
                    feature.Destroy()
                    target_feature.Destroy()

    finally:
        source.Destroy()
        if target:
            target.Destroy()


