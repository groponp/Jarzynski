#! __program__: Compute Kd - A tool for compute Dissociation constant (Kd) from Jarzynski PMF.
#! __author__ : Ropón-Palacios G. 
#! __date__   : Thu 4 Mar 10:55, 2023. 
#! __email__  : groponp@gmail.com 

import pandas as pd 
import numpy as np
import time 
import optparse

#! #! setup class
#!-----------------------------------------------

class IO: 
    def __init__(self):
        pass
        
    def message(self, string, type="INFO"):
        if type == "INFO":
            print("[INFO    ] {}.".format(string))
        else:
            print("[ERROR   ] {}".format(string)) 

    def read_file(self, file):
        file_name = file 
        df = pd.read_csv(file_name) 
        pmf1_min, pmf1_max = df.iloc[:1,1].values[0] , df.iloc[-1:,1].values[0]  #! PMF_NO_BETA
        pmf2_min, pmf2_max = df.iloc[:1,2].values[0] , df.iloc[-1:,2].values[0]  #! PMF_WITH_BETA

        return pmf1_min, pmf1_max, pmf2_min, pmf2_max 
    
    def write_ofile(self, ofile_name, kd1, kd2, unit):
        dict_name = dict()
        dict_name["Kd_TYPE"] = ["Kd1", "Kd2"]
        dict_name["Kd_VAL"] = [kd1, kd2]
        dict_name["UNITS"] = [unit, unit]
        dict_name["DESCRIPTION"] = ["PM_NO_BETA", "PMF_WITH_BETA"]

        df = pd.DataFrame.from_dict(dict_name)
        df.to_csv(ofile_name, index=False) 

    def usage(self): 
        print("[USAGE    ] \"%opt1: python jarzynski.py kd -f PMF.csv -o kd.csv -u nM -b 1000 -t 300 -e gmx\"")
        print("[USAGE    ] \"%opt2: python jarzynski.py kd --file=PMF.csv --ofile=kd.csv --units=nM --box_volume=1000 --temperature=300 --engine=gmx\"")

    def main(self):
        info=f"""<Compute Dissosiation constant from PMF>""" + "\n" + """wrote by: Ropón-Palacios G."""
    
        parser = optparse.OptionParser(description=info, version="%prog v1.0")
        parser.add_option("-f", "--ifile", help="Name of the input file", type=str)
        parser.add_option("-u", "--units", help="Units of the output. [M, mM, nM]", type=str)
        parser.add_option("-o", "--ofile", help="Name of the output file", type=str)
        parser.add_option("-b", "--box_volume", help="Volume of box used in nm^3", type=float)   
        parser.add_option("-t", "--temperature", help="Absolute temperature [K]", type=float)  
        parser.add_option("-e", "--engine", help="Engine that you used to compute [namd, gmx]", type=str)
        parser.add_option("--usage", help="Print usage", action="store_true", dest="usage")

        opts, args = parser.parse_args()
        return opts

class Kd(IO):
    def __init__(self, file, boxVol, T, engine):
        self.file = file 
        self.engine = engine 
        self.T = T                                                #! Absolute temperature in K.
        self.pmf1_min, self.pmf1_max, self.pmf2_min, self.pmf2_max = super().read_file(self.file) 
        if self.engine == "gmx":
            self.kb = 0.001982923700 * 4.1840                     #! Boltzmann constant in kJ/mol*K units. 
        else:
            self.kb = 0.001982923700                              #! Boltzmann constant in kcal/mol*K units. 
        self.beta = 1/(self.kb*self.T)                            #! Beta' Boltzmann value. 
        self.boxVol = boxVol                                      #! Box volumen of simulation. 
        self.Ccomp  = self.boxVol                                 #! Computational concentrarion used, unit A^3
        self.Cstandard = 1/1661                                   #! Standard concentration, unit in A^3
    
    def deltaG(self):
        dG1 = float(self.pmf1_max - self.pmf1_min)  #! PMF_NO_BETA
        dG2 = float(self.pmf2_max - self.pmf2_min)  #! PMF_WITH_BETA

        dG1_bind = dG1 + self.beta * np.log(self.Ccomp/self.Cstandard)
        dG2_bind = dG2 + self.beta * np.log(self.Ccomp/self.Cstandard)

        return dG1_bind, dG2_bind


    def compute_kd(self, unit):
        dG1_bind, dG2_bind = self.deltaG()
        if unit == "M":
            kd1 =  np.exp(dG2_bind/self.beta) #! PMF_NO_BETA
            kd2 =  np.exp(dG2_bind/self.beta) #! PMF_WITH_BETA
            return kd1, kd2, unit
        
        elif unit == "mM":
            kd1 =  (np.exp(dG2_bind/self.beta)) * 1E6 #! PMF_NO_BETA
            kd2 =  (np.exp(dG2_bind/self.beta)) * 1E6 #! PMF_WITH_BETA
            return kd1, kd2, unit

        elif unit == "nM":
            kd1 =  (np.exp(dG2_bind/self.beta)) * 1E9 #! PMF_NO_BETA
            kd2 =  (np.exp(dG2_bind/self.beta)) * 1E9 #! PMF_WITH_BETA
            return kd1, kd2, unit

        else:
            super().message("You haven't select any unit")

''''
#! Invoke to class and methods
#!-----------------------------------------------
if __name__ == '__main__': 
    import pandas as pd 
    import numpy as np
    import time 
    import optparse

    opts = IO().main()

    if opts.usage:
        IO().usage()

    else:
        IO().message("Start to compute Dissociation constant [Kd].")
        time.sleep(2)
        kd1, kd2, unit = Kd(file=opts.file, boxVol=opts.box_volume).compute_kd(unit=opts.unit)
        IO().message("Wrote output file.")
        IO().write_ofile(ofile_name=opts.ofile, kd1=kd1, kd2=kd2, unit=unit)

'''
   
