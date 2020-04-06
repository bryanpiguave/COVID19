# -*- coding: utf-8 -*-
def f(x):
    return 2*x[0]+x[1]+x[2]+x[3]


import numpy 
factores= ['V1','V2','V3','V4']
mean_values = numpy.array([5,5,25,1])

#Uncertainty index 
unc=5 #Measured in percentage
ub2=ub1=mean_values*(1+unc/100)  # 5% up mean
lb2=lb1=mean_values*(1-unc/100)  # 5% below mean
#Dimensions
nd=len(lb1) #determines number of variables considered in sensitivity analysis
np=1000     #sample size
x=(numpy.random.rand(np,nd))
one =numpy.ones(np)
sample1 = (1+2*(x-1)*(unc/100)) # The % moved between plus or minus the unc%
M1 = sample1*mean_values # sample 1
y=(numpy.random.rand(np,nd))
sample2 = 1+2*(y-1)*(unc/100) # The % moved between plus or minus the unc%
M2 = (sample2*mean_values) # sample 2
z=(numpy.random.rand(np,nd))
sample3 = 1+2*(z-1)*(unc/100) # The % moved between plus or minus the unc%
M3 = sample3*mean_values # sample 3
lista_N=[]
lista_NTj=[]
NTj=numpy.zeros((np,nd))



for j in range(nd):
    Nj=numpy.zeros((np,nd))
    Nj=M2.copy()
    Nj[:,j]=M1[:,j].copy()
    lista_N.append(Nj) 
    NTj=numpy.zeros((np,nd))
    NTj=M1[:,:].copy()
    NTj[:,j]=M2[:,j].copy()
    lista_NTj.append(NTj) 




# Sizing the output vectors
Ys = numpy.zeros(np)
YR = numpy.zeros(np)
YN = numpy.zeros((np,nd))
YTp = numpy.zeros((np,nd))
gamma2_list=[]

for i in range(len(M1)):
    Ys[i]=f(M1[i,:])
    YR[i]=f(M2[i,:])
for matrix in range(len(lista_N)):
    for exp in range(len(lista_N[0])):
        YN[exp,matrix]=f(lista_N[matrix][exp,:])
        YTp[exp,matrix]=f(lista_NTj[matrix][exp,:])


f0 = 0.5*(YR.mean()+Ys.mean())
Variance = (0.5*(1/np))*(sum(Ys*Ys) + sum(YR*YR)) - f0**2
Variance =1
gama2 = (sum(Ys*YR) + sum(YN*YTp))/(2*np)

V=numpy.zeros(nd)
for i in range(nd):
    V[i]= 1/(2*np)* ((sum(Ys*YTp[:,i])+sum(YR*YN[:,i]))-gama2[i])

s = (V - f0*f0)/Variance
import matplotlib.pyplot as plt
plt.hist(numpy.concatenate((Ys,YR)))
plt.show()
#st = 1 - (Vp - f0*f0)/Variance
#sHS = (V - gama2)/Variance
#stHS = 1 - (Vp - gama2)/Variance
