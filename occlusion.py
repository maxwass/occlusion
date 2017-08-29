import random
import sys
import os
import numpy as numpy
import time
import unittest
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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


#Tests
ext = [(1, 1), (1, 3), (3, 3), (3, 1)]
x_coordinates = [1,1,3,3,1]
y_coordinates = [1,3,3,1,1]

polygon1 = Polygon(ext)
x_output, y_output =   shapelyPoly2plot(polygon1)

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
map_width = 15
map_height = 15

plt.ion()  #interactive mode: https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
plt.show()

plt.close()
fig = plt.figure()
ax = fig.add_subplot(111) # number of rows. cols, current plot number




#plot polygons
ax.fill(x1,y1, zorder = 10)
ax.fill(x2, y2, zorder = 10)
#plot line
ax.quiver(xy0[0], xy0[1], xy1[0], xy1[1], units = 'xy', scale = 1, zorder = 5)

#print line.intersects(p1)
#print line.intersection(p1)
#print line.intersects(p2)
plt.axis('equal')
plt.grid()
ax.set_xlim([-1, map_width+1])
ax.set_ylim([-1, map_height+1])

#ax.add_patch(patches.Circle((0.5, 0.5), 0.2), zorder = 1)

#plot threat
threat_x = 3
threat_y = 8
threat = plt.Circle((threat_x,threat_y), radius=.25, color='r', fill=True, zorder = 15)
ax.add_artist(threat)


#time.sleep(4)
#loop through every point and check if it is occluded

#first try to first row
for x in range(0,map_width):
    for y in range(0, map_height):
        threat_to_vertex_coordinates = [(threat_x,threat_y),(x,y)]
        line_threat_to_vertex = LineString(threat_to_vertex_coordinates)
        print("Vertex ( %i, %i ): " % (x ,y))

        for obs in obstacles:
            occluded = line_threat_to_vertex.intersects(obs)
            print("     Occluded: %s" % occluded)
            if occluded:
               v = plt.Circle((x,y), radius=.25, color='k', fill=True, zorder = 13)
               ax.add_artist(v)
               break
            else:
               v = plt.Circle((x,y), radius=.25, color='g', fill=True, zorder = 13)
               ax.add_artist(v)

        plt.draw()
        plt.pause(0.001)



#current robot viewing location
robot_x = 1
robot_y = 10
robot = plt.Circle((robot_x,robot_y), radius=.25, color='b', fill=True, zorder = 15)
ax.add_artist(robot)
plt.draw()
plt.pause(0.001)









time.sleep(10)


'''                                                                             
coor = list(polygon.exterior.coords)                                            
print coor                                                                      
plt.show()                                                                      
plt.hold(True)                                                                  
                                                                                
                                                                                
                                                                                
                                                                                
#clear matplotlib plots                                                         
plt.close()                                                                     
                                                                                
#size of grid                                                                   
rows = 10; columns = 10                                                         
x_c = [0,1,2,3,4,5,6,7,8,9]                                                     
                                                                                
matrix = numpy.zeros((rows, columns))                                           
                                                                                
a = numpy.ones(10)                                                              
for i in range(0,rows,1):                                                       
        plt.plot(a*i,x_c, 'ro')                                                 
        plt.hold(True)                                                          
                                                                                
                                                                                
plt.show()                                                                      
'''
