# -*- coding:utf-8 -*-
'''
libeller.shapefile

Created on Oct 25, 2012
@author: ray
'''
import os
import subprocess


def shapesort(source, target, layer, keys,
              fields=tuple(), desc=False, overwrite=False):

    if not os.path.exists(source):
        raise ValueError('source dataset does not exist.')

    if not overwrite and os.path.exists(target):
        raise ValueError('target dataset already exists.')

    keys = list(k.lower() for k in keys)
    fields = list(f.lower() for f in fields)

    fields = ' '.join(fields) if fields else '*'
    sort_keys = ' '.join(keys)
    sort_order = 'ASC' if not desc else 'DESC'

    if 'area' in keys:
        keys[keys.index('area')] = 'OGR_GEOM_AREA'

    sql = 'select %(field)s from %(table)s order by %(key)s %(order)s' \
            % dict(field=fields, table=layer, key=sort_keys, order=sort_order)
    print sql
    command = ['ogr2ogr', '-sql', sql, target, source]
    if overwrite:
        command.append('-overwrite')

    popen = subprocess.Popen(command)
    popen.communicate()

