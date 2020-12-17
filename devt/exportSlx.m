path = "/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-slx-models-only-failed-by-matlab-to-convert-to-slx-r2019b/ctrl_student - for MCLAB.slx";
tokens = path.split('.');
path2016A = tokens(1) + "_2016A.slx";
path2016B= tokens(1) + "_2016B.slx";
path2017A = tokens(1) + "_2017A.slx";
path2017B = tokens(1) + "_2017B.slx";
path2018A = tokens(1) + "_2018A.slx";
path2018B = tokens(1) + "_2018B.slx";


open_system(path);
save_system(gcs, path2017A, 'ExportToVersion', 'R2017A');
close_system(path);