function [city_path] = path_search(name)
    path = dir('**/gsp_traffic/**/*'+name+'.mat');
    if isempty(path) 
        fprintf('No such city named %s\n',name)
        city_path = NaN;
    else
        city_path = sprintf('%s/%s',path(1).folder,path(1).name);
    end
end

