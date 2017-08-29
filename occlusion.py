import random
import sys
import os
import numpy as numpy
import time
import unittest
import matplotlib.pyplot as plt

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon


            
def shapelyPoly2plot(polygon):
    x_coor = []
    y_coor = []

    # extract xy tuple coordinates and manipulate into
    # list of the x_coordinate and list of the y_coordinates
    # polygon.exterior.coor --> [ (x0, y0), (x1,y1), ...., (xn, yn), (x0, y0) ]
    # desired format        -->  [x0, x1, ..., xn, x0]   [y0, y1, ..., yn, y0]
    #print('polygon: ', list(polygon.exterior.coords))
    xy_tuples = list(polygon.exterior.coords)

    coordinate_count = 0
    for xy in xy_tuples:
        x_coor.append(xy[0])
        y_coor.append(xy[1])
        coordinate_count += 1

    #print(coordinate_count, " coordinates")
    #print("x_coor: ", x_coor)
    #print("y_coor: ", y_coor)
    #print("\n")

    return x_coor, y_coor


##test shapelyPoly2plot




#Tests
ext = [(1, 1), (1, 3), (3, 3), (3, 1)]
x_coordinates = [1,1,3,3,1]
y_coordinates = [1,3,3,1,1]

polygon1 = Polygon(ext)
x_output, y_output =   shapelyPoly2plot(polygon1)

print x_output
print x_coordinates
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

x1,y1 = shapelyPoly2plot(p1)
x2,y2 = shapelyPoly2plot(p2)
tc.assertEqual(ext_x1, x1)
tc.assertEqual(ext_y1, y1)
tc.assertEqual(ext_x2, x2)
tc.assertEqual(ext_y2, y2)

#line data
line1 = [(0,0),(6,6)]
line = LineString(line1)
xy0 = line.coords[0]
xy1 = line.coords[1]



#plotting
plt.close()
fig = plt.figure()
ax = fig.add_subplot(111) # number of rows. cols, current plot number

#plot polygons
ax.fill(x1,y1)
ax.fill(x2, y2)
#plot line
ax.quiver(xy0[0], xy0[1], xy1[0], xy1[1], units = 'xy', scale = 1)

print line.intersects(p1)
print line.intersection(p1)
print line.intersects(p2)
plt.axis('equal')
plt.grid()

#plt.plot(ext_x, ext_y)
plt.show()


























