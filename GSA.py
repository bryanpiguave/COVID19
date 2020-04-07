# -*- coding: utf-8 -*-
def f(x):
    import math
    return x[0]+x[1]+math.sin(x[2])+x[3]


import numpy as np
factores= ['V1','V2','V3','V4']
mean_values = np.array([5,5,25,1])

#Uncertainty index 
unc=5 #Measured in percentage
ub2=ub1=mean_values*(1+unc/100)  # 5% up mean
lb2=lb1=mean_values*(1-unc/100)  # 5% below mean
#Dimensions
nd=len(lb1) #determines number of variables considered in sensitivity analysis
sample_size=10000    #sample size
x=(np.random.rand(sample_size,nd))
one =np.ones(sample_size)
sample1 = (1+2*(x-1)*(unc/100)) # The % moved between plus or minus the unc%
M1 = sample1*mean_values # sample 1
y=(np.random.rand(sample_size,nd))
sample2 = 1+2*(y-1)*(unc/100) # The % moved between plus or minus the unc%
M2 = (sample2*mean_values) # sample 2
z=(np.random.rand(sample_size,nd))
sample3 = 1+2*(z-1)*(unc/100) # The % moved between plus or minus the unc%
M3 = sample3*mean_values # sample 3
lista_N=[]
lista_NTj=[]
NTj=np.zeros((sample_size,nd))



for j in range(nd):
    Nj=np.zeros((sample_size,nd))
    Nj=M2.copy()
    Nj[:,j]=M1[:,j].copy()
    lista_N.append(Nj) 
    NTj=np.zeros((sample_size,nd))
    NTj=M1[:,:].copy()
    NTj[:,j]=M2[:,j].copy()
    lista_NTj.append(NTj) 




# Sizing the output vectors
Ys = np.zeros(sample_size)
YR = np.zeros(sample_size)
YN = np.zeros((sample_size,nd))
YTp = np.zeros((sample_size,nd))
gamma2_list=[]

for i in range(len(M1)):
    Ys[i]=f(M1[i,:])
    YR[i]=f(M2[i,:])
for matrix in range(len(lista_N)):
    for exp in range(len(lista_N[0])):
        YN[exp,matrix]=f(lista_N[matrix][exp,:])
        YTp[exp,matrix]=f(lista_NTj[matrix][exp,:])


f0 = 0.5*(YR.mean()+Ys.mean())
Variance = (sum(Ys*Ys) + sum(YR*YR))/(2*sample_size) - f0*f0
gama2 = (sum(Ys*YR) + sum(YN*YTp))/(2*sample_size)

V=np.zeros(nd)
V_q=np.zeros(nd)
for i in range(nd):
    V[i]= (sum(Ys*YTp[:,i])+sum(YR*YN[:,i])) / (2*sample_size)
    V_q[i] = (sum(Ys*YN[:,i])+sum(YR*YTp[:,i])) / (2*sample_size)
s = (V - f0*f0)/Variance
st = 1 - (V_q - f0*f0)/Variance

sHS = (V - gama2)/Variance
stHS = 1 - (V_q - gama2)/Variance

import matplotlib.pyplot as plt
plt.hist(np.concatenate((Ys,YR)))
plt.show()



labels =['X1','X2',"X3",'X4']
x=np.arange(len(labels))
fig, ax = plt.subplots()
width = 0.30  # the width of the bars
rects1 = ax.bar(x - width/2, list(s), width, label='S')
rects2 = ax.bar(x + width/2, list(st), width, label='ST')
ax.set_ylabel('Scores')
ax.set_xlabel('Variables')
ax.legend()
plt.show()