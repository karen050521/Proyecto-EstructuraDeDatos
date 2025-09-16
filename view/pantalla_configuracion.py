"""
Pantalla de configuración del juego donde se puede modificar el árbol AVL.
Responsabilidad: Interfaz para administrar obstáculos antes de iniciar el juego.
"""

import pygame
from typing import Optional, Tuple


class PantallaConfiguracion:
    """
    Pantalla que permite configurar el árbol de obstáculos antes de jugar.
    """

    def __init__(self, ancho=800, alto=600):
        """
        Inicializa la pantalla de configuración.

        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        self.gestor_juego = None  # Se asigna externamente

        # Áreas de la interfaz
        self.area_arbol = pygame.Rect(50, 100, 400, 400)
        self.area_controles = pygame.Rect(500, 100, 250, 400)

        # Estado de la interfaz
        self.obstaculo_seleccionado = None
        self.mostrando_recorrido = False
        self.tipo_recorrido_actual = None
        self.recorrido_actual = []

        # Controles de entrada
        self.campo_x = ""
        self.campo_y = ""
        self.tipo_seleccionado = "roca"
        self.campo_activo = None

    def dibujar(self, screen):
        """
        Dibuja toda la pantalla de configuración.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_fondo(self, screen):
        """
        Dibuja el fondo y las divisiones de la pantalla.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_arbol(self, screen):
        """
        Dibuja la visualización gráfica del árbol AVL.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_nodo(self, screen, nodo, x, y, nivel):
        """
        Dibuja un nodo individual del árbol.

        Args:
            screen: Superficie de pygame donde dibujar
            nodo: Nodo del árbol a dibujar
            x (int): Posición X del nodo
            y (int): Posición Y del nodo
            nivel (int): Nivel del nodo en el árbol
        """
        pass

    def dibujar_controles(self, screen):
        """
        Dibuja los controles de la interfaz (campos, botones).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        pass

    def dibujar_campo_texto(self, screen, texto, x, y, ancho, activo):
        """
        Dibuja un campo de texto.

        Args:
            screen: Superficie donde dibujar
            texto (str): Texto actual del campo
            x, y (int): Posición del campo
            ancho (int): Ancho del campo
            activo (bool): Si el campo está activo
        """
        pass

    def dibujar_boton(self, screen, texto, x, y, ancho, alto, activo=True):
        """
        Dibuja un botón.

        Args:
            screen: Superficie donde dibujar
            texto (str): Texto del botón
            x, y (int): Posición del botón
            ancho, alto (int): Dimensiones del botón
            activo (bool): Si el botón está habilitado
        """
        pass

    def dibujar_recorrido(self, screen):
        """
        Dibuja el recorrido actual si está activo.

        Args:
            screen: Superficie donde dibujar
        """
        pass

    def manejar_evento(self, evento):
        """
        Maneja los eventos de entrada del usuario.

        Args:
            evento: Evento de pygame

        Returns:
            str: Acción a realizar ('iniciar_juego', 'salir', None)
        """
        pass

    def manejar_clic_mouse(self, pos):
        """
        Maneja los clics del mouse en la interfaz.

        Args:
            pos (Tuple[int, int]): Posición del clic

        Returns:
            str: Acción a realizar o None
        """
        pass

    def manejar_tecla(self, tecla):
        """
        Maneja las teclas presionadas.

        Args:
            tecla: Tecla presionada
        """
        pass

    def agregar_obstaculo(self):
        """
        Intenta agregar un nuevo obstáculo con los datos ingresados.

        Returns:
            bool: True si se agregó correctamente
        """
        pass

    def eliminar_obstaculo_seleccionado(self):
        """
        Elimina el obstáculo actualmente seleccionado.

        Returns:
            bool: True si se eliminó correctamente
        """
        pass

    def mostrar_recorrido_anchura(self):
        """
        Activa la visualización del recorrido en anchura.
        """
        pass

    def mostrar_recorrido_profundidad(self):
        """
        Activa la visualización del recorrido en profundidad.
        """
        pass

    def limpiar_recorrido(self):
        """
        Limpia la visualización de recorridos.
        """
        pass

    def validar_entrada_obstaculo(self, x, y):
        """
        Valida que las coordenadas ingresadas sean válidas.

        Args:
            x (str): Coordenada X como string
            y (str): Coordenada Y como string

        Returns:
            Tuple[bool, str]: (Es válido, mensaje de error)
        """
        pass

    def obtener_nodo_en_posicion(self, pos):
        """
        Obtiene el nodo del árbol que está en la posición especificada.

        Args:
            pos (Tuple[int, int]): Posición del mouse

        Returns:
            Optional: Nodo en esa posición o None
        """
        pass

    def calcular_posicion_nodo(self, nodo, nivel, indice_en_nivel):
        """
        Calcula la posición visual de un nodo en el árbol.

        Args:
            nodo: Nodo del árbol
            nivel (int): Nivel del nodo
            indice_en_nivel (int): Índice del nodo en su nivel

        Returns:
            Tuple[int, int]: Posición (x, y) del nodo
        """
        pass
