"""
Paula Caceres Burgos

"""
import numpy as np
import matplotlib.pyplot as plt

"""
-------------------------Creacion del paisaeje---------------------------
"""


def paisaje(alto, largo, tiempo, paso=1):
    """
    Inputs:
    =====
    alto : [int] alto del paisaje
    largo : [int] ancho del paisaje
    tiempo : [int] tiempo actual
    paso : [float] paso entre las distancias
    Outputs:
    ====
    matriz : [ndarray (alto,ancho)] matriz con numeros de 0, 1, 2, 3 y 4
            que indican el mapeo del paisaje
            0 : dominio de la planta
            1 : dominio de la atmosfera
            2 : dominio del mar
            3 : dominio del suelo
            4 : dominio del suelo nevado
    """
    fila = int(alto/paso)
    columna = int(largo/paso)
#   creacion de matriz de unos
    matriz = np.ones([fila, columna])  # aqui es solo atmosfera
#   definicion de los indices en que se encuentran los elementos ############
    ancho_mar = int((1200 + 400 * 0.617) / paso)
    ancho_planta = ancho_mar + int(100 / paso)
    ancho_planicie = ancho_planta + int(300 / paso)
    ancho1_cumbre1 = ancho_planicie + int((800 / paso))
    ancho2_cumbre1 = ancho1_cumbre1 + int((300 / paso))
    ancho1_cumbre2 = ancho1_cumbre1 + int((500 / paso))
    alto_cumbre1 = int((1500 + 200 * 0.617) / paso)
    alto_cumbre2 = int((1850 + 100 * 0.617) / paso)
    alto_valle = int((1300 + 200 * 0.617) / paso)
    alto_monte = int(100 / paso)
#   definicion de los lugares en que se encuentran los elementos del paisaje
#   lugar de planta
    matriz[0][ancho_mar:ancho_planta] = 0
#   lugar del mar
    matriz[0][:ancho_mar] = 2
#   lugar del suelo y el suelo nevado
#   pendientes que describen la montana
    pend_incl_0 = alto_monte / (ancho_planicie - ancho_planta)
    pend_incl_1 = (alto_cumbre1 -
                   alto_monte)/(ancho1_cumbre1 - ancho_planicie)
    pend_incl_2 = (alto_cumbre1 -
                   alto_valle) / (ancho2_cumbre1 - ancho1_cumbre1)
    pend_incl_3 = (alto_cumbre2 -
                   alto_valle) / (ancho1_cumbre2 - ancho2_cumbre1)
    for i in range(alto_monte):
        matriz[i][int((1 / pend_incl_0) * i + ancho_planta) + 1:] = 3
    for j in range(ancho_planicie, ancho1_cumbre1):
        matriz[int((j - ancho_planicie) * pend_incl_1) + alto_monte][j:] = 3
    for j in range(ancho1_cumbre1, ancho2_cumbre1):
        matriz[alto_cumbre1 - int((j - ancho1_cumbre1) * pend_incl_2)][j:] = 1
    for j in range(ancho2_cumbre1, ancho1_cumbre2):
        alto = int((j - ancho2_cumbre1) * pend_incl_3) + alto_valle
        if (alto >= 1800):
                matriz[alto][j:] = 4
        else:
            matriz[alto][j:] = 3
    for j in range(ancho1_cumbre2, columna):
        matriz[alto_cumbre2 - int((j - ancho1_cumbre2) * pend_incl_2)][j:] = 1
#    fig2 = plt.figure(2)
#    fig2.clf()
#    ax2 = fig2.add_subplot(111)
#    ax2.set_xlabel("largo",fontsize=15)
#    ax2.set_ylabel("alto",fontsize=15)
#    ax2.set_title("Geografía de Litoral Central con paso "+str(paso))
#    ax2.imshow(matriz, origin='bottom', interpolation='nearest')
#    ax2.contour(matriz, origin='lower')
#    fig2.show()

    return matriz

"""
-------------Funciones de temperatura para cada espacio del paisaje---------
"""


def mar(tiempo):
    """
    Inputs:
    ======
    tiempo : [int] tiempo actual

    Outputs:
    ======
    T_mar : [float] temperatura del mar
    """
    if (tiempo > 8 and tiempo <= 16):
        T_mar = 4 + 2 * (tiempo - 8)
    if (tiempo > 16):
        T_mar = 20 - 2 * (tiempo - 16)
    else:
        T_mar = 4
    return T_mar

    
def planta(tiempo):
    """
    Inputs:
    ======
    tiempo : [int] tiempo actual
    
    Outputs:
    ======
    T_planta : [float] temperatura de la planta
    """
    T_planta = 500 * (np.cos(np.pi * tiempo / 12) + 2)
    return T_planta


def atmosfera(tiempo, altura):
    """
    Inputs:
    ======
    tiempo : [int] tiempo actual
    altura : [int] altura en que se encuentra

    Outputs:
    ======
    T_atm : [float] temperatura de la atmosfera
    """
    if (tiempo > 8 and tiempo <= 16):
        T_atm = 4 + 2 * (tiempo - 8)  - (6/100) * altura
    if (tiempo > 16):
        T_atm = 20 - 2 * (tiempo - 16)  - (6/100) * altura
    else:
        T_atm = 4  - (6/100) * altura
    return T_atm
    
"""
temperatura suelo y suelo nevado:
"""

T_suelo = 15
T_nevado = 0


"""
---------Funcion que crea matriz con las temperaturas segun el tiempo-------
"""


def set_Condiciones_borde(paisaje, dimensiones, tiempo, paso):
    """
    Inputs:
    ======
    paisaje : [func]
    dimensiones : [lista de dos elementos int]
    tiempo : [int]
    paso : [float]

    Outpus:
    ======
    matriz_aux : [ndarray (filas,columnas)]
    """
    
    filas = dimensiones[0]
    columnas = dimensiones[1]
    vista = paisaje(filas, columnas, tiempo, paso)
    matriz_aux = vista.copy()
    for i in range(int(filas/paso)):
        for j in range(int(columnas/paso)):
            if(vista[i][j] == 0):
                matriz_aux[i][j] = planta(tiempo)
            if(vista[i][j] == 1):
                matriz_aux[i][j] = atmosfera(tiempo, i)
            if(vista[i][j] == 2):
                matriz_aux[i][j] = mar(tiempo)
            if(vista[i][j] == 3):
                matriz_aux[i][j] = T_suelo
            if(vista[i][j] == 4):
                matriz_aux[i][j] = T_nevado
    return matriz_aux


"""
---------------Implementacion del metodo de la relajacion---------------------
"""

def una_iteracion(matriz_temp, filas, columnas, tiempo, paso, h=0.01, w=1):
    """
    Inputs:
    ======
    matriz_temp : [ndarray (filas,columnas)]
    h : [float]
    w : [float]

    Outputs: 
    ======
    matriz_temp : [ndarray]
    """
    matriz_paisaje = paisaje(filas, columnas, tiempo, paso)
    for i in range(1, int(filas/paso)-1):
        for j in range(1, int(columnas/paso)-1):
            if(matriz_paisaje[i][j] == 1):
                matriz_temp[i, j] = ((1 - w) * matriz_temp[i, j] +
                            w / 4 * (matriz_temp[i+1, j] + matriz_temp[i-1, j] +
                                     matriz_temp[i, j+1] + matriz_temp[i, j-1] +
                                     h**2 ))

    return matriz_temp


def no_ha_convergido(matriz_temp, matriz_temp_prev, tol_relativa):
    """
    Inputs:
    ======
    matriz_temp : [ndarray (filas,columnas)]
    matriz_temp_prev : [ndarray (filas,columnas)]
    tol_relativa : [float]

    Outputs:
    ======
    output > tol_relativa : [boolean]
    """
    non_zero = matriz_temp != 0
    diff_relativa = (matriz_temp_prev[non_zero] -
                     matriz_temp[non_zero]) / matriz_temp[non_zero]
    output = max(np.fabs(diff_relativa))
    return output > tol_relativa

def convergencia(matriz_temp, matriz_temp_prev, tol_relativa, itermax, filas, columnas, tiempo, paso):
    """
    iteracion del metodo de la sobre relajacion hasta que converge 

    Inputs:
    =======
    matriz_temp : [ndarray (filas,columnas)]
    matriz_temp_prev : [ndarray (filas,columnas)]
    tol_relativa : [float]
    itermax : [int]
    filas : [int]
    columnas : [int]
    tiempo : [float]
    paso : [int]

    Outputs:
    ======
    matriz_temp : [ndarray (filas,columans)]
    """
    contador = 0
    while no_ha_convergido(matriz_temp, matriz_temp_prev, tol_relativa) and contador < itermax :
        matriz_temp_prev = matriz_temp.copy()
        matriz_temp = una_iteracion(matriz_temp, filas, columnas, tiempo, paso, h=0.01)
        contador += 1
    return matriz_temp

"""
----------------Definicion de los parametros del paisaje---------------------
"""


def plot_paisaje(filas, columnas, tiempo, paso, itermax=1000, h=0.01, tol_relativa=1e-5):
    """
    Grafica el paisaje litoral y el impacto en la temperatura

    Inputs 
    =====
    filas : [int] Alto del paisaje en unidades de metro
    columnas : [int] Ancho de paisaje en unidades de metro
    tiempo : [float] hora 
    paso : [int] paso en que se aplica el metodo de la sobrerelajacion
    itermax : [int] iteración del método de la sobrerelajación 
    h : [float] constante 
    tol_relativa : [float] tolerancia del método 

    Outputs
    =====
    None
    """
    matriz_temp = set_Condiciones_borde(paisaje, [filas, columnas], tiempo, paso)
    
    matriz_temp_prev = matriz_temp.copy()
    matriz_temp = una_iteracion(matriz_temp, filas, columnas, tiempo, paso, h=0.01)
    matriz_temp_final = convergencia(matriz_temp, matriz_temp_prev, tol_relativa, itermax, filas, columnas, tiempo, paso)
    plt.xlabel("largo",fontsize=15)
    plt.ylabel("alto",fontsize=15)
    plt.title("Temperatura de Geografía de Litoral Central a las " +str(tiempo)+"hrs", fontsize=10)
    plt.imshow(np.log10(matriz_temp), origin='lower',interpolation='nearest',cmap = "jet", extent=(0,40,0,20))
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=14)
    cbar.ax.set_title('log T/ºC ')
    plt.show()


#plot_paisaje(2000,4000,16,10)
"""
def Temp_promedio_atm(matriz_temp):
    
    Inputs:
    =====
    matriz_temp : [ndarray (filas,columnas)] matriz de temperatura
    Outputs:
    =====
    t_prom : [float] temperatura promedio
    
    matriz_paisaje = paisaje(filas, columnas, tiempo, paso)
    contador = 0
    suma_temp = 0
    for i in range(int(filas/paso)):
        for j in range(int(columnas/paso)):
            if(matriz_paisaje[i][j]==1):
                suma_temp += matriz_temp[i][j]
                contador += 1
    t_prom = suma_temp / contador
    
    return t_prom
"""

#Temp_promedio_atm(matriz_temp)
#Temp_promedio_atm(matriz_temp_0)
