# -*- coding: utf-8 -*-

import numpy 
factores= ['Infectados','camas','Vulnerables','movilidad']
rango   = [[1,10],[1,10],[0,50],[0.1,2]]
problem = {'num_vars': len(factores), 'names': factores ,'bounds': rango}

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

sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
M1 = sample*mean_values # sample 1

sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
M2 = (sample*mean_values) # sample 2

sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
M3 = sample*mean_values # sample 3


# Sizing the output vectors
Y = numpy.zeros(np)
YR = numpy.zeros(np)
Yp = numpy.zeros((np,nd))
YTp = numpy.zeros((np,nd))

f0 = 0.5 * (YR.mean() + Y.mean());
Variance = (0.5*(1/np))*(sum(Y*Y) + sum(YR*YR)) - f0*f0
Variance=1
gama2 = 1/(2*np) * numpy.transpose(sum(Y*YR) + sum(Yp*YTp))

V = 1/(2*np)* (numpy.transpose(Yp)*Y+ numpy.transpose(YTp)*YR);
Vp = 1/(2*np) * (numpy.transpose(YTp)*Y + numpy.transpose(Yp)*YR);

s = (V - f0*f0)/Variance;
st = 1 - (Vp - f0*f0)/Variance;

sHS = (V - gama2)/Variance
stHS = 1 - (Vp - gama2)/Variance
