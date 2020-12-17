#!/usr/bin/python3

# This script print the count of slx (good, bad, total) and mdl files for original and processed corpus 


import os 
import glob 
import json 


# path_corpus_original = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-mdls-slxs.bak'
path_corpus_original = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-mlds-slxs-copy-github-united'
path_corpus_processed = '/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus'

datasets = ['github', 'matlab-central', 'other', 'source-forge']

summary = {}
slx_total_all = []
slx_good_all = [] 
for dataset in datasets:
    slx_total = glob.glob(f'{path_corpus_original}/{dataset}/slxs/*.slx')
    slx_good = glob.glob(f'{path_corpus_processed}/{dataset}/*.slx')
    mdl_total = glob.glob(f'{path_corpus_original}/{dataset}/mdls/*.mdl')

    # because this file (this is a 'bad' slx file) is not picked by the above regex
    if dataset == 'github':
        slx_total.append('/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-mlds-slxs-copy-github-united/github/slxs/._double_integrator.slx')

    slx_total_all += slx_total 
    slx_good_all += slx_good
    
    summary[dataset] = {
        'slx_total': len(slx_total),
        'slx_good': len(slx_good),
        'slx_bad': len(slx_total) - len(slx_good),
        'mdl_total': len(mdl_total), 
        'models_total': len(slx_total) + len(mdl_total),
    }

# # correction for 'github' dataset (because model '._double_integrator.slx' is not captured by above regex )
# summary['github']['slx_total'] += 1
# summary['github']['slx_bad'] += 1


summary['TOTAL'] = {}
keys = summary['github'].keys()
for key in keys:
    summary['TOTAL'][key] = 0
    for dataset in datasets:
        summary['TOTAL'][key] += summary[dataset][key]


print('\n\nSUMMARY:')
print(json.dumps(summary, indent=4))

#---------------------------------------------------
# print 'bad' slx files
slx_total_all = [os.path.basename(x) for x in slx_total_all]
slx_good_all = [os.path.basename(x) for x in slx_good_all]

slx_total_all = set(slx_total_all)
slx_good_all = set(slx_good_all)

slx_bad_all = slx_total_all.difference(slx_good_all)

print("\n\nBAD SLX FILES:")
for x in slx_bad_all:
    print(x)
