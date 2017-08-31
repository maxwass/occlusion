import random
import sys
import os
import numpy as numpy
from numpy import linalg as LA
import time
import unittest
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import helper as user_fun
import heapq as hp

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon


#plotting
map_width = 15; map_height = 15
plt.close()
plt.ion()  #interactive mode: https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
plt.show()
fig = plt.figure()
ax = fig.add_subplot(111) # number of rows. cols, current plot number
plt.axis('equal')
plt.grid()
ax.set_xlim([-3, map_width+3])
ax.set_ylim([-3, map_height+3])

#obstacles
ext1 = [(1,1), (1,3), (3,3), (3,1), (1,1)]
ext2 = [(7,7), (8,8), (9,9), (8,12), (7,7)]
ext3 = [(5,5), (5,7), (10,7), (10,5), (5,5)]
ext4 = [(2,9), (2,10), (4,10), (4,9), (2,9)]
p1 = Polygon(ext1); p2 = Polygon(ext2); p3 = Polygon(ext3); p4 = Polygon(ext4)
raw_obstacles = []
raw_obstacles.append(ext1);raw_obstacles.append(ext2); raw_obstacles.append(ext3); raw_obstacles.append(ext4);
obstacles = [p1,p3,p4]


for obs in obstacles:
    obs_x, obs_y = user_fun.shapelyPoly2plot(obs)
    ax.fill(obs_x, obs_y, color="magenta", zorder=10)


#plot threat & robot
threat_x = 3; threat_y = 8; robot_x = 10; robot_y = 13
threat = plt.Circle((threat_x,threat_y), radius=.25, color='r', fill=True, zorder = 15)
robot  = plt.Circle((robot_x, robot_y), radius=.25, color='b', fill=True, zorder = 15)
ax.add_artist(threat); ax.add_artist(robot)

#loop through every point and check if it is occluded
#maintain a heap of nonoccluded points

h = [] #list for heap

for x in range(0,map_width):
    for y in range(0, map_height):
        line_threat_to_vertex = LineString([(threat_x,threat_y),(x,y)])
        print("Vertex ( %i, %i ): " % (x ,y))

        #calc nodes Weight for selection
        v_weight = user_fun.nodeWeight((x,y), (threat_x,threat_y), (robot_x,robot_y))

        #check if current node is occluded from threat by any obstacle
        occluded = False
        for obs in obstacles:
            occluded = line_threat_to_vertex.intersects(obs)
            if occluded:
                break # this breaks out of y loop??

        #if occluded then plot black circle
        if occluded:
            v = plt.Circle((x,y), radius=.25, color='k', fill=True, zorder = 13)
            ax.add_artist(v)
            #print "     Occluded was true"
            continue
        #if not occluded print green circle
        else:
            v = plt.Circle((x,y), radius=.25, color='g', fill=True, zorder = 13)
            plt.text(x - .3, y, str(int(v_weight)), color="blue", fontsize=8 , zorder=18)
            ax.add_artist(v)
            hp.heappush(h, (-v_weight, (x,y))) # - because deafult is min heap
            #print "     Occluded was false"


bestGoalPoints = hp.nsmallest(5,h)
#bestGoalPoints = user_fun.scoutGoal(raw_obstacles, (threat_x, threat_y), (robot_x, robot_y), (map_width, map_height))
for n in bestGoalPoints:
    val = n[0]; node = n[1];
    print node
    l = plt.Circle((node[0], node[1]), radius=.4, color='orange', fill=False, zorder=10)
    ax.add_artist(l)


plt.draw()
plt.pause(0.001)

# keep plot on screen for a bit
time.sleep(25)

