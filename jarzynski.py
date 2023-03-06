import sys
import pandas as pd 
import numpy as np
import time 
import optparse


#! check input of module.
tool = sys.argv[1]

if tool == "pmf":
    from src.compute_jarzynski import IO 
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

elif tool == "kd":
    from src.computeKd import IO 
    opts = IO().main()

    if opts.usage:
        IO().usage()

    else:
        IO().message("Start to compute Dissociation constant [Kd].")
        time.sleep(2)
        kd1, kd2, unit = Kd(file=opts.file, boxVol=opts.box_volume).compute_kd(unit=opts.unit)
        IO().message("Wrote output file.")
        IO().write_ofile(ofile_name=opts.ofile, kd1=kd1, kd2=kd2, unit=unit)

else: 
    IO().message("You haven't select any tool.")
    IO().message("%usage: jarzysnki pmf -h or jarzysnki kd -h")




