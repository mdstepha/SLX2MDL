- This directory contains the following sub-directories: 
  1. slx
      - This direcotry contains total of 543 slx files used to conduct the evaluation experiments as discussed in the paper. The slx files grouped into the following four datasets: 
        1. github             (contains 335 slx files)
        2. matlab-central     (contains 171 slx files)
        3. source-forge       (contains 17 slx files)
        4. other              (contains 20 slx files)
      - All of these files are in SLX version R2019b.
      - These files were originally curated and published by Chowdhury et al. (S. A. Chowdhury, L. S. Varghese, S. Mohian, T. T. Johnson, and C. Csall-ner, “A curated corpus of simulink models for model-based empirical stud-ies,”  in2018  IEEE/ACM  4th  International  Workshop  on  Software  Engi-neering  for  Smart  Cyber-Physical  Systems  (SEsCPS).IEEE,  2018,  pp.45–48)

  2. mdl_simulink
     - This directory contains the same files as in the directory slx, but saved in mdl format (using simulink's built-in file-format conversion tools). The results of our transformation will be compared with these models to evaluate the validity of SLX2MDL. 
  3. mdl_SLX2MDL
     - This directory contains the results of SLX2MDL transformation for the files contained in the directory slx. The directory structure is preserved. 
