#!/usr/bin/python3 

# ASSUMPTIONS: 
# - The following files are present in current directory: 
#   - slx2mdl - github.csv 
#   - slx2mdl - matlab-central.csv 
#   - slx2mdl - other.csv 
#   - slx2mdl - sourceforge.csv 


import os 
import json 

READABLE = True 

data = {
    'github': {
        'filepath': 'slx2mdl - github.csv',
        'g': 0,
        'bin': 0,
        'x': 0, 
        'dis': 0,
        'total': 0,
    },
    'matlab-central': {
        'filepath': 'slx2mdl - matlab-central.csv',
        'g': 0,
        'bin': 0,
        'x': 0, 
        'dis': 0,
        'total': 0,
    },
    'other': {
        'filepath': 'slx2mdl - other.csv',
        'g': 0,
        'bin': 0,
        'x': 0, 
        'dis': 0,
        'total': 0,
    },
    'sourceforge': {
        'filepath': 'slx2mdl - sourceforge.csv',
        'g': 0,
        'bin': 0,
        'x': 0, 
        'dis': 0,
        'total': 0,
    }
}

missing = 0
summary = {
    'g': 0,
    'bin': 0,
    'x': 0,
    'dis': 0,
    # 'missing': 0,
    'total': 0,
}

for dataset, innermap in data.items():
    filepath = innermap['filepath']
    with open(filepath, 'r') as file:
        for i in range(5): # first 5 lines are headers
            file.readline() 
        for line in file.readlines():
            line = line.strip() 
            if line:
                data[dataset]['total'] += 1
                summary['total'] += 1
                tokens = line.split(',')
                sn, model, status = tokens[:3]
                # print(model)
                status = status.strip() 
                status = status.replace('*', '')
                assert status in ['g', 'bin', 'x', 'dis','']
                if status:
                    innermap[status] += 1
                    summary[status] += 1
                else: 
                    missing += 1
                    # summary['missing'] += 1 
                    print(f'missing status for {dataset}/{model}')


        # rename dict keys (for readable printing)
        if READABLE:
            innermap['good transformations'] = innermap.pop('g')
            innermap['good except for binary files'] = innermap.pop('bin')
            innermap['failed transformations'] = innermap.pop('x')
            innermap['discarded slx files'] = innermap.pop('dis')
        
# rename dict keys (for readable printing)
if READABLE:
    summary['good transformations'] = summary.pop('g')
    summary['good except for binary files'] = summary.pop('bin')
    summary['failed transformations'] = summary.pop('x')
    summary['discarded slx files'] = summary.pop('dis')


print('\n\nreport')
print(json.dumps(data, indent=4))
print("\n\nsummary")
print(json.dumps(summary, indent=4))



    


