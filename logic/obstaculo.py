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

    def __init__(
        self,
        x: int,
        y: int,
        tipo: TipoObstaculo,
        ancho: int = 30,
        alto: int = 30,
    ) -> None:
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

    def obtener_daño(self) -> int:
        """
        Obtiene el daño que causa este obstáculo al carrito.

        Returns:
            int: Puntos de daño que causa este obstáculo
        """
        return self.DAÑO_POR_TIPO.get(self.tipo, 0)

    def obtener_rectangulo_colision(self) -> dict:
        """
        Obtiene el rectángulo de colisión del obstáculo.

        Returns:
            dict: Diccionario con 'x', 'y', 'ancho', 'alto' del rectángulo
        """
        return {"x": self.x, "y": self.y, "ancho": self.ancho, "alto": self.alto}

    def esta_en_rango(self, x_min: int, x_max: int, y_min: int, y_max: int) -> bool:
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
        return x_min <= self.x <= x_max and y_min <= self.y <= y_max

    def obtener_sprite_nombre(self) -> str:
        """
        Obtiene el nombre del sprite asociado a este tipo de obstáculo.

        Returns:
            str: Nombre del archivo de sprite (sin extensión)
        """
        return self.tipo.value

    def __str__(self) -> str:
        """
        Representación en string del obstáculo.

        Returns:
            str: Información del obstáculo
        """
        return f"Obstaculo({self.tipo.value} en ({self.x}, {self.y}), daño: {self.obtener_daño()})"

    def __eq__(self, other: object) -> bool:
        """
        Compara dos obstáculos por coordenadas.

        Args:
            other (Obstaculo): Otro obstáculo a comparar

        Returns:
            bool: True si tienen las mismas coordenadas
        """
        if not isinstance(other, Obstaculo):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """
        Hash del obstáculo basado en sus coordenadas.

        Returns:
            int: Hash del obstáculo
        """
        return hash((self.x, self.y))
