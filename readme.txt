	# Dispersión COVID 19 

	WORK IN PROGRESS

	v0.9

	para más información:
	Daniel Orellana V. Universidad de Cuenca
	daniel.orelana@ucuenca.edu.ec
	https://www.twitter.com/temporalista

	## Instrucciones generales

	- Descargar los archivos de esta carpeta.
	- Abrir el modelo epiDEM COV.html en el navegador (El funcionamiento es más lento)
	- Alternativamente instalar NetLogo y abrir el modelo epiDEM COV.nlogo (simulación más rápida y funciones adicionales)

	## De qué se trata?

	Este modelo es una ampliación del modelo epiDEM desarrolado por Yang, C. and Wilensky, U. (2011).Simula la propagación espacial de un virus en dos poblaciones semi-cerradas bajo una serie de condiciones, tales como mobilidad interna, predisposición a la cuarentena, medidas personales de sanidad, etc. El modelo no busca realizar predicciones sino ilustrar cómo afectan los cambios de estas medidas en la propagación del virus.

	En general, el modelo permite a los usuarios:
	1) Entender la dinámica de una enfermedad emergente como el COVID-19 en relación a medidas de control, cuarentenas, prohibición de viajes, etc.
	2) Experimentar la comparación de medidas entre dos poblaciones similares
	3) Entender el concepto de #AplanarLaCurva para evitar el colapso del sistema de salud
	4) (por desarrollar) Explorar el impacto de comportamientos de pánico en algunos comportamientos emergentes: desabastecimiento,  saturación de los hospitales, etc.

	## Cambios con respecto a Yang, C. and Wilensky, U. (2011)
	- Inclusión de una variable que representa el estado de salud general de la persona está representado en una escala del 1 al 10. Al inicio, cada persona recibe un valor de saludo de una distribución normal (media=7 std=2). Durante el período sintomático, el estado de salud se deteriora a una tasa DS hasta curarse o hasta llegar a 0 (fallecimiento).

	-  Cada "país" tiene sus propias variables, por lo que es posible comparar situaciones y medidas distintas.
	-  Código reificado para mejorar la legibilidad y extensibilidad.
	- Se introduce el factor de " eficacia de medidas personales",es decir, cada agente tiene una probabilidad de adoptar comportamientos que disminuyen la probabilidad de contagio en un factor de eficacia *emp*
	- Se introduce como variables el número inicial de infectados en cada país.
	- El R0 se calcula para cada país de forma independiente.	
	




	## Algunas características en esta versión: 

	- No está modelado el supuesto de una recaida y se asume inmunidad completa luego de la recuperación.
	- El estado de salud general de la persona está representado en una escala del 1 al 10. 
	- Al inicio, cada persona recibe un valor de saludo de una distribución normal (media=7 std=2). Cuando el estado de salud se deteriora hasta 0, la persona fallece.

	##Aspectos a revisar:

	Potenciales colaboradores pueden enfocarse en revisar y validar algunos aspectos:

	- Suposiciones teóricas: El moelo está basado en Yang, C. and Wilensky, U. (2011). Sin embargo, es necesario revisar estas suposiciones (Ej. el R0 es un resultado del modelo) para el caso del COVID (ej, el R0 es calculado como resultado del modelo)

	- Características del COVID-19. El modelo es genérico, pero es posible calibrarlo para algunas características del COVID-19: Período de incubación, período sintomático, retardo del autoaislamiento, etc.




## Modelos relacionados

epiDEM basic, HIV, Virus and Virus on a Network are related models.

## Cómo citar

Si desea utilizar este modelo, por favor incluir las siguientes citas:

* Orellana, D. (2020) Exploring preventive measures for spatial dispersion of epidemies: An ABM approach based on epiDEMTravelandControl model. Universidad de Cuenca.


Modelo Original:

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

## Funciones pendientes