#!/usr/bin/python3 

import shutil 
import os 


def install_unix():
    """Install slx2mdl in unix-like OS (macos, linux)"""
    path = os.path.expanduser('~/.SLX2MDL')  # installation directory
    # remove ~/.slx2mdl/ (if exists previously), 
    if os.path.exists(path):
        shutil.rmtree(path)

    # copy all contents of slx-mdl-tranformation/ to ~/.slx2mdl/
    shutil.copytree('../SLX2MDL', path)

    filepath = os.path.expanduser('~/.SLX2MDL/slx2mdl.py')
    symlink_path = '/usr/local/bin/slx2mdl'

    # remove symbolic link, if exists previously
    if os.path.exists(symlink_path):
            os.remove(symlink_path)

    os.system(f"ln -s {filepath} {symlink_path}")

    print("SLX2MDL installed successfully.")
    print("You can now use it from the command line using the command slx2mdl.")    


if __name__ == '__main__': 
    install_unix() 
