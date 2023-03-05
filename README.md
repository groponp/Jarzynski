# Jarzynski Tool
This repository contains a python script, which allows to rebuild the PMF based on the Jarzysnki Equality framework. For this you need to pass a file in CSV format, where you have the work values ​​(kcal/mol/A) of all the replicas, the first column has to be the distance in (Angstrom). If you have any questions, you can contact me at groponp@gmail.com.

<img src="figures/slide_3.jpeg">

## Usage Jarzynski 
```bash
python compute_jarzynski.py --usage 

#! Return 
[USAGE    ] "%opt1: python compute_jarzynski.py -f work_matrix.csv -o reconstructed_PMF.csv"
[USAGE    ] "%opt2: python compute_jarzynski.py --file=work_matrix.csv -ofile=reconstructed_PMF.csv"
```

## Usage Kd 
```
python computeKd.py --usage 

#! Return 
[USAGE    ] \"%opt1: python computeKd.py -f PMF.csv -o kd.csv -u nM -b 1000.0"
[USAGE    ] \"%opt2: python computeKd.py --file=PMF.csv --ofile=kd.csv --units=nM --box_volume=1000.0"

    def main(self):
```


## License 
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)