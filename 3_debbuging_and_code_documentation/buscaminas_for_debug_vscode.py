'''
Codigo interactivo para 'jugar' buscaminas (not really). 
Crea un mapa con dimensiones dimx x dimy con 0=safe y 1=bomb de manera random, 
se da una coordenada dentro del mapa y muestra donde hay bombas en la vecindad de esa coordenada.
Las coordenadas del mapa van del (1,1) a (dimx,dimy).
'''

import numpy as np
import matplotlib.pyplot as plt

# pedimos las dimensiones
dimx, dimy = (int(input('Elije las dimensiones del mapa (ej para 5x6: 5 y luego 6):')), 
                    int(input('por ')))
np.random.seed(924*dimx*dimy)
new_map = []
for i in range(dimy):
    # dibujamos el mapa de 0 y 1 random con dimesiones dimx x dimy
    this_row = []
    for j in range(dimx):
        this_row += [np.random.randint(0, 2)] 
    new_map.append(this_row)

# pedimos las coordenadas del jugador
coord_x, coord_y = (int(input('elije una coordenada para el eje x entre entre un mapa de '
                    +str(dimx)+'x'+str(dimy)+': '))-1, int(input('y una para el eje y: '))-1)


def see_vecinity(new_map, coord_x, coord_y):
    '''Funcion que revisa los alrrederores de el punto del jugador
    
    Parameters
    ----------
        new_map : list
            matrix de 0 y uno
        coord_x : int
            coordenada en x
        coord_y : int
    '''
    if coord_x == dimx:
        cords_x_to_see = [coord_x-1, coord_x]
    elif coord_x == 0:
        cords_x_to_see = [coord_x, coord_x+1]
    else:
        cords_x_to_see = [coord_x-1, coord_x, coord_x+1]  

    if coord_y == dimy:
        cords_y_to_see = [coord_y-1, coord_y]
    elif coord_y == 0:
        cords_y_to_see = [coord_y, coord_y+1]
    else:
        cords_y_to_see = [coord_y-1, coord_y, coord_y+1]

    vecinos = []
    for x in cords_x_to_see:
        for y in cords_y_to_see:
            vecinos = [[new_map[y][x], (y, x)]]

    return where_bomb(vecinos)
    
def where_bomb(vecinos):
    '''Funcion que revisa cual es bomba entre los vecinos
    
    Parameters
    ----------
        vecinos : list
            lista de listas con valor de un lugar vecino 
            y sus coordenadas
    '''
    print('\n')
    for i in vecinos:
        if i[0] == 1:
            print('bomb in ', i[1])
        else:
            print('safe in ', i[1])

# con esto se corre el juego
see_vecinity(new_map, coord_x, coord_y)

# mostramos el mapa
plt.figure()
plt.imshow(new_map, cmap='Reds')
plt.plot(coord_x, coord_y, 'og')
plt.gca().invert_yaxis()
plt.gca().xaxis.set_visible(False)
plt.gca().yaxis.set_visible(False)
plt.gca().text(coord_x+0.17, coord_y-0.2, 'tu', fontsize=15, color='g')
plt.title('Mapa')
plt.show()