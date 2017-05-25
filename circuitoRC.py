import numpy as np
import matplotlib.pyplot as plt
import pylab
import random

#Este ejercicio se hizo teniendo como guia el Bayesian parameter estimation de ComputoCienciasUniandes

#Carga los datos
datos = np.loadtxt("CircuitoRC.txt")
tiempo = datos[:,0]
carga = datos[:,1]

def likelihood(carga, q_model):
        chi_cuadrado = (1.0/2.0)*sum(((carga-q_model)/100)**2)
        return np.exp(-chi_cuadrado)

Vi=10

def modelo(time, R, C):
        return Vi*C*(1-np.exp(-time/(R*C)))

caminata_R = np.empty((0))
caminata_C = np.empty((0))
l_walk = np.empty((0))

caminata_R = np.append(caminata_R, np.random.random())
caminata_C = np.append(caminata_C, np.random.random())

Q_init = modelo(tiempo, caminata_R[0], caminata_C[0])
l_walk = np.append(l_walk, likelihood(carga, Q_init))

n_iterations = 10000

for i in range(n_iterations):
        R_prime = np.random.normal(caminata_R[i], 0.1)
        C_prime = np.random.normal(caminata_C[i], 0.1)

	Q_init = modelo(tiempo, caminata_R[i], caminata_C[i])
        Q_prime = modelo(tiempo, R_prime, C_prime)

	l_prime = likelihood(carga, Q_prime)
        l_init = likelihood(carga, Q_init)

	alpha = l_prime/l_init
        if(alpha>=1.0):
                caminata_R = np.append(caminata_R, R_prime)
                caminata_C = np.append(caminata_C, C_prime)
                l_walk = np.append(l_walk, l_prime)
        else:
                beta = np.random.random()
                if(beta<=alpha):
                        caminata_R = np.append(caminata_R, R_prime) 	
                        caminata_C = np.append(caminata_C, C_prime)
                        l_walk = np.append(l_walk, l_prime)

		else:
                        caminata_R = np.append(caminata_R, caminata_R[i])
                        caminata_C = np.append(caminata_C, caminata_C[i])
                        l_walk = np.append(l_walk, l_init)

max_metodo = np.argmax(l_walk)
R_mejor = caminata_R[max_metodo]
C_mejor = caminata_C[max_metodo]
Q_mejor = modelo(tiempo,R_mejor, C_mejor)


j= "El mejor R es  %f Ohm" %R_mejor
h= "El mejor C es %f F" %C_mejor

fig = plt.figure()
ax = plt.axes()
ax.set_xlabel("Resistencia")
ax.set_ylabel("verosimilitud")
ax.set_title("Resistencia vs Verosimilitud ")
plt.scatter(caminata_R, -np.log(l_walk))
ax.legend()
plt.savefig('Verosimilitud_R.png')
plt.close()

fig = plt.figure()
ax = plt.axes()
ax.set_xlabel("Capacitancia")
ax.set_ylabel("verosimilitud")
ax.set_title("Capacitancia vs Verosimilitud ")
plt.scatter(caminata_C, -np.log(l_walk))
ax.legend()
plt.savefig('Verosimilitud_C.png')
plt.close()

fig = plt.figure()
ax = plt.axes()
ax.set_xlabel("Valor de R")
ax.set_ylabel("Frecuencia")
ax.set_title("Histograma de R ")
plt.hist(caminata_R, 25)
ax.legend()
plt.savefig('Histograma_R.png')
plt.close()

fig = plt.figure()
ax = plt.axes()
ax.set_xlabel("Valor de C")
ax.set_ylabel("Frecuencia")
ax.set_title("Histograma de C ")
plt.hist(caminata_C, 25)
ax.legend()
plt.savefig('Histograma_C.png')
plt.close()

fig = plt.figure()
ax = plt.axes()
ax.set_xlabel("Tiempo")
ax.set_ylabel("Carga")
ax.set_title("Histograma de Carga vs Tiempo")
plt.scatter(tiempo, carga, label="Datos", color='red')
plt.plot(tiempo,Q_mejor)
plt.text(40,10,j)
plt.text(40,5,h)
ax.legend()
plt.savefig('Best_Fit.png')
plt.close()

#-------------------------------------------------------------------------------
#Este ejercicio se realizo utilizando la guia de github que se eneuntra en 
#https://github.com/ComputoCienciasUniandes/MetodosComputacionales/blob/master/notes/14.MonteCarloMethods/bayes_MCMC.ipynb
#-------------------------------------------------------------------------------
