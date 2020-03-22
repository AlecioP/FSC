COMPILER=g++
DEBUGGER=gdb
AVAILABLECORES=4
PTTN=24
FLINE=0
RUN=bin/mpi/bin/mpirun

release :
	$(COMPILER) main.cpp -lmpi -I ./bin/mpi/include -L ./bin/mpi/lib 
	$(RUN) -n $(AVAILABLECORES) ./a.out -pttn=$(PTTN) -fline=$(FLINE)

clean :
	rm ./a.out
	rm -R tmp
	rm -R data/patients
install :
	python utils/fakeData.py
	sh utils/configurempi.sh
