#!/usr/bin/python3 

import os 
import glob 

dataset = 'github'
dataset = 'matlab-central'
# dataset = 'source-forge'
# dataset = 'other'

csv_filepath = f"/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/devt/slx2mdl - {dataset}.csv"
models_sheet = []

with open(csv_filepath, 'r') as file: 
    for i in range(5): # first 5 lines are headers
        file.readline() 
    for line in file.readlines():
        line = line.strip()
        tokens = line.split(',')
        model = tokens[1]
        model += ".slx"
        models_sheet.append(model)


print(f"# models in sheet (all): {len(models_sheet)}")
models_sheet = set(models_sheet)
print(f"# models in sheet (unique): {len(models_sheet)}")

models_corpus = glob.glob(f'/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus/{dataset}/*.slx')
models_corpus = [os.path.basename(x) for x in models_corpus]
print(f"# models in corpus (all): {len(models_corpus)}")
models_corpus = set(models_corpus)
print(f"# models in corpus (unique): {len(models_corpus)}")


models_only_sheet = models_sheet.difference(models_corpus)
models_only_corpus = models_corpus.difference(models_sheet)

print(f"\nmodels only sheet:") 
for x in models_only_sheet:
    print(x)

print(f"\nmodels only corpus:") 
for x in models_only_corpus:
    print(x)

    

