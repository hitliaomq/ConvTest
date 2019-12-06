#!python
#
#a open source code for convergency test for vasp for any parameters
#
# This code will generate scripts(shell or pbs) for convergence test
# 
# usage:
#   python convtest_prl.py [template_folder] [INPUT.convtest] [pbs_file] 
#   if the input file is the default, then using . to replace the name
#   default value
#       template_folder : template 
#       input_file : INPUT.convtest 
#       pbs_file template/convtest.pbs
# Output:
#   some scripts.
#   convtest_PARAM.sh or convtest_PARAM.pbs

from sys import argv
import random
import warnings
import shutil
import os
import re
import numpy as np
import parser_convtest as cnvt

def write_head():
    pass

# set the default
flag_test = 1
template_folder = "template"
input_file = "INPUT.convtest"
pbs_file = template_folder + "/convtest.pbs"
# handle the input files
if len(argv) > 1 :
    template_folder = argv[1]
    pbs_file = template_folder + "/convtest.pbs"
    if len(argv) > 2 :
        input_file = argv[2]
        if len(argv) > 3 :
            pbs_file = argv[3]

if input_file == ".":
    input_file = "INPUT.convtest"

if not os.path.exists(input_file):
    raise IOError("The input file doesn't exist.")
if not os.path.exists(pbs_file) :
    warnings.warn("pbs file doesn't exist. Shell scripts will be generated.")
    script_ext = ".sh"
    flag_pbs = 0
else:
    script_ext = ".pbs"
    flag_pbs = 1

dict_param, dict_input = cnvt.input_parser(INPUT = input_file)
VASPRUN = int(dict_input["VASPRUN"])
print(VASPRUN)

for PARAM in dict_param:
    os.mkdir(PARAM)
    paramlist = dict_param[PARAM]
    #shutil.copyfile(template_folder + "/*", PARAM)
    #os.chdir(PARAM)
    list_convtest = []
    for param_val in paramlist:
        if type(param_val) is list:
            name_subfolder = PARAM + "/" + "-".join(param_val)
        else:
            name_subfolder = PARAM + "/" + param_val
        os.mkdir(name_subfolder)
        os.system("cp " + template_folder + "/* " + name_subfolder)
        #shutil.copyfile(template_folder + "/*", name_subfolder)
        #os.chdir(name_subfolder)
        print(param_val)
        RunStr = "python3 update_files.py " + PARAM + " " + param_val + " " + name_subfolder
        os.system(RunStr)
        if VASPRUN == 1:
            # run vasp in current folder, don't generate the script file
            os.chdir(name_subfolder)
            if flag_test :
                energy = random.random()
            else:
                os.system("mpirun vasp_std")
                energy = cnvt.get_energy()
            list_convtest.append([param_val, str(energy)])
            os.chdir("../../")
    if VASPRUN == 0 :
        # generate the script for submit the script later
        name_script = "script_" + PARAM + script_ext
        if flag_pbs:
            # pbs script
            pass
        else:
            # shell script
            pass
        pass
    else:
        # generated a list_convtest, write it out
        name_fileout = "ConvTest_" + PARAM + ".txt"
        fid = open(name_fileout, "w")
        for i in range(0, len(list_convtest)):
            fid.write("%s\t\t%s\n" % (list_convtest[i][0], list_convtest[i][1]))
        fid.close()
