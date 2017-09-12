from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon

import unittest

import helper as user_fun




#Tests
ext = [(1, 1), (1, 3), (3, 3), (3, 1)]
x_coordinates = [1,1,3,3,1]
y_coordinates = [1,3,3,1,1]

polygon1 = Polygon(ext)
x_output, y_output =   user_fun.shapelyPoly2plot(polygon1)

#print x_output
#print x_coordinates
tc = unittest.TestCase('__init__')
tc.assertEqual(x_output, x_coordinates, "Shapely2plot: X coordinates incorrect")
tc.assertEqual(y_output, y_coordinates, "Shapely2plot: Y coordinates incorrect")
#^^^


#polygon data
ext1 = [(1,1),(1,3),(3,3),(3,1),(1,1)]
ext_x1 = [1,1,3,3,1]
ext_y1 = [1,3,3,1,1]
ext2 = [(7,7),(8,8),(9,9),(8,12),(7,7)]
ext_x2 = [7,8,9,8,7]
ext_y2 = [7,8,9,12,7]

p1 = Polygon(ext1)
p2 = Polygon(ext2)
obstacles = [p1,p2]

x1,y1 = user_fun.shapelyPoly2plot(p1)
x2,y2 = user_fun.shapelyPoly2plot(p2)
tc.assertEqual(ext_x1, x1)
tc.assertEqual(ext_y1, y1)
tc.assertEqual(ext_x2, x2)
tc.assertEqual(ext_y2, y2)

#line data
line1 = [(0,0),(6,6)]
line = LineString(line1)
xy0 = line.coords[0]
xy1 = line.coords[1]








#testing nodeWeight
#data
tw = unittest.TestCase('__init__')
xy0_threat = (1,1)
xy0_robot  = (0,0)
xy0_node   = (3,2)
total0 = 7.2558 #1/0.7071 + 2.236 + 3.605
#tw.assertAlmostEqual(nodeWeight(xy0_node, xy0_threat, xy0_robot), total0, 3, "nodeWeight Calculation Wrong")

#data
xy1_threat = (2,2)
xy1_robot  = (4,2)
xy1_node   = (0,2)

total1 = 4 #1/0 + 2 + 2
user_fun.nodeWeight(xy1_node, xy1_threat, xy1_robot)