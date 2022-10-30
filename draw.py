# -*- coding:utf-8 -*-
__author__ = 'zh33rmao'

from qgis.core import (
  QgsApplication,
  QgsDataSourceUri,
  QgsCategorizedSymbolRenderer,
  QgsClassificationRange,
  QgsPointXY,
  QgsProject,
  QgsExpression,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsFeatureRequest,
  QgsFeatureRenderer,
  QgsGeometry,
  QgsGraduatedSymbolRenderer,
  QgsMarkerSymbol,
  QgsMessageLog,
  QgsRectangle,
  QgsRendererCategory,
  QgsRendererRange,
  QgsSymbol,
  QgsVectorDataProvider,
  QgsVectorLayer,
  QgsVectorFileWriter,
  QgsWkbTypes,
  QgsSpatialIndex,
  QgsVectorLayerUtils
)

from qgis.core.additions.edit import edit

from qgis.PyQt.QtGui import (
    QColor,
)

import qgis.utils
def draw():
    from qgis.PyQt.QtCore import QVariant
    layer = iface.activeLayer()
    features = layer.getFeatures()

    pair = dict()

    for feature in features:
        # 检索每一个要素的几何和属性
        print("Feature ID: ", feature.id())
        # 获取几何
        geom = feature.geometry()
        # 获取属性
        attrs = feature.attributes()
        key = feature['bh']
        print(type(feature['bh']))
        value = geom
        pair[key] = value

    # create layer
    vl = QgsVectorLayer("LineString", "desire_lines", "memory")
    # vl = iface.addVectorLayer("f:\\dl.shp", "Ports layer", "ogr")
    pr = vl.dataProvider()

    # add fields
    pr.addAttributes([QgsField("edgeid", QVariant.Int),
                      QgsField("origin", QVariant.Int),
                      QgsField("destination", QVariant.Int),
                      QgsField("value", QVariant.Int)])
    vl.updateFields()  # tell the vector layer to fetch changes from the provider

    layer = QgsProject.instance().mapLayersByName("od")[0]
    features = layer.getFeatures()

    for feature in features:
        # 检索每一个要素的几何和属性
        print("Feature ID: ", feature.id())
        # 获取几何
        ori = int(feature['origin'])
        # print(type(ori))
        dest = int(feature['destination'])
        value = int(feature['value'])
        # 获取属性
        attrs = feature.attributes()
        print("ori: {0}; dest: {1}; value: {2}".format(ori,dest,value))
        # add a feature
        fet = QgsFeature()
        print("ori: {0}; dest: {1}".format(pair.get(ori), pair.get(dest)))
        # print(type(QgsGeometry.fromPolylineXY([pair.get(ori).asPoint(),pair.get(dest).asPoint()]).asPolyline()))
        fet.setGeometry(QgsGeometry.fromPolylineXY([pair.get(ori).asPoint(),pair.get(dest).asPoint()]))
        fet.setAttributes([ori*100+dest, ori, dest, value])
        pr.addFeatures([fet])

    vl.updateExtents()
    QgsProject.instance().addMapLayer(vl)
