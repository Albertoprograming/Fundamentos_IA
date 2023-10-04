class Puzzle:
    def __init__(self, estado_inicial, estado_meta):
        self.state = estado_inicial
        self.estado_meta = estado_meta
        self.movimientos = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Movimientos izquierda, arriba, derecha, abajo

    def is_goal(self):
        return self.state == self.estado_meta

    def find_empty(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 'e':
                    return i, j

    def get_possible_moves(self):
        empty_i, empty_j = self.find_empty()
        possible_movimiento = []
        # itera a través de los movimientos definidos
        for move in self.movimientos:
            new_i, new_j = empty_i + move[0], empty_j + move[1]
            if 0 <= new_i < len(self.state) and 0 <= new_j < len(self.state[new_i]):
                possible_movimiento.append((new_i, new_j))

        return possible_movimiento

    def hacer_mov(self, move):
        empty_i, empty_j = self.find_empty()
        new_i, new_j = move
        self.state[empty_i][empty_j], self.state[new_i][new_j] = self.state[new_i][new_j], self.state[empty_i][empty_j]

    def dfs_limited(self, depth_limit):
        visited_states = set()  # Utilizar un conjunto para evitar estados duplicados
        stack = [(self.state, depth_limit)]

        while stack:
            current_state, current_depth = stack.pop()

            if current_state == self.estado_meta:
                return True

            if current_depth == 0:
                continue

            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                new_state = [row[:] for row in current_state]
                self.hacer_mov(move)
                if tuple(map(tuple, new_state)) not in visited_states:
                    stack.append((new_state, current_depth - 1))
                    visited_states.add(tuple(map(tuple, new_state)))
                
                # Deshacer el movimiento después de explorar
                self.hacer_mov((move[0] * -1, move[1] * -1))

        return False
# Función para imprimir el estado del rompecabezas
def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

# Convertir las cadenas de texto en listas de listas para representar los rompecabezas
GOAL = '''1-2-3
8-4-5
7-6-e
'''
INICIAL = '''2-8-3
1-e-4
7-6-5'''

goal_puzzle = [list(row.split('-')) for row in GOAL.split('\n') if row]
initial_puzzle = [list(row.split('-')) for row in INICIAL.split('\n') if row]

# Crear objetos Puzzle con los estados iniciales y objetivo
initial_state = Puzzle(initial_puzzle, goal_puzzle)

# Realizar la búsqueda en profundidad limitada con un límite de profundidad de 15
depth_limit = 15
visited_states = []  # Almacenar los estados visitados
if initial_state.dfs_limited(depth_limit):
    print("Se encontró una solución:")
    print_puzzle(initial_state.state)
    visited_states.append([row[:] for row in initial_state.state])  # Copiar la matriz de estado
else:
    print("No se encontró una solución dentro del límite de profundidad.")

# Imprimir todas las matrices visitadas
print("\nMatrices visitadas:")
for state in visited_states:
    print_puzzle(state)
