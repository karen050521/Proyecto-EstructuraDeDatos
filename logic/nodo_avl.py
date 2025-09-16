"""
Nodo para el árbol AVL que almacena obstáculos por coordenadas.
Responsabilidad: Representar un nodo individual del árbol con balanceamiento automático.
"""


class NodoAVL:
    """
    Nodo individual del árbol AVL que contiene un obstáculo.
    Mantiene referencias a hijos, altura y factor de balance.
    """

    def __init__(self, obstaculo):
        """
        Inicializa un nodo AVL con un obstáculo.

        Args:
            obstaculo (Obstaculo): Obstáculo a almacenar en este nodo
        """
        self.obstaculo = obstaculo
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

    def obtener_factor_balance(self):
        """
        Calcula el factor de balance del nodo.

        Returns:
            int: Diferencia entre altura del subárbol izquierdo y derecho
        """
        pass

    def actualizar_altura(self):
        """
        Actualiza la altura del nodo basándose en las alturas de sus hijos.
        """
        pass

    def es_mayor_que(self, otro_obstaculo):
        """
        Compara este nodo con otro obstáculo según las reglas de ordenamiento.
        Primero por coordenada X, luego por Y en caso de empate.

        Args:
            otro_obstaculo (Obstaculo): Obstáculo a comparar

        Returns:
            bool: True si este nodo debe ir a la derecha del otro
        """
        pass

    def es_igual_a(self, otro_obstaculo):
        """
        Verifica si este nodo contiene el mismo obstáculo (mismas coordenadas).

        Args:
            otro_obstaculo (Obstaculo): Obstáculo a comparar

        Returns:
            bool: True si tienen las mismas coordenadas
        """
        pass

    def __str__(self):
        """
        Representación en string del nodo para debugging.

        Returns:
            str: Información del obstáculo contenido
        """
        pass
