"""
Módulo de lógica de negocio del juego.
Contiene todas las estructuras de datos y algoritmos principales.
"""

from .arbol_avl import ArbolAVL
from .carrito import Carrito
from .obstaculo import Obstaculo, TipoObstaculo
from .gestor_juego import GestorJuego, EstadoJuego
from .nodo_avl import NodoAVL

__all__ = [
    'ArbolAVL',
    'Carrito', 
    'Obstaculo',
    'TipoObstaculo',
    'GestorJuego',
    'EstadoJuego',
    'NodoAVL'
]
