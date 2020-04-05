# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:22:57 2020

@author: Bryan Piguave
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:58:36 2020

@author: Bryan Piguave
"""


import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Conectar netlogo
def CONNECT_NL(path):
    import pyNetLogo
    netlogo = pyNetLogo.NetLogoLink()
    netlogo.load_model(path)
    return netlogo

#Simulacion con sampling
def simulacion(experiments,ticks, file_to_open):
    netlogo =CONNECT_NL(file_to_open)
    num_exp =len(experiments)
    comando=''
    err=[]
    #Resultados a obtener: Muertos
    results =np.zeros(shape=[num_exp])
    #Parámetros de simulación
    netlogo.command('set Poblacion 1000')   
    netlogo.command('set camas 8')
    netlogo.command('set Infectados 5')
    netlogo.command('set tiempo-recuperacion 15')
    for exp in range(len(experiments)):   
        for factor in experiments.columns:
            valor=experiments[factor][exp]
            comando += 'set {} {} '.format(factor,str(valor))
        netlogo.command(comando)            
        #netlogo.command('set efecto-precauciones-per 8 set probabilidad-recuperacion 40')
        netlogo.command('setup')
        try:
            netlogo.command('repeat {} [go]'.format(ticks))
        except:
            err.append(exp)
        results[exp]  = netlogo.report('muertes')   
    #Para cerrar Netlogo
    netlogo.kill_workspace()
    print("completado")
    return results,err

#Programa Principal
#multiprocessing import Process,Pool
if __name__=='__main__':
    #Path de netlogo
    file_to_open = os.path.join(".","spatialCOVID19-master","epiDEM COV_v13.nlogo")
    #file_to_open = path_folder / "epiDEM COV_v13.nlogo"
    
    #Numero de ticks o días
    ticks = '20'
    
    factores= ['precauciones-per','Tasa-Deteccion','Vulnerables','movilidad','probabilidad-contagio']
    problem = {'num_vars': len(factores), 'names': factores}        
    mean_values = np.array([25,50,25,1,25])
    #Uncertainty index 
    unc=5                            # Measured in percentage
    ub2=ub1=mean_values*(1+unc/100)  # 5% up mean
    lb2=lb1=mean_values*(1-unc/100)  # 5% below mean
    #Dimensions
    nd=len(lb1)                      #determines number of variables considered in sensitivity analysis
    sample_size=3                   #sample size
    x=(np.random.rand(sample_size,nd))
    one =np.ones(sample_size)
    
    sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
    M1 = sample*mean_values      # sample 1
    x=(np.random.rand(sample_size,nd))
    sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
    M2 = (sample*mean_values)    # sample 2
    x=(np.random.rand(sample_size,nd))
    sample = 1+2*(x-1)*(unc/100) # The % moved between plus or minus the unc%
    M3 = sample*mean_values      # sample 3
    
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
    Y,err1 =simulacion(experiments1, ticks, file_to_open)
    YR,err2 =simulacion(experiments1, ticks, file_to_open)
    
    YN = np.zeros((sample_size,nd))
    YTp = np.zeros((sample_size,nd))
    gamma2_list=[]
    err_N= [[]] * len(lista_N)
    err_Nj= [[]]*len(lista_N)
    
    for i in range(len(lista_N)):
        experiment = pd.DataFrame(lista_N[i],columns=problem['names']) 
        YN[:,i],err_N[i] =simulacion(experiment, ticks, file_to_open)
        experiment = pd.DataFrame(lista_NTj[i],columns=problem['names']) 
        YTp[:,i],err_Nj[i]=simulacion(experiment, ticks, file_to_open)
        
    f0 = 0.5 * (YR.mean() + Y.mean());
    Variance = (0.5*(1/sample_size))*(sum(Y*Y) + sum(YR*YR)) - f0*f0
    gama2 = (sum(Y*YR) + sum(YN*YTp))/(2*sample_size)
    
    #Histograma
    plt.title('Histograma')
    plt.xlabel('Muertes')
    plt.hist(np.concatenate((Y,YR)))
    plt.show()
   
    #processes = []
    #results=[]
    #for i in range(len(dfs)):
    #    process=Process(target=simulacion,args=(dfs[i], ticks, file_to_open))
    #    processes.append(process)
    #    process.start()
    #    process.join() 
    
    