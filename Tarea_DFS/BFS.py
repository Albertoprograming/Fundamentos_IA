class EstadoPuzzle:
    def _init_(self, configuracion, nivel, padre, movimiento):
        self.configuracion = configuracion
        self.nivel = nivel
        self.padre = padre
        self.movimiento = movimiento

    def _eq_(self, otro):
        return self.configuracion == otro.configuracion

    def _str_(self):
        return f"Nivel: {self.nivel}\nMovimiento: {self.movimiento}\n{self.configuracion[0]}\n{self.configuracion[1]}\n{self.configuracion[2]}\n"

class SolucionadorPuzzle:
    def _init_(self, configuracion_inicial, configuracion_meta):
        self.estado_inicial = EstadoPuzzle(configuracion_inicial, 1, None, "Inicial")
        self.configuracion_meta = configuracion_meta
        self.cola = [self.estado_inicial]
        self.visitados = set()
        self.soluciones = []

    def resolver(self):
        while self.cola:
            estado_actual = self.cola.pop(0)
            if estado_actual.configuracion == self.configuracion_meta:
                self.construir_solucion(estado_actual)
                return
            self.visitados.add(tuple(map(tuple, estado_actual.configuracion)))
            x, y = self.obtener_posicion_casilla_vacia(estado_actual.configuracion)

            vecinos = self.generar_vecinos(estado_actual, x, y)
            self.cola.extend(vecinos)

    def obtener_posicion_casilla_vacia(self, configuracion):
        for i in range(3):
            for j in range(3):
                if configuracion[i][j] == 0:
                    return i, j

    def generar_vecinos(self, estado, x, y):
        vecinos = []
        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in movimientos:
            nueva_x, nueva_y = x + dx, y + dy
            if 0 <= nueva_x < 3 and 0 <= nueva_y < 3:
                nueva_configuracion = [list(fila) for fila in estado.configuracion]
                nueva_configuracion[x][y], nueva_configuracion[nueva_x][nueva_y] = nueva_configuracion[nueva_x][nueva_y], nueva_configuracion[x][y]
                if tuple(map(tuple, nueva_configuracion)) not in self.visitados:
                    nuevo_nivel = estado.nivel + 1
                    movimiento_nombre = self.obtener_nombre_movimiento(dx, dy)
                    vecino = EstadoPuzzle(nueva_configuracion, nuevo_nivel, estado, movimiento_nombre)
                    vecinos.append(vecino)
        return vecinos

    def obtener_nombre_movimiento(self, dx, dy):
        if dx == 1:
            return "Abajo"
        elif dx == -1:
            return "Arriba"
        elif dy == 1:
            return "Derecha"
        else:
            return "Izquierda"

    def construir_solucion(self, estado):
        while estado:
            self.soluciones.insert(0, estado)
            estado = estado.padre

if _name_ == "_main_":
    configuracion_meta = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    configuracion_inicial = [[1, 2, 3], [0, 4, 6], [7, 5, 8]]

    solucionador = SolucionadorPuzzle(configuracion_inicial, configuracion_meta)
    solucionador.resolver()

    for i, solucion in enumerate(solucionador.soluciones):
        print(f"Paso {i + 1} - {solucion.movimiento}")
        print(solucion)