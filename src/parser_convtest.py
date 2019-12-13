#!python
#
#a open source code for convergency test for vasp for any parameters
#

import os
import re
import warnings
import numpy as np

def input_parser(INPUT = "INPUT.convtest"):
    # to store the input parameters not in the INCAR or KPOINTS, set the default value
    dict_input = {'VASPRUN' : 0, 'KEEPRESULT' : 'ALL', 'ISTEST' : 1}  
    dict_param = {}  # to store the input parameters of the tag in INCAR or KPOINTS
    flag_multi = 0  #the flag for multi-lines, 1 for multi, 0 for single
    flag_param_start = 0    #the flag for the start of the tag-val pair, it often occure after the PARAM
    list_kw = kwlist_parser()
    fopen = open(INPUT, 'r')
    for eachline in fopen:
        eachline = eachline.strip('\n')
        #print(eachline)
        if not is_blank_comments(eachline):
            eachline = eachline.split("#")[0].strip()  #the content after # is neglected
            filename = re.split("\[|\]", eachline)
            if len(filename) > 1:
                #the file name
                filename = filename[1]
                #print(filename)
            else:
                params = re.split('\s+', eachline)
                tag = params[0].upper()
                if tag == "PARAM" or tag == "PARAMLIST" or tag == "END_PARAMLIST":
                    #the param and value must be in the same line
                    #only the paramlist is allowed to be multi lines
                    if len(params) > 1:
                        #the param and value must be in the same line
                        if tag == "PARAM":
                            #the start of the tag
                            if flag_param_start == 1:
                                raise IOError("No PARAMLIST after PARAM")
                            tag_key = params[1]
                            if is_in_kwlist(tag_key, list_kw):
                                flag_param_start = 1
                            #print(tag_key)
                        elif tag == "PARAMLIST":
                            #the end of the tag
                            if flag_param_start == 0:
                                raise IOError("Multi PARAMLISTs for current PARAM")
                            tag_val_tmp = params[1:]
                            tag_val = paramlist_parser(tag_val_tmp)
                            #print(tag_val)
                            dict_param[tag_key] = tag_val
                            flag_param_start = 0
                    else:
                        #the param and values in different lines
                        #Note, only paramlist can be input by multi lines
                        if tag == "PARAMLIST" :
                            if flag_param_start == 0:
                                raise IOError("Multi PARAMLISTs for current PARAM")
                            if flag_multi == 1:
                                raise IOError("No end mark for current PARAMLIST")
                            flag_multi = 1  # start the multilines
                            tag_val = []
                        elif tag == "END_PARAMLIST" :
                            if flag_multi == 0:
                                raise IOError("redundent end mark for current PARAMLIST")
                            flag_multi = 0
                            dict_param[tag_key] = tag_val
                            flag_param_start = 0
                else:                    
                    if flag_multi :
                        #This case is just read the value of PARAMLIST between the PARAMLIST and END_PARAMLIST
                        tag_val.append(params)
                    else:
                        # in this case, the len of params must lager than 1
                        # That's to say the tag-value pair
                        #if is_in_kwlist(tag, list_kw):
                        #    pass
                        if tag in list_kw:
                            tag_key = tag
                            tag_val_tmp = params[1:]
                            tag_val = paramlist_parser(tag_val_tmp)
                            dict_param[tag_key] = tag_val
                        else:
                            # only two elements in current situation
                            # it means it must be VASPRUN or KEEPRESULT ......
                            dict_input[tag] = params[1]
    return dict_param, dict_input

def incar_parser(INCAR = "./template/INCAR"):
    '''
    The test INCAR file is taken from https://cms.mpi.univie.ac.at/vasp/guide/node91.html
    Input: INCAR
        Requires: the value can't contain space, for example the value for the SYSTEM
    Output :
        INCAR_dict : A dict contains all the parameters(key) in the INCAR file and corresponding settings(value)
        key_order : A list contains all the parameters as the order of the original INCAR file
    '''
    INCAR_dict = {}
    key_order = []
    fopen = open(INCAR, 'r')
    for eachline in fopen:
        eachline = eachline.strip('\n')
        #print(eachline)
        if not is_blank_comments(eachline):
            eachline = eachline.split("#")[0].strip()  #the content after # is neglected
            linei = eachline.split(";")
            for tags in linei:
                #neglect lines not tag-value pairs, such as : Start parameter for this Run:
                tagsi = tags.split("=")
                if len(tagsi) > 1:
                    incar_key = re.split('\s+', tagsi[0].strip())[0]
                    incar_val = re.split('\s+', tagsi[1].strip())[0]
                    INCAR_dict[incar_key] = incar_val
                    key_order.append(incar_key)          
    return INCAR_dict, key_order

def incar_write(INCAR_dict, key_order, dst_folder = "."):
    incar = open(dst_folder + '/INCAR', 'w+')
    for keys in key_order:
        incar.write("%s  =  %s\n" % (keys, INCAR_dict[keys]))
    incar.close()

def kpoint_update(kpoints, kpoint_folder= "."):
    #kpoints support two mode, 1.Only one number, a means a x a x a
    # 2. three numbers: a, b, c, means a x b x c
    # 
    # Note: it's update, so the KPOINTS file keep in the same folder
    if (type(kpoints) is int) or (type(kpoints) is float):
        kpoints = str(int(kpoints))
        kpoints = [kpoints, kpoints, kpoints]
    elif type(kpoints) is str :
        try:
            kpoints = str(int(float(kpoints)))
            kpoints = [kpoints, kpoints, kpoints]
        except Exception as e:
            raise e
    elif type(kpoints) is list and len(kpoints) == 3:
        pass
    else:
        raise IOError('The input of the type of length of kpoints is not correct')
    kp_template = open(kpoint_folder + "/KPOINTS", 'r')
    kp_file = open(kpoint_folder + "/KPOINTStmp", 'w+')
    k_count = 0
    for eachline in kp_template:
        if k_count == 3:
            kp_file.write("  %d  %d  %d\n" % (int(kpoints[0]), int(kpoints[1]), int(kpoints[2])))
        else:
            kp_file.write(eachline)
        k_count = k_count + 1
    kp_template.close()
    kp_file.close()
    os.remove(kpoint_folder + "/KPOINTS")
    os.rename(kpoint_folder + "/KPOINTStmp", kpoint_folder +  "/KPOINTS")

def poscar_update(scale_factor, poscar_folder="."):
    #poscar_update is for EOS
    #Note: this version is only work on the scale factor, as a result, 
    #      using the fractional coordinate
    #INPUT: scale_factor, unit %, range from -10 to 10
    pos_template = open(poscar_folder + "/POSCAR", "r")
    pos_file = open(poscar_folder + "/postmp", "w+")
    pos_count = 0
    for eachline in pos_template:
        if pos_count == 1:
            scale_factor_new = float(eachline.strip("\n").strip())*(1.0 + float(scale_factor)/100.0)
            pos_file.write("%f\n" % scale_factor_new)
        else:
            pos_file.write(eachline)
        pos_count = pos_count + 1
    pos_template.close()
    pos_file.close()
    os.remove(poscar_folder + "/POSCAR")
    os.rename(poscar_folder + "/postmp", poscar_folder + "/POSCAR")
    

def kwlist_parser(KWLIST = "kwlist"):
    # read all the keyword of vasp. INCAR tag + KPOINTS
    list_kw = []
    fopen = open(KWLIST, 'r')
    for eachline in fopen:
        eachline = eachline.strip('\n')
        #print(eachline)
        if not is_blank_comments(eachline):
            list_kw.append(eachline)
    return list_kw

def is_blank_comments(line):
    #to judge the line is blank or comments
    # 1 for blank or comments
    # 0 for not
    flag = 0
    if len(line) < 1:   
        #blank line
        flag = 1
    elif line[0] == "#":    
        #comment line
        flag = 1
    return flag

def is_in_kwlist(kw, kwlist):
    flag = 0
    if kw in kwlist:
        flag = 1
    else:
        warnings.warn("Warning: The keyword " + kw + " is not in the keyword list, and it is neglected.")
    return flag

def paramlist_parser(paramlist):
    #input : paramlist
    #        a list
    if len(paramlist) > 1:
        # if the length is longer than 1, it's just the tag_val
        tag_val = paramlist
    else:
        #the length of paramlist equals to 1, then
        #it must be start..interval..end
        range_param = paramlist[0].split("..")
        range_param = [float(x) for x in range_param]
        range_param = np.arange(range_param[0], range_param[2]+range_param[1], range_param[1])
        tag_val = [str(x) for x in range_param]
    return tag_val

def get_energy(folder_name = "."):
    FileName = folder_name + "/OSZICAR"
    fopen = open(FileName, 'r')
    for eachline in fopen:
        linei = eachline.split("=")
        if len(linei) > 2:
            energy = linei[2].strip().split(" ")[0]
    fopen.close()
    energy = float(energy)
    return Energy

def code_run():
    runstr = "mpirun vasp_std"
    return runstr

'''
INCAR_dict, key_order = incar_parser(INCAR = "template/INCAR")
print(INCAR_dict)
print(key_order)
incar_write(INCAR_dict, key_order)

INPUT_dict = input_parser(INPUT = "INPUT.convtest")
print(INPUT_dict)

kpoints = ['12', '11', '15']
print(type(kpoints))
kpoint_write(kpoints, kpoint_template = "template/KPOINTS")
'''

'''
kw = kwlist_parser(KWLIST = "kwlist")
print(kw)

if "ENCUT" in kw:
    print("True")
'''
