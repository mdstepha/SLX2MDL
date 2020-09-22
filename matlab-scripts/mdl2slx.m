function mdl2slx(mdlFilePath, slxFolderPath)
% Convert mdl file to slx
%
% parameters: 
% -----------
% mdlFilePath   : (string) absoulte path of the mdl file to be converted
% slxFolderPath : (string, optional) absoulte path of folder containing slx files (to
%                          be generated). 
%                          This folder will be created if it does not exist 
%                          yet. 
%                          If not provided, the same folder as that of mdl
%                          file will be used 


    % this will be appended to the slx filename 
    slx_suffix = '_org';   

    mdlFilePath = string(mdlFilePath); 
    

    [mdlFolderPath, name, ext] = fileparts(mdlFilePath); 

    if nargin == 1
        slxFolderPath = mdlFolderPath; 
    end
    
    slxFolderPath = string(slxFolderPath);
    
    
    if mdlFolderPath == slxFolderPath
        % create backup of original mdl file 
        mdlFilePathBak = mdlFilePath + ".bak"; 
        copyfile(mdlFilePath, mdlFilePathBak);
        
        % get the mdl files present in mdl-folder 
        % this information is needed to delete any additional mdl files 
        % created (which happens if the slx file is saved in the same folder
        % as the mdl file), and to restore original mdl files 
        mdlFileNamesBefore = getSlxFileNamesInSlxFolderPath(mdlFolderPath); 
    end
    
    
    % create slx-folder if it does not exist already 
    if ~ exist(slxFolderPath, 'dir')
        mkdir (slxFolderPath); 
    end 
    
    % create slx file (with same name as mdl file) 
    slxFilePath = fullfile(slxFolderPath, name + slx_suffix + ".slx"); 
    load_system(mdlFilePath); 
    save_system(gcs, slxFilePath); 
    close_system(gcs); 
    
    % make sure only previously existing mdl files are there when the
    % function exits 
    if mdlFolderPath == slxFolderPath
        % delete newly created mdl files, if any
        mdlFileNamesAfter = getSlxFileNamesInSlxFolderPath(mdlFolderPath); 
        mdlFileNamesNew = setdiff(mdlFileNamesAfter, mdlFileNamesBefore); 
        for i=1:length(mdlFileNamesNew)
            fp = fullfile(mdlFolderPath, mdlFileNamesNew(i)); 
            delete(fp); 
        end
        
        % restore original mdl file 
        movefile(mdlFilePathBak, mdlFilePath); 
    end
    
end 


function mdlFileNames = getSlxFileNamesInSlxFolderPath(mdlFolderPath)
    mdlFilesStruct = dir(fullfile(mdlFolderPath, '*.mdl*')); 
    mdlFileNames = string.empty; 
    for i=1:length(mdlFilesStruct)
        mdlFileNames = [mdlFileNames mdlFilesStruct(i).name]; 
    end
end