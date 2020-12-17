#!/usr/bin/python3

import os 
import glob 

ext = 'mdl'
# ext = 'slx'


path_gh = f'/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-mdls-slxs.bak/github/{ext}s'
path_ghd = f'/Users/bhisma/courses/archive/cse-690-grad-research/slx-mdl-transformation/simulink-models/corpus-mdls-slxs.bak/github-downloaded/{ext}s'

# full path i.e. absolute path 
gh = glob.glob(os.path.join(path_gh,f'*.{ext}'))
ghd = glob.glob(os.path.join(path_ghd,f'*.{ext}'))

# filename only i.e. no folder path 
gh = [os.path.basename(x) for x in gh]
ghd = [os.path.basename(x) for x in ghd]

print(f'# github: {len(gh)}')
print(f'# github downloaded: {len(ghd)}')

gh = set(gh)
ghd = set(ghd)

union = gh.union(ghd)
intersection = gh.intersection(ghd)
only_gh = gh.difference(ghd)
only_ghd = ghd.difference(gh)


print(f"#gh: {len(gh)}")
print(f"#ghd: {len(ghd)}")

print(f"#sum: {len(gh) + len(ghd)}")
print(f"#union: {len(union)}")
print(f"#intersection: {len(intersection)}")


print(f"#only_gh: {len(only_gh)}")
print(f"#only_ghd: {len(only_ghd)}")


print("\n\nONLY github")
only_gh = sorted(only_gh)
for x in only_gh:
    print(x)



