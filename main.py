import pandas as pd
import numpy as np
import os
import sys

def parse_if_number(s):
	try: return float(s)
	except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
	return np.fromstring(s, sep=' ') if s else None

def binarize(array,th):
	b = np.array([]) 
	for v in np.nditer(array):
		if(v>th):
			b = np.append(b,1)
		else:
			b = np.append(b,0)
	return b
def main():
	#Change working directory to the one containing this script
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	#Input files directory
	PATIENTS_DATA = "data/patients/"
	#Clear configuration files directory
	os.system('rm -R tmp')
	os.system('mkdir tmp')
	#Count input files
	cmd = "ls -ld " + PATIENTS_DATA + "* | wc -l"
	output = os.popen(cmd).read().rstrip()
	#Load files
	all_files = os.listdir(PATIENTS_DATA)
	#Iterate patients
	for f in range(0,int(output)):
		complete = PATIENTS_DATA + all_files[f]
		patient_simulation(complete,f)

	
# @data_filename : relative path + filename of the input file
# @patient : integer representing the id of the patient
def patient_simulation(data_filename,patient):
	
	#Pandas::read_csv to load file
	expr = pd.read_csv(data_filename, converters = {'IS_OUTPUT':parse_if_number})
	#Extract not output genes' names
	genes = (expr[expr.IS_OUTPUT==0]).gene_name
	#Extract not output genes' data
	expr = expr[expr.IS_OUTPUT==0]
	pure_data = expr.drop(['gene_name','IS_OUTPUT'],axis=1)
	#Number of colums of data table
	data_columns = pure_data.shape[1]

	#Iteration for the single patient over the temporal dimension
	for i in range(0,data_columns):
		column = pure_data['T'+str(i)]
		netIn = np.array([])
		#Conversion from string to float of the column 
		for data in column.iteritems():
			to_append = float(data[1])
			netIn = np.append(netIn,to_append)
		b = np.array([])
		#Write the configuration file for Maboss

		#Iterate all possible threshold values
		for th in range(1,10):
			s = 0.1*th
			#Binarize expression vector according to threshold
			b = binarize(netIn,s)
			#Formatting the vector for Maboss
			configuration = "\""
			for j in range(0,b.size):
				configuration = configuration + str(genes.iloc[j]) + ".istate=" + str(int(b[j])) + "\n"
			configuration = configuration + "\""
			#Write *.cfg file for the current simulation
			cmd = "echo " + configuration + " 1>tmp/sim_th="+str(s)+"T="+str(i)+"ptt="+str(patient)+".cfg"
			os.system(cmd)
	
main()
