#!python
#
# Update files(INCAR or KPOINTS) according to input
# Usage:
#   python update_files.py PARAM VALUE
#   e.g. python update_file.py ENCUT 300 [incar_template/kpoints_template folder]

import parser_convtest as genstr
#from sys import argv

'''
param = argv[1]
param_val = argv[2]

if len(argv) > 2:
    template_folder = argv[3]
else:
    template_folder = "."
    #template_file = argv[3]
'''

def update_file(param = "EOS", param_val = 0, template_folder = "."):
    if param == "KPOINTS":
        genstr.kpoint_update(param_val, kpoint_folder = template_folder)
    elif param == "EOS":
        genstr.poscar_update(param_val, poscar_folder = template_folder)
    else:
        INCAR_dict, key_order = genstr.incar_parser(INCAR = template_folder + "/INCAR")
        INCAR_dict[param] = param_val
        genstr.incar_write(INCAR_dict, key_order, dst_folder = template_folder)