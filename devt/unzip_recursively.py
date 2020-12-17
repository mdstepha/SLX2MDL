#!/usr/bin/python3 

# This script unzips a .zip file recursively. (The zip filepath is provided as the argument to this script)
# All zip files (including the nested zip files) are unzipped at their current locations.
# Original zip file is not deleted 

# IMPORTANT: 
# - This script is idempotent. (old extracted files are overridden each time the script executes)
# - path must be absolute          

import os 
import sys 
import zipfile
import glob 

# tracks files/dirs that have been unzipped 
done = [] 

def extract(rootpath):
    ''' If rootpath is *.zip, 
        - its contents are extracted to the same directory as the rootpath. 
        - for the extracted contents, 
          - if it is a zip file, extract() is applied recursively 
          - if it is a directory, extract() is applied recursively
          - it is is any other file, it is ignored.  
        If rootpath is a directory path,
        - extract() is applied to all of its contents.'''



    print(f'rootpath: {rootpath}')
    global done 

    if rootpath in done: 
        return 

    done.append(rootpath) 
    if os.path.isdir(rootpath):  # rootpath is a directory path
        # absolute paths of contents 
        contents = glob.glob(f'{rootpath}/*')
        for c in contents:
            extract(c)   
    elif os.path.isfile(rootpath): # rootpath is a filepath 

        if rootpath.endswith('.zip'):
            extract_to = os.path.split(rootpath)[0]  # directory where the zip file is

            with zipfile.ZipFile(rootpath, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            contents = glob.glob(f'{extract_to}/*')
            for c in contents:
                extract(c) 


if __name__ == '__main__': 
    zip_filepath = sys.argv[1]
    extract(zip_filepath)

    