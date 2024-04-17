function [files] = city_names(country)
    paths = dir('**/'+country+'*.mat');
    if isempty(paths)
        fprintf('%s is not contained in this dataset\n',name)
    else
        files = strings(numel(paths), 1); % ファイル名を格納するセル配列を初期化
        for i = 1:numel(paths)
            [~, filename, ~] = fileparts(paths(i).name);% delete extension
            parts = split(filename, '_');  % split a string
            files{i} = parts{2}; % pull out the city name
        end
    end
end