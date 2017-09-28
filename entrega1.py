
#import math
from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import math, datetime, random

#maquinas = (('A',(1,2) , 300) , ('B', (2,0) , 300) , ('C',(3,0) , 300), ('R' , (3,3) , 0))
MOVIMIENTOS = {"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}
salida = (3,3)
LONGITUD = 3

def tupleToList(t):
	return [list(row) for row in t]

def listToTuple(t):
	return tuple(tuple(row) for row in t)	

class Bomberobot(SearchProblem):	

	def actions (self,state):

		state2 = tupleToList(state)
		#Posiciones de las maquinas
		listamaquinas=[x for x in state2 if(x[0] !="R")]
		robot = state2[3]
		empujar = False
		acciones = []
		mayor500 = False
		extinguir = False

		for lista in listamaquinas:
			if lista[2] > 500:
				mayor500 = True

		
		if mayor500 != True:	
			#Movimientos adyacentes
			if robot[1][0] > 0:#Arriba 
				acciones.append(("Moverse","U"))    
			if robot[1][0] <  LONGITUD :#ABAJO
				acciones.append(("Moverse","D"))
			if robot[1][1] > 0:#izquierda       
				acciones.append(("Moverse","L"))
			if robot[1][1] < LONGITUD:
			 	acciones.append(("Moverse","R"))
		  
			#Acciones mover objeto o extinguir
			for maquina in listamaquinas :
				if maquina[1] == robot[1] :
					if maquina[1] != salida:
						#Agregar accion de mover
						extinguir = True
						if robot[1][0] > 0:#Arriba 
							acciones.append(("Empujar-U",maquina[0]))    
			  			if robot[1][0] < LONGITUD :#ABAJO
			  				acciones.append(("Empujar-D",maquina[0]))
			  			if robot[1][1] > 0:#izquierda
			  				acciones.append(("Empujar-L",maquina[0]))
			  			if robot[1][1] < LONGITUD:
			  				acciones.append(("Empujar-R",maquina[0]))

			if extinguir == True:
				acciones.append(("Extinguir",'0'))

		#print 'Acciones', acciones
		return acciones


	def result(self, state, action):
		#Accion empujarArriba
		#print 'Accion', action
		#print 'State Inicial', state

		robot = state[3]
		accion, objeto = action
		itemBaja = 0
		#listamaquinas=[x for x in state if(x[0] !="R")]

		#Lista de maquinas
		listaElementos = tupleToList(state)

		filaRobot = robot[1][0]
		colRobot = robot[1][1]

		#Mover unicamente el robot
		if accion == "Moverse":
			filaRobot = filaRobot + MOVIMIENTOS[objeto][0]   
			colRobot = colRobot + MOVIMIENTOS[objeto][1]
			#xRobot = movimiento(xRobot)

			listaElementos[3][1] = (filaRobot,colRobot)

		#else:
			#Empujar y mover robot
		elif 'Empujar' in action[0] :			
			accion , lugar =  action[0].split("-")

			#Mover el robot
			filaRobot = filaRobot + MOVIMIENTOS[lugar][0]    
			colRobot = colRobot + MOVIMIENTOS[lugar][1]	
			listaElementos[3][1] = (filaRobot,colRobot)


			#Mover la maquina
			for item,lista in enumerate(listaElementos):
				if lista[0] == objeto:
					listaElementos[item][1] = (filaRobot,colRobot)

		elif accion == "Extinguir":
			#Bajar temperatura
			
			#print 'Extinguir', accion

			for item,lista in enumerate(listaElementos):
				if listaElementos[item][0] != 'R' and listaElementos[item][1] != salida and lista[1] == robot[1]:
						listaElementos[item][2] = listaElementos[item][2] - 150


		#Aumentar la temperatura en 25 grados si no esta en la salida
		for item,lista in enumerate(listaElementos):
			if listaElementos[item][0] != 'R' and listaElementos[item][1] != salida:
				listaElementos[item][2] = listaElementos[item][2] + 25	

				#if listaElementos[item][2] >= 500:
				#	return None
		
		#print 'State final', listToTuple(listaElementos)
		return listToTuple(listaElementos)


	def is_goal (self,state):
		listaElementos = tupleToList(state)
		
		#for i in listaElementos:
		#	if i[1] ==  salida:
		#		print i
		if state[0][1] == salida and state[1][1] == salida and state[2][1] == salida and state[3][1] == salida :
			#print 'Final', state
			return True
		else:
			#print 'No meta',state
			return False


	def cost(self, state1, action, state2):
			return 1


	def heuristic(self,state):
		distancia = 0
		
		#cambiar por algoritmo de manhatan
		mx_1 = state[0][1][0]
		my_1 = state[0][1][1]
		mx_2 = state[1][1][0]
		my_2 = state[1][1][1]
		mx_3 = state[2][1][0]
		my_3 = state[2][1][1]
		sx = salida[0]
		sy = salida[1]

		return abs(sx - mx_1) + abs(sy - my_1) + abs(sx - mx_2) + abs(sy - my_2) + abs(sx - mx_3) + abs(sy - my_3)

def resolver(metodo_busqueda,posiciones_aparatos):
	
	maquina = []
	i = 1
	for posicion in posiciones_aparatos:
		maquina.append((str(i),posicion,300))
		i += 1
	maquina.append(('R' , (3,3) , 0))
	maquina = listToTuple(maquina)

	problema = Bomberobot(maquina)
	#visor = BaseViewer()
	
	#Busquedas, Grafo -> graph_search=True
	if (metodo_busqueda == 'breadth_first'): # En amplitud
		resultado = breadth_first(problema, graph_search= True)#, viewer=visor)
	elif (metodo_busqueda == 'depth_first'): # Profundidad
		resultado = depth_first(problema, graph_search= True)#, viewer=visor)
	elif (metodo_busqueda == 'greedy'): # Avara
		resultado = greedy(problema, graph_search= True)#, viewer=visor)
	elif (metodo_busqueda == 'astar'): # Estrella
		resultado = astar(problema, graph_search=True)#, viewer=visor)
	#print(visor.stats)



	return resultado

if __name__ == '__main__':

	print 'Inicio', datetime.datetime.now()

	aparatos = ((1, 2), (2, 0), (3, 0))
	resultado = resolver('greedy',aparatos)

#	print 'Estado meta:'
#	print resultado.state
#	print 'Camino:'
#	for accion, estado in resultado.path():
#		print 'Movi', accion
#		print 'Llegue a', estado
	print 'costo', str(resultado.cost)
	print 'profundidad', str(resultado.depth)	
	print 'Fin', datetime.datetime.now()

