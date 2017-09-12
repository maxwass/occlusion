function [ matlab_array ] = pylist2matarray( py_list )
    matlab_array = zeros(1,length(py_list));
    for i = 1:length(py_list)
        entry_wrapper = py_list(i);
        entry = entry_wrapper{1};
        matlab_array(i) = entry;
    end
end

