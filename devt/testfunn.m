function slxFilepaths = testfunn(slxFolderpath)
    slxFilesStruct = dir(fullfile(slxFolderpath, '*.slx*')); 
    slxFilepaths = string.empty; 
    for i=1:length(slxFilesStruct)
        slxFilepath = fullfile(slxFolderpath, slxFilesStruct(i).name); 
        slxFilepaths = [slxFilepaths slxFilepath]; 
    end
end