import pandas as pd
import numpy as np
import os
import sys
import pdb
import time

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
	#pdb.set_trace()
	#Change working directory to the one containing this script
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	#Input files directory
	PATIENTS_DATA = "data/patients/"
	#Clear configuration files directory
	os.system('rm -R tmp')
	os.system('mkdir tmp')
	#Create results directory
	os.system('mkdir tmp/simoutput')
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
	#Timing variables
	start_t = 0
	finish_t = 0
	start_th = 0
	finish_th = 0
	
	#Pandas::read_csv to load file
	expr = pd.read_csv(data_filename, converters = {'IS_OUTPUT':parse_if_number})
	#Extract output genes' names
	outgenes = (expr[expr.IS_OUTPUT==1]).gene_name
	#Extract not output genes' names
	genes = (expr[expr.IS_OUTPUT==0]).gene_name
	#Extract not output genes' data
	expr = expr[expr.IS_OUTPUT==0]
	pure_data = expr.drop(['gene_name','IS_OUTPUT'],axis=1)
	#Number of colums of data table
	data_columns = pure_data.shape[1]
	
	#Create the vector describing the simulation for the patient
	each_token = (outgenes.size+1)
	patient_description = np.full(shape=10*each_token,fill_value=-1)

	#Iteration for the single patient over the temporal dimension
	for i in range(0,data_columns):
		start_t= time.time()
		column = pure_data['T'+str(i)]
		netIn = np.array([])
		#Conversion from string to float of the column 
		for data in column.iteritems():
			to_append = float(data[1])
			netIn = np.append(netIn,to_append)
		b = np.array([])
		#Write the configuration file for Maboss

		#Iterate all possible threshold values
		for th in range(1,11):
			start_th= time.time()
			s = 0.1*th
			#Binarize expression vector according to threshold
			b = binarize(netIn,s)
			#Formatting the vector for Maboss
			configuration = "\""
			for j in range(0,b.size):
				configuration = configuration + str(genes.iloc[j]) + ".istate=" + str(int(b[j])) + ";\n"
			configuration = configuration + "\""
			#Write *.cfg file for the current simulation
			noExtFile = "sim_th="+str(s)+"T="+str(i)+"ptt="+str(patient)
			conFile = noExtFile + ".cfg"
			cmd = "echo " + configuration + " 1>tmp/"+conFile
			os.system(cmd)
			#Find out os 
			binDir = ''
			if(sys.platform.startswith('linux')):
				binDir = 'linux-x86'
			elif(sys.platform.startswith('win32') or sys.platform.startswith('cygwin')):
				binDir = 'win-x86'
			elif(sys.platform.startswith('darwin')):
				binDir = 'macos-x86'
			else:
				raise Exception("Operative system is not supported. Aborting...")
			#Write the command
			simulate = "bin/maboss/"+binDir+"/MaBoSS -c tmp/"+conFile+" -c data/configuration.cfg" \
				+" -o tmp/simoutput/"+noExtFile+"__ data/grn.bnd"
			#Start the simulation
			os.system(simulate)
			#Read fixed points output file
			fixedfile = "tmp/simoutput/"+noExtFile + "___fp.csv"
			FXP = pd.read_csv(fixedfile,converters={'Proba':parse_if_number},skiprows=1,sep='\t')
			
			#Init result vector
			simresult = np.zeros(outgenes.size)
			#Select fixed points with probability more than threshold
			fpCol = FXP[FXP.Proba>s]
			if(fpCol.empty==True):
				finish_th = time.time()
				th_time = finish_th-start_th
				print("Threshold iteration time elapsed : " + str(th_time))
				continue
			#Extract states in the fixed point
			fixed_point = fpCol.iloc[0].State
			fp_genes = fixed_point.split(' -- ')
			#Generate result vector from extracted genes of the fixed point
			resindex = 0
			for el in outgenes.iteritems():
				if(el[1] in fp_genes):
					simresult[resindex] = 1
				resindex+=1
			simresult = np.append(simresult,i)
			
			if(patient_description[(th-1)*each_token + (each_token-1)]==-1):
				for fill in range(0,each_token):
					patient_description[(th-1)*each_token+fill] = simresult[fill]
			finish_th= time.time()
			th_time = finish_th-start_th
			print("Threshold iteration time elapsed : " + str(th_time))
		#END_FOR TH
		finish_t = time.time()
		t_time = finish_t-start_t
		print("Time iteration time elapsed : " + str(t_time))
	#END_FOR TIME
	print(patient_description)
#END_DEF PATIENT_SIMULATION	
main()
