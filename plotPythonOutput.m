function [ fig ] = plotPythonOutput( obstacles, threatPos, robotPos, mapSize, nBestPoints )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
%%plot output
fig = figure();
ax  = axes;  % number of rows. cols, current plot number
hold on

radius_threat = 5;
radius_robot = radius_threat;

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

hold off
end

