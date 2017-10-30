from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import math, datetime, random

class Vidon(SearchProblem):
	def actions(self,state):
		#accciones = [vidonALlenar,VidonQueLLena,litros]
		acciones = []

		for vidonALlenar in state:
			if vidonALlenar[1] < vidonALlenar[0]: #Si no esta completo llenar el vidon con la canilla
				
				litrosACompletar = vidonALlenar[0]-vidonALlenar[1]

				acciones.append((vidonALlenar,None,(litrosACompletar,0)))

				for vidonQueLLena in state:#Llnar con otro vidon
					if vidonQueLLena[1] != 0 and vidonQueLLena != vidonALlenar:
						
						if vidonQueLLena[1] >= litrosACompletar:
							acciones.append((vidonALlenar,vidonQueLLena,litrosACompletar))
						else:
							acciones.append((vidonALlenar,vidonQueLLena,vidonQueLLena[1]))
		print 'ACCIONES', acciones
		return acciones

	def is_goal(self,state):
		print 'ESTADO',state
		a,b,c = state
		return c[1] == 1

	def cost(self,state1,action,state2):
		return action[2]

	def heuristic(self,state):
		return 1

	def result(self,action,state):
		nuevoEstado = []

		vidonALlenar,vidonQueLLena,litrosACompletar = action
		
		for i in state:
			if i == vidonALlenar:
				pelado = vidonALlenar[1]+litrosACompletar[0]
				nuevoEstado.append((vidonALlenar[0],pelado))
			elif i == vidonQueLLena:
				pelado1 = vidonQueLLena[1]-litrosACompletar[0]
				nuevoEstado.append((vidonQueLLena[0],pelado1))
			else:
				nuevoEstado.append(i)
		
		return tuple(nuevoEstado)


def resolver(metodo_busqueda): 
	
	inicial = [(12,12),(8,0),(3,0)]


	#inicial = [(1, 0), (2, 0), (3, 2), (4, 4), (5, 1)]
	print 'inicial', inicial

	problema = Vidon(tuple(inicial))
	visor = BaseViewer()
	
	#Busquedas, Grafo -> graph_search=True
	if (metodo_busqueda == 'breadth_first'): # En amplitud
		resultado = breadth_first(problema, graph_search= True)#, viewer=visor)
	elif (metodo_busqueda == 'depth_first'): # Profundidad
		resultado = depth_first(problema, graph_search= True)#, viewer=visor)
	elif (metodo_busqueda == 'greedy'): # Avara
		resultado = greedy(problema, graph_search= True)#, viewer=visor)
	elif (metodo_busqueda == 'astar'): # Estrella
		print 'problema', problema
		resultado = astar(problema, graph_search=True)#, viewer=visor)
	#print(visor.stats)


	print(visor.stats)




if __name__ == '__main__':

	#print 'Inicio', datetime.datetime.now()


	resultado = resolver('astar')
	print('Estado meta:')
	print(resultado)
	print(type(resultado))
	print('Camino:')
	for accion, estado in resultado.path():
		print 'Movi', accion
		print 'Llegue a', estado
	print 'costo', str(resultado.cost)
	print 'profundidad', str(resultado.depth)	
	print 'Fin', datetime.datetime.now()




