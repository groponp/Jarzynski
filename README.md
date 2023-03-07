# Jarzynski Tool
This repository contains a python script, which allows to rebuild the PMF based on the Jarzysnki Equality framework. For this you need to pass a file in CSV format, where you have the work values ​​(kcal/mol/A) of all the replicas, the first column has to be the distance in (Angstrom). If you have any questions, you can contact me at groponp@gmail.com.

<img src="figures/slide_3.jpeg">

## Install
```bash
git clone git@github.com:groponp/Jarzynski.git
cd jarzynski 
#! create a conda env or python env to manage it.
conda create -n jarzynski python=3.9
conda activate jarzysnki 
pip install pyinstaller 
pip install -r requirements.txt 

#! make executable to PATH
pyinstaller --onefile jarzynski.py 
cd dist/
exe=`pwd`
echo "export PATH=\"${exe}:$PATH\"" >> ~/.zshrc  #| For macOS 
echo "export PATH=\"${exe}:$PATH\"" >> ~/.bashrc  #| For linux

source ~/.zshrc  #! for macOS
source ~/.bashrc #! for linux

#! test 
cd 
jarzynski pmf -h 

#! return
Usage: jarzynski [options]

<Compute Jarzynski Equality> wrote by: Ropón-Palacios G.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f IFILE, --ifile=IFILE
                        Name of the input file, units inputs:  Distance [nm]
                        and Work [kJ/mol]
  -o OFILE, --ofile=OFILE
                        Name of the output file, units output: PMF [kJ/mol]
  -e ENGINE, --engine=ENGINE
                        Engine that you use to compute [namd, gmx]
  -t TEMPERATURE, --temperature=TEMPERATURE
                        Absolute temperature the MD [K]
  -u, --usage           Print usage
```

## Usage Jarzynski 
```bash
jarzynski pmf --usage 

#! Return 
[USAGE    ] "%opt1: jarzynski pmf -f work_matrix.csv -o reconstructed_PMF.csv -t 300 -e gmx"
[USAGE    ] "%opt2: jarzynski pmf --file=work_matrix.csv --ofile=reconstructed_PMF.csv --temperature=300 --engine=gmx"
```

## Usage Kd 
```bash
jarzynski.py  --usage 

#! Return 
[USAGE    ] "%opt1: jarzynski kd -f PMF.csv -o kd.csv -u nM -b 1000 -t 300 -e gmx"
[USAGE    ] "%opt2: jarzynski kd --file=PMF.csv --ofile=kd.csv --units=nM --box_volume=1000 --temperature=300 --engine=gmx"
```


## License 
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)