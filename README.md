# slx2mdl-transormation

ARGUMENTS AND USAGE: 
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
  - In both cases, the error is logged to the file error-log.txt  
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
  - specifies whether to run the transformation in 'development' mode or in 'prodution' mode
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
        

EXAMPLE USAGE: 

1. 
./slx2mdl --mode single --slx-filepath a/b/c/mymodel.slx  --mdl-filepath=x/y/z/mymodel_converted.mdl

2. 
./slx2mdl --mode batch --slx-dirpath a/b/my_slx_files --exit-on-failure no 

  

