import itertools
from simpleai.search import (backtrack, CspProblem, LEAST_CONSTRAINING_VALUE,
                             min_conflicts, MOST_CONSTRAINED_VARIABLE)

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
	a1,a2,p1,p2 = variables
	va1,va2,vp1,vp2 = valores
	print 'Variables', a1,a2,p1,p2
	print 'Valores',va1,va2,vp1,vp2
	if va1 == 'Verde' and va2 == 'Blanco':
		print p1 < vp2
		return vp1 < vp2
	elif va1 == 'Blanco' and va2 == 'Verde':
		print vp2 < vp1
		return vp2 < vp1
	return True #no es ni verde ni blanco la asignacion se puede realizar

def verde_escudo(variables,valores):
		va1,va2 = valores
		if va1 == 'Verde':
			if va2 =='Cruz':
				print va1,va2
				return True
			else:
				return False

		
#izquierda del blanco sea el verde
lista_res = []
for vikingo in vikingos:
	for vikingo2 in vikingos:
		if vikingo != vikingo2:
			lista_res.append(((vikingo,'Armaduras'),(vikingo2,'Armaduras'),(vikingo,'Posicion'),(vikingo2,'Posicion'))) #se forma la variable

for restriccion in lista_res:
	restricciones.append((restriccion,verde_izquierda_blanco))


#verde escudo
#for vikingo in vikingos:
#	restricciones.append((((vikingo,'Armaduras'),(vikingo,'Escudos')),verde_escudo))


problem = CspProblem(variables, dominios, restricciones)

print('backtrack:')
result = backtrack(problem,
                   variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE,
                   inference=True)

print(result)

#print 'DOMINIOS', dominios