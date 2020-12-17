function mdl2slxFolder(mdlFolderPath, slxFolderPath)
% Converts all mdl files in given folder to slx files
%
% parameters: 
% -----------
% mdlFolderPath : (string) absoulte path of folder containing mdl files (to
%                          be converted)
% slxFolderPath : (string) absoulte path of folder containing slx files (to
%                          be generated). 
%                          This folder will be created if it does not exist 
%                          yet. 


    mdlFolderPath = string(mdlFolderPath); 
    slxFolderPath = string(slxFolderPath); 

    % create slx-folder if it does not exist already 
    if ~ exist(slxFolderPath, 'dir')
        mkdir (slxFolderPath); 
    end 
    
    mdlFileNames = getMdlFileNamesInMdlFolderPath(mdlFolderPath); 
    for i=1:length(mdlFileNames)
       mdlFilePath = fullfile(mdlFolderPath, mdlFileNames(i)); 
       mdl2slx(mdlFilePath, slxFolderPath); 
    end

end 

function mdlFileNames = getMdlFileNamesInMdlFolderPath(mdlFolderPath)
    mdlFilesStruct = dir(fullfile(mdlFolderPath, '*.mdl*')); 
    mdlFileNames = string.empty; 
    for i=1:length(mdlFilesStruct)
        mdlFileNames = [mdlFileNames mdlFilesStruct(i).name]; 
    end
end