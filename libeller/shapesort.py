# -*- coding:utf-8 -*-
'''
libeller.shapefile

Created on Oct 25, 2012
@author: ray
'''
import os
import subprocess


def shapesort(source, target, layer, keys=list(),
              fields=tuple(), overwrite=False):

    if not os.path.exists(source):
        raise ValueError('source dataset does not exist.')

    if not overwrite and os.path.exists(target):
        raise ValueError('target dataset already exists.')

    fields = ' '.join(f.lower() for f in fields) if fields else '*'

    sort_keys = list()
    for key, order in keys:
        sort_keys.append('%s %s' % (key.lower(), order.lower()))

    sort_keys = ','.join(sort_keys)

    sql = 'select %(field)s from %(table)s order by %(key)s' \
            % dict(field=fields, table=layer, key=sort_keys)
    print sql
    command = ['ogr2ogr', '-sql', sql, target, source]
    if overwrite:
        command.append('-overwrite')

    popen = subprocess.Popen(command)
    popen.communicate()
