# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:58:36 2020

@author: Bryan Piguave
"""

 
import pandas as pd
import numpy as np
from SALib.sample import saltelli

#Conectar netlogo
def CONNECT_NL(path):
    import pyNetLogo
    netlogo = pyNetLogo.NetLogoLink()
    netlogo.load_model(path)
    netlogo.command('setup')
    return netlogo

#Simulacion con sampling
def simulacion(experiments,ticks):
    netlogo =CONNECT_NL(path)
    num_exp =len(experiments)
    #Resultados a obtener:      Turtles    Infected   Cured  Hospitalized
    results =np.zeros(shape=[num_exp,3])       
    for exp in range(len(experiments)):   
        for factor in problem['names']:
            valor=experiments[factor][exp]
            if factor =='movilidad':
                netlogo.command('set {} {}'.format(factor,str(round(valor,1))))
            else:
                netlogo.command('set {} {}'.format(factor,str(int(valor))))                
        netlogo.command('setup')
        ####### REVISAR #########################
        netlogo.command('repeat {} [go]'.format(ticks))
        results[exp,0]  = sum(netlogo.report('[infected?] of turtles'))  
        results[exp,1]  = sum(netlogo.report('[cured?] of turtles'))
        results[exp,2]  = sum(netlogo.report('[hospitalized?] of turtles'))
        ##########################################
    results = {'Infectados_final':results[:,0],
               'Curados':results[:,1],
               'Hospitalizados':results[:,2]
               }
    names =list(results.keys())
    
    results_df = pd.DataFrame(results,columns=names)
    
    #Para cerrar Netlogo
    netlogo.kill_workspace()
    return results_df

#Programa Principal
#Path de netlogo
    
path = r'C:\Users\usuario\Dropbox\PythonEnhanced\COVID19\spatialCOVID19-master\epiDEM COV_v13.nlogo'
#path = "C:\\Users\\ssala\\Dropbox\\PythonEnhanced\\COVID19\\spatialCOVID19-master\\epiDEM COV_v13.nlogo"
#path = ".\\spatialCOVID19-master\\epiDEM COV_v13.nlogo"

#Numero de ticks o días
ticks = '120'
#Import the sampling and analysis modules for a Sobol variance-based
#Sensitivity analysis
factores= ['Infectados','camas','Vulnerables','movilidad']
rango   = [[1,10],[1,10],[0,50],[0.1,2]]
problem = {'num_vars': len(factores), 'names': factores ,'bounds': rango}

#Tamaño de muestra
n = 1000
param_values = saltelli.sample(problem, n, calc_second_order=True)
experiments = pd.DataFrame(param_values,columns=problem['names'])

#Simulacion
results = simulacion(experiments,ticks)


#Gráfica de Datos
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,len(results.columns), sharey=True)
for i, n in enumerate(results.columns):
    ax[i].hist(results[n], 20)
    ax[i].set_xlabel(n)
ax[0].set_ylabel('Counts')
fig.set_size_inches(10,4)
fig.subplots_adjust(wspace=0.1)
plt.show()

#Bivariate scatter plot
import seaborn as sns
import scipy
nrow=2
ncol=2
fig, ax = plt.subplots(nrow, ncol, sharey=True)
y = results['Infectados_final']
for i, a in enumerate(ax.flatten()):
    x = param_values[:,i]
    sns.regplot(x, y, ax=a, ci=None, color='k',scatter_kws={'alpha':0.2, 's':4, 'color':'gray'})
    pearson = scipy.stats.pearsonr(x, y)
    a.annotate("r: {:6.3f}".format(pearson[0]), xy=(0.15, 0.85), xycoords='axes fraction',fontsize=13)
    if divmod(i,ncol)[1]>0:
        a.get_yaxis().set_visible(False)
        a.set_xlabel(problem['names'][i])
        a.set_ylim([0,1.1*np.max(y)])
fig.set_size_inches(9,9,forward=True)
fig.subplots_adjust(wspace=0.2, hspace=0.3)

# Analysis
from SALib.analyze import sobol
Si = sobol.analyze(problem, results['Infectados_final'].values, calc_second_order=True,print_to_console=False)
Si_filter = {k:Si[k] for k in ['ST','ST_conf','S1','S1_conf']}
Si_df = pd.DataFrame(Si_filter, index=problem['names'])

fig, ax = plt.subplots(1)
indices = Si_df[['S1','ST']]
err = Si_df[['S1_conf','ST_conf']]
indices.plot.bar(yerr=err.values.T,ax=ax)
fig.set_size_inches(8,4)
plt.show()



