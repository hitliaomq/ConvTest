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
import convtest.parser_convtest as cnvt

def write_head(filename, flag_pbs, pbs_file):
    if flag_pbs:
        # write the head of pbs file
        # in the pbs_file, there is no vasp run code, such as mpirun vasp_std
        os.system("cp " + pbs_file + " " + filename)
    else:
        # wirte the head of sh script
        fid = open(filename, 'w+')
        fid.write("#!sh\n")
        fid.close()

def update_file(param = "EOS", param_val = 0, template_folder = "."):
    if param == "KPOINTS":
        cnvt.kpoint_update(param_val, kpoint_folder = template_folder)
    elif param == "EOS":
        cnvt.poscar_update(param_val, poscar_folder = template_folder)
    else:
        INCAR_dict, key_order = cnvt.incar_parser(INCAR = template_folder + "/INCAR")
        INCAR_dict[param] = param_val
        cnvt.incar_write(INCAR_dict, key_order, dst_folder = template_folder)

'''
# set the default
#flag_test = 1
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
'''

def convtest(template_folder = "template", input_file = "INPUT.convtest", pbs_file = "convtest.pbs"):
    pbs_file = template_folder + "/" + pbs_file

    if input_file == ".":
        input_file = "INPUT.convtest"

    if not os.path.exists(input_file):
        raise IOError("The input file doesn't exist.")

    dict_param, dict_input = cnvt.input_parser(INPUT = input_file)
    VASPRUN = int(dict_input["VASPRUN"])
    KPRESULT = dict_input["KEEPRESULT"]
    flag_test = int(dict_input["ISTEST"])

    if not os.path.exists(pbs_file) :
        if not VASPRUN :
            warnings.warn("pbs file doesn't exist. Shell scripts will be generated.")
        script_ext = ".sh"
        flag_pbs = 0
    else:
        script_ext = ".pbs"
        flag_pbs = 1


    #print(VASPRUN)

    for PARAM in dict_param:
        name_fileout = "ConvTest_" + PARAM + ".txt"
        os.mkdir(PARAM)
        paramlist = dict_param[PARAM]
        #shutil.copyfile(template_folder + "/*", PARAM)
        #os.chdir(PARAM)
        list_convtest = []
        param_val_count = 0
        for param_val in paramlist:
            if type(param_val) is list:
                name_subfolder = PARAM + "/" + "-".join(param_val)
            else:
                name_subfolder = PARAM + "/" + param_val
            os.mkdir(name_subfolder)
            os.system("cp " + template_folder + "/* " + name_subfolder)
            #use the CONTCAR in previous step as the new POSCAR
            if (VASPRUN == 1) and (PARAM != "EOS"):
                if param_val_count > 0:
                    os.system("cp " + name_prefolder + "/CONTCAR " + name_subfolder + "/POSCAR")
                name_prefolder = name_subfolder
                param_val_count = param_val_count + 1
            #shutil.copyfile(template_folder + "/*", name_subfolder)
            #os.chdir(name_subfolder)
            print(param_val)
            update_file(PARAM, param_val, name_subfolder)
            '''
            RunStr = "python3 update_files.py " + PARAM + " " + param_val + " " + name_subfolder
            os.system(RunStr)
            '''
            if VASPRUN == 1:
                # run vasp in current folder, don't generate the script file
                os.chdir(name_subfolder)
                if flag_test :
                    energy = random.random()
                else:
                    os.system(cnvt.code_run())
                    energy = cnvt.get_energy()
                    #os.system("cp CONTCAR POSCAR")
                if PARAM == "EOS":
                    V = cnvt.get_vol()
                    list_convtest.append([param_val, V, str(energy)])
                else:
                    list_convtest.append([param_val, str(energy)])
                os.chdir("../../")
        if VASPRUN == 0 :
            # generate the script for submit the script later
            name_script = "script_" + PARAM + script_ext
            # write the head of the script
            write_head(name_script, flag_pbs, pbs_file)
            # write the loop of the script
            fid = open(name_script, "a+")
            #line_for = "for " + " ".join(paramlist) + ";\n"
            fid.write("for param in " + " ".join(paramlist) + ";\n")
            fid.write("do\n")
            fid.write("cd " + PARAM + "/$param\n")
            # Update the structure. Don't need here, because I have done it before, and created a folder containing all the files
            #RunStr = "python3 update_files.py " + PARAM + " $param " +  PARAM + "/$param"
            #fid.write(RunStr + "\n")
            fid.write(cnvt.code_run() + "\n")
            fid.write("E=`tail -1 OSZICAR | awk '{printf \"%12.6f \\n\", $5}'`\n")
            #fid.write("cp CONTCAR ../../CONTCAR\n")
            fid.write("cd ../../\n")
            fid.write("echo $param $E >> " + name_fileout + "\n")
            #How to get the previous folder name
            #fid.write("cp " + PARAM + "/$param/CONTCAR " PARAM + "/$param/POSCAR\n")
            fid.write("done\n")
            fid.close()
        else:
            # generated a list_convtest, write it out
            
            fid = open(name_fileout, "w")
            for i in range(0, len(list_convtest)):
                for x in list_convtest[i]:
                    fid.write(str(x))
                    fid.write("\t")
                fid.write("\n")
                #if PARAM == "EOS":
                #    fid.write("%s\t%s\t%s\n" % (list_convtest[i][0], list_convtest[i][1], list_convtest[i][2]))
                #else:
                #    fid.write("%s\t%s\n" % (list_convtest[i][0], list_convtest[i][1]))
            fid.close()
            if KPRESULT == "MIN":
                #if KPRESULT is MIN, delete all the generated files in the sub-folder
                os.system("rm -rf " + PARAM)
