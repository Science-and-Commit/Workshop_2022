def funcion_paralelizada_process(raza, output):
    output.put(f'La raza de este perro es {raza}')

def funcion_paralelizada_pool(raza):
    return f'La raza de este perro es {raza}'