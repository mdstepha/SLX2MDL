function failedPaths = slx2mdlFolder(slxFolderPath, mdlFolderPath)
% Converts all slx files in given folder to mdl files
%
% parameters: 
% -----------
% slxFolderPath : (string) absoulte path of folder containing slx files (to
%                          be converted)
% mdlFolderPath : (string) absoulte path of folder containing mdl files (to
%                          be generated). 
%                          This folder will be created if it does not exist 
%                          yet. 


    slxFolderPath = string(slxFolderPath); 
    mdlFolderPath = string(mdlFolderPath); 

    % create mdl-folder if it does not exist already 
    if ~ exist(mdlFolderPath, 'dir')
        mkdir (mdlFolderPath); 
    end 
    
    slxFileNames = getSlxFileNamesInSlxFolderPath(slxFolderPath); 
    failedPaths = string.empty; 
    for i=1:length(slxFileNames)
       slxFilePath = fullfile(slxFolderPath, slxFileNames(i)); 
       bdclose('all')
       try
       slx2mdl(slxFilePath, mdlFolderPath);
       catch ME
           bdclose('all')
           disp("*** ERROR: Conversion failed for " + slxFilePath);
           disp(ME);
           failedPaths = [failedPaths slxFilePath];
       end 
    end
    
    if ~ isempty(failedPaths)
       disp("Conversion failed for the following slx files");
       for i = 1 : length(failedPaths)
          disp(failedPaths(i));
       end
    else 
        disp("All conversions were successful.");
    end 

end 

function slxFileNames = getSlxFileNamesInSlxFolderPath(slxFolderPath)
    slxFilesStruct = dir(fullfile(slxFolderPath, '*.slx*')); 
    slxFileNames = string.empty; 
    for i=1:length(slxFilesStruct)
        slxFileNames = [slxFileNames slxFilesStruct(i).name]; 
    end
end