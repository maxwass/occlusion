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

plot = False

#plotting
map_width = 15; map_height = 15
'''
if plot:
    plt.close()
    plt.ion()  #interactive mode: https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
    plt.show()
    fig = plt.figure()
    ax = fig.add_subplot(111) # number of rows. cols, current plot number
    plt.axis('equal')
    plt.grid()
    ax.set_xlim([-3, map_width+3])
    ax.set_ylim([-3, map_height+3])
'''
#obstacles
ext1 = [(1,1), (1,3), (3,3), (3,1), (1,1)]
ext2 = [(7,7), (8,8), (9,9), (8,12), (7,7)]
ext3 = [(5,5), (5,7), (10,7), (10,5), (5,5)]
ext4 = [(2,9), (2,10), (4,10), (4,9), (2,9)]
p1 = Polygon(ext1); p2 = Polygon(ext2); p3 = Polygon(ext3); p4 = Polygon(ext4)
raw_obstacles = []
raw_obstacles.append(ext1);raw_obstacles.append(ext2); raw_obstacles.append(ext3); raw_obstacles.append(ext4);
obstacles = [p1,p3,p4]
'''
if plot:
    for obs in obstacles:
        obs_x, obs_y = user_fun.shapelyPoly2plot(obs)
        ax.fill(obs_x, obs_y, color="magenta", zorder=10)
'''

#plot threat & robot
threat_x = 3; threat_y = 8; robot_x = 10; robot_y = 13
if plot:
    plt.close()
    plt.ion()  # interactive mode: https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
    plt.show()
    fig = plt.figure()
    ax = fig.add_subplot(111)  # number of rows. cols, current plot number
    plt.axis('equal')
    plt.grid()
    ax.set_xlim([-3, map_width + 3])
    ax.set_ylim([-3, map_height + 3])

    for obs in obstacles:
        obs_x, obs_y = user_fun.shapelyPoly2plot(obs)
        ax.fill(obs_x, obs_y, color="magenta", zorder=10)

    threat = plt.Circle((threat_x,threat_y), radius=.25, color='r', fill=True, zorder = 15)
    robot  = plt.Circle((robot_x, robot_y), radius=.25, color='b', fill=True, zorder = 15)
    ax.add_artist(threat); ax.add_artist(robot)






if plot:
    #loop through every point and check if it is occluded
    #maintain a heap of nonoccluded points

    h = [] #list for heap

    for x in range(0,map_width):
        for y in range(0, map_height):
            #create a line segment connecting the threat and current node
            #if this line intersects any of the obstacles, the node is 'occluded'
            threat_to_vertex_line = LineString([(threat_x,threat_y),(x,y)])

            #calc node's value for selection later: for later optimization, put inside 'else'
            v_weight = user_fun.nodeValue((x,y), (threat_x,threat_y), (robot_x,robot_y))

            #check if current node is occluded from threat by any obstacle
            occluded = False
            for obs in obstacles:
                occluded = threat_to_vertex_line.intersects(obs)
                if occluded:
                    break

            #if occluded then plot black circle, else print green circle and add to heap
            if occluded:
                v = plt.Circle((x,y), radius=.25, color='k', fill=True, zorder = 13)
                ax.add_artist(v)
                continue
            else:
                v = plt.Circle((x,y), radius=.25, color='g', fill=True, zorder = 13)
                plt.text(x - .3, y, str(int(v_weight)), color="blue", fontsize=8 , zorder=18)
                ax.add_artist(v)
                hp.heappush(h, (-v_weight, (x,y))) # negate because min heap


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


else:
    print "Inputs: threat: %s, robot: %s, mapSize: %s" % ((threat_x, threat_y), (robot_x, robot_y),(map_width, map_height))

    #print "matlabHelper:"
    #user_fun.matlabInterfacePrintingInputs(raw_obstacles, (threat_x, threat_y), (robot_x, robot_y), (map_width, map_height))
    bestGoalPoints = user_fun.scoutGoal(raw_obstacles, (threat_x, threat_y), (robot_x, robot_y), (map_width, map_height))
    user_fun.plotOutputs(raw_obstacles, (threat_x, threat_y), (robot_x, robot_y), (map_width, map_height), bestGoalPoints)
    #print bestGoalPoints
    #user_fun.printHelloFromMat()







