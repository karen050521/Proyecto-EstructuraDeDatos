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
        self.mostrar_arbol = False
        self.ventana_arbol = None

    def dibujar(self, screen):
        """
        Dibuja toda la pantalla de juego.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_fondo(self, screen):
        """
        Dibuja el fondo del juego (cielo, etc.).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_carretera(self, screen):
        """
        Dibuja la carretera y los carriles.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_carrito(self, screen):
        """
        Dibuja el carrito del jugador.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_obstaculos(self, screen):
        """
        Dibuja todos los obstáculos visibles en pantalla.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_obstaculo(self, screen, obstaculo):
        """
        Dibuja un obstáculo individual.

        Args:
            screen: Superficie de pygame donde dibujar
            obstaculo: Obstáculo a dibujar
        """
        pass

    def dibujar_hud(self, screen):
        """
        Dibuja la interfaz de usuario (energía, distancia, controles).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_barra_energia(self, screen):
        """
        Dibuja la barra de energía del carrito.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_informacion_juego(self, screen):
        """
        Dibuja información del juego (distancia, puntos, etc.).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_controles_disponibles(self, screen):
        """
        Dibuja los controles disponibles en pantalla.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_ventana_arbol(self, screen):
        """
        Dibuja la ventana emergente con el árbol AVL si está activa.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

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
