#!python
#

def get_phase(poscar_folder="."):
    #get the phase name and mass
    fid_poscar = open(poscar_folder + "/POSCAR", "r")
    pos_count = 0
    for eachline in fid_poscar:
        if pos_count == 5:
            chem = eachline.strip("\n").strip().split()
        if pos_count == 6:
            chem_num = eachline.strip("\n").strip().split()
        pos_count = pos_count + 1
    chem = [s.capitalize() for s in chem]
    phase = []
    mass = 0
    for i in range(0, len(chem)):
        phase.append(chem[i])
        phase.append((chem_num[i]))
        mass = mass +atom_cfg()[chem[i]][2]*float(chem_num[i])
    phase = "".join(phase)
    return phase, mass

def write_gibbs(evdata = "ConvTest_EOS.txt", poscar_folder="template", units = {'V' : 'ang3', 'E' : 'ev'}, fit = "bm4"):
    phase, mass = get_phase(poscar_folder)
    vfree = 1
    ingfile = phase + ".ing"
    fopen = open(ingfile, 'a')
    fopen.write('mm ' + str(mass) + '\n')
    fopen.write('vfree ' + str(vfree) + '\n')
    fopen.write("pressure 0 \n")
    fopen.write("temperature 0 100 3000 \n")
    fopen.write("phase " + phase + " \\\n")
    fopen.write("      file " + evdata + " \\\n")
    fopen.write("      units energy " + units["E"] + " volume " + units["V"] + " \\\n")
    fopen.write("      fit " + fit + " \n")
    fopen.write("end\n")


def atom_cfg():
    #https://www.nist.gov/pml/periodic-table-elements
    dict_pt = {
    'H' : [1, 'Hydrogen', 1.008, '1s', 13.5984],
    'He': [2,  'Helium', 4.0026, '1s2', 24.5874], 
    'Li': [3,  'Lithium', 6.94, '1s2 2s', 5.3917],
    'Be': [4,  'Beryllium', 9.0122, '1s2 2s2', 9.3227],
    'B' : [5,  'Boron', 10.81, '1s22s22p', 8.2980],
    'C' : [6,  'Carbon', 12.011, '1s22s22p2', 11.2603],
    'N' : [7,  'Nitrogen', 14.007, '1s22s22p3', 14.5341],
    'O' : [8,  'Oxygen', 15.999, '1s22s22p4', 13.6181],
    'F' : [9,  'Fluorine', 18.998, '1s22s22p5', 17.4228],
    'Ne': [10, 'Neon', 20.180, '1s22s22p6', 21.5645],
    'Na': [11, 'Sodium', 22.990, '[Ne]3s', 5.1391],
    'Mg': [12, 'Magnesium', 24.305, '[Ne]3s2', 7.6462],
    'Al': [13, 'Aluminum', 26.982, '[Ne]3s23p', 5.9858],
    'Si': [14, 'Silicon', 28.085, '[Ne]3s23p2', 8.1517],
    'P' : [15, 'Phosphorus', 30.974, '[Ne]3s23p3', 10.4867],
    'S' : [16, 'Sulfur', 32.06, '[Ne]3s23p4', 10.3600],
    'Cl': [17, 'Chlorine', 35.45, '[Ne]3s23p5', 12.9676],
    'Ar': [18, 'Argon', 39.948, '[Ne]3s23p6', 15.7596],
    'K' : [19, 'Potassium', 39.098, '[Ar]4s', 4.3407],
    'Ca': [20, 'Calcium', 40.078, '[Ar]4s2', 6.1132],
    'Sc': [21, 'Scandium', 44.956, '[Ar]3d4s2', 6.5615],
    'Ti': [22, 'Titanium', 47.867, '[Ar]3d24s2', 6.8281],
    'V' : [23, 'Vanadium', 50.942, '[Ar]3d34s2', 6.7462],
    'Cr': [24, 'Chromium', 51.996, '[Ar]3d54s', 6.7665],
    'Mn': [25, 'Manganese', 54.938, '[Ar]3d54s2', 7.4340],
    'Fe': [26, 'Iron', 55.845, '[Ar]3d64s2', 7.9025],
    'Co': [27, 'Cobalt', 58.933, '[Ar]3d74s2', 7.8810],
    'Ni': [28, 'Nickel', 58.693, '[Ar]3d84s2', 7.6399],
    'Cu': [29, 'Copper', 63.546, '[Ar]3d104s', 7.7264],
    'Zn': [30, 'Zinc', 65.38, '[Ar]3d104s2', 9.3942],
    'Ga': [31, 'Gallium', 69.723, '[Ar]3d104s24pp', 5.9993],
    'Ge': [32, 'Germanium', 72.630, '[Ar]3d104s24p2', 7.8994],
    'As': [33, 'Arsenic', 74.922, '[Ar]3d104s24p3', 9.7886],
    'Se': [34, 'Selenium', 78.971, '[Ar]3d104s24p4', 9.7524],
    'Br': [35, 'Bromine', 79.904, '[Ar]3d104s24p5', 11.8138],
    'Kr': [36, 'Krypton', 83.798, '[Ar]3d104s24p6', 13.9996],
    'Rb': [37, 'Rubidium', 85.468, '[Kr]5s', 4.1771],
    'Sr': [38, 'Strontium', 87.62, '[kr]5s2', 5.6949],
    'Y' : [39, 'Yttrium', 88.906, '[Kr]4d5s2', 6.2173],
    'Zr': [40, 'Zirconium', 91.224, '[Kr]4d25s2', 6.6341],
    'Nb': [41, 'Niobium', 92.906, '[Kr]4d45s', 6.7589],
    'Mo': [42, 'Molybdenum', 95.95, '[Kr]4d55s', 7.0924],
    'Tc': [43, 'Technetium', 97, '[Kr]4d55s2', 7.1194],
    'Ru': [44, 'Ruthenium', 101.07, '[Kr]4d75s', 7.3605],
    'Rh': [45, 'Rhodium', 102.91, '[Kr]4d85s', 7.4589],
    'Pd': [46, 'Palladium', 106.42, '[Kr]4d10', 8.3369],
    'Ag': [47, 'Silver', 107.87, '[Kr]4d105s', 7.5762],
    'Cd': [48, 'Cadmium', 112.41, '[Kr]4d105s2', 8.9938],
    'In': [49, 'Indium', 114.82, '[Kr]4d105s25p', 5.7864],
    'Sn': [50, 'Tin', 118.71, '[Kr]4d105s25p2', 7.3439],
    'Sb': [51, 'Antimony', 121.76, '[Kr]4d105s25p3', 8.6084],
    'Te': [52, 'Tellurium', 127.6, '[Kr]4d105s25p4', 9.0097],
    'I' : [53, 'Iodine', 126.90, '[Kr]4d105s25p5', 10.4513],
    'Xe': [54, 'Xenon', 131.29, '[Kr]4d105s25p6', 12.1298],
    'Cs': [55, 'Cesium', 132.91, '[Xe]6s', 3.8939],
    'Ba': [56, 'Barium', 137.33, '[Xe]6s2', 5.2117],
    'La': [57, 'Lanthanum', 138.91, '[Xe]5d6s2', 5.5769],
    'Ce': [58, 'Cerium', 140.12, '[Xe]4f5d6s2', 5.5386],
    'Pr': [59, 'Praseodymium', 140.91, '[Xe]4f36s2', 5.4702],
    'Nd': [60, 'Neodymium', 144.24, '[Xe]4f46s2', 5.5250],
    'Pm': [61, 'Promethium', 145, '[Xe]4f56s2', 5.577],
    'Sm': [62, 'Samarium', 150.36, '[Xe]4f66s2', 5.6437],
    'Eu': [63, 'Europium', 151.96, '[Xe] 4f7 6s2', 5.6704],
    'Gd': [64, 'Gadolinium', 157.25, '[Xe] 4f7 5d 6s2', 6.1498],
    'Tb': [65, 'Terbium', 158.93, '[Xe] 4f9 6s2', 5.8638],
    'Dy': [66, 'Dysprosium', 162.50, '[Xe] 4f10 6s2', 5.9391],
    'Ho': [67, 'Holmium', 164.93, '[Xe] 4f11 6s2', 6.0215],
    'Er': [68, 'Erbium', 167.26, '[Xe] 4f12 6s2', 6.1077],
    'Tm': [69, 'Thulium', 168.93, '[Xe] 4f13 6s2', 6.1843],
    'Yb': [70, 'Ytterbium', 173.05, '[Xe] 4f14 6s2', 6.2542],
    'Lu': [71, 'Lutetium', 174.97, '[Xe] 4f14 5d 6s2', 5.4259],
    'Hf': [72, 'Hafnium', 178.49, '[Xe] 4f14 5d2 6s2', 6.8251],
    'Ta': [73, 'Tantalum', 180.95, '[Xe] 4f14 5d3 6s2', 7.5496],
    'W' : [74, 'Tungsten', 183.84, '[Xe] 4f14 5d4 6s2', 7.8640],
    'Re': [75, 'Rhenium', 186.21, '[Xe] 4f14 5d5 6s2', 7.8335],
    'Os': [76, 'Osmium', 190.23, '[Xe] 4f14 5d6 6s2', 8.4382],
    'Ir': [77, 'Iridium', 192.22, '[Xe] 4f14 5d7 6s2', 8.9670],
    'Pt': [78, 'Platinum', 195.08, '[Xe] 4f14 5d9 6s', 8.9588],
    'Au': [79, 'Gold', 196.97, '[Xe] 4f14 5d10 6s', 9.2256],
    'Hg': [80, 'Mercury', 200.59, '[Xe] 4f14 5d10 6s2', 10.4375],
    'Tl': [81, 'Thallium', 204.38, '[Hg] 6p', 6.1083],
    'Pb': [82, 'Lead', 207.2, '[Hg] 6p2', 7.4167],
    'Bi': [83, 'Bismuth', 208.98, '[Hg] 6p3', 7.2855],
    'Po': [84, 'Polonium', 209, '[Hg] 6p4', 8.414],
    'At': [85, 'Astatine', 210, '[Hg] 6p5', 9.3175],
    'Rn': [86, 'Radon', 222, '[Hg] 6p6', 10.7485],
    'Fr': [87, 'Francium', 223, '[Rn] 7s', 4.0727],
    'Ra': [88, 'Radium', 226, '[Rn] 7s2', 5.2784],
    'Ac': [89, 'Actinium', 227, '[Rn] 6d 7s2', 5.3802],
    'Th': [90, 'Thorium', 232.04, '[Rn] 6d2 7s2', 6.3067],
    'Pa': [91, 'Protactinium', 231.04, '[Rn] 5f2 6d 7s2', 5.89],
    'U' : [92, 'Uranium', 238.03, '[Rn] 5f3 6d 7s2', 6.1941],
    'Np': [93, 'Neptunium', 237, '[Rn] 5f4 6d 7s2', 6.2655],
    'Pu': [94, 'Plutonium', 244, '[Rn] 5f6 7s2', 6.0258],
    'Am': [95, 'Americium', 243, '[Rn] 5f7 7s2', 5.9738],
    'Cm': [96, 'Curium', 247, '[Rn] 5f7 6d 7s2', 5.9914],
    'Bk': [97, 'Berkelium', 247, '[Rn] 5f9 7s2', 6.1978],
    'Cf': [98, 'Califormium', 251, '[Rn] 5f10 7s2', 6.2817],
    'Es': [99, 'Einsteinium', 252, '[Rn] 5f11 7s2', 6.3676],
    'Fm': [100,'Fermium', 257, '[Rn] 5f12 7s2', 6.50],
    'Md': [101,'Mendelevium', 258, '[Rn] 5f13 7s2', 6.58],
    'No': [102,'Nobelium', 259, '[Rn] 5f14 7s2', 6.66],
    'Lr': [103,'Lawrencium', 266, '[Rn] 5f14 7s2 7p', 4.96],
    'Rf': [104,'Rutherfordium', 267, '[Rn] 5f14 6d2 7s2', 6.02],
    'Db': [105,'Dubnium', 268, '[Rn] 5f14 6d3 7s2', 6.8],
    'Sg': [106,'Seaborgium', 269, '[Rn] 5f14 6d4 7s2', 7.8],
    'Bh': [107,'Bohrium', 270, '[Rn] 5f14 6d5 7s2', 7.7],
    'Hs': [108,'Hassium', 269, '[Rn] 5f14 6d6 7s2', 7.6]
    }
    return dict_pt

write_gibbs()