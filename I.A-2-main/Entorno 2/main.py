# Librerias
import pygame
import random
import os
import platform

# Clase aspiradora
class Aspiradora:
    # Constructor de la aspiradora
    def __init__(self, coord_x, coord_y, entorno, n_suciedad) -> None:
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.entorno = entorno
        self.suciedad = n_suciedad
        
        # Variables del entorno
        self.puntuacion = 0 
        self.movimientos = 0
        self.destino_x = None
        self.destino_y = None
    
    # Esta funcion le permite al agente evaluar si necesita limpiar una casilla, o seguir moviendose
    def percibir_suciedad(self) -> None:
        if self.entorno[self.coord_y][self.coord_x] == "sucia": # Limpia la suciedad
            self.limpiar()
        else:
            if self.destino_x is None and self.destino_y is None:
                self.establecer_destino() # Establece un nuevo destino si no hay uno
            self.mover() # Se mueve a otra celda

    # Establecer un nuevo destino para la aspiradora
    def establecer_destino(self) -> None:
        for i in range(5):
            for j in range(5):
                if self.entorno[i][j] == "sucia":
                    self.destino_x = j
                    self.destino_y = i
                    return
    
    # Direcciones posibles en que la aspiradora puede moverse en el entorno
    def mover(self) -> None:
        # Si existe un destino, entonces la aspiradora se movera
        if self.destino_x is not None and self.destino_y is not None: # Si el destino es none, no se movera
            if self.coord_x < self.destino_x:
                self.coord_x += 1
            elif self.coord_x > self.destino_x:
                self.coord_x -= 1
            
            if self.coord_y < self.destino_y:
                self.coord_y += 1
            elif self.coord_y > self.destino_y:
                self.coord_y -= 1
            
            self.movimientos += 1
            
            # Si se ha llegado al destino, se reinicia el destino
            if self.coord_x == self.destino_x and self.coord_y == self.destino_y:
                self.destino_x = None # Se restablecen las cordenadas a none
                self.destino_y = None


    # Accion de la aspiradora para limpiar una casilla
    def limpiar(self) -> bool:
        if self.entorno[self.coord_y][self.coord_x] == "sucia":
            self.entorno[self.coord_y][self.coord_x] = "limpia"
            self.puntuacion += 1
            self.suciedad -= 1
            return True
        return False
    

# Clase entorno
class Entorno:
    # Constructor del entorno
    def __init__(self) -> None:
        self.celdas = [["limpia" for _ in range(5)] for _ in range(5)]
        self.total_suciedad = 0
        self.generar_suciedad()
    
    # Funcion que genera el estado de suciedad dentro del entorno
    # Esta funcion se cambio porque generaba suciedad en la misma celda varias veces
    def generar_suciedad(self) -> None:
        celdas_ocupadas = set()  # Esta variable guarda las coordenadas de las celdas ya ocupadas
        self.total_suciedad = random.randint(5, 10)
        
        while len(celdas_ocupadas) < self.total_suciedad:
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if (x, y) not in celdas_ocupadas:  # Solo generar suciedad en celdas nuevas
                self.celdas[x][y] = "sucia"
                celdas_ocupadas.add((x, y))


def main() -> None:
    # Define el sistema operativo
    if platform.system() == "Linux":
        CLEAR = "clear"
    else:
        CLEAR = "cls"


    os.system(CLEAR)
    numero_simulaciones = int(input("Numero de simulaciones deseadas: "))

    # Se inicia el modulo de pygame
    pygame.init()

    # Opciones de la ventana, tamaño de la celda
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ANCHO_VENTANA = 500
    ALTO_VENTANA = 500
    RESOLUCION = (ALTO_VENTANA, ANCHO_VENTANA)
    TAMANO_CELDA = 100

    pantalla = pygame.display.set_mode(RESOLUCION)
    pygame.display.set_caption("Entorno de aspiradora")

    # Cargamos la imagen de la basura y de la aspiradora
    basura_img = pygame.image.load("src/compost.png")
    asp_img = pygame.image.load("src/aspiradora.png")
    # Escalamos las imagenes
    basura_img = pygame.transform.scale(basura_img, (TAMANO_CELDA - 50, TAMANO_CELDA - 50))
    asp_img = pygame.transform.scale(asp_img, (TAMANO_CELDA - 50, TAMANO_CELDA - 50))

    
    # Creamos un reloj para controlar el tiempo de actualizacion de la ventana y asi
    # poder ver el funcionamiento del agente
    clock = pygame.time.Clock()
    
    puntuaciones = []  # Lista para almacenar las puntuaciones de cada simulación
    movimientos_totales = 0
    
    for i in range(numero_simulaciones):
        # Variables de simulación
        tiempo_simulacion = 100  # Número de iteraciones
        iteracion = 0
   
        # Generamos el entorno y la aspiradora
        entorno = Entorno()
        aspiradora_agente = Aspiradora(0, 0, entorno.celdas, entorno.total_suciedad)
    
        while iteracion < tiempo_simulacion and aspiradora_agente.suciedad != 0:
            # Eventos del programa, tales como entradas de inputs
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            aspiradora_agente.percibir_suciedad()
            
            pantalla.fill(WHITE)

            # Dibujamos el entorno
            for fila in range(5):
                for columna in range(5):
                    x = columna * TAMANO_CELDA
                    y = fila * TAMANO_CELDA
                    color = WHITE 
                    if entorno.celdas[fila][columna] == "sucia":
                        # Coordenadas de la basura
                        x_celda = columna * TAMANO_CELDA
                        y_celda = fila * TAMANO_CELDA
                        
                        
                        # Centramos la imagen
                        img_ancho, img_alto = basura_img.get_size()  # Obtener tamaño de la imagen

                        # Calcular el desplazamiento para centrar la imagen dentro de la celda
                        x_centrada = x_celda + (TAMANO_CELDA - img_ancho) // 2
                        y_centrada = y_celda + (TAMANO_CELDA - img_alto) // 2

                        # Dibujamos la imagen
                        pantalla.blit(basura_img, (x_centrada, y_centrada))
                        pygame.draw.rect(pantalla, BLACK, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)
                    else:
                        pygame.draw.rect(pantalla, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                        pygame.draw.rect(pantalla, BLACK, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)

            # Dibujar las aspiradora
            x_celda = aspiradora_agente.coord_x * TAMANO_CELDA
            y_celda = aspiradora_agente.coord_y * TAMANO_CELDA

            # Centrar la imagen en la celda
            img_ancho, img_alto = asp_img.get_size()  # Obtiene el tamaño de la imagen

            # Calcular el desplazamiento
            x_centrada = x_celda + (TAMANO_CELDA - img_ancho) // 2
            y_centrada = y_celda + (TAMANO_CELDA - img_alto) // 2

            # Dibujar la imagen centrada
            pantalla.blit(asp_img, (x_centrada, y_centrada))

            pygame.display.flip()
            clock.tick(20) # Aumentar o disminuir para la velocidad de la simulacion, recomiendo una velocidad alta
            iteracion += 1
        
        # Almacenar la puntuación y los movimientos para cada simulación
        puntuaciones.append(aspiradora_agente.puntuacion)
        movimientos_totales += aspiradora_agente.movimientos
        print(f"Simulación {i+1} -> Puntuación: {aspiradora_agente.puntuacion}, Movimientos: {aspiradora_agente.movimientos}")

    # Calcular la puntuación media global y la media de movimientos
    puntuacion_media = sum(puntuaciones) / numero_simulaciones
    movimientos_medios = movimientos_totales / numero_simulaciones

    print(f"Puntuación media global: {puntuacion_media}")
    print(f"Número medio de movimientos: {movimientos_medios}")

    pygame.quit()


if __name__ == "__main__":
    main()