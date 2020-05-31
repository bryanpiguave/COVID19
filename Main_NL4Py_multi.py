# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:39:29 2020

@author: Bryan Piguave
"""

import os.path
import pandas as pd
import numpy as np
from SALib.sample import saltelli

def Netlogo_NL4Py(experiments,ticks,path_to_netlogo,file_to_open,results):
    import nl4py
    nl4py.startServer(path_to_netlogo)
    workspace=nl4py.newNetLogoHeadlessWorkspace()
    workspace.openModel(file_to_open)
    #Resultados a obtener:     Infected   Cured  Hospitalized
    for exp in range(len(experiments)):   
        workspace.command('set turtles 600')
        for factor in experiments.columns:
            valor=experiments[factor][exp]
            if factor =='movilidad':
                workspace.command('set {} {}'.format(factor,str(round(valor,1))))
            else:
                workspace.command('set {} {}'.format(factor,str(int(valor))))                
        workspace.command('setup')
        ####### REVISAR #########################
        workspace.command('repeat {} [go]'.format(ticks))
        results.append(workspace.report('count turtles with [infected?]'))
        print(workspace.report('count turtles with [infected?]'))
        ##########################################
    workspace.closeModel()
    nl4py.deleteAllHeadlessWorkspaces()
    nl4py.stopServer()
    return results

#Programa Principal
#Path de netlogo 
    
from multiprocessing import Process,Manager
if __name__=='__main__':
    #Path de netlogo
    file_to_open = os.path.join(".","spatialCOVID19-master","epiDEM COV_v13.nlogo")
    #file_to_open = path_folder / "epiDEM COV_v13.nlogo"
    path_to_netlogo = 'C:/Program Files/NetLogo 6.1.1/'
    #Numero de ticks o días
    ticks = '40'
    #Import the sampling and analysis modules for a Sobol variance-based
    #Sensitivity analysis
    factores= ['Infectados','camas','Vulnerables','movilidad']
    rango   = [[1,10],[1,10],[0,50],[0.1,2]]
    problem = {'num_vars': len(factores), 'names': factores ,'bounds': rango}
    
    #Tamaño de muestra
    n = 2
    param_values = saltelli.sample(problem, n, calc_second_order=True)
    experiments = pd.DataFrame(param_values,columns=problem['names'])
    #Simulacion
    #results=simulacion(experiments, ticks, file_to_open)
    manager = Manager()
    processes=[]
    results=list()
    dfs=np.split(experiments,2)
    idx=dfs[0].index
    for i in range(len(dfs)):
        process=Process(target=Netlogo_NL4Py,args=(experiments,ticks,path_to_netlogo,file_to_open,results))
        process.start()
        process.join()
    results=results.values()
    
