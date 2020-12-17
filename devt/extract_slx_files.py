#!/usr/bin/python3

# this script copies all slx files (included nested) from a INPUT_DIR into the OUTPUT_DIR 
# If two or more source file's name match (eg: a/b/c.slx, a/x/y/c.slx), 
# the later ones will be renamed (by adding numeric suffix) when copied to the destination folder 

# INPUT_DIR = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/Corpus/Other'
# OUTPUT_DIR = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-slx-models-only/other'

# INPUT_DIR = '/Users/bhisma/courses/cse-700-simvma/Corpus/SourceForge'
# OUTPUT_DIR = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-slx-models-only/source-forge'

# INPUT_DIR = '/Users/bhisma/courses/cse-700-simvma/Corpus/GitHub'
# OUTPUT_DIR = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-slx-models-only/github'

# INPUT_DIR = '/Users/bhisma/courses/cse-700-simvma/Corpus/Matlab Central'
# OUTPUT_DIR = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-slx-models-only/matlab-central'

# INPUT_DIR = '/Users/bhisma/tmp/corpus/corpus-stephan/Corpus/SourceForge'
INPUT_DIR = '/Users/bhisma/tmp/corpus/corpus-downloaded/corpus-github-downloaded'
OUTPUT_DIR = '/Users/bhisma/tmp/corpus-with-downloaded/github-downloaded/mdls'

import os
from shutil import copyfile



for root, dirs, files in os.walk(INPUT_DIR):
    for file in files:
        if file.endswith('.mdl'):
            filenameonly, ext = os.path.splitext(file)
            src = os.path.join(root, file)
            dst = os.path.join(OUTPUT_DIR, file)
            # rename (by adding a numeric suffix) if name clashes with a file already in destination folder 
            if os.path.exists(dst):
                print(f"found duplicate filename: {src}. (This will be renamed.)")
            i = 0
            while os.path.exists(dst):
                i += 1
                dst = os.path.join(OUTPUT_DIR, filenameonly + str(i) + ext)
            copyfile(src, dst)
        