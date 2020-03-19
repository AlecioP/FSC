from __future__ import print_function
import random as rnd
import os
import sys

TIME_STEPS = 10
PATIENTS = 100
GENES = [
"ECMicroenv",
"DNAdamage",
"Metastasis",
"Migration",
"Invasion",
"EMT",
"Apoptosis",
"CellCycleArrest",
"GF",
"TGFbeta",
"p21",
"CDH1",
"CDH2",
"VIM",
"TWIST1",
"SNAI1",
"SNAI2",
"ZEB1",
"ZEB2",
"AKT1",
"DKK1",
"CTNNB1",
"NICD",
"p63",
"p53",
"p73",
"miR200",
"miR203",
"miR34",
"AKT2",
"ERK",
"SMAD"]

IS_OUTPUT = [0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

rnd.seed()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.system('rm -R ../data/patients')
os.system('mkdir ../data/patients')

for p in range(0,PATIENTS):
	filename = "expr_data_patient" + str(p) + ".csv"
	create = "touch ../data/patients/" + filename
	os.system(create)
	relative = "../data/patients/"+filename
	FD = open(relative,'w')
	print("gene_name,",end='',file=FD)
	for i in range(0,TIME_STEPS):
		print("T"+str(i)+",",end='',file=FD)
	print("IS_OUTPUT",file=FD)

	for i in range(0,len(GENES)):
		print(str(GENES[i])+",",end='',file=FD)
		for j in range(0,TIME_STEPS):
			print(str(round(rnd.random(),4))+",",end='',file=FD)
		print(str(IS_OUTPUT[i]),file=FD)
	FD.close()
	
