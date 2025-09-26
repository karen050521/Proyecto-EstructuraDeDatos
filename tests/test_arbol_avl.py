"""
Pruebas unitarias para el Árbol AVL.
"""

import unittest
import sys
import os

# Añadir directorio padre al sys.path para poder importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.arbol_avl import ArbolAVL
from logic.obstaculo import Obstaculo, TipoObstaculo


class TestArbolAVL(unittest.TestCase):
    """Pruebas para la clase ArbolAVL."""
    
    def setUp(self):
        """Inicializa un árbol para cada prueba."""
        self.arbol = ArbolAVL()
        
    def test_arbol_vacio(self):
        """Verifica que un árbol nuevo esté vacío."""
        self.assertIsNone(self.arbol.raiz)
        self.assertEqual(0, self.arbol.obtener_total_obstaculos())
    
    def test_insertar_obstaculo(self):
        """Verifica que se pueda insertar un obstáculo."""
        obstaculo = Obstaculo(100, 1, TipoObstaculo.ROCA)
        resultado = self.arbol.insertar(obstaculo)
        
        self.assertTrue(resultado)
        self.assertEqual(1, self.arbol.obtener_total_obstaculos())
        self.assertIsNotNone(self.arbol.raiz)
    
    def test_insertar_obstaculo_duplicado(self):
        """Verifica que no se pueda insertar un obstáculo duplicado."""
        obstaculo1 = Obstaculo(100, 1, TipoObstaculo.ROCA)
        obstaculo2 = Obstaculo(100, 1, TipoObstaculo.CONO)  # Mismas coordenadas
        
        self.arbol.insertar(obstaculo1)
        resultado = self.arbol.insertar(obstaculo2)
        
        self.assertFalse(resultado)  # No debería permitir duplicados
        self.assertEqual(1, self.arbol.obtener_total_obstaculos())
    
    def test_buscar_obstaculo(self):
        """Verifica que se pueda buscar un obstáculo por coordenadas."""
        obstaculo = Obstaculo(100, 1, TipoObstaculo.ROCA)
        self.arbol.insertar(obstaculo)
        
        # Buscar existente
        resultado = self.arbol.buscar(obstaculo)
        self.assertIsNotNone(resultado)
        self.assertEqual(100, resultado.x)
        self.assertEqual(1, resultado.y)
        
        # Buscar inexistente
        obstaculo_inexistente = Obstaculo(200, 1, TipoObstaculo.ROCA)
        resultado = self.arbol.buscar(obstaculo_inexistente)
        self.assertIsNone(resultado)
    
    def test_buscar_en_rango(self):
        """Verifica la búsqueda por rango de coordenadas."""
        # Insertar varios obstáculos
        self.arbol.insertar(Obstaculo(100, 0, TipoObstaculo.ROCA))
        self.arbol.insertar(Obstaculo(200, 1, TipoObstaculo.CONO))
        self.arbol.insertar(Obstaculo(300, 2, TipoObstaculo.HUECO))
        self.arbol.insertar(Obstaculo(400, 0, TipoObstaculo.ACEITE))
        
        # Buscar en un rango que incluye todos
        resultados = self.arbol.buscar_en_rango(0, 500, 0, 2)
        self.assertEqual(4, len(resultados))
        
        # Buscar en un rango que incluye solo algunos
        resultados = self.arbol.buscar_en_rango(150, 350, 0, 2)
        self.assertEqual(2, len(resultados))
        
        # Verificar que los resultados están ordenados por X
        self.assertEqual(200, resultados[0].x)
        self.assertEqual(300, resultados[1].x)
        
        # Buscar en un rango vacío
        resultados = self.arbol.buscar_en_rango(500, 600, 0, 2)
        self.assertEqual(0, len(resultados))
    
    def test_eliminar_obstaculo(self):
        """Verifica que se pueda eliminar un obstáculo del árbol."""
        obstaculo = Obstaculo(100, 1, TipoObstaculo.ROCA)
        self.arbol.insertar(obstaculo)
        
        resultado = self.arbol.eliminar(obstaculo)
        self.assertTrue(resultado)
        self.assertEqual(0, self.arbol.obtener_total_obstaculos())
        self.assertIsNone(self.arbol.raiz)
        
        # Eliminar obstáculo inexistente
        resultado = self.arbol.eliminar(obstaculo)
        self.assertFalse(resultado)

    def test_recorrido_en_profundidad(self):
        """Verifica el recorrido en profundidad (in-order)."""
        # Insertar obstáculos en desorden
        self.arbol.insertar(Obstaculo(300, 1, TipoObstaculo.ROCA))
        self.arbol.insertar(Obstaculo(100, 1, TipoObstaculo.CONO))
        self.arbol.insertar(Obstaculo(500, 1, TipoObstaculo.HUECO))
        self.arbol.insertar(Obstaculo(200, 1, TipoObstaculo.ACEITE))
        self.arbol.insertar(Obstaculo(400, 1, TipoObstaculo.BARRERA))
        
        # El recorrido in-order debe dar los nodos ordenados por X
        recorrido = self.arbol.recorrido_en_profundidad()
        
        self.assertEqual(5, len(recorrido))
        self.assertEqual(100, recorrido[0].x)
        self.assertEqual(200, recorrido[1].x)
        self.assertEqual(300, recorrido[2].x)
        self.assertEqual(400, recorrido[3].x)
        self.assertEqual(500, recorrido[4].x)

    def test_recorrido_en_anchura(self):
        """Verifica el recorrido en anchura."""
        # Crear un árbol simple para verificar
        self.arbol.insertar(Obstaculo(300, 1, TipoObstaculo.ROCA))  # Raíz
        self.arbol.insertar(Obstaculo(100, 1, TipoObstaculo.CONO))  # Izquierdo
        self.arbol.insertar(Obstaculo(500, 1, TipoObstaculo.HUECO))  # Derecho
        
        recorrido = self.arbol.recorrido_en_anchura()
        
        self.assertEqual(3, len(recorrido))
        # La raíz debe ser la primera
        self.assertEqual(300, recorrido[0].x)
        # Luego los nodos del segundo nivel (izquierda y derecha)
        self.assertTrue(recorrido[1].x == 100 and recorrido[2].x == 500 or 
                       recorrido[1].x == 500 and recorrido[2].x == 100)


if __name__ == '__main__':
    unittest.main()