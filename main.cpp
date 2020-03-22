#include <iostream>
#include <cstdlib>
#include <mpi.h>
#include <regex>
#include <string>
using namespace std;

int main(int argc,char** argv){
	//Number of patients to analize
	regex ptt("-pttn=([0-9]+)");
	//First patient to analize
	regex fline("-fline=([0-9]+)");

	int patients,first_line;

	for(int i=0;i<argc;i++){
		size_t st;
		smatch ptt_match,fline_match;
		string option(argv[i]);
//		cout<<"Iteration "<<i<<" option : "<<option<<endl;
		regex_search(option,ptt_match,ptt);
		if(ptt_match.size()>0){ 
			patients = stoi(ptt_match.str(1));
//			cout<<"Iteration "<<i<<" found pttn option..."<<endl;
		}
		regex_search(option,fline_match,fline);
		if(fline_match.size()>0){ 
			first_line = stoi(fline_match.str(1));
//			cout<<"Iteration "<<i<<" found line option..."<<endl;
		}
	}



	MPI_Init(&argc, &argv);

	// Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    if(world_rank==0){
		//Clear configuration files directory
		system("rm -R tmp");
		system("mkdir tmp");
		//Log file
		system("touch tmp/errors.log");
		//Create results directory
		system("mkdir tmp/simoutput");
	}
	MPI_Barrier(MPI_COMM_WORLD);
    if(patients%world_size!=0 && world_rank==0){
    	string warn = "";
    	warn = warn + "Warning : The number of patients is not a";
    	warn = warn + " multiple of the number of cores";
    	cout<<warn<<endl;
    }
    patients = (patients/world_size)*world_size;

    string simulate = "python main.py -num=" + to_string(patients/world_size);
    simulate = simulate + " -start=" + to_string((patients/world_size)*world_rank + first_line);
    if(world_rank==0)
    	simulate = simulate + "-master";
    system(simulate.c_str());

	MPI_Finalize();
	return 0;
}
