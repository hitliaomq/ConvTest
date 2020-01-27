#!python

import convtest
import convtest.convtest_prl as convtest

template_folder = "template"
input_file = "INPUT.convtest"
pbs_file = "convtest.pbs"

convtest.convtest(template_folder, input_file, pbs_file)