#!python
#
# Update files(INCAR or KPOINTS) according to input
# Usage:
#   python update_files.py PARAM VALUE
#   e.g. python update_file.py ENCUT 300 [incar_template/kpoints_template folder]

import parser_convtest as genstr
from sys import argv

param = argv[1]
param_val = argv[2]
flag_kp = 0
if param == "KPOINTS":
    flag_kp = 1

if len(argv) > 2:
    template_folder = argv[3]
else:
    template_folder = "."
    #template_file = argv[3]

if flag_kp:
    genstr.kpoint_update(param_val, kpoint_folder = template_folder)
else:
    INCAR_dict, key_order = genstr.incar_parser(INCAR = template_folder + "/INCAR")
    INCAR_dict[param] = param_val
    genstr.incar_write(INCAR_dict, key_order, dst_folder = template_folder)