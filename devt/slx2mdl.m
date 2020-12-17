function slx2mdl(slxFilePath, mdlFolderPath)
% Convert slx file to mdl
% 
% Conversion is not guaranteed to succeed. so, put this function in
% try-catch construct (in the caller) 
%
% parameters: 
% -----------
% slxFilePath   : (string) absoulte path of the slx file to be converted
% mdlFolderPath : (string, optional) absoulte path of folder containing mdl files (to
%                          be generated). 
%                          This folder will be created if it does not exist 
%                          yet. 
%                          If not provided, the same folder as that of slx
%                          file will be used 
% 
% IMPORTANT: 
% ----------
% - Matlab/Simulink does not allow to save a mdl file with more than 63
%   character filename. So, if the slx file is long such that the resulting
%   mdl filename would be longer than 63 character, the name will be truncated
%   such that it will be 63 character long.



    % this will be appended to the mdl filename 
    mdl_suffix = '_org';   

    slxFilePath = string(slxFilePath); 
    

    [slxFolderPath, name, ext] = fileparts(slxFilePath); 
    
    name = char(name);
    if length(name) > 59
        name = name(1:59);
    end
    name = string(name);
   

    if nargin == 1
        mdlFolderPath = slxFolderPath; 
    end
    
    mdlFolderPath = string(mdlFolderPath);
    
    
    if slxFolderPath == mdlFolderPath
        % create backup of original slx file 
        slxFilePathBak = slxFilePath + ".bak"; 
        copyfile(slxFilePath, slxFilePathBak);
        
        % get the slx files present in slx-folder 
        % this information is needed to delete any additional slx files 
        % created (which happens if the mdl file is saved in the same folder
        % as the slx file), and to restore original slx files 
        slxFileNamesBefore = getSlxFileNamesInSlxFolderPath(slxFolderPath); 
    end
    
    
    % create mdl-folder if it does not exist already 
    if ~ exist(mdlFolderPath, 'dir')
        mkdir (mdlFolderPath); 
    end 
    
    % create mdl file (with same name as slx file) 
    mdlFilePath = fullfile(mdlFolderPath, name + mdl_suffix + ".mdl"); 
    load_system(slxFilePath); 
    save_system(gcs, mdlFilePath); 
    close_system(gcs); 
    
    % make sure only previously existing slx files are there when the
    % function exits 
    if slxFolderPath == mdlFolderPath
        % delete newly created slx files, if any
        slxFileNamesAfter = getSlxFileNamesInSlxFolderPath(slxFolderPath); 
        slxFileNamesNew = setdiff(slxFileNamesAfter, slxFileNamesBefore); 
        for i=1:length(slxFileNamesNew)
            fp = fullfile(slxFolderPath, slxFileNamesNew(i)); 
            delete(fp); 
        end
        
        % restore original slx file 
        movefile(slxFilePathBak, slxFilePath); 
    end
    
end 


function slxFileNames = getSlxFileNamesInSlxFolderPath(slxFolderPath)
    slxFilesStruct = dir(fullfile(slxFolderPath, '*.slx*')); 
    slxFileNames = string.empty; 
    for i=1:length(slxFilesStruct)
        slxFileNames = [slxFileNames slxFilesStruct(i).name]; 
    end
end