#README


*convtest* is an open source code to do the convergence test  by *vasp*. It supports **ANY** parameters.

## Usage

1. Prepare the template of All VASP-needed files [INCAR, POSCAR, POTCAR, KPOINTS]
2. Prepare the INPUT.convtest file to specify the parameters for convergence test.
3. If run the test on HPC using PBS(now, it only support PBS now), prepare the pbs scripts.

## INPUT file format



| Syntax    | States                                                       | Examples                                                     |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| PARAM     | Specify the parameters for convergence test, case insensitive | PARAM    ENCUT                                               |
| PARAMLIST | The value list of the parameters, case insensitive<br />There are two ways to specify the value<br />1. Keep in one line with the PARAMLIST key words<br />2. Multilines(must with end mark  END_PARAMLIST) | 1.For cut-off<br />PARAMLIST 200..30..500(two dots)<br />or<br />PARAMLIST 200 230 260 ... 500<br />2.For KPOINTS<br />PARAMLIST<br />2 3 4<br />3 4 5<br />...<br />END_PARAMLIST |

## Author

Mingqing Liao(廖名情)
liaomq1900127@163.com

Phase Research Lab(PRL) @ Penn State(PSU)

FGMS Group @ Harbin Institute of Technology
