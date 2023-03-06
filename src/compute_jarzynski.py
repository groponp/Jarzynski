#! __program__: Compute Jarzynski - A tool to calculate Free energy from non-equlibrium MD
#! __author__ : Ropón-Palacios G. 
#! __date__   : Thu 2 Mar 17:50, 2023. 
#! __email__  : groponp@gmail.com 

import pandas as pd 
import numpy as np
import time 
import optparse

#! setup class
#!-----------------------------------------------

class IO: 
    def __init__(self):
        pass
        
    def message(self, string):
        print("[INFO    ] {}.".format(string)) 

    def read_file(self, file):
        file_name = file 
        df = pd.read_csv(file_name) 
        matrix_w = df.iloc[:,1:-1].to_numpy()
        row, col = df.shape 
        d =  df.iloc[:,0].to_list() 
        return matrix_w, int(row), int(col-1), d 
    
    def write_ofile(self, ofile_name, pmf_no_beta, pmf_with_beta, d):
        dict_name = dict()
        dict_name["DISTANCE"] = d
        dict_name["PMF_NO_BETA"] = pmf_no_beta
        dict_name["PMF_WITH_BETA"] = pmf_with_beta 

        df = pd.DataFrame.from_dict(dict_name)
        df.to_csv(ofile_name, index=False) 

    def usage(self): 
        print("[USAGE    ] \"%opt1: python jarzynski.py pmf -f work_matrix.csv -o reconstructed_PMF.csv -t 300 -e gmx\"")
        print("[USAGE    ] \"%opt2: python jarzynski.py pmf --file=work_matrix.csv -ofile=reconstructed_PMF.csv --temperature=300 --engine=gmx\"")

    def main(self):
        info=f"""<Compute Jarzynski Equality>""" + "\n" + """wrote by: Ropón-Palacios G."""
    
        parser = optparse.OptionParser(description=info, version="%prog v1.0.3")
        parser.add_option("-f", "--ifile", help="Name of the input file, units inputs:  Distance [nm] and Work [kJ/mol]", type=str)
        parser.add_option("-o", "--ofile", help="Name of the output file, units output: PMF [kJ/mol]", type=str)
        parser.add_option("-e", "--engine", help="Engine that you use to compute [namd, gmx]", type=str)
        parser.add_option("-t", "--temperature", help="Absolute temperature the MD [K]", type=float)    
        parser.add_option("-u", "--usage", help="Print usage", action="store_true", dest="usage")

        opts, args = parser.parse_args()
        return opts



class Jarzynski(IO):
    def __init__(self, file, T, engine):
        self.T = T
        self.engine = engine                                      #! Temperature in K units.
        if self.engine == "gmx":
            self.kb = 0.001982923700 * 4.1840                     #! Boltzmann constant in kJ/mol*K units. 
        else:
            self.kb = 0.001982923700                              #! Boltzmann constant in kcal/mol*K units. 
        self.beta = 1/(self.kb*self.T)                            #! Beta' Boltzmann value. 
        self.Te  = self.kb*self.T                                 #! Thermal energy
        self.file = str(file) 
        self.m, self.r, self.c, self.d = super().read_file(file)
        self.cum_work = self.cummulative_work() 
        self.w1_avg, self.w2_avg_sq, self.w0_avg = self.compute_2do_expasion()

    def cummulative_work(self):
        cum_work = np.cumsum((self.m*0.1*0.01), axis=0)   #! Sum work by column , axis =0.
        #cum_work = np.cumsum(self.m, axis=0)   #! Sum work by column , axis =0.
        return cum_work 
    
    def compute_2do_expasion(self):
        """
        Calcualte work as <w^2>, <w>^2 and <w>.
        """
        #! calculate <w^2>
        w1_square = np.zeros((self.r, self.c))          #! Create a matrix of numpy with r, c shape.
        w1_square = np.square(self.cum_work) 
        w1_average = w1_square.mean(axis=1)

        #! calculate <w>^2
        w2_average = self.cum_work.mean(axis=1)
        w2_average_squared = np.square(w2_average) 

        #! calculate <w>
        w0_average = self.cum_work.mean(axis=1) 

        return w1_average, w2_average_squared, w0_average
    
    def reconstruct_PMF(self): 
        """
        Principal function to calculate PMF 
            - In this function we are going to reconstruct PMF, through the iterate of 
            work values calculate before. 

            Eq:
            ------------------
             PMF = <W> -1/2βσ^2,                                                  
                     where σ^2 is:  σ^2 = <W^2>-<W>^2. 
        """
        diff_w1_w2 = []
        zip_object = zip(self.w1_avg, self.w2_avg_sq)

        for i,j in zip_object:
            diff_w1_w2.append(i-j)

        pmf_no_beta = []
        pmf_with_beta = [] 

        m, r,c,d = super().read_file(self.file) 

        for i in range(len(self.w0_avg)):
            deltaG1 = self.w0_avg[i]-(diff_w1_w2[i])     
            deltaG2 = self.w0_avg[i]-(0.5*self.beta*diff_w1_w2[i])
            pmf_no_beta.append(deltaG1)
            pmf_with_beta.append(deltaG2)

        return pmf_no_beta, pmf_with_beta, d 

'''
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
        IO().message("Reading Non-equilibrium dynamics data.")
        time.sleep(1)
        IO().message("Reconstruct PMF from Non-equilibrium dynamics.")
        time.sleep(1)
        pmf1, pmf2,d = Jarzynski(file=opts.file).reconstruct_PMF()  
        IO().message("Writng Ofile to {}".format())
        IO().write_ofile(ofile_name=opts.ofile, pmf_no_beta=pmf1, pmf_with_beta=pmf2, d=d)
        IO().message("Done.")
'''




