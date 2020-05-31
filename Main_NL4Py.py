# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:39:29 2020

@author: Bryan Piguave
"""

import os.path
import pandas as pd
import numpy as np

def simulacion_NL4Py(experiments,ticks,path_to_netlogo,file_to_open):
    import nl4py
    nl4py.startServer(path_to_netlogo)
    workspace=nl4py.newNetLogoHeadlessWorkspace()
    workspace.openModel(file_to_open)
    #Resultados a obtener:    Muertos
    results =[]
    comando=''
    err=[]
    #Parámetros de simulación
    workspace.command('set Poblacion 1000 set camas 8 set Infectados 5 set tiempo-recuperacion 15')   
    for exp in range(len(experiments)):   
        for factor in experiments.columns:
            valor=experiments[factor][exp]
            comando += 'set {} {} '.format(factor,str(valor))
        workspace.command(comando)
        workspace.command('setup')
        try:
            workspace.command('repeat {} [go]'.format(ticks))
        except:
            err.append(exp)
        results.append(workspace.report('muertes'))
        ##########################################
    workspace.closeModel()
    nl4py.deleteAllHeadlessWorkspaces()
    nl4py.stopServer()
    results =pd.DataFrame(data=np.array(results),columns=['Muertes'])
    return results,err

#Programa Principal
#Path de netlogo 
    
file_to_open = os.path.join(".","spatialCOVID19-master","epiDEM COV_v13.nlogo")
#file_to_open = path_folder / "epiDEM COV_v13.nlogo"
path_to_netlogo = 'C:/Program Files/NetLogo 6.1.1/'

#Numero de ticks o días
ticks = '40'


#Import the sampling and analysis modules for a Sobol variance-based
factores= ['precauciones-per','Tasa-Deteccion','Vulnerables','movilidad','probabilidad-contagio']
problem = {'num_vars': len(factores), 'names': factores}        
mean_values = np.array([25,50,25,1,25])
#Uncertainty index 
unc=5 #Measured in percentage
ub2=ub1=mean_values*(1+unc/100)  # 5% up mean
lb2=lb1=mean_values*(1-unc/100)  # 5% below mean
#Dimensions
nd=len(lb1) #determines number of variables considered in sensitivity analysis
sample_size=10    #sample size
x=(np.random.rand(sample_size,nd))
one =np.ones(sample_size)

sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
M1 = sample*mean_values # sample 1
x=(np.random.rand(sample_size,nd))
sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
M2 = (sample*mean_values) # sample 2
x=(np.random.rand(sample_size,nd))
sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
M3 = sample*mean_values # sample 3

lista_N=[]
lista_NTj=[]
for i in range(len(M1[0])):
    Nj=M2
    NTj=M1
    Nj[:,i]=M1[:,i]
    NTj[:,i]=M2[:,i]
    lista_N.append(Nj)
    lista_NTj.append(NTj)
    
#Simulacion
experiments1 = pd.DataFrame(M1,columns=problem['names'])
experiments2 = pd.DataFrame(M2,columns=problem['names']) 
#err guarda los indices de los que tuvieron un error
Y,err1 =simulacion_NL4Py(experiments1,ticks,path_to_netlogo,file_to_open)
YR,err2 =simulacion_NL4Py(experiments2,ticks,path_to_netlogo,file_to_open)

YN = np.zeros((sample_size,nd))
YTp = np.zeros((sample_size,nd))
gamma2_list=[]
err_N= [[]] * len(lista_N)
err_Nj= [[]]*len(lista_N)

for i in range(len(lista_N)):
    experiment = pd.DataFrame(lista_N[i],columns=problem['names']) 
    YN[:,i],err_N[i] =simulacion_NL4Py(experiment,ticks,path_to_netlogo,file_to_open)
    experiment = pd.DataFrame(lista_NTj[i],columns=problem['names']) 
    YTp[:,i],err_Nj[i]=simulacion_NL4Py(experiment,ticks,path_to_netlogo,file_to_open)
    


