function failedPaths = updateSlxVersionFolder(oldSlxFolderPath, newSlxFolderPath)
% Convert all slx files in oldSlxFolderPath to new slx version (i.e. matlab
% version installed in the machine) 
% 
% parameters: 
% -----------
% oldSlxFolderPath : (string) absoulte path of the folder containing slx files.
%                    - These slx files are assumed NOT to be nested in inner
%                      directories i.e. all slx files are available immediately
%                      inside the oldSlxFolderPath. Any slx file presented in an 
%                      inner directory will be ignored. 
% 
% newSlxFolderPath : (string, optional) absoulte path of the folder where the 
%                    generated new slx-version models are to be saved. 
%                    - The filenames will be the same as the old slx files.
%                    - This argumen is optional. 
%                    - If this argument is not provided or if it is the same
%                      as the same as 'oldSlxFolderPath', the old slx file will
%                      be overridden by the new slx file.

    oldSlxFolderPath = string(oldSlxFolderPath); 
    newSlxFolderPath = string(newSlxFolderPath);
    
    % create new slx-folder if it does not exist already 
    if ~ exist(newSlxFolderPath, 'dir')
        mkdir (newSlxFolderPath); 
    end 
  
    oldSlxFileNames = getSlxFileNamesInSlxFolderPath(oldSlxFolderPath); 
    failedPaths = string.empty; 
    for i=1:length(oldSlxFileNames)
       oldSlxFilePath = fullfile(oldSlxFolderPath, oldSlxFileNames(i)); 
       newSlxFilePath = fullfile(newSlxFolderPath, oldSlxFileNames(i)); 
       bdclose('all')
       try
       updateSlxVersion(oldSlxFilePath, newSlxFilePath)
       catch ME
           bdclose('all')
           disp("*** ERROR: Updating slx version failed for " + oldSlxFilePath);
           disp(ME);
           failedPaths = [failedPaths oldSlxFilePath];
       end 
    end
    
    if ~ isempty(failedPaths)
       disp("Updating slx version failed for the following slx files");
       for i = 1 : length(failedPaths)
          disp(failedPaths(i));
       end
    else 
        disp("All slx-version-updates were successful");
    end 

end 

function slxFileNames = getSlxFileNamesInSlxFolderPath(slxFolderPath)
    slxFilesStruct = dir(fullfile(slxFolderPath, '*.slx*')); 
    slxFileNames = string.empty; 
    for i=1:length(slxFilesStruct)
        slxFileNames = [slxFileNames slxFilesStruct(i).name]; 
    end
end