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
def mar(hora, Esp):
    """
    Temp para el mar en funcion del tiempo
    ====
    Inputs:
    hora:
    Esp:
    Output:
    Esp:
    """
    if 0 <= hora <= 8:
        Esp = 4
    if 8 < hora <= 16:
        Esp = 4 + (16 / 8) * hora
    if 16 < hora < 24:
        Esp = 16 - (16 / 8) * hora
    return Esp


def atmosfera(hora, Esp, altura):
    """
    Temp para la atmosfera en funcion del tiempo y altura
    """
    if 0 <= hora <= 8:
        Esp = 4 - (12 / 200.0) * altura
    if 8 < hora <= 16:
        Esp = 4 + (16 / 8) * hora - (12 / 200.0) * altura
    if 16 < hora < 24:
        Esp = 16 - (16 / 8) * hora - (12 / 200.0) * altura
    return Esp


def tierra(Esp):
    """
    Temp para la tierra, es constante
    """
    Esp = 15
    return Esp


def nieve(Esp):
    """
    Temp para la nieve, es constante
    """
    Esp = 0
    return Esp


def chimenea(hora, Esp):
    """
    Temp para la chimenea en funcion del tiempo
    """
    Esp = 500 * (np.cos((np.pi / 12) * hora) + 2)
    return Esp


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
    Inputs:
        Espacio : Matriz con ceros y una hora
    Outputs:
        Espacio: Los bordes geográficos con numeros que separan por tipo
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
BordesFijos = CreaBordes(Borde)


#aplicar cond borde en la atmósfera
#hacer el espacio con montañitas y todo
def Inicial(Bordes, temperaturas, hora):
    """
    Aplica las condiciones de borde
    Se definen los rangos donde cambia el borde usando los x
    Luego se itera en el largo y en el ancho segun la geografía
    Devuelve el espacio con las condiciones de borde temp
    Se agregan los valores de la atmósfera también
    Inputs:
        Bordes : Bordes geográficos
        temperaturas: matriz de ceros para temp
        hora: la hora
    Outputs: 
        temperaturas: Matriz con temperaturas asociadas a esa hora
    """
    for i in range(len(Bordes[0, :])):
        if Bordes[0, i] == 4:
            temperaturas[0, i] = chimenea(hora, temperaturas[0][i])
        for j in range(len(Bordes[:, 0])):
            if Bordes[j, i] == 0:
                T = atmosfera(hora, temperaturas[j][i], j)
                temperaturas[j, i] = T
            if Bordes[j, i] == 1:
                temperaturas[j, i] = tierra(temperaturas[j][i])
            if Bordes[j, i] == 3:
                temperaturas[j, i] = nieve(temperaturas[j][i])
            if Bordes[j, i] == 2:
                temperaturas[j, i] = mar(hora, temperaturas[j][i])
    return temperaturas


#Aplicar la edp para la atmósfera
def Itera_uno(temp, Bordes, w=1):
    """
    Funcion para iterar un paso con la ecuacion de Laplace
    Inputs:
        temp : matriz con temperaturas
        Bordes: matriz con bordes
        w : parámetro w de sobre relajación
    Outputs:
        temp : Matriz de temperaturas una iteración después
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
    Inputs (Matriz una iteracion antes y una despues y una tolerancia)
    Outputs (True a la tolerancia o False)
    """
    nozero = temp != 0
    #diff_relativa=[]
    diff_relativa = ((temp_antes[nozero] - temp[nozero]) / temp[nozero])
    output = np.max(np.fabs(diff_relativa))
    return output > tol


def convergencia(Temp, BordesFijos, hora, tol=1, itermax=5000, w=1):
    """
    Funcion que hace que la solucion converga
    Utiliza otras funciones dentro de ella
    Inputs (Matriz con ceros para poner la temperatura, los bordes y la hora.
            se le puede dar tambien la tolerancia, iteracion max y
            parámetro w del método de sobre relajacion)
    Outputs (Matriz de temperaturas que convergió)
    """
    N = 0
    temp_antes = Inicial(BordesFijos, Temp, hora)
    temp = Itera_uno(temp_antes, BordesFijos, w)
    while no_ha_convergido(temp, temp_antes, tol) and N < itermax:
        #print('paciencia '+str(N))
        temp_antes = temp.copy()
        temp = Itera_uno(temp_antes, BordesFijos)
        N += 1
    #prints para no olvidar estos números importantes
    print(N)
    return temp

def plot_paisaje(Temp, BordesFijos, hora, w, title):
    temp_final = convergencia(Temp,BordesFijos , hora, w=w)
    plt.imshow(np.log(temp_final+13), origin='bottom', interpolation='nearest', cmap=plt.get_cmap('jet'), extent=(0,4,0,2))
    plt.colorbar()
    plt.title(title)
    plt.xlabel('Distancia', fontsize=14)
    plt.ylabel('Altura', fontsize=14)
    plt.show()
    return


#Datos Finales (Se demoran mucho en converger)
#Temperatura_final0 = convergencia(Temp, BordesFijos, 0, w=1.5)
#Temperatura_final8 = convergencia(Temp, BordesFijos, 8, w=1.5)
#Temperatura_final16 = convergencia(Temp, BordesFijos, 16, tol=1e-2, w=1.6)


#Nueva=Temp.copy()
#NuevaTemp=Inicial(BordesFijos, Nueva,12)
#
#####################GRAFICOS#######################
##plot bordes
#plt.clf()
#plt.imshow(np.log(NuevaTemp+13), origin='bottom', interpolation='nearest', 
#           cmap='jet')
#plt.colorbar()
#plt.title('Planta apagada, 12 hrs', fontsize=14)
#plt.xlabel('Distancia', fontsize=14)
#plt.ylabel('Altura', fontsize=14)
#plt.savefig('SinPlantaActiva.jpg')
#plt.show()


##plot hora 0
#plt.clf()
#plt.imshow(np.log(Temperatura_final0+13), origin='bottom', 
#           interpolation='nearest', cmap=plt.get_cmap('jet'), extent=(0,4,0,2))
#plt.colorbar()
#plt.title('Perfil de temperatura en la zona, 0 hrs', fontsize=14)
#plt.xlabel('Distancia', fontsize=14)
#plt.ylabel('Altura', fontsize=14)
#plt.savefig('Temp0.jpg')
#plt.show()
#
#
##plot hora 8
#plt.clf()
#plt.imshow(np.log(Temperatura_final8+13), origin='bottom', 
#           interpolation='nearest', cmap=plt.get_cmap('jet'), extent=(0,4,0,2))
#plt.colorbar()
#plt.title('Perfil de temperatura en la zona, 8 hrs', fontsize=14)
#plt.xlabel('Distancia', fontsize=14)
#plt.ylabel('Altura', fontsize=14)
#plt.savefig('Temp8.jpg')
#plt.show()
#
#
#
##plot hora 16
#plt.clf()
#plt.imshow(np.log(Temperatura_final16+13), origin='bottom', 
#           interpolation='nearest', cmap=plt.get_cmap('jet'), extent=(0,4,0,2))
#plt.colorbar()
#plt.title('Perfil de temperatura en la zona, 16 hrs', fontsize=14)
#plt.xlabel('Distancia', fontsize=14)
#plt.ylabel('Altura', fontsize=14)
#plt.savefig('Temp16.jpg')
#plt.show()




#BUSQUEDA DE numero de iteraciones para diferentes w y la temp promedio 
#####################
#w=np.linspace(1,1.9,9)
#T=np.zeros(9)
#for i in range(len(w)):
#    NuevaTemp=Temp.copy()
#    Temp_final = convergencia(Temp, BordesFijos, 20,tol=1, w=w[i])
#    promedioT=0
#    Contador=0
#    for j in range(len(Temp_final[0,:])):
#        for k in range(len(Temp_final[:,0])):
#            if BordesFijos[k,j]== 0:
#                promedioT+=Temp_final[k,j]
#                Contador += 1
#    T[i]=(promedioT/Contador)
#print(T)    
    

#Conv_12=[62,61,61,60,58,56,54,53,58]
#Conv_20=[895, 1002, 894, 893, 891, 445, 667, 448, 328]
#T_20=[-22.5, -22.08,  -22.5, -22.5, -22.5, -24.7, -23.45, -24.5, -24.58]
#plt.plot(w,Conv_20)
#plt.title('w vs Numero de iteraciones, 20 hrs', fontsize=14)
#plt.xlabel('w', fontsize=14)
#plt.ylabel('N de iteraciones', fontsize=14)
#plt.savefig('w_vs_N_20.jpg')
#plt.show()


#plt.plot(w,T_20)
#plt.title('w vs T promedio, 20 hrs', fontsize=14)
#plt.xlabel('w', fontsize=14)
#plt.ylabel('Temperatura', fontsize=14)
#plt.savefig('w_vs_T_20.jpg')
#plt.show()


