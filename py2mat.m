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

pwd;
pyversion;
py.sys.path;



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

%obstacle_list = '[[(1,1), (1,2), (2,2), (2,1), (1,1)]]';
p1 = py.tuple({1,1});
p2 = py.tuple({1,2});
p3 = py.tuple({2,2});
p4 = py.tuple({2,1});
p5 = py.tuple({1,1});
obs_1 = py.list({p1,p2,p3,p4,p5});


obs_list = py.list;
obs_list.append(obs_1);

robotPos  = py.tuple({3,3});   %'(3,3)';
threatPos = py.tuple({5,5});   %'(5,5)';
mapSize   = py.tuple({10,15}); %'(10,15)';
%one = py.helper.printHelloFromMat();
r = py.helper.matlabInterfacePrintingInputs(obs_list, threatPos, robotPos, mapSize);
disp(r);

