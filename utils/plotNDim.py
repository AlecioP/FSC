import numpy as np
import pandas as pd
import random
from sklearn import svm



def naive_calculator(npa):
	#print("naive")
	return 1

#This function takes two matrices of shape
# [n_samples_1 x n_features]
# [n_samples_2 x n_features]
# and returns a matrix of shape
# [n_samples_1 x n_samples_2]
# representing the similarity matrix
# where the value M[i,j] stands for the 
# similarity score between sample i and j
def simKernel(M1,M2):
	KERNEL_EX = ""
	KERNEL_EX = KERNEL_EX + "Cannot compute SVM kernel."
	KERNEL_EX = KERNEL_EX + "Input matrices have different"
	KERNEL_EX = KERNEL_EX + "number of features. Aborting..."
	shape1 = M1.shape
	shape2 = M2.shape
	#Check shape coherence 
	if(shape1[1] <> shape2[1]):
		raise Exception(KERNEL_EXCEPTION)
	#Create empty result matrix
	M = np.empty([shape1[1],shape1[1]])
	#Iterate samples in first Matrix (shape1)
	for i in range(0,shape1[0]):
		#Iterate samples in second Matrix (shape2)
		for j in range(0,shape2[0]):
			counter = 0
			#Compare features for each couple of samples
			#from M1 and M2 respectively
			for k in range(0,shape1[1]):
				#Increment the counter for each match
				if(M1[i][k] == M2[j][k]):
					counter+=1
			#The element of the result matrix is given
			#by the element-wise similarity
			M[i][j] = counter/shape1[1]
	return M


FILE = "results.csv"

res = pd.read_csv(FILE,header=None)

noY = res.iloc[0].to_numpy()

for row in range(1,len(res.index)):
	current = res.iloc[row].to_numpy() 
	noY = np.vstack((noY,current))

Y = np.zeros(noY.shape[0])

outcome_calc = naive_calculator

for i in range(0,noY.shape[0]):
	Y[i] = outcome_calc(noY[i])

xY = np.column_stack((noY,Y))

#debug
Y[0] = 0
#debug
MODEL = svm.SVC(kernel=simKernel)
MODEL.fit(noY,Y)

######################__MODEL_CREATION__######################
def user_input():
	return np.random.randint(low=0,high=1,size=63)
NEW_PATIENT = user_input()

from sklearn.preprocessing import StandardScaler
features = res.columns
# Separating out the features
px = res.loc[:, features].values
# Standardizing the features
px = StandardScaler().fit_transform(px)

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(px)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['P1', 'P2'])
finalDf = principalDf

import matplotlib.pyplot as plt
plt.scatter(finalDf.P1,finalDf.P2,marker="x")

plt.show()