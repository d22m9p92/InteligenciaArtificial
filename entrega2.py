import itertools

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
dominiosPredefinidos = [(('A', 'Posicion'),[1]), (('B', 'Armaduras'),'Rojo'), (('C', 'Armas'),'Garrote'), (('D', 'Escudos'),'Trebol'), (('E', 'Amuletos'),'Pendiente')]

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
		dominios[variable] = armaduras	

	elif _objeto == 'Armas':
		dominios[variable] = armas

	elif _objeto == 'Escudos':
		dominios[variable] = escudos

	elif _objeto == 'Amuletos':
		dominios[variable] = amuletos

	else:
		dominios[variable] = posiciones 	

for dominio_ in dominiosPredefinidos:
	clave, valor = dominio_
	dominios[clave] = valor



print 'DOMINIOS', dominios