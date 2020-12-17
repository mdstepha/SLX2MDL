function cleanSlxFilepathFolder(folderPath)
% Change the names of slx files in given folder , if necessary, to make it a valid filename that can be
% loaded in matlab
% 
% assumption: slx files are immediately inside the folder
% 
% parameters: 
% -----------
% folderPath: (string) absoulte path of folder containing simulink model 
%             files
% 

    folderPath = string(folderPath); 
    oldSlxFileNames = getSlxFileNamesInSlxFolderPath(folderPath);
    
    oldSlxFilePaths = string.empty; 
    for i = 1 : length(oldSlxFileNames)
        oldSlxFileName = oldSlxFileNames(i);
        oldSlxFilePath = fullfile(folderPath, oldSlxFileName);
        oldSlxFilePaths = [oldSlxFilePaths oldSlxFilePath]; 
    end
    
    for i = 1 : length(oldSlxFilePaths)
        oldSlxFilePath = oldSlxFilePaths(i);
        newSlxFilePath = cleanSlxFilepath(oldSlxFilePath);
        % if filepath gets changed by the 'cleaning' action, rename 
        if oldSlxFilePath ~= newSlxFilePath
            disp(oldSlxFilePath + " --> " + newSlxFilePath); 
            movefile(oldSlxFilePath, newSlxFilePath);
        end 
    end


end

function slxFileNames = getSlxFileNamesInSlxFolderPath(slxFolderPath)
    slxFilesStruct = dir(fullfile(slxFolderPath, '*.slx*')); 
    slxFileNames = string.empty; 
    for i=1:length(slxFilesStruct)
        slxFileNames = [slxFileNames slxFilesStruct(i).name]; 
    end
end