#!/bin/sh
CURRENT=$(pwd)

curl  http://www.mpich.org/static/downloads/3.3.2/mpich-3.3.2.tar.gz --output archive.tar.gz
tar xfz archive.tar.gz
mv mpi* mpich
cd mpich
mkdir ../bin
mkdir ../bin/mpi

PREF="${CURRENT}/bin/mpi"
./configure --prefix=${PREF}
make -j4
make -j4 install

cd ..
rm -R mpich
rm archive.tar.gz
exit
