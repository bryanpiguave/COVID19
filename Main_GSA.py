# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:22:57 2020

@author: Bryan Piguave
"""


import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def CONNECT_NL(path):
    # To connect netlogo
    
    import pyNetLogo
    netlogo = pyNetLogo.NetLogoLink()
    netlogo.load_model(path)
    return netlogo

def iterador(experiments,netlogo,M3):
    comando=''
    err=[]
    #Resultados a obtener: Muertos
    num_exp =len(experiments)
    results =np.zeros(shape=[num_exp])
    for exp in range(len(experiments)):   
        for factor in experiments.columns:
            valor=experiments[factor][exp]
            comando += 'set {} {} '.format(factor,str(valor))
        netlogo.command(comando)            
        netlogo.command('setup')
        try:
            netlogo.command('repeat {} [go]'.format(ticks))
        except:
            for exp in range(len(experiments)):   
                for factor in experiments.columns:
                    valor=M3[exp,list(experiments.columns).index(factor)]
                    comando += 'set {} {} '.format(factor,str(valor))
                    netlogo.command(comando)            
                    netlogo.command('setup')
                    try:
                        netlogo.command('repeat {} [go]'.format(ticks))
                    except:
                        continue
            err.append(exp)
        results[exp]  = netlogo.report('muertes')   
    return results,err

def simulacion_doble(experiments1,experiments2,M3,file_to_open):
    netlogo =CONNECT_NL(file_to_open)   
    #Parámetros de simulación
    netlogo.command('set Poblacion 1000 set camas 8 set Infectados 5 set tiempo-recuperacion 15 set efecto-precauciones-per 8 set probabilidad-recuperacion 40')   
    Y,err1 = iterador(experiments1,netlogo,M3)
    YR,err2= iterador(experiments2,netlogo,M3)  
    #Para cerrar Netlogo
    netlogo.kill_workspace()
    return Y,err1,YR,err2

def iterador_Nj(experiments,netlogo,f0):
    comando=''
    err=[]
    #Resultados a obtener: Muertos
    num_exp =len(experiments)
    results =np.zeros(shape=[num_exp])
    for exp in range(len(experiments)):   
        for factor in experiments.columns:
            valor=experiments[factor][exp]
            comando += 'set {} {} '.format(factor,str(valor))
        netlogo.command(comando)            
        netlogo.command('setup')
        try:
            netlogo.command('repeat {} [go]'.format(ticks))
        except:
            err.append(exp)
            results[exp]  = f0
            continue
        results[exp]  = netlogo.report('muertes')   
    return results,err

def simulacion_multiple(lista_N,lista_NTj,ticks,f0,file_to_open):
    netlogo =CONNECT_NL(file_to_open)   
    #Parámetros de simulación
    netlogo.command('set Poblacion 1000 set camas 8 set Infectados 5 set tiempo-recuperacion 15 set efecto-precauciones-per 8 set probabilidad-recuperacion 30')   
    YN = np.zeros((sample_size,nd))
    YTp = np.zeros((sample_size,nd))   
    err_N= [[]] * len(lista_N)
    err_Nj= [[]]*len(lista_N)       
    for i in range(len(lista_N)):
        data_N = pd.DataFrame(lista_N[i],columns=factores) 
        data_NTj = pd.DataFrame(lista_NTj[i],columns=factores)   
        YN[:,i],err_N[i] =iterador_Nj(data_N,netlogo,f0)
        YTp[:,i],err_Nj[i]=iterador_Nj(data_NTj,netlogo,f0)
    netlogo.kill_workspace()
    return YN,YTp,err_N,err_Nj

   
    
def sim_N(experiments,ticks, file_to_open,media):
    netlogo =CONNECT_NL(file_to_open)
    #Parámetros de simulación
    netlogo.command('set Poblacion 1000 set camas 8 set probabilidad-recuperacion 40 set Infectados 5 set tiempo-recuperacion 15 set efecto-precauciones-per 8 ')   
    results,err=iterador_Nj(experiments,netlogo,f0) 
    #Para cerrar Netlogo
    netlogo.kill_workspace()
    return results,err



#Main Prog Principal
if __name__=='__main__':
    #Path de netlogo
    file_to_open = os.path.join(".","spatialCOVID19-master","epiDEM COV_v13.nlogo")
    #file_to_open = path_folder / "epiDEM COV_v13.nlogo"
    #Numero de ticks o días
    ticks = '10'
    factores= ['precauciones-per','Tasa-Deteccion','Vulnerables','movilidad','probabilidad-contagio']      
    mean_values = np.array([25,30,25,1,25])
    #Uncertainty index 
    unc=5                            # Measured in percentage
    ub2=ub1=mean_values*(1+unc/100)  # 5% up mean
    lb2=lb1=mean_values*(1-unc/100)  # 5% below mean
    #Dimensions
    nd=len(lb1)                      #determines number of variables considered in sensitivity analysis
    sample_size=5                  #sample size 
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
         
    for j in range(nd):
        Nj=np.zeros((sample_size,nd))
        Nj=M2.copy()
        Nj[:,j]=M1[:,j].copy()
        lista_N.append(Nj) 
        NTj=M1[:,:].copy()
        NTj[:,j]=M2[:,j].copy()
        lista_NTj.append(NTj) 

           
    #Simulation
    experiments1 = pd.DataFrame(M1,columns=factores)
    experiments2 = pd.DataFrame(M2,columns=factores) 
    Y,err1,YR,err2=simulacion_doble(experiments1,experiments2,M3,file_to_open)
        
    f0 = 0.5*(YR.mean()+Y.mean())                                       
    Variance = (sum(Y*Y) + sum(YR*YR))/(2*sample_size) - f0*f0   
    
    gamma2_list=[]
    
    YN,YTp,err_N,err_Nj=simulacion_multiple(lista_N,lista_NTj,ticks,f0,file_to_open)
    
    gama2 = (sum(Y*YR) + sum(YN*YTp))/(2*sample_size)
    
    V=np.zeros(nd)
    V_q=np.zeros(nd)
    for i in range(nd):
        V[i]= (sum(Y*YTp[:,i])+sum(YR*YN[:,i])) / (2*sample_size)
        V_q[i] = (sum(Y*YN[:,i])+sum(YR*YTp[:,i])) / (2*sample_size)
        
    s = (V - f0*f0)/Variance
    st = 1 - (V_q - f0*f0)/Variance
    
    sHS = (V - gama2)/Variance
    stHS = 1 - (V_q - gama2)/Variance
          
    #Histogram
    plt.title('Histograma')
    plt.xlabel('Muertes')
    plt.hist(np.concatenate((Y,YR)))
    plt.show()
          
    x=np.arange(len(factores))
    fig, ax = plt.subplots()
    width = 0.30  # the width of the bars
    rects1 = ax.bar(x - width/2, list(sHS), width, label='S')
    rects2 = ax.bar(x + width/2, list(stHS), width, label='ST')
    ax.set_ylabel('Scores')
    ax.set_xlabel('Variables')
    ax.legend()
    plt.show()
    
    x=np.arange(len(factores))
    fig, ax = plt.subplots()
    width = 0.30  # the width of the bars
    rects1 = ax.bar(x - width/2, list(s), width, label='S')
    rects2 = ax.bar(x + width/2, list(st), width, label='ST')
    ax.set_ylabel('Scores')
    ax.set_xlabel('Variables')
    ax.legend()
    plt.show()
    
    
    