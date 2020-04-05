COMPILER=g++
DEBUGGER=gdb
AVAILABLECORES=4
PTTN=48
FLINE=0
RUN=bin/mpi/bin/mpirun
LIBS=./bin/mpi/lib/libmpi.a ./bin/mpi/lib/libpmpi.a

release :
	$(COMPILER) main.cpp $(LIBS) -I bin/mpi/include  -v
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
