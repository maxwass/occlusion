%% Change to the relevant paths
addpath('/Users/maxwasserman/PycharmProjects/occlusion/');
path2occlusion = '/Users/maxwasserman/PycharmProjects/occlusion/';
path2helper = '/Users/maxwasserman/PycharmProjects/occlusion/helper.py';
if count(py.sys.path, path2occlusion) == 0
    insert(py.sys.path,int32(0),path2occlusion);
    insert(py.sys.path,int32(0),path2helper);
end
 
%% Clear the last import of 'helper' and other classes
clear classes; % needed if python code changes

%% Import Helper 'module' and reload it
mod = py.importlib.import_module('helper');% throws error if helper not on the python search path
py.reload(mod);


%% Take Data from rest of program
load occlusion_info.mat

%% Data processing: Build Obstacles, Data structs for location for threat and robot, and map size
   
%%obstacle builder: 
%   Takes in 1xn Cell Array of { [M1x2], ..., [Mnx2]}
%   Takes each coord_list => [Mix2] array and creates a (x,y) tuple
%    from each row k: 1->i, (x,y) = coord_list(j,:)
%  `Create new obstacle by appending i tuples together in a list
%   Add this new obstacle to a list of obstacles
obstacles = py.list;
numObstacles = length(occlusion(1,:));
for i = 1:numObstacles
    coord_list = occlusion{i};
    numCoordinatePairs = length(coord_list);
    new_obs = py.list;
    
   %disp(coord_list);
   %disp(numCoordinatePairs);
    for j = 1:numCoordinatePairs
        %disp(coord_list(j,:))
        new_obs.append( py.tuple({coord_list(j,1), coord_list(j,2)}) )
    end
    obstacles.append(new_obs)
end

disp(obstacles)

threatPos = py.tuple({py.int(target_ref(1)), py.int(target_ref(2))});
%threatPos = py.tuple({py.int(100), py.int(100)});
robotPos  = py.tuple({py.int(start_ref(1)),  py.int(start_ref(2))}); 
mapSize   = py.tuple({py.int(x_map_ref(2)),  py.int(y_map_ref(2))}); %+1?

%one = py.helper.printHelloFromMat();
%r = py.helper.matlabInterfacePrintingInputs(obs_list, threatPos, robotPos, mapSize);

%% Python call: scoutGoal -> 5 best candidate points
tic
nBestPoints = py.helper.scoutGoal(obstacles, threatPos, robotPos, mapSize);
tBestPoints = toc

%% Take output of scoutGoal and plot best candidates with obstacles, threat, robot
f = plotPythonOutput(obstacles, threatPos, robotPos, mapSize, nBestPoints);
