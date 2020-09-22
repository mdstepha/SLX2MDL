function slx2mdl(slxFilePath, mdlFolderPath)
% Convert slx file to mdl
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


    % this will be appended to the mdl filename 
    mdl_suffix = '_org';   

    slxFilePath = string(slxFilePath); 
    

    [slxFolderPath, name, ext] = fileparts(slxFilePath); 

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