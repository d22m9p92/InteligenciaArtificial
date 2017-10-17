import itertools
from simpleai.search import (backtrack, CspProblem, LEAST_CONSTRAINING_VALUE,min_conflicts, MOST_CONSTRAINED_VARIABLE)

#variables son los elementos una lista
#dominios 

vikingos = ['A','B','C','D','E']
objetos = ['Armaduras','Armas','Escudos','Amuletos','Posicion']

#Lista de elementos sin los que son predefinidos anteriormente
armaduras = ['Verde' , 'Amarillo' , 'Azul' , 'Blanco']
armas = ['Martillo' , 'Hacha' , ' Lanza' , 'Espada' ]
escudos = ['Cruz' , 'Pajaros' ,  'Dragon' , 'Arbol']
amuletos = ['Pulsera' , 'Cinturon' , 'Moneda' , 'Anillo']
posiciones = list(a for a in range(6) if a > 1)
dominiosPredefinidos = [(('A', 'Posicion'),[1]), (('B', 'Armaduras'),['Rojo']), (('C', 'Armas'),['Garrote']), (('D', 'Escudos'),['Trebol']), (('E', 'Amuletos'),['Pendiente'])]

variables = []
dominios = {}
restricciones = []

for vikingo in vikingos:
	for objeto in objetos:
		variables.append((vikingo,objeto))


#dominios[('A', 'Posiciona')] = armaduras

for variable in variables:
	_vikingo, _objeto = variable

	if _objeto == 'Armaduras':
		dominios[variable] = armaduras[:]

	elif _objeto == 'Armas':
		dominios[variable] = armas[:]

	elif _objeto == 'Escudos':
		dominios[variable] = escudos[:]

	elif _objeto == 'Amuletos':
		dominios[variable] = amuletos[:]

	else:
		dominios[variable] = posiciones[:] 	

for dominio_ in dominiosPredefinidos:
	clave, valor = dominio_
	dominios[clave] = valor


def verde_izquierda_blanco(variables,valores):

	armadura1, armadura2, pos1, pos2 = variables
	val_armadura1,val_armadura2,val_posicion1,val_posicion2 = valores
	#print 'Variables', a1,a2,p1,p2
	#print 'Valores',va1,va2,vp1,vp2
	if val_armadura1 == 'Verde' and val_armadura2 == 'Blanco':
		#print pos1 < val_posicion2
		return val_posicion1 < val_posicion2
	elif val_armadura1 == 'Blanco' and val_armadura2 == 'Verde':
		#print val_posicion2 < val_posicion1
		return val_posicion2 < val_posicion1
	return True #no es ni verde ni blanco la asignacion se puede realizar


def verde_escudo(variables,valores):
	valor1,valor2 = valores
	if valor1 == 'Verde':
		if valor2 =='Cruz':
			return True
		else:
			return False
	return True


def	martillo_anillo(variables,valores): ####El guerrero que usaba un martillo de guerra, tenia un anillo con un dibujo de un herrero para la suerte
	valor1 , valor2 = valores
	if valor1 == 'Martillo':
		if valor2 =='Anillo':
			return True
		else: 
			return False
	return True


def amarillo_hacha(variables,valores):###El jefe recuerda que el guerrero de amarillo usaba un hacha danesa
	valor1 , valor2 = valores
	if valor1 =='Amarillo':
		if valor2 == 'Hacha':
			return True
		else:
			return False
	return True

def tercero_pajaros(variables, valores):####El guerrero del centro tenia un bello escudo decorado con dibujos de mil pajaros diferentes
	valor1 , valor2 = valores
	if valor1 == 3 :
		if valor2 == 'Pajaros':
			return True
		else:
			return False
	return True


def lanza_pulsera(variables, valores): 
	#### El guerrero que usaba lanza, se ubicaba al lado del guerrero que usaba una brillante pulsera de oro para la suerte
	arma , amuleto , posicion1 , posicion2  = variables
	val_arma, val_amuleto ,val_posicion1 , val_posicion2 = valores
	
	if val_arma == 'Lanza' and val_amuleto == 'Pulsera': 
		if posicion1 == posicion2 + 1 or posicion1 == posicion2 -1:
			return True
		else:
			return False
	return True

def cinturon_hacha(variables, valores):  
##el guerrero que usaba un cinturon de cuero decorado como amuleto, se ubicaba al lado del guerrero del hacha 
	amuleto , arma , posicion1 , posicion2  = variables
	val_amuleto,val_arma ,val_posicion1 , val_posicion2 = valores
	if val_arma == 'Hacha' and val_amuleto == 'Cinturon': 
		if val_posicion1 == val_posicion2 + 1 or val_posicion1 == val_posicion2 -1:
			return True
		else:
			return False
	return True

def espada_dragon(variables, valores):  
#el guerrero que usaba espada usaba un escudo decorado con un dibujo de un dragon
	valor1 , valor2 = valores
	if valor1 == 'Dragon':
		if valor2 == 'Espada':
			return True
		else:
			return False
	return True

def lanza_arbol(variables, valores):  
# el guerrero de la lanza siempre estaba al lado del guerrero del escudo con dibujo de arbol
	escudo , arma , posicion1 , posicion2  = variables
	val_escudo,val_arma ,val_posicion1 , val_posicion2 = valores
	if val_arma == 'Lanza' or val_escudo == 'Lanza':
		if val_posicion1 == val_posicion2 + 1 or val_posicion1 == val_posicion2 -1:
			return True
		else:
			return False
	return True	

def diferentes(variables,valores):
	valor1, valor2 = valores
	lista = list(valores)
	return len(lista) == len(set(lista))

#izquierda del blanco sea el verde
lista_res = []
for vikingo in vikingos:
	for vikingo2 in vikingos:
		if vikingo != vikingo2:
			lista_res.append(((vikingo,'Armaduras'),(vikingo2,'Armaduras'),(vikingo,'Posicion'),(vikingo2,'Posicion'))) #se forma la variable

for restriccion in lista_res:
	restricciones.append((restriccion,verde_izquierda_blanco))


#verde escudo
for vikingo in vikingos:
	restricciones.append((((vikingo,'Armaduras'),(vikingo,'Escudos')),verde_escudo))		

#martillo anillo
for vikingo in vikingos:
	restricciones.append((((vikingo,'Armas'),(vikingo,'Amuletos')),martillo_anillo))	

#amarillo hacha
for vikingo in vikingos:
	restricciones.append((((vikingo,'Armaduras') , (vikingo,'Armas')) , amarillo_hacha))

#posicion 3 - pajaro
for vikingo in vikingos:
	restricciones.append((((vikingo,'Posicion') , (vikingo,'Escudos')) , tercero_pajaros))

#guerrero con lanza a lado del de pulsera
for vikingo in vikingos:
	for vikingo2 in vikingos:
		if vikingo != vikingo2:
			lista_res.append(((vikingo,'Armas'),(vikingo2,'Amuletos'),(vikingo,'Posicion'),(vikingo2,'Posicion'))) #se forma la variable

for restriccion in lista_res:
	restricciones.append((restriccion,lanza_pulsera))


#cinturon hacha
for vikingo in vikingos:
	for vikingo2 in vikingos:
		if vikingo != vikingo2:
			lista_res.append(((vikingo,'Amuletos'),(vikingo2,'Armas'),(vikingo,'Posicion'),(vikingo2,'Posicion'))) #

for restriccion in lista_res:
	restricciones.append((restriccion,cinturon_hacha))

#espada dragon
for vikingo in vikingos:
	restricciones.append((((vikingo,'Escudos') , (vikingo,'Armas')) , espada_dragon))

#lanza arbol
for vikingo in vikingos:
	for vikingo2 in vikingos:
		if vikingo != vikingo2:
			lista_res.append(((vikingo,'Escudos'),(vikingo2,'Armas'),(vikingo,'Posicion'),(vikingo2,'Posicion'))) #

for restriccion in lista_res:
	restricciones.append((restriccion,lanza_arbol))


#Posiciones distintas
lista = []
for b in vikingos:
	lista.append((b,'Posicion'))

for i,j in itertools.combinations(lista, 2):
	restricciones.append(((i, j), diferentes))
	

#Armadura distinta
lista_arm = []
for _armadura in vikingos:
	lista_arm.append((_armadura,'Armaduras'))

for i,j in itertools.combinations(lista_arm, 2):	
	restricciones.append(((i, j), diferentes))


#Escudos distintos
lista = []
for _escudo in vikingos:
	lista.append((_escudo,'Escudos'))

for i,j in itertools.combinations(lista, 2):
	restricciones.append(((i, j), diferentes))


#Amuleto distintos
lista = []
for _amuleto in vikingos:
	lista.append((_amuleto,'Amuletos'))

for i,j in itertools.combinations(lista, 2):
	restricciones.append(((i, j), diferentes))

#Armas distintas
lista = []
for _arma in vikingos:
	lista.append((_arma,'Armas'))

for i,j in itertools.combinations(lista, 2):
	restricciones.append(((i, j), diferentes))


def resolver(metodo_busqueda, iteraciones):
	problem = CspProblem(variables, dominios, restricciones)

	if metodo_busqueda == 'backtrack':
		result = backtrack(problem, variable_heuristic = MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE, inference=True)
		return resultado
	if metodo_busqueda == 'min_conflicts':
		result = min_conflicts(problem, iterations_limit=500)
		return resultado





#print 'DOMINIOS', dominios