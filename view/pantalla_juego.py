"""
Pantalla principal del juego donde ocurre la acción.
Responsabilidad: Renderizar el juego y manejar la interacción durante la partida.
"""

import pygame
from typing import List


class PantallaJuego:
    """
    Pantalla principal donde se ejecuta el juego.
    """

    def __init__(self, ancho=800, alto=600):
        """
        Inicializa la pantalla de juego.

        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        self.gestor_juego = None  # Se asigna externamente

        # Configuración de la carretera
        self.alto_carretera = 300
        self.y_carretera = alto - self.alto_carretera
        self.carriles = [
            self.y_carretera + 50,  # Carril inferior (y=0)
            self.y_carretera + 150,  # Carril medio (y=1)
            self.y_carretera + 250,  # Carril superior (y=2)
        ]

        # Configuración visual
        self.offset_camara = 0
        self.posicion_carrito_pantalla = 100  # Posición fija del carrito en pantalla

        # HUD
        self.alto_hud = 80
        self.mostrar_arbol = True  # Activar visualización del árbol por defecto
        self.mostrar_hitbox = False
        self.visualizador_arbol = None
        
        # Inicializar visualizador del árbol
        from view.visualizador_arbol import VisualizadorArbol
        self.visualizador_arbol = VisualizadorArbol(ancho=400, alto=400)

    def dibujar(self, screen):
        """
        Dibuja toda la pantalla de juego.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        self.dibujar_fondo(screen)
        self.dibujar_carretera(screen)
        self.dibujar_obstaculos(screen)
        self.dibujar_carrito(screen)
        self.dibujar_hud(screen)
        
        # Dibujar árbol AVL si está habilitado
        if self.mostrar_arbol and self.gestor_juego:
            self.dibujar_visualizacion_arbol(screen)

    def dibujar_fondo(self, screen):
        """
        Dibuja el fondo del juego (cielo, etc.).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        # Fondo azul cielo
        screen.draw.filled_rect(pygame.Rect(0, 0, self.ancho, self.y_carretera), (135, 206, 235))

    def dibujar_carretera(self, screen):
        """
        Dibuja la carretera y los carriles.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        # Carretera principal (gris)
        screen.draw.filled_rect(
            pygame.Rect(0, self.y_carretera, self.ancho, self.alto_carretera),
            (100, 100, 100)
        )
        
        # Líneas divisorias de carriles
        for i, y_carril in enumerate(self.carriles):
            if i < len(self.carriles) - 1:
                # Línea blanca discontinua
                for x in range(0, self.ancho, 20):
                    screen.draw.line(
                        (x, y_carril + 50),
                        (x + 10, y_carril + 50),
                        (255, 255, 255)
                    )

    def dibujar_carrito(self, screen):
        """
        Dibuja el carrito del jugador.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        if not self.gestor_juego or not self.gestor_juego.carrito:
            return
        
        carrito = self.gestor_juego.carrito
        
        # Calcular posición en pantalla
        x_pantalla = self.posicion_carrito_pantalla
        y_pantalla = self.carriles[carrito.y] - 15  # Centrar en el carril
        
        # Ajustar por salto
        if carrito.esta_saltando():
            # Calcular altura del salto
            progreso = carrito.tiempo_salto / carrito.duracion_salto
            altura_salto = int(carrito.altura_salto * 4 * progreso * (1 - progreso))
            y_pantalla -= altura_salto
        
        # Color del carrito según estado
        if carrito.estado.value == "saltando":
            color = (255, 255, 0)  # Amarillo
        elif carrito.estado.value == "colisionando":
            color = (255, 0, 0)    # Rojo
        else:
            color = (0, 100, 255)  # Azul
        
        # Dibujar carrito como rectángulo
        rect_carrito = pygame.Rect(x_pantalla, y_pantalla, carrito.ancho, carrito.alto)
        screen.draw.filled_rect(rect_carrito, color)
        screen.draw.rect(rect_carrito, (255, 255, 255))
        
        # Dibujar hitbox en modo debug
        if self.mostrar_hitbox:
            screen.draw.rect(rect_carrito, (255, 0, 0), 1)
            screen.draw.text(
                "HITBOX",
                (x_pantalla, y_pantalla - 15),
                fontsize=10,
                color="red"
            )

    def dibujar_obstaculos(self, screen):
        """
        Dibuja todos los obstáculos visibles en pantalla.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        if not self.gestor_juego or not self.gestor_juego.carrito:
            return
        
        carrito = self.gestor_juego.carrito
        
        # Dibujar obstáculos visibles
        for obstaculo in self.gestor_juego.obstaculos_visibles:
            # Calcular posición en pantalla
            x_pantalla = obstaculo.x - carrito.x + self.posicion_carrito_pantalla
            y_pantalla = self.carriles[obstaculo.y] - 15
            
            # Solo dibujar si está en pantalla
            if -50 <= x_pantalla <= self.ancho + 50:
                self.dibujar_obstaculo(screen, obstaculo, x_pantalla, y_pantalla)

    def dibujar_obstaculo(self, screen, obstaculo, x, y):
        """
        Dibuja un obstáculo individual.

        Args:
            screen: Superficie de pygame donde dibujar
            obstaculo: Obstáculo a dibujar
            x, y: Posición en pantalla
        """
        # Color según tipo de obstáculo
        colores = {
            "roca": (139, 69, 19),      # Marrón
            "cono": (255, 165, 0),      # Naranja
            "hueco": (0, 0, 0),         # Negro
            "aceite": (105, 105, 105),  # Gris oscuro
            "barrera": (255, 0, 0)      # Rojo
        }
        
        color = colores.get(obstaculo.tipo.value, (128, 128, 128))
        
        # Dibujar obstáculo como rectángulo
        rect_obstaculo = pygame.Rect(x, y, obstaculo.ancho, obstaculo.alto)
        screen.draw.filled_rect(rect_obstaculo, color)
        screen.draw.rect(rect_obstaculo, (255, 255, 255))
        
        # Dibujar hitbox en modo debug
        if self.mostrar_hitbox:
            screen.draw.rect(rect_obstaculo, (255, 0, 0), 1)
        
        # Dibujar tipo de obstáculo como texto
        screen.draw.text(
            obstaculo.tipo.value[:3].upper(),
            (x + 2, y + 2),
            fontsize=8,
            color="white"
        )

    def dibujar_hud(self, screen):
        """
        Dibuja la interfaz de usuario (energía, distancia, controles).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        if not self.gestor_juego or not self.gestor_juego.carrito:
            return
        
        # Fondo del HUD
        screen.draw.filled_rect(
            pygame.Rect(0, 0, self.ancho, self.alto_hud),
            (0, 0, 0, 128)  # Negro semi-transparente
        )
        
        # Barra de energía
        self.dibujar_barra_energia(screen)
        
        # Información del juego
        self.dibujar_informacion_juego(screen)
        
        # Controles disponibles
        self.dibujar_controles_disponibles(screen)

    def dibujar_barra_energia(self, screen):
        """
        Dibuja la barra de energía del carrito.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        carrito = self.gestor_juego.carrito
        porcentaje = carrito.obtener_porcentaje_energia()
        
        # Fondo de la barra
        screen.draw.filled_rect(
            pygame.Rect(10, 10, 200, 20),
            (50, 50, 50)
        )
        
        # Barra de energía
        ancho_energia = int(200 * porcentaje)
        color_energia = (0, 255, 0) if porcentaje > 0.5 else (255, 255, 0) if porcentaje > 0.2 else (255, 0, 0)
        
        screen.draw.filled_rect(
            pygame.Rect(10, 10, ancho_energia, 20),
            color_energia
        )
        
        # Texto de energía
        screen.draw.text(
            f"Energia: {int(porcentaje * 100)}%",
            (220, 12),
            fontsize=14,
            color="white"
        )

    def dibujar_informacion_juego(self, screen):
        """
        Dibuja información del juego (distancia, puntos, etc.).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        stats = self.gestor_juego.obtener_estadisticas()
        
        # Distancia recorrida
        screen.draw.text(
            f"Distancia: {stats['distancia_recorrida']}/{stats['distancia_total']}m",
            (10, 40),
            fontsize=12,
            color="white"
        )
        
        # Puntuación
        screen.draw.text(
            f"Puntuacion: {stats['puntuacion']}",
            (10, 55),
            fontsize=12,
            color="white"
        )
        
        # Obstáculos visibles
        screen.draw.text(
            f"Obstaculos visibles: {stats['obstaculos_visibles']}",
            (300, 12),
            fontsize=12,
            color="white"
        )

    def dibujar_controles_disponibles(self, screen):
        """
        Dibuja los controles disponibles en pantalla.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        # Controles en la esquina inferior derecha
        x = self.ancho - 200
        y = self.alto - 80
        
        screen.draw.text(
            "Controles:",
            (x, y),
            fontsize=12,
            color="white"
        )
        
        screen.draw.text(
            "↑↓ Mover carril",
            (x, y + 15),
            fontsize=10,
            color="white"
        )
        
        screen.draw.text(
            "ESPACIO Saltar",
            (x, y + 30),
            fontsize=10,
            color="white"
        )
        
        screen.draw.text(
            "P Pausar",
            (x, y + 45),
            fontsize=10,
            color="white"
        )
        
        screen.draw.text(
            "T Mostrar Árbol",
            (x, y + 60),
            fontsize=10,
            color="white"
        )
        
        screen.draw.text(
            "H Mostrar Hitboxes",
            (x, y + 75),
            fontsize=10,
            color="white"
        )
        
        screen.draw.text(
            "B Recorrido en anchura",
            (x - 80, y + 90),
            fontsize=10,
            color="white"
        )
        
        screen.draw.text(
            "D Recorrido en profundidad",
            (x - 80, y + 105),
            fontsize=10,
            color="white"
        )

    def dibujar_visualizacion_arbol(self, screen):
        """
        Dibuja la visualización del árbol AVL.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        if not self.gestor_juego or not self.visualizador_arbol:
            return
            
        # Dibujar fondo semitransparente
        fondo_rect = pygame.Rect(self.ancho - 420, 50, 400, 400)
        s = pygame.Surface((400, 400), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))  # Fondo negro semitransparente
        screen.blit(s, (self.ancho - 420, 50))
        
        # Dibujar título
        screen.draw.text(
            "Visualización del Árbol AVL",
            (self.ancho - 410, 60),
            fontsize=14,
            color="white"
        )
        
        # Actualizar el árbol con los obstáculos visibles actuales
        self.visualizador_arbol.recorrido_actual = self.gestor_juego.obstaculos_visibles
        
        # Dibujar el árbol
        self.visualizador_arbol.dibujar_arbol(
            screen, 
            self.gestor_juego.arbol_obstaculos,
            x_offset=self.ancho - 420, 
            y_offset=50
        )
        
        # Información adicional
        total_nodos = self.gestor_juego.arbol_obstaculos.obtener_total_obstaculos()
        obstaculos_visibles = len(self.gestor_juego.obstaculos_visibles)
        screen.draw.text(
            f"Total de obstáculos: {total_nodos}",
            (self.ancho - 410, 430),
            fontsize=12,
            color="white"
        )
        screen.draw.text(
            f"Obstáculos visibles: {obstaculos_visibles}",
            (self.ancho - 410, 450),
            fontsize=12,
            color="yellow" if obstaculos_visibles > 0 else "white"
        )
        
        # Posición del carrito
        if self.gestor_juego.carrito:
            screen.draw.text(
                f"Posición del carrito: {self.gestor_juego.carrito.x}",
                (self.ancho - 410, 470),
                fontsize=12,
                color="cyan"
            )

    def manejar_evento(self, evento):
        """
        Maneja los eventos de entrada del usuario.

        Args:
            evento: Evento de pygame

        Returns:
            str: Acción a realizar ('pausar', 'configurar', 'salir', None)
        """
        pass

    def manejar_teclas_juego(self, teclas_presionadas):
        """
        Maneja las teclas que controlan el juego en tiempo real.

        Args:
            teclas_presionadas: Estado actual de las teclas
        """
        pass

    def actualizar_camara(self):
        """
        Actualiza la posición de la cámara basándose en el carrito.
        """
        pass

    def convertir_coordenada_mundo_a_pantalla(self, x_mundo, y_mundo):
        """
        Convierte coordenadas del mundo del juego a coordenadas de pantalla.

        Args:
            x_mundo (int): Coordenada X en el mundo
            y_mundo (int): Coordenada Y en el mundo (carril)

        Returns:
            Tuple[int, int]: Coordenadas de pantalla (x, y)
        """
        pass

    def esta_en_pantalla(self, x_mundo):
        """
        Verifica si una coordenada X del mundo está visible en pantalla.

        Args:
            x_mundo (int): Coordenada X en el mundo

        Returns:
            bool: True si está visible
        """
        pass

    def mostrar_ventana_arbol(self):
        """
        Muestra la ventana emergente con el árbol AVL.
        """
        pass

    def ocultar_ventana_arbol(self):
        """
        Oculta la ventana emergente del árbol AVL.
        """
        pass

    def dibujar_efecto_colision(self, screen, posicion):
        """
        Dibuja un efecto visual cuando ocurre una colisión.

        Args:
            screen: Superficie de pygame donde dibujar
            posicion: Posición donde ocurrió la colisión
        """
        pass

    def dibujar_particulas_salto(self, screen):
        """
        Dibuja efectos de partículas cuando el carrito salta.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass
