# SLX2MDL transformation

---
## INSTALLATION:
  - Linux, MacOS 
    - Make sure '/usr/local/bin/' is in the env var PATH
    - Make sure python3 is installed 
    - Run the script INSTALL.py as follows: 
      - try: ./INSTALL.py 
      - if that does not work, try: sudo ./INSTALL.py  
    - Now, you can use the command 'slx2mdl' (see example usage below) from the command line to use this software. 
  - Windows 
    - Make sure python3 is installed.
    - SLX2MDL can be used in a Windows machine too. No specific installation is required. To use the tool, go to the command prompt and use it as: 
      - python3 <path_to_slx2mdl.py> [options]

---

## ARGUMENTS AND USAGE: 
  - mode
    - specifies the mode in which the tool is to be used. 
    - valid values: 
      - 'single' 
        - default mode 
        - for converting single slx file to mdl format 
        - the output filepath is determined by the argument 'mdl-filepath' 

      - 'batch'
        - for converting multiple slx files to mdl format 
        - the output will be produced in the following directory: 
          ( <current_path>/outputs-<input_slx_directory_name> )

  - slx-filepath
    - relevent only when mode = single 
    - specifies the filepath of the slx file to be converted to mdl format 
    - can be either an absolute path or a relative path 


  - mdl-filepath 
    - relevant only when mode = single 
    - specifies the filepaath of the output mdl file. 
    - can be either an absolute path or a relative path. 
    - optional
    - if not provided, default path ( <current_path>/<input_slx_filename_without_extension>.mdl ) will be used 


  - slx-dirpath
    - relevent only when mode = batch  
    - specifies the path of the folder containing slx files to be convereted
      to mdl format.
    - slx files are assumed to be immediately inside this folder i.e. not
      nested in inner folders  
    - can be either an absolute path or a relative path 


  - exit-on-failure 
    - relevent only when mode = batch 
    - specifies whether to continue processing other slx files if
      transformation failes in any one of them. 
    - In both cases, the error is logged to the file error.log  
    - valid values:
      - 'yes'
        - Transformation stops as soon as an error occurs when transforming
          any one of the slx files. 
        - The output directory will contain results for the conversions made
          so far only.
        - This feature is intended to be used for development purpose only.
          So, it may not be quite useful to the end user.
      - 'no' 
        - default option 
        - Transformation does not stop as soon as an error occurs when 
          transforming any one of the slx files. 
        - The output directory will contains results for all successful 
          conversions. 

  - devt-mode 
    - specifies whether to run the transformation in 'development' mode or in 'production' mode
    - valid values: 
      - 'yes' 
        - working directory is not deleted after transformation completes so that intermediate files 
          produced during the transformation are preserved. These files are helpful for debugging purpose.
        - in 'single' mode, the output mdl file, along with other intermediate files, are available 
          at <current_directory>/working-dir. 
        - in 'batch' mode, the output mdl file, along with other intermediate files, are available at 
          <current_directory>/working-dir-<input_slx_directory_name>. Inside this directory, a separate 
          sub-directory is created for each input slx file. 
      - 'no' 
        - default option 
        - working directory is deleted after transformation completes; intermediate files produced 
          during the tranformation are not available to the user. 
        - in 'single' mode, output mdl filepath is available at current directory unless the 
          argument mdl-filepath is set to some other path. 
        - in 'batch' mode, output mdl files are available immediately inside 
          <current_directory>/outputs-<name_of_input_slx_directory>


  - remove-slx
    - specifies whether to delete the source slx file after the transformation completes successfully
    - relevant only when mode = 'batch' and devt-mode = 'yes' (default option is used in other cases)
    - this is useful during development time when we need to test this tool on a large set of slx files (batch mode), by fixing the transformation logic (mostly adding new components as they are discovered) incrementally as new components are discovered -- we don't want to run the tool again in the slx files that were transformed successfully. 
    - valid options: 
      - 'yes' 
        - original slx file is deleted if the transformation (for this slx file) completes successfully in batch mode 
      - 'no'
        - default option 
        - original slx file is not deleted

  - report-performance 
    - specifies whether to print performance details after executing a slx-to-mdl transformation 
    - valid options:
      - 'yes'
        - prints performance metrics i.e. number_of_lines_in_output_mdl_file, time_taken
        - if devt-mode = yes, the performance metrics are also written in working-dir/performance-report.csv. If mode = batch, the metrics of all slx2mdl conversions are written in the same csv file. 
      - 'no'
        - default option
        - does not print these details 
      
---
## EXAMPLE USAGE (Command line): 
- On Unix-like OS (after installing slx2mdl)
  1. slx2mdl --mode single --slx-filepath a/b/c/mymodel.slx  --mdl-filepath=x/y/z/mymodel_converted.mdl
  2. slx2mdl --mode batch --slx-dirpath a/b/my_slx_files --exit-on-failure no 

- On Windows OS (This approach is valid for Unix-like OS as well)
  1. python3 <path_to_slx2mdl.py> --mode single --slx-filepath a/b/c/mymodel.slx  --mdl-filepath=x/y/z/mymodel_converted.mdl
  2. python3 <path_to_slx2mdl.py> --mode batch --slx-dirpath a/b/my_slx_files --exit-on-failure no 

--- 
## EVALUATION EXPERIMENTS: 
We evaluated SLX2MDL using a corpus of Simulink models curated by Chowdhury et al. This corpus is available to download at https://github.com/verivital/slsf_randgen/wiki/. 

### DATASET PREPARATION: 
The Simulink models included in the corpus are not perfectly suitable for evaluationg SLX2MDL for various reasons explained in our paper. Therefore, we needed to pre-process these models. The following steps were performed to pre-process the corpus and make it suitalbe for evaluating SLX2MDL. 

1. Download the corpus made available by chowdhury et al. from https://drive.google.com/drive/folders/0ByjpWd4Nz7vtd0M1THRaRmF4c1k?resourcekey=0-QdVV_c6L5rumeFsnvRqBEw. 
2. Update Corpus/Github directory by downloading and adding missing Simulink models (These models are not included in the corpus due to licensing issues. However, their github links are provided in the corpus). 
3. Retain only .slx files in the corpus. All other files are not useful for our evaluation purpose. Also update the directory structure such that all these slx files are immediately inside the corresponding directory (github/matlab-central/other/source-forge), that is, they are not nested in inner directories. If this causes filename conflicts, resolve the conflict by adding a numeric suffix to the slx filename. 
4. Remove any .slx files that are invalid. 1 slx file was found to be invalid. 
5. Save all the slx files to R2019b version. Remove any slx files that cannot be updated to this version. 2 slx files were found to fail this conversion. 
6. Convert all slx files to mdl format using Simulink's built-in conversion functionality. Don't delete the original slx files. This conversion gives the ground-truth MDL files with which to compare the results of our transformation. 

### DATASET 
Following above pre-processing, we obtained the following dataset (included in *evaluation/dataset*): 
<pre>
dataset
├── readme.md 
├── mdl_simulink
│   ├── github 
│   ├── matlab-central 
│   ├── other
│   └── source-forge
├── mdl_SLX2MDL
│   ├── outputs-github 
│   ├── outputs-matlab-central 
│   ├── outputs-other
│   └── outputs-source-forge
└── slx
    ├── github 
    ├── matlab-central 
    ├── other
    └── source-forge
</pre>

### RUNNING EVALUATION EXPERIMENTS: 
- After preparing the dataset, we ran SLX2MDL in 'batch' mode for the Simulink models contained in each folder inside *evaluation/dataset/slx*. We then saved the results of the conversion inside *evaluation/dataset/mdl_SLX2MDL*. in corresponding sub-directories. 
- Then, for each transformation, we conducted model comparison between the mdl file produced by SLX2MDL and the mdl file produced by Simulink's comparison tool. We inspected the differences manually, and logged the results in the following csv files. These csv reports are self-explanatory. 
  - slx2mdl - github.csv 
  - slx2mdl - matlab-central.csv 
  - slx2mdl - other.csv 
  - slx2mdl - sourceforge.csv 
- Then, we summarized the results of these log files using *evaluation/print_evaluation_report.py*. 

### RESULTS: 
This script *evaluation/print_evaluation_report.py* produces the following output: 

<pre>
report
{
    "github": {
        "filepath": "slx2mdl - github.csv",
        "total": 339,
        "good transformations": 307,
        "good except for binary files": 28,
        "failed transformations": 0,
        "discarded slx files": 4
    },
    "matlab-central": {
        "filepath": "slx2mdl - matlab-central.csv",
        "total": 171,
        "good transformations": 132,
        "good except for binary files": 39,
        "failed transformations": 0,
        "discarded slx files": 0
    },
    "other": {
        "filepath": "slx2mdl - other.csv",
        "total": 20,
        "good transformations": 15,
        "good except for binary files": 5,
        "failed transformations": 0,
        "discarded slx files": 0
    },
    "sourceforge": {
        "filepath": "slx2mdl - sourceforge.csv",
        "total": 17,
        "good transformations": 17,
        "good except for binary files": 0,
        "failed transformations": 0,
        "discarded slx files": 0
    }
}


summary
{
    "total": 547,
    "good transformations": 471,
    "good except for binary files": 72,
    "failed transformations": 0,
    "discarded slx files": 4
}
</pre>
