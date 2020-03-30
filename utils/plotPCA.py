import numpy as np
import pandas as pd
import random
from sklearn import svm 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pylab as pl

#Calculate for each output gene the mean value
#over the TH dimension
#Then binarize the outcoming vector according to
#the parameter @PERC
#Return the mean of the binarized vector 
#which in turn is binarized too
def statistical_calc(npa,PERC):
	global PRINT_PERC
	if(PRINT_PERC == False):
		print("Percentual is : " + str(PERC))
		PRINT_PERC = True
	outXth = np.empty((9,7))
	for i in range(0,63):
		outXth[i/7][i%7] = npa[i]
	df=pd.DataFrame(outXth)
	df = df.drop([6],axis=1)
	means = df.mean(axis=0)
	binarized = (means > PERC).astype(int)
	return int(means.mean() > 0.5)

def user_input():
	return np.random.randint(low=0,high=1,size=63)

PRINT_PERC = False

FILE = "data/results.csv"

res = pd.read_csv(FILE,header=None)

noY = res.iloc[0].to_numpy()

for row in range(1,len(res.index)):
	current = res.iloc[row].to_numpy() 
	noY = np.vstack((noY,current))

Y = np.zeros(noY.shape[0])

outcome_calc = statistical_calc

for i in range(0,noY.shape[0]):
	Y[i] = outcome_calc(noY[i],0.5)

features = res.columns

px = res.loc[:, features].values

px = StandardScaler().fit_transform(px)

redX = PCA(n_components=2).fit_transform(px)

MODEL = svm.SVC(kernel='poly', gamma=2)
MODEL.fit(redX,Y)

######################__MODEL_CREATION__######################
#Clear
plt.clf()

#Plot nearest
plt.scatter(MODEL.support_vectors_[:, 0], MODEL.support_vectors_[:, 1], s=80, facecolors='none', zorder=10, edgecolors='k')
#Plot every point
plt.scatter(redX[:, 0], redX[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired, edgecolors='k')


plt.axis('tight')
df = pd.DataFrame(redX)
x_min = df[0].min()
x_max = df[0].max()
y_min = df[1].min()
y_max = df[1].max()

#Define area division resolution
XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
#Create the classifier 
Z = MODEL.decision_function(np.c_[XX.ravel(), YY.ravel()])
# Put the result into a color plot
Z = Z.reshape(XX.shape)



#Color areas of class
plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
#Plot areas edges
plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'], levels=[-.5, 0, .5])

#Set view point and zoom 
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

pn = 0
for tx,ty in zip(redX[:,0],redX[:,1]):
	pn+=1
	if(pn%10 != 0):
		continue
	pl.text(tx, ty, str(pn), color="green", fontsize=12)
pl.margins(0.1)

plt.show()
