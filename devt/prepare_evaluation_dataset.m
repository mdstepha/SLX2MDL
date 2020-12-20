% working_dir = "/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models";
working_dir = "/Users/bhisma/tmp";
corpus_src = "corpus-all.bak";
datasets = ["github", "matlab-central", "other", "source-forge"];
path_logfile = "/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/matlab-scripts/pipeline.log";


path_corpus_bak = working_dir + "/" + corpus_src; 
path_corpus_mdls_slxs = working_dir + "/" + "corpus-mdls-slxs-copy";
path_corpus_mdls_slxs_github_united = working_dir + "/" + "corpus-mdls-slxs-copy-github-united";
path_corpus_slxs = working_dir + "/" + "corpus-slxs";
path_corpus_slxs_valid = working_dir + "/" + "corpus-slxs-valid";
path_corpus_slxs_valid_r2019b = working_dir + "/" + "corpus-slxs-valid-r2019";
path_corpus_slxs_valid_r2019b_with_org_mdls = working_dir + "/" + "corpus-slxs-valid-r2019_with_org_mdls";
path_corpus_output = working_dir + "/" + "corpus";

% empty the log file 
cmd = "echo ' ' > " + path_logfile; disp(cmd); unix(cmd);  


% remove directories recursively, if exist
if exist(path_corpus_mdls_slxs, 'dir')
    rmdir(path_corpus_mdls_slxs, 's');
end 

if exist(path_corpus_mdls_slxs_github_united, 'dir')
    rmdir(path_corpus_mdls_slxs_github_united, 's');
end 

if exist(path_corpus_slxs, 'dir')
    rmdir(path_corpus_slxs, 's');
end

if exist(path_corpus_slxs_valid, 'dir')
    rmdir(path_corpus_slxs_valid, 's');
end

if exist(path_corpus_slxs_valid_r2019b, 'dir')
    rmdir(path_corpus_slxs_valid_r2019b, 's');
end

if exist(path_corpus_slxs_valid_r2019b_with_org_mdls, 'dir')
    rmdir(path_corpus_slxs_valid_r2019b_with_org_mdls, 's');
end 


% cp -r corpus-mdls-slxs.bak corpus-mdls-slxs 
cmd = "cp -r " + path_corpus_bak + " " + path_corpus_mdls_slxs; disp(cmd); unix(cmd);

% create all directories
mkdir(path_corpus_mdls_slxs_github_united); 
mkdir(path_corpus_slxs);
mkdir(path_corpus_slxs_valid);
mkdir(path_corpus_slxs_valid_r2019b);
% mkdir(path_corpus_slxs_valid_r2019b_with_org_mdls);

% populate path_corpus_mdls_slxs_github_united; 
cmd = "cp -r " + path_corpus_mdls_slxs + "/* " + path_corpus_mdls_slxs_github_united; disp(cmd); unix(cmd);
% first: delete directories 'github-downloaded' and 'github-not-downloaded'
cmd = "rm -rf " + path_corpus_mdls_slxs_github_united + "/github*"; disp(cmd); unix(cmd); 
% second: merge repos 'github-downloaded' and 'github-not-downloaded'
cmd = "mkdir -p " + path_corpus_mdls_slxs_github_united + "/github/slxs"; disp(cmd); unix(cmd);
cmd = "mkdir -p " + path_corpus_mdls_slxs_github_united + "/github/mdls"; disp(cmd); unix(cmd); 
cmd = "cp -r " + path_corpus_mdls_slxs + "/github-downloaded/slxs/*.slx " + path_corpus_mdls_slxs_github_united + "/github/slxs/"; disp(cmd); unix(cmd);
cmd = "cp -r " + path_corpus_mdls_slxs + "/github-downloaded/mdls/*.mdl " + path_corpus_mdls_slxs_github_united + "/github/mdls/"; disp(cmd); unix(cmd);
cmd = "cp -r " + path_corpus_mdls_slxs + "/github-not-downloaded/slxs/*.slx " + path_corpus_mdls_slxs_github_united + "/github/slxs/"; disp(cmd); unix(cmd);
cmd = "cp -r " + path_corpus_mdls_slxs + "/github-not-downloaded/mdls/*.slx " + path_corpus_mdls_slxs_github_united + "/github/mdls/"; disp(cmd); unix(cmd);


% populate path_corpus_slxs 
for i = 1 : length(datasets)
    dataset = datasets(i);
    from = path_corpus_mdls_slxs_github_united + "/" + dataset + "/slxs";
    to = path_corpus_slxs + "/" + dataset;
    cmd = "cp -r " + from + " " + to; disp(cmd); unix(cmd);
end

% rename slx files in path_corpus_slxs, if required, to make them valid
for i = 1 : length(datasets)
    dataset = datasets(i);
    folderpath = path_corpus_slxs + "/" + dataset; 
    cleanSlxFilepathFolder(folderpath); 
end


% populate path_corpus_slxs_valid 
unix("echo '' >> " + path_logfile);
cmd = "echo 'INVALID SLX FILES' >> " + path_logfile; disp(cmd); unix(cmd);  

for i = 1 : length(datasets)
    dataset = datasets(i);
    cmd = "mkdir " + path_corpus_slxs_valid + "/" + dataset; disp(cmd); unix(cmd);
    slxFiles = dir(fullfile(path_corpus_slxs + "/" + dataset, '*.slx'));
    for j = 1 : length(slxFiles)
        slxFile = slxFiles(j);
        src = fullfile(slxFile.folder, slxFile.name); 
        bdclose('all')
        try
            load_system(src);
            % if successfully loaded, copy the slx file to path_corpus_slxs_valid
            dst = fullfile(path_corpus_slxs_valid + "/" + dataset, slxFile.name);
            disp(dst);
            copyfile(src, dst);
            close_system(src);
            bdclose('all');
        catch ME 
            bdclose('all');
            cmd = "echo '" + src + "' >> " + path_logfile; disp(cmd); unix(cmd);  
        end 
    end
end


% populate path_corpus_slxs_valid_r2019b
unix("echo '' >> " + path_logfile);
cmd = "echo 'SLX VERSION UPDATE TO R2019 FAILED FOR:' >> " + path_logfile; disp(cmd); unix(cmd);  

for i = 1 : length(datasets)
    dataset = datasets(i);
    cmd = "mkdir " + path_corpus_slxs_valid_r2019b + "/" + dataset; disp(cmd); unix(cmd);
    oldpath = path_corpus_slxs_valid + "/" + dataset;
    newpath = path_corpus_slxs_valid_r2019b + "/" + dataset; 
    failedPaths = updateSlxVersionFolder(oldpath, newpath); 
    for j = 1 : length(failedPaths)
        failedPath = failedPaths(j); 
        cmd = "echo '" + failedPath + "' >> " + path_logfile; disp(cmd); unix(cmd);  
    end
end

% populate path_corpus_slxs_valid_r2019b_with_org_mdls
unix("echo '' >> " + path_logfile);
cmd = "echo 'SLX-TO-MDL CONVERSION (USING MATLAB) FAILED FOR:' >> " + path_logfile; disp(cmd); unix(cmd);  
cmd = "cp -r " + path_corpus_slxs_valid_r2019b + " " + path_corpus_slxs_valid_r2019b_with_org_mdls; disp(cmd); unix(cmd);

for i = 1 : length(datasets)
    dataset = datasets(i);
    folderpath = path_corpus_slxs_valid_r2019b_with_org_mdls + "/" + dataset; 
    failedPaths = slx2mdlFolder(folderpath, folderpath);  
    for j = 1 : length(failedPaths)
        failedPath = failedPaths(j); 
        cmd = "echo '" + failedPath + "' >> " + path_logfile; disp(cmd); unix(cmd);  
    end
end

% finally rename the output dir 'corpus_slxs_valid_r2019b_with_org_mdls' to 'corpus'
cmd = "mv " + path_corpus_slxs_valid_r2019b_with_org_mdls + " " + path_corpus_output; disp(cmd); unix(cmd);


