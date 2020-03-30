COMPILER=g++
DEBUGGER=gdb
AVAILABLECORES=4
PTTN=48
FLINE=0
RUN=bin/mpi/bin/mpirun

release :
	$(COMPILER) main.cpp -I bin/mpi/include -L bin/mpi/lib -lmpi
	$(RUN) -n $(AVAILABLECORES) ./a.out -pttn=$(PTTN) -fline=$(FLINE)

clean :
	rm ./a.out
	rm -R tmp
	rm -R data/patients
install :
	python utils/fakeData.py
	sh utils/configurempi.sh
plot:
	python -W ignore utils/plotPCA.py
