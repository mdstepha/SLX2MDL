function filepath = cleanSlxFilepath(filepath)
% Change slx filename (in given filepath), if necessary, to make it a valid filename that can be
% loaded in matlab
% eg: 'a-b-c/d/e f/my awesome-model.slx' --> 'a-b-c/d/e f/my_awesome_model.slx'  
% parameters: 
% -----------
% filepath: (string) 

    filepath = string(filepath);
    [dirpath, filename, ext] = fileparts(filepath); 
    filename = strrep(filename, '-', '_'); 
    filename = strrep(filename, ' ', '_');

    filepath = fullfile(dirpath, filename);
    filepath = filepath + ext; 
end