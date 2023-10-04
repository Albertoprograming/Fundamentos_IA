#Busque en profundidad recursivo
#OASM
#01/10/2023

class Jueguito:
    def __init__(self, estado_inicial, estado_meta):
        self.state = estado_inicial
        self.estado_meta = estado_meta
        self.movimientos = [(1, 0), (0, 1), (-1, 0), (0, -1) ]  # Movimientos izquierda, arriba, derecha, abajo
        
        
    def ig_me(self):#definimos si el estado inicial es igual al objetivo devuelve true si son iguales
        return self.state == self.estado_meta
    
#buscamos "e" posicion como tupla de fila y columna
    def find_empty(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 'e':
                    return i, j
                #obtenenmos las posiciones a las que se puede mover el espacio vacio.
    def posible_mov(self):
        empty_i, empty_j = self.find_empty()
        possible_movimiento = []
    #itera a traves de los movimientos definidos 
        for move in self.movimientos:
            new_i, new_j = empty_i + move[0], empty_j + move[1]
            if 0 <= new_i < len(self.state) and 0 <= new_j < len(self.state[new_i]):  # Corregido aquí
                possible_movimiento.append((new_i, new_j))

        return possible_movimiento
#almacenar posibles soluciones,  toma una posición mov y mueve el espacio vacío a esa posición intercambiando sus valores con la casilla en la que se va a mover
    def hacer_mov(self, move):
        empty_i, empty_j = self.find_empty()
        new_i, new_j = move
        self.state[empty_i][empty_j], self.state[new_i][new_j] = self.state[new_i][new_j], self.state[empty_i][empty_j]
#no sirve
    def basura(self, move):
        self.hacer_mov(move)  # Deshacer el movimiento es igual que hacerlo
        
#busqueda en profundidad limitada
#recibe como parametro el limite para parar
    def dfs_limited(self, depth_limite):
        if self.ig_me():
            return True
        if depth_limite == 0:#verificar profundidad si ha llegado a cero
            return False#si llego al limite
#ni limite ni meta encontrada
        possible_mov = self.posible_mov()
        for move in possible_mov:
            new_state = Jueguito([row[:] for row in self.state], self.estado_meta)  #  copia profunda
            new_state.hacer_mov(move)
            if new_state.dfs_limited(depth_limite - 1):
                visited_states.append([row[:] for row in new_state.state])  # Agregar copia de la matriz visitada
                return True

        return False

# Función para imprimir el estado del rompecabezas
def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

# Convertir las cadenas de texto en listas de listas para representar los rompecabezas
Meta = '''1-2-3
8-e-4
7-6-5
'''
INICIAL = '''2-8-3
1-4-e
7-6-5'''

meta_puzzle = [list(row.split('-')) for row in Meta.split('\n') if row]
initial_puzzle = [list(row.split('-')) for row in INICIAL.split('\n') if row]

# Crear objetos Puzzle con los estados iniciales y objetivo
initial_state = Jueguito(initial_puzzle, meta_puzzle)

# Realizar la búsqueda en profundidad limitada con un límite de profundidad de 15
depth_limite = 5
visited_states = []  # Almacenar los estados visitados
if initial_state.dfs_limited(depth_limite):
    print("Se encontró una solucion de:")
    print_puzzle(initial_state.state)
    visited_states.append([row[:] for row in initial_state.state])  # Copiar la matriz de estado
else:
    print("No se encontro una solución dentro del limite de profundidad.")

# Imprimir todas las matrices visitadas
print("\nResultado y Matrices visitadas:")
for state in visited_states:
    print_puzzle(state)
