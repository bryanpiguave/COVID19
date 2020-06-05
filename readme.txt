    # COVID 19 

	WORK IN PROGRESS
	
	For more information, please contact:
	
	Daniel Orellana V. Universidad de Cuenca
	daniel.orelana@ucuenca.edu.ec
	
	Bryan V. Piguave
	bpiguave@espol.edu.ec
	
	Santiago Salas
	sdsalas@espol.edu.ec
	
	Dany De Cecchis
	dany@espol.edu.ec
	
	

	## Python libraries required
    
    - Numpy 	 1.18.1
    - Pandas 	 1.0.1
    - Matplotlib 3.1.3
    - jpype1  	 0.7.5 
    - pyNetlogo  0.4.1
	
	
	## How to run this model
    
    To run this model, you have download the files from this repository. 
    Python 3.7.6 and Netlogo 6.1.1 are required to script files.
    
    
    

	## About
	
	This model is an extension from epiDEM model developed by Yang, C. and Wilensky U. (2011)
    It simulates the spatial spread of a virus in two semi-closed populations under a series of conditions, such as internal mobility, predisposition to quarantine, personal health measures, etc.
    The model is not intended to make predictions, but rather to illustrate how changes in these measures affect the spread of the virus.

	In general, the model allows users to:
    1) Understand the dynamics of an emerging disease such as COVID-19 in relation to control measures, quarantines, travel prohibition, etc.
    2) Experience measurement comparison
    3) Understand the concept of #Flatten the curve to avoid the collapse of the health system
    4) Explore the impact on saturation of hospitals.

    
    The Sobol method, which is variance-based sensitivity analysis, was employed to classify the most sensitive parameters.
    
    
    
    

	## Changes Yang, C. and Wilensky, U. (2011)
	
	- Each "country" has its own variables, making it possible to compare different situations and measures.
    - Reified code to improve readability and extensibility.
    - The "efficacy of personal measures" factor is introduced, that is, each agent has a probability of adopting behaviors that decrease the probability of contagion by an efficacy factor * emp *
    - The initial number of infected in each country is entered as variables.
    - The R0 is calculated for each country independently.
	
	## Features of this version: 

	- The assumption of a relapse is not modeled and full immunity is assumed after recovery.
    - The person's general health status is represented on a scale from 1 to 10.
    - At the beginning, each person receives a greeting value from a normal distribution (mean = 7 std = 2). When the state of health deteriorates to 0, the person dies.

	##Aspects to consider:

	As with many epidemiological models, the number of people becoming infected over time, in the event of an epidemic, traces out an "S-curve." It is called an S-curve because it is shaped like a sideways S. 
	By changing the values of the parameters using the slider, try to see what kinds of changes make the S curve stretch or shrink.
    Whenever there's a spread of the disease that reaches most of the population, we say that there was an epidemic. 
    The reproduction number serves as an indicator for the likeliness of an epidemic to occur, if it is greater than 1. If it is smaller than 1, then it is likely that the disease spread will stop short, and we call this an endemic.
    Notice how the introduction of various human behaviors, such as travel, inoculation, isolation and quarantine, help constrain the spread of the disease, and what changes that brings to the population level in terms of rate and time taken of disease spread, as well as the population affected.




## Related models

epiDEM basic, HIV, Virus and Virus on a Network are related models.

## How to cite

If you would like to use this model, please include the following cites:

* Orellana, D. (2020) Exploring preventive measures for spatial dispersion of epidemies: An ABM approach based on epiDEMTravelandControl model. Universidad de Cuenca.

Original model:

* Yang, C. and Wilensky, U. (2011).  NetLogo epiDEM Travel and Control model.  http://ccl.northwestern.edu/netlogo/models/epiDEMTravelandControl.  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

Please cite the NetLogo software as:

* Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.



## COPYRIGHT AND LICENSE

Copyright de esta version: Daniel Orellana, Universidad de Cuenca

![CC BY-NC-SA 3.0](http://ccl.northwestern.edu/images/creativecommons/byncsa.png)

Copyright del modelo original: 2011 Uri Wilensky.

![CC BY-NC-SA 3.0](http://ccl.northwestern.edu/images/creativecommons/byncsa.png)

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.  To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.

Commercial licenses are also available. To inquire about commercial licenses, please contact Uri Wilensky at uri@northwestern.edu.

<!-- 2011 Cite: Yang, C. -->
