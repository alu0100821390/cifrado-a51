##########################################################################################
## Universidad de La Laguna						 										##
## Escuela Superior de Ingeniería y Tecnología	 										##
## Grado en Ingeniería Informática				 										##
## Seguridad en Sistemas Informáticos			 										##
## Fecha: 14/03/2016							 										##
## Autor: Kevin Estévez Expósito (alu0100821390) 										##
## 																						##
## Práctica 4: Cifrado A5/1											 					##
## Descripción: Cifrado y descifrado de mensajes mediante el cifrado A5/1.				##
## 				Se descartan los primeros 'n_desc' bits generados.						##
##											 											##
## Ejecución: py a51_mod.py '"mensaje"'													##
## Ejemplo de ejecución: py a51_mod.py "Hola Mundo!"									##
## Ejemplo de semilla: 1001000100011010001010110011110001001101010111100110111100001111 ## 				 							##
##########################################################################################


import sys


##### FUNCIONES #####

# Función que calcula el bit mayoritario... (COMPLETAR)
def mayoria(lfsr_1, lfsr_2, lfsr_3):
	aux_1 = lfsr_1['semilla'][lfsr_1['bit_mayoria']] * lfsr_2['semilla'][lfsr_2['bit_mayoria']]
	aux_2 = lfsr_1['semilla'][lfsr_1['bit_mayoria']] * lfsr_3['semilla'][lfsr_3['bit_mayoria']]
	aux_3 = lfsr_2['semilla'][lfsr_2['bit_mayoria']] * lfsr_3['semilla'][lfsr_3['bit_mayoria']]
	return (aux_1 ^ aux_2 ^ aux_3)

	
##### PROGRAMA PRINCIPAL #####

# INICIALIZACIÓN DE LOS DATOS COMUNES #

mensaje_original = sys.argv[1]

semilla = str(input("Introduzca una semilla de 64 bits: "))
while len(semilla) != 64:
	semilla = str(input("Introduzca una semilla de 64 bits: "))

semilla_1 = []
semilla_2 = []
semilla_3 = []

# Se divide la semilla para los 3 registros #
for i in range(0, 19):
	semilla_1.append(int(semilla[i]))
semilla_1.reverse()

for i in range(19, 41):
	semilla_2.append(int(semilla[i]))
semilla_2.reverse()

for i in range(41, 64):
	semilla_3.append(int(semilla[i]))
semilla_3.reverse()

# Se inicializa los polinomios de cada registro #
polinomio_1 = [13, 16, 17, 18]
polinomio_2 = [20, 21]
polinomio_3 = [7, 20, 21, 22]

# Se inicializa los bits utilizados para la función mayoría #
bit_mayoria_1 = 8
bit_mayoria_2 = 10
bit_mayoria_3 = 10

# Número de generaciones iniciales que serán descartadas #
n_desc = 10


# CIFRADO #

# Se inicializa los 3 registros para el cifrado #
lfsr_1 = {'semilla': semilla_1, 'polinomio': polinomio_1, 'bit_mayoria': bit_mayoria_1}
lfsr_2 = {'semilla': semilla_2, 'polinomio': polinomio_2, 'bit_mayoria': bit_mayoria_2}
lfsr_3 = {'semilla': semilla_3, 'polinomio': polinomio_3, 'bit_mayoria': bit_mayoria_3}

# Se genaran los n_desc bits iniciales que se descartan #
for i in range(n_desc):
	print ()
	print ("Iteración", i + 1, "(DE DESCARTE)")
	print (lfsr_1['semilla'])
	print (lfsr_2['semilla'])
	print (lfsr_3['semilla'])

	entrada_1 = 0
	entrada_2 = 0
	entrada_3 = 0
	
	bit_1 = lfsr_1['semilla'][len(lfsr_1['semilla']) - 1]
	for i in range(len(lfsr_1['polinomio'])):
		entrada_1 = entrada_1 ^ lfsr_1['semilla'][lfsr_1['polinomio'][i]]

	bit_2 = lfsr_2['semilla'][len(lfsr_2['semilla']) - 1]
	for i in range(len(lfsr_2['polinomio'])):
		entrada_2 = entrada_2 ^ lfsr_2['semilla'][lfsr_2['polinomio'][i]]

	bit_3 = lfsr_3['semilla'][len(lfsr_3['semilla']) - 1]
	for i in range(len(lfsr_3['polinomio'])):
		entrada_3 = entrada_3 ^ lfsr_3['semilla'][lfsr_3['polinomio'][i]]
	
	bit_mayoria = mayoria(lfsr_1, lfsr_2, lfsr_3)
	
	if lfsr_1['semilla'][lfsr_1['bit_mayoria']] == bit_mayoria:
		lfsr_1['semilla'].insert(0, entrada_1)
		lfsr_1['semilla'].pop()
	
	if lfsr_2['semilla'][lfsr_2['bit_mayoria']] == bit_mayoria:
		lfsr_2['semilla'].insert(0, entrada_2)
		lfsr_2['semilla'].pop()
	
	if lfsr_3['semilla'][lfsr_3['bit_mayoria']] == bit_mayoria:
		lfsr_3['semilla'].insert(0, entrada_3)
		lfsr_3['semilla'].pop()

print ()
print ("Se han descartado los", n_desc, "bits iniciales.")
print ()


# Se genera la secuencia cifrante #
salida = ''

for i in range(len(mensaje_original) * 8):
	print ()
	print ("Iteración", i + 1)
	print (lfsr_1['semilla'])
	print (lfsr_2['semilla'])
	print (lfsr_3['semilla'])
	
	entrada_1 = 0
	entrada_2 = 0
	entrada_3 = 0
	
	bit_1 = lfsr_1['semilla'][len(lfsr_1['semilla']) - 1]
	for i in range(len(lfsr_1['polinomio'])):
		entrada_1 = entrada_1 ^ lfsr_1['semilla'][lfsr_1['polinomio'][i]]

	bit_2 = lfsr_2['semilla'][len(lfsr_2['semilla']) - 1]
	for i in range(len(lfsr_2['polinomio'])):
		entrada_2 = entrada_2 ^ lfsr_2['semilla'][lfsr_2['polinomio'][i]]

	bit_3 = lfsr_3['semilla'][len(lfsr_3['semilla']) - 1]
	for i in range(len(lfsr_3['polinomio'])):
		entrada_3 = entrada_3 ^ lfsr_3['semilla'][lfsr_3['polinomio'][i]]
	
	salida += str(bit_1 ^ bit_2 ^ bit_3)
	
	bit_mayoria = mayoria(lfsr_1, lfsr_2, lfsr_3)
	
	if lfsr_1['semilla'][lfsr_1['bit_mayoria']] == bit_mayoria:
		lfsr_1['semilla'].insert(0, entrada_1)
		lfsr_1['semilla'].pop()
	
	if lfsr_2['semilla'][lfsr_2['bit_mayoria']] == bit_mayoria:
		lfsr_2['semilla'].insert(0, entrada_2)
		lfsr_2['semilla'].pop()
	
	if lfsr_3['semilla'][lfsr_3['bit_mayoria']] == bit_mayoria:
		lfsr_3['semilla'].insert(0, entrada_3)
		lfsr_3['semilla'].pop()
	
	print ("Secuencia cifrante:", salida)

print ()
print ("Cifrando mensaje original...")	

mensaje_cifrado = ''
for i in range(len(mensaje_original)):
	mensaje_cifrado += chr(int(salida[i*8:(i+1)*8], 2) ^ ord(mensaje_original[i]))

print ("Mensaje cifrado: " + mensaje_cifrado)
print ()


# DESCIFRADO #

semilla_1 = []
semilla_2 = []
semilla_3 = []

# Se divide la semilla para los 3 registros #
for i in range(0, 19):
	semilla_1.append(int(semilla[i]))
semilla_1.reverse()

for i in range(19, 41):
	semilla_2.append(int(semilla[i]))
semilla_2.reverse()

for i in range(41, 64):
	semilla_3.append(int(semilla[i]))
semilla_3.reverse()

# Se inicializa los 3 registros para el descifrado #
lfsr_1_desc = {'semilla': semilla_1, 'polinomio': polinomio_1, 'bit_mayoria': bit_mayoria_1}
lfsr_2_desc = {'semilla': semilla_2, 'polinomio': polinomio_2, 'bit_mayoria': bit_mayoria_2}
lfsr_3_desc = {'semilla': semilla_3, 'polinomio': polinomio_3, 'bit_mayoria': bit_mayoria_3}

# Se genaran los n_desc bits iniciales que se descartan #
for i in range(n_desc):
	entrada_1 = 0
	entrada_2 = 0
	entrada_3 = 0
	
	bit_1 = lfsr_1_desc['semilla'][len(lfsr_1_desc['semilla']) - 1]
	for i in range(len(lfsr_1_desc['polinomio'])):
		entrada_1 = entrada_1 ^ lfsr_1_desc['semilla'][lfsr_1_desc['polinomio'][i]]

	bit_2 = lfsr_2_desc['semilla'][len(lfsr_2_desc['semilla']) - 1]
	for i in range(len(lfsr_2_desc['polinomio'])):
		entrada_2 = entrada_2 ^ lfsr_2_desc['semilla'][lfsr_2_desc['polinomio'][i]]

	bit_3 = lfsr_3_desc['semilla'][len(lfsr_3_desc['semilla']) - 1]
	for i in range(len(lfsr_3_desc['polinomio'])):
		entrada_3 = entrada_3 ^ lfsr_3_desc['semilla'][lfsr_3_desc['polinomio'][i]]
	
	bit_mayoria = mayoria(lfsr_1_desc, lfsr_2_desc, lfsr_3_desc)
	
	if lfsr_1_desc['semilla'][lfsr_1_desc['bit_mayoria']] == bit_mayoria:
		lfsr_1_desc['semilla'].insert(0, entrada_1)
		lfsr_1_desc['semilla'].pop()
	
	if lfsr_2_desc['semilla'][lfsr_2_desc['bit_mayoria']] == bit_mayoria:
		lfsr_2_desc['semilla'].insert(0, entrada_2)
		lfsr_2_desc['semilla'].pop()
	
	if lfsr_3_desc['semilla'][lfsr_3_desc['bit_mayoria']] == bit_mayoria:
		lfsr_3_desc['semilla'].insert(0, entrada_3)
		lfsr_3_desc['semilla'].pop()


# Se genera la secuencia descifrante #
salida = ''

for i in range(len(mensaje_cifrado) * 8):
	entrada_1 = 0
	entrada_2 = 0
	entrada_3 = 0
	
	bit_1 = lfsr_1_desc['semilla'][len(lfsr_1_desc['semilla']) - 1]
	for i in range(len(lfsr_1_desc['polinomio'])):
		entrada_1 = entrada_1 ^ lfsr_1_desc['semilla'][lfsr_1_desc['polinomio'][i]]

	bit_2 = lfsr_2_desc['semilla'][len(lfsr_2_desc['semilla']) - 1]
	for i in range(len(lfsr_2_desc['polinomio'])):
		entrada_2 = entrada_2 ^ lfsr_2_desc['semilla'][lfsr_2_desc['polinomio'][i]]

	bit_3 = lfsr_3_desc['semilla'][len(lfsr_3_desc['semilla']) - 1]
	for i in range(len(lfsr_3_desc['polinomio'])):
		entrada_3 = entrada_3 ^ lfsr_3_desc['semilla'][lfsr_3_desc['polinomio'][i]]
	
	salida += str(bit_1 ^ bit_2 ^ bit_3)
	
	bit_mayoria = mayoria(lfsr_1_desc, lfsr_2_desc, lfsr_3_desc)
	
	if lfsr_1_desc['semilla'][lfsr_1_desc['bit_mayoria']] == bit_mayoria:
		lfsr_1_desc['semilla'].insert(0, entrada_1)
		lfsr_1_desc['semilla'].pop()
	
	if lfsr_2_desc['semilla'][lfsr_2_desc['bit_mayoria']] == bit_mayoria:
		lfsr_2_desc['semilla'].insert(0, entrada_2)
		lfsr_2_desc['semilla'].pop()
	
	if lfsr_3_desc['semilla'][lfsr_3_desc['bit_mayoria']] == bit_mayoria:
		lfsr_3_desc['semilla'].insert(0, entrada_3)
		lfsr_3_desc['semilla'].pop()

print ("Descifrando mensaje cifrado...")
print ("Secuencia descifrante:", salida)

mensaje_descifrado = ''
for i in range(len(mensaje_cifrado)):
	mensaje_descifrado += chr(int(salida[i*8:(i+1)*8], 2) ^ ord(mensaje_cifrado[i]))

print ("Mensaje descifrado: " + mensaje_descifrado)


sys.exit(0)
