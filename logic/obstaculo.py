"""
Clase que representa un obstáculo en el juego.
Responsabilidad: Encapsular las propiedades y comportamiento de un obstáculo individual.
"""

from enum import Enum


class TipoObstaculo(Enum):
    """Tipos de obstáculos disponibles en el juego."""

    ROCA = "roca"
    CONO = "cono"
    HUECO = "hueco"
    ACEITE = "aceite"
    BARRERA = "barrera"


class Obstaculo:
    """
    Representa un obstáculo en el juego con posición, tipo y propiedades de daño.
    """

    # Configuración de daño por tipo de obstáculo
    DAÑO_POR_TIPO = {
        TipoObstaculo.ROCA: 20,
        TipoObstaculo.CONO: 10,
        TipoObstaculo.HUECO: 15,
        TipoObstaculo.ACEITE: 5,
        TipoObstaculo.BARRERA: 25,
    }

    def __init__(self, x, y, tipo, ancho=30, alto=30):
        """
        Crea un nuevo obstáculo.

        Args:
            x (int): Posición X en la carretera (distancia)
            y (int): Posición Y (carril: 0=abajo, 1=medio, 2=arriba)
            tipo (TipoObstaculo): Tipo de obstáculo
            ancho (int): Ancho del obstáculo en píxeles
            alto (int): Alto del obstáculo en píxeles
        """
        self.x = x
        self.y = y
        self.tipo = tipo
        self.ancho = ancho
        self.alto = alto

    def obtener_daño(self):
        """
        Obtiene el daño que causa este obstáculo al carrito.

        Returns:
            int: Puntos de daño que causa este obstáculo
        """
        pass

    def obtener_rectangulo_colision(self):
        """
        Obtiene el rectángulo de colisión del obstáculo.

        Returns:
            dict: Diccionario con 'x', 'y', 'ancho', 'alto' del rectángulo
        """
        pass

    def esta_en_rango(self, x_min, x_max, y_min, y_max):
        """
        Verifica si el obstáculo está dentro del rango especificado.

        Args:
            x_min (int): Límite inferior X
            x_max (int): Límite superior X
            y_min (int): Límite inferior Y
            y_max (int): Límite superior Y

        Returns:
            bool: True si está dentro del rango
        """
        pass

    def obtener_sprite_nombre(self):
        """
        Obtiene el nombre del sprite asociado a este tipo de obstáculo.

        Returns:
            str: Nombre del archivo de sprite (sin extensión)
        """
        pass

    def __str__(self):
        """
        Representación en string del obstáculo.

        Returns:
            str: Información del obstáculo
        """
        pass

    def __eq__(self, other):
        """
        Compara dos obstáculos por coordenadas.

        Args:
            other (Obstaculo): Otro obstáculo a comparar

        Returns:
            bool: True si tienen las mismas coordenadas
        """
        pass

    def __hash__(self):
        """
        Hash del obstáculo basado en sus coordenadas.

        Returns:
            int: Hash del obstáculo
        """
        pass
