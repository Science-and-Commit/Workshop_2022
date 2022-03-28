#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 16:25:11 2018

@author: paulina
"""

import numpy as np
import matplotlib.pyplot as plt


#Crear matrices
Temp = np.zeros([200, 400])
Borde = np.zeros([200, 400])


#Funciones para en el futuro aplicar las condiciones de borde
def mar(hora):
    """
    Temperatura para el mar en funcion del tiempo
    ------
    Inputs
    ------
    hora : [float] Hora por evaluar
    ------
    Output:
    ------
    t : [float] temperatura del mar
    """
    if 0 <= hora <= 8:
        t = 4
    if 8 < hora <= 16:
        t = 4 + (16 / 8) * (hora-8)
    if 16 < hora < 24:
        t = 20 - (16 / 8) * (hora-16)
    return t


def atmosfera(hora, altura):
    """
    Temp para la atmosfera en funcion del tiempo y altura
    -----
    Input
    -----
    hora : [float] hora 
    altura : [float] altura en dm
    -----
    Output
    -----
    t : temperatura de la atmosfera
    """
    if 0 <= hora <= 8:
        t = 4 - (6/100) * altura
    if 8 < hora <= 16:
        t = 4 + (16 / 8) * (hora-8) - (6/100) * altura
    if 16 < hora < 24:
        t = 20 - (16 / 8) * (hora-16) - (6/100) * altura
    return t


def tierra():
    """
    Temperatura para la tierra, es constante
    -----
    Input
    -----
    None
    -----
    Output
    -----
    t : [int] temperatura de la tierra en grados celsius = 15ºC
    """
    t = 15
    return t


def nieve():
    """
    Temperatura para la nieve, es constante
    -----
    Input
    -----
    None
    -----
    Output
    -----
    t : [int] temperatura de la nieve en grados celsius = 0ºC
    """
    t = 0
    return t


def chimenea(hora):
    """
    Temperatura para la chimenea en funcion del tiempo
    -----
    Input
    -----
    hora : [float] hora
    -----
    Output
    -----
    t : [int] temperatura de chimenea segun la hora
    """
    t = 500 * (np.cos((np.pi / 12) * hora) + 2)
    return t


#hacer el espacio con montañitas y todo
def CreaBordes(Espacio):
    """
    Aplica las condiciones de borde
    Se definen los rangos donde cambia el borde usando los x
    Luego se itera en el largo y en el ancho segun la geografía
    Devuelve el espacio con las condiciones de borde
    Se agregan los valores de la atmósfera también
    atmosfera=0
    mar=1
    tierra=2
    nieve=3
    chimenea=4
    ------
    Inputs
    ------
    Espacio : [np.zeros(N,N)] Matriz con ceros
    -------
    Outputs
    -------
    Espacio: [np.matrix] Los bordes geográficos con numeros que separan por tipo
    """
    x2 = 121.36
    x3 = 131.36
    x4 = 161.36
    x5 = 241.36
    x6 = 271.36
    x7 = 321.36
    x8 = 400.0
    for i in range(len(Espacio[0, :])):
        if i <= x2:
            Espacio[0, i] = 1
        if x2 < i <= x3:
            Espacio[0, i] = 4
        if x3 < i <= x4:
            for j in range(len(Espacio[:, 0])):
                pendiente = 10.0 / (x4 - x3)
                if j <= (pendiente * (i - x3)):
                    Espacio[j, i] = 2
        if x4 < i <= x5:
            for j in range(len(Espacio[:, 0])):
                pendiente = (150.68 - 10.0) / (x5 - x4)
                if j <= (pendiente * (i - x4) + 10.0):
                    Espacio[j, i] = 2
        if x5 < i <= x6:
            for j in range(len(Espacio[:, 0])):
                pendiente = (130.68 - 150.68) / (x6 - x5)
                if j <= (pendiente * (i - x5) + 150.68):
                    Espacio[j, i] = 2
        if x6 < i <= x7:
            for j in range(len(Espacio[:, 0])):
                pendiente = (185.34 - 130.68) / (x7 - x6)
                if j <= (pendiente * (i - x6) + 130.68):
                    if j <= 180.0:
                        Espacio[j, i] = 2
                    else:
                        Espacio[j, i] = 3
        if x7 < i <= x8:
            for j in range(len(Espacio[:, 0])):
                pendiente = (110.0 - 185.34) / (x8 - x7)
                if j <= (pendiente * (i - x7) + 185.34):
                    if j <= 180.0:
                        Espacio[j, i] = 2
                    else:
                        Espacio[j, i] = 3
    return Espacio


#SE crea la matriz con la geografía del problema
#BordesFijos = CreaBordes(Borde)


#aplicar cond borde en la atmósfera
#hacer el espacio con montañitas y todo
def Inicial(Bordes, temperaturas, hora):
    """
    Aplica las condiciones de borde
    Se definen los rangos donde cambia el borde usando los x
    Luego se itera en el largo y en el ancho segun la geografía
    Devuelve el espacio con las condiciones de borde temp
    Se agregan los valores de la atmósfera también
    ------
    Input
    ------
    Bordes : [np.matrix] Bordes geográficos
    temperaturas: [np.zeros(N,N)] matriz de ceros para temp
    hora: [float] la hora
    -------
    Output
    -------
    temperaturas: [np.matrix] Matriz con temperaturas asociadas a esa hora
    """
    for i in range(len(Bordes[0, :])):
        if Bordes[0, i] == 4:
            temperaturas[0, i] = chimenea(hora)
        for j in range(len(Bordes[:, 0])):
            if Bordes[j, i] == 0:
                T = atmosfera(hora, j)
                temperaturas[j, i] = T
            if Bordes[j, i] == 2:
                temperaturas[j, i] = tierra()
            if Bordes[j, i] == 3:
                temperaturas[j, i] = nieve()
            if Bordes[j, i] == 1:
                temperaturas[j, i] = mar(hora)
    return temperaturas


#Aplicar la edp para la atmósfera
def Itera_uno(temp, Bordes, w=1):
    """
    Funcion para iterar un paso con la ecuacion de Laplace
    Inputs:
        temp : [np.matrix] matriz con temperaturas
        Bordes: [np.matrix] matriz con bordes
        w : [float] parámetro w de sobre relajación
    Outputs:
        temp : [np.matrix] Matriz de temperaturas una iteración después
    """
    temp = temp.copy()
    for i in range(1, len(temp[0, :]) - 1):
        for j in range(1, len(temp[:, 0]) - 1):
            if Bordes[j][i] == 0:
                temp[j][i] = ((1 - w) * temp[j][i] +
                              w / 4 * (temp[j][i+1] + temp[j][i-1] +
                                       temp[j+1][i] + temp[j-1][i]))
    return temp


##Esto es un test para Itera_uno
###################
#Pr=Temp.copy()
#Prueba=Inicial(BordesFijos,Pr,6)
#Prueba2=Itera_uno(Prueba,BordesFijos)
#
#a=(Prueba[1,:]-Prueba2[1,:])
#for i in range(len(a)):
#    if a[i] != 0:
#        print(a[i])
####################


#hacer recurrencia para converger temp
def no_ha_convergido(temp, temp_antes, tol):
    """
    Prueba si los datos han convergido
    -----
    Inputs
    ------
    temp : [np.matrix] Matriz una iteracion antes
    temp_antes : [np.matrix] Matriz una iteracion despues
    tol : [float]  Tolerancia
    -------
    Outputs
    -------
    condicion : [bool] True a la tolerancia o False
    """
    nozero = temp != 0
    diff_relativa = ((temp_antes[nozero] - temp[nozero]) / temp[nozero])
    output = np.max(np.fabs(diff_relativa))
    condicion = output > tol
    return condicion

def convergencia(Temp, BordesFijos, hora, tol=1, itermax=5000, w=1):
    """
    Funcion que hace que la solucion converga
    Utiliza otras funciones dentro de ella  
    -----
    Input
    -----
    Temp : [np.zeros(N,N)] Matriz con ceros para poner la temperatura
    BordesFijos : [np.matrix] Bordes del paisaje
    hora : [float] la hora
    tol : [float] Tolerancia, por defecto 1 
    itermax : [int] numero máximo de iteraciones, por defecto 5000
    w : [float] parámetro del método de sobre relajación, por defecto 1
    ------
    Output
    ------
    temp : [np.matrix] Matriz de temperaturas que convergió
    """
    N = 0
    temp_antes = Inicial(BordesFijos, Temp, hora)
    temp = Itera_uno(temp_antes, BordesFijos, w)
    while no_ha_convergido(temp, temp_antes, tol) and N < itermax:
        #print('paciencia '+str(N))
        temp_antes = temp.copy()
        temp = Itera_uno(temp, BordesFijos)
        N += 1
    #prints para no olvidar estos números importantes
    #print(N)
    return temp

def plot_paisaje(Temp, BordesFijos, hora, w, tol=1):
    """
    Grafica el paisaje a una cierta hora
    -----
    Input
    -----
    Temp : [np.zeros(N,N)] matriz de ceros para la temperatura
    BordesFijos : [np.matrix] matriz con los bordes del paisaje
    hora : [float] la hora
    w : [float] parámtero de relajación
    tol : [float] tolerancia del método de relajación, por defecto = 1
    -----
    Output
    -----
    None
    """
    #plt.imshow()
    #plt.show()
    temp_final = convergencia(Temp,BordesFijos, hora, w=w, tol=tol)
    plt.imshow(np.log10(temp_final+13), origin='lower', interpolation='nearest', cmap=plt.get_cmap('jet'), extent=(0,4,0,2))
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=14)
    cbar.ax.set_title('$log T/ºC $')
    title = 'Hora {}'.format(hora)
    plt.title(title, fontsize=14)
    plt.xlabel('Distancia [km]', fontsize=14)
    plt.ylabel('Altura [km]', fontsize=14)
    plt.show()
    return


#Datos Finales (Se demoran mucho en converger)
#Temperatura_final0 = convergencia(Temp, BordesFijos, 0, w=1.5)
#Temperatura_final8 = convergencia(Temp, BordesFijos, 8, w=1.5)
#Temperatura_final16 = convergencia(Temp, BordesFijos, 16, tol=1e-2, w=1.6)


#Nueva=Temp.copy()
#NuevaTemp=Inicial(BordesFijos, Nueva,12)


