function updateSlxVersion(oldSlxFilePath, newSlxFilePath)
% Convert an older slx-formatted simulink model to the version of simulink
% installed in the machine (r2019 for my mac)
% 
% parameters: 
% -----------
% oldSlxFilePath : (string) absoulte path of the old slx file to be converted
% newSlxFilePath : (string, optional) absoulte path of the new slx file to 
%                  be generated. 
%                  - This argument is optional. 
%                  - If this argument is not provided or if it is the same
%                    as the same as 'oldSlxFilePath', the old slx file will
%                    be overridden by the new slx file.


load_system(oldSlxFilePath);
save_system(gcs, newSlxFilePath);
close_system(gcs);

end 