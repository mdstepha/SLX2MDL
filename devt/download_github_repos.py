#!/usr/bin/python3 

# this script downloads (clones) all the github repos (hyperlinks contained in Corpus/GitHub/github_data.mat)

import os 

download_path = '/Users/bhisma/courses/cse-700-simvma/corpus-github-downloaded/'

# these hyperlinks are contained from Corpus/GitHub/github_data.mat 
links = [
    'https://github.com/mabrauer/hyperloop_sl',
    'https://github.com/WEC-Sim/WEC-Sim',
    'https://github.com/sbuadu/TTK4851',
    'https://github.com/elenaeli/HEV',
    'https://github.com/seanryu99/ATWS',
    'https://github.com/paulhandy/waveguidetripod',
    'https://github.com/lstan972/robot_class_qut',
    'https://github.com/CentroEPiaggio/primitives',
    'https://github.com/lab-automatica-uch/dcmotor',
    'https://github.com/jorgangelov/JorgCopterPos',
    'https://github.com/ndc466/Inverted-Pendulum-Simulation',
    'https://github.com/zhouheng2018/Matlab_Programming',
    'https://github.com/madcowswe/quadMATLAB',
    'https://github.com/Brosengren/ISUCoursework',
    'https://github.com/drosen1967/KalmanProject',
    'https://github.com/quantlabs/MatlabSimulink2CPP',
    'https://github.com/ene21/CPS_Thesis',
    'https://github.com/JoeZhu123/Matlab_Program',
    'https://github.com/mclabNTNU/CS_EnterpriseI_cRIOlab',
    'https://github.com/zhangpn/DiagramLayoutManager',
    'https://github.com/cristovao-trevisan/vent-pendulum-control',
    'https://github.com/Alexanderallenbrown/MotionBase',
    'https://github.com/AU-Eco-Shell-Marathon/MotorController',
    'https://github.com/Alicewithrabbit/MATLAB',
    'https://github.com/nthatte/WaterRunnerProject',
    'https://github.com/zapv1348/ecen5458',
    'https://github.com/dch33/Quad-Sim',
    'https://github.com/nasa/T-MATS',
    'https://github.com/nasa/TTECTrA',
    'https://github.com/analogdevicesinc/MathWorks_tools',
    'https://github.com/steventen/Simulink-Model-Parsing-Tools',
    'https://github.com/coco-team/benchmarks/tree/master/Simulink',
    'https://github.com/kit-cel/simulink-hackrf'
]


for link in links:
    project_name = link.split('/')[-1]
    dstpath = os.path.join(download_path, project_name)
    if not os.path.exists(dstpath):
        cmd = f'git clone {link} {dstpath}'
        print(f'executing: {cmd}')
        os.system(cmd)
    else: 
        print(f"'{dstpath}' exists, skipped.")