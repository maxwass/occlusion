%export PYTHONPATH=$PYTHONPATH:/Users/maxwasserman/PycharmProjects/occlusion

%add path of project: which filename to give? pyhton or matlab script?
%[own_path, name, ext] = fileparts(mfilename('./py2mat.m'));
% own_path = '.'
% module_path = fullfile(own_path, '..')
% python_path = py.sys.path %'/usr/bin/python';
% if count(python_path, module_path) == 0
%     insert(python_path, int32(0), module_path);
% end
% insert(python_path, int32(0), module_path);

% if count(py.sys.path,'') == 0
%     insert(py.sys.path,int32(0),'');
% end
%insert(py.sys.path, int32(0), '/Users/maxwasserman/PycharmProjects/occlusion/helper.py');

%pwd;
%pyversion;
%py.sys.path;

addpath('/Users/maxwasserman/PycharmProjects/occlusion/');

path2occlusion = '/Users/maxwasserman/PycharmProjects/occlusion/';
path2helper = '/Users/maxwasserman/PycharmProjects/occlusion/helper.py';

if count(py.sys.path, path2occlusion) == 0
    insert(py.sys.path,int32(0),path2occlusion);
    insert(py.sys.path,int32(0),path2helper);
end
 
%%in matlab include folder occlusion & all subfolders in path
clear classes; % needed if python code changes
mod = py.importlib.import_module('helper');% throws error if helper not on the python search path
py.reload(mod);
%% custom test data

% %obs_1 = py.list({p1,p2,p3,p4,p5});
% %ext1 = [(1,1), (1,3), (3,3), (3,1), (1,1)]
% e1p1 = py.tuple({1,1}); e1p2 = py.tuple({1,3});
% e1p3 = py.tuple({3,3}); e1p4 = py.tuple({3,1});
% e1p5 = py.tuple({1,1});
% 
% %ext2 = [(7,7), (8,8), (9,9), (8,12), (7,7)]
% e2p1 = py.tuple({7,7}); e2p2 = py.tuple({8,8});
% e2p3 = py.tuple({9,9}); e2p4 = py.tuple({8,12});
% e2p5 = py.tuple({7,7});
% 
% %ext3 = [(5,5), (5,7), (10,7), (10,5), (5,5)]
% e3p1 = py.tuple({5,5}); e3p2 = py.tuple({5,7});
% e3p3 = py.tuple({10,7}); e3p4 = py.tuple({10,5});
% e3p5 = py.tuple({5,5});
% 
% %ext4 = [(2,9), (2,10), (4,10), (4,9), (2,9)]
% e4p1 = py.tuple({2,9}); e4p2 = py.tuple({2,10});
% e4p3 = py.tuple({4,10}); e4p4 = py.tuple({4,9});
% e4p5 = py.tuple({2,9});
% 
% obs_1 = py.list({e1p1, e1p2, e1p3, e1p4, e1p5});
% obs_2 = py.list({e2p1, e2p2, e2p3, e2p4, e2p5});
% obs_3 = py.list({e3p1, e3p2, e3p3, e3p4, e3p5});
% obs_4 = py.list({e4p1, e4p2, e4p3, e4p4, e4p5});
% 
% 
% obs_list = py.list;
% obs_list.append(obs_1);
% %obs_list.append(obs_2);
% obs_list.append(obs_3);
% obs_list.append(obs_4);
% %obs_list.append(obs_5);

%% integration with Daewon

load occlusion_info.mat
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

%threatPos = py.tuple({py.int(target_ref(1)), py.int(target_ref(2))});
threatPos = py.tuple({py.int(100), py.int(100)});
robotPos  = py.tuple({py.int(start_ref(1)),  py.int(start_ref(2))}); 
mapSize   = py.tuple({py.int(x_map_ref(2)),  py.int(y_map_ref(2))}); %+1?

%one = py.helper.printHelloFromMat();
%r = py.helper.matlabInterfacePrintingInputs(obs_list, threatPos, robotPos, mapSize);
tic
nBestPoints = py.helper.scoutGoal(obstacles, threatPos, robotPos, mapSize);
tBestPoints = toc;
disp(tBestPoints);


%%plot output
fig = figure();
ax  = axes;  % number of rows. cols, current plot number
hold on


shapely_obs = py.helper.rawObs2ShapelyPoly(obstacles);
while(length(shapely_obs) ~= 0)
    obs = shapely_obs.pop;
    obs_x_y = py.helper.shapelyPoly2plot(obs);
    obs_x = pylist2matarray(obs_x_y(1).cell{1});
    obs_y = pylist2matarray(obs_x_y(2).cell{1});
    p = fill(ax, obs_x, obs_y, 'm');
end
    fprintf('   plotted obstacles...');



    %plot the n Best returned points from scoutGoal
while(length(nBestPoints) ~= 0)
    scoutPoint = nBestPoints.pop;
    val   = scoutPoint{1};
    point = pylist2matarray(scoutPoint{2});
    
    radius_point = radius_threat;
    pos_point = [(point-radius_robot) radius_point radius_point];
    rectangle(ax,'Position', pos_point, 'Curvature', [1 1], 'FaceColor','green');
    t = text('Position',point-radius_point,'string',num2str(point), 'Color', 'b', 'FontSize', 15);
end

    fprintf('   plotted best points...')

    
center_threat = pylist2matarray(threatPos);
radius_threat = 5;
pos_threat = [(center_threat-radius_threat) radius_threat radius_threat];
h_t = rectangle(ax,'Position', pos_threat, 'Curvature', [1 1], 'FaceColor','red');
uistack(h_t,'up',2)

center_robot = pylist2matarray(robotPos);
radius_robot = radius_threat;
pos_robot = [(center_robot-radius_robot) radius_robot radius_robot];
h_r = rectangle(ax,'Position', pos_robot, 'Curvature', [1 1], 'FaceColor','blue');
uistack(h_r,'up',2)

    fprintf('   plotted threat/robot...')
    
axis(ax,'equal')
axis(ax,'manual')
grid(ax)
mapSize_cell = mapSize.cell;
width = mapSize_cell{1}; height = mapSize_cell{2};
xlim([-3, width + 3]);
ylim([-3, height + 3]);

% py.helper.plotOutputs(obstacles, threatPos, robotPos, mapSize, nBestPoints);
% disp(nBestPoints)






