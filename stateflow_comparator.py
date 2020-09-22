#!/usr/bin/python3 

import sys 

file1 = sys.argv[1]
file2 = sys.argv[2]

lines1 = []
lines2 = [] 

n_multiline_strings = 0 
start = False 
with open(file1) as file:
    for line in file: 
        if line.startswith('Stateflow {'): 
            start = True 
        if start: 
            line = line.strip() 
            if line.startswith('"'): 
                n_multiline_strings += 1 
                continue 
            if line: 
                lines1.append(line)

start = False 
with open(file2) as file: 
    for line in file: 
        if line.startswith('Stateflow {'): 
            start = True 
        if start: 
            line = line.strip() 
            if line: 
                lines2.append(line)



line__first_tokens1 = [(line, line.split()[0]) for line in lines1]
line__first_tokens2 = [(line, line.split()[0]) for line in lines2]


line__first_tokens1_only = line__first_tokens1[:]
line__first_tokens2_only = line__first_tokens2 

for ln1, t1 in line__first_tokens1:
    for ln2, t2 in line__first_tokens2_only: 
        if t1 == t2: 
            line__first_tokens1_only.remove((ln1, t1))
            line__first_tokens2_only.remove((ln2, t2))
            break  


print('lines in file 1 only:')
print('---------------------')
for ln, t in line__first_tokens1_only:
    print(t, ':', ln)

print('lines in file 2 only:')
print('---------------------')
print()
for ln, t in line__first_tokens2_only:
    print(t, ':', ln)




print() 
print(f"\n\ntotal lines in file 1: {len(lines1)}")
print(f"total lines in file 2: {len(lines2)}")
