function [city_path] = path_search_directed(name)
    path = dir('**/gsp_traffic_directed/**/*'+name+'.mat');
    if isempty(path) 
        fprintf('No such city named %s\n',name)
        city_path = NaN;
    else
        city_path = sprintf('%s/%s',path(1).folder,path(1).name);
    end
end

