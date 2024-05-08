#!/bin/tcsh
#PBS -q long

module load python/3.9
# pip install SALib
cd $PBS_O_WORKDIR

# python /home/orchidee02/quanpan/phd/orchidas/src/orchidas.py task.xml 
# python /home/orchidee02/quanpan/phd/orchidas/src/orchidas.py ./taskBE-Bra1996.xml
