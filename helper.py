import numpy as numpy
import time
from numpy import linalg as LA
import matplotlib.pyplot as plt
import heapq as hp
import shapely.geometry as shapely
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import Point


def nodeValue(xy_node, xy_threat, xy_robot):
    #find euclidean distance between current node & robot, node & threat
    a = numpy.subtract(xy_robot,  xy_node)
    b = numpy.subtract(xy_threat, xy_node)

    node2threat_dist = LA.norm(list(a))
    node2robot_dist  = LA.norm(list(b))

    #print "node2robot:  norm: %s,  vector: %s =  node %s - robot  %s" % (node2robot_dist,   a, xy_node, xy_robot)
    #print "node2threat: norm: %s   vector  %s =  node %s - threat %s" % (node2threat_dist,  b,  xy_node, xy_threat)

    #line connecting robot and threat: we will use this to find points on opposite side of the threat
    line_threat2robot = LineString([xy_threat, xy_robot])


    #find perpendicular distance from node to line
    node2line_dist    = line_threat2robot.distance(Point(xy_node))
    node2line_dist = LA.norm(numpy.cross( numpy.asarray(xy_robot)- numpy.asarray(xy_threat), numpy.asarray(xy_threat)-numpy.asarray(xy_node)))/LA.norm(numpy.asarray(xy_robot)-numpy.asarray(xy_threat))
    #print "node2line_dist %.3f" % node2line_dist

    #cap how close a point can be from the line: will be using in denominator- cannot divide by zero
    closest_allowable = .25

    if node2line_dist < closest_allowable:
        node2line_dist = closest_allowable

    node2line_weight   = 8
    node2robot_weight  = 3
    node2threat_weight = 3
    #node2line_dist = LA.norm(numpy.cross( numpy.subtract(xy_robot-xy_threat), numpy.subtract(xy_threat-xy_node)))/LA.norm(numpy.subtract(xy_robot-xy_threat))


    total_weight = node2threat_weight*node2threat_dist + (-1)*node2robot_weight*node2robot_dist + node2line_weight*(1/node2line_dist)
    #print "xy_node: %s, xy_threat: %s, xy_robot: %s" % ((xy_node,), (xy_threat,), (xy_robot,))
    #print "total weigth =  %.3f = node2threat_dist %.3f + node2robot_dist %.3f + (weight * 1/node2line_dist: %.3i * %.3f)" % (total_weight, node2threat_dist, node2robot_dist, node2line_weight, 1/node2line_dist)

    return total_weight


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

def rawObs2ShapelyPoly(rawObstacleList):
    obstacles = []
    for raw_obs in rawObstacleList:
        # print raw_obs
        obs = shapely.Polygon(raw_obs)
        obstacles.append(obs)


    return obstacles

def occlusionMap(obstacles, threatPos, robotPos, mapSize):
    map_width = mapSize[0];   map_height = mapSize[1]
    threat_x  = threatPos[0]; threat_y   = threatPos[1]
    robot_x   = robotPos[0];  robot_y    = robotPos[1]

    minHeap = []

    for x in range(0, map_width):
        for y in range(0, map_height):
            line_threat_to_vertex = LineString([(threat_x, threat_y), (x, y)])

            # calc nodes Weight for selection
            v_weight = nodeValue((x, y), (threatPos[0], threatPos[1]), (robot_x, robot_y))
            #print "Vertex ( ", x, ", ", y, " ):  Value:", v_weight

            # check if current node is occluded from threat by any obstacle
            occluded = False
            for obs in obstacles:
                occluded = line_threat_to_vertex.intersects(obs)
                if occluded:
                    break

            # if occluded then plot black circle
            if occluded:
                continue
            # if not occluded print green circle
            else:
                #print (x,y)
                hp.heappush(minHeap, (-v_weight, (x, y)))  # - because deafult is min heap

    return minHeap


#example scoutGoal(..., (tx,ty), (rx,ry), (mw,mh))
def scoutGoal(rawObstacleList, threatPos, robotPos, mapSize):
    obstacles = rawObs2ShapelyPoly(rawObstacleList)

    #build an occlusion map and find the best xy for scout
    minHeapVertices = occlusionMap(obstacles, threatPos, robotPos, mapSize)

    # lets look at & return the 5 best candidate points
    nsmallest = hp.nsmallest(5, minHeapVertices)
    print "Best coordinates:"
    for n in nsmallest:
        val = n[0];
        node = n[1];
        print (val, node)


    #plotOutputs(rawObstacleList, threatPos, robotPos, mapSize, nsmallest)

    return nsmallest

#check format of each input
    #rawObstacleList: list of coordinate lists
    #format: (  ((x0,y0), (x1,y1),...,(xn,yn)), ...)
def matlabInterfacePrintingInputs(rawObstacleList, threatPos, robotPos, mapSize):
    #print "rawObstacleList"
    for raw_obs in rawObstacleList:
        print "obstacle:{0}".format(raw_obs)


    #threatPos: tuple of (tx,yx)
    print "threatPos {0}".format(threatPos)

    #robotPos: tuple of (rx,ry)
    print "robotPos {0}".format(robotPos)

    #mapSize: tuple of (mapWidth, mapHeight)
    print "mapSize {0}".format(mapSize)



#after getting the optimal points from scoutGoal,lets take a look at these returned points
def plotOutputs(rawObstacleList, threatPos, robotPos, mapSize, nBestPoints):
    print "About to plot..."

    #convert the rawObstacles list to list of shapely polygons
    obstacles = rawObs2ShapelyPoly(rawObstacleList)

    plt.close()
    #plt.ion()  # interactive mode: https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
    fig = plt.figure()

    ax = fig.add_subplot(111)  # number of rows. cols, current plot number
    plt.axis('equal')
    plt.grid()
    ax.set_xlim([-3, mapSize[0] + 3])
    ax.set_ylim([-3, mapSize[1] + 3])


    #convert shapelyPolygon format to format for plotting library
    for obs in obstacles:
        obs_x, obs_y = shapelyPoly2plot(obs)
        ax.fill(obs_x, obs_y, color="magenta", zorder=10)

    print "   plotted obstacles..."

    threat = plt.Circle((threatPos[0], threatPos[1]), radius=.25, color='r', fill=True, zorder=15)
    robot = plt.Circle((robotPos[0], robotPos[1]), radius=.25, color='b', fill=True, zorder=15)
    ax.add_artist(threat)
    ax.add_artist(robot)
    print "   plotted threat/robot..."

    #plot the n Best returned points from scoutGoal
    for scoutPoint in nBestPoints:
        val   = scoutPoint[0]
        point = scoutPoint[1]
        sp    = plt.Circle((point[0], point[1]), radius=.25, color='g', fill=True, zorder=12)
        ax.add_artist(sp)



    print "   plotted best points..."
    return
    #plt.show()
    plt.draw()
    plt.pause(.01)
    time.sleep(5)


def printHelloFromMat():
    print "Hello!!!!!!!!!!!!"