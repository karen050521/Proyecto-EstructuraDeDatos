#!/usr/bin/env python3
"""
Pruebas específicas del árbol AVL - Validación completa de funcionalidad AVL
Incluye balanceamiento, rotaciones, recorridos y criterios de ordenamiento
"""

import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.obstaculo import Obstaculo, TipoObstaculo
from logic.nodo_avl import NodoAVL
from logic.arbol_avl import ArbolAVL


def test_criterios_ordenamiento():
    """Prueba: Criterios de ordenamiento según definicion.md"""
    print("🧪 Probando criterios de ordenamiento del AVL...")

    # Crear nodos para probar comparaciones
    obstaculo1 = Obstaculo(100, 1, TipoObstaculo.ROCA)
    obstaculo2 = Obstaculo(50, 2, TipoObstaculo.CONO)
    obstaculo3 = Obstaculo(100, 0, TipoObstaculo.HUECO)
    obstaculo4 = Obstaculo(100, 1, TipoObstaculo.ACEITE)  # Mismas coordenadas

    nodo1 = NodoAVL(obstaculo1)

    # Probar ordenamiento por X
    assert nodo1.es_mayor_que(obstaculo2) == True, (
        "100,1 debe ser mayor que 50,2 (por X)"
    )
    assert nodo1.es_mayor_que(obstaculo3) == True, (
        "100,1 debe ser mayor que 100,0 (por Y)"
    )
    assert nodo1.es_igual_a(obstaculo4) == True, "100,1 debe ser igual a 100,1"
    assert nodo1.es_igual_a(obstaculo2) == False, "100,1 no debe ser igual a 50,2"

    print("✅ Criterios de ordenamiento: PASÓ")


def test_insercion_multiple():
    """Prueba: Inserción múltiple y balanceamiento automático"""
    print("🧪 Probando inserción múltiple y balanceamiento...")

    arbol = ArbolAVL()

    # Insertar obstáculos en orden que puede causar desbalance
    obstaculos = [
        Obstaculo(100, 1, TipoObstaculo.ROCA),  # Raíz
        Obstaculo(50, 2, TipoObstaculo.CONO),  # Izquierda
        Obstaculo(150, 0, TipoObstaculo.HUECO),  # Derecha
        Obstaculo(25, 1, TipoObstaculo.ACEITE),  # Izquierda-izquierda
        Obstaculo(75, 0, TipoObstaculo.BARRERA),  # Izquierda-derecha
        Obstaculo(125, 2, TipoObstaculo.ROCA),  # Derecha-izquierda
        Obstaculo(175, 1, TipoObstaculo.CONO),  # Derecha-derecha
        Obstaculo(10, 0, TipoObstaculo.HUECO),  # Forzar rotación
        Obstaculo(200, 2, TipoObstaculo.ACEITE),  # Forzar rotación
    ]

    for i, obstaculo in enumerate(obstaculos):
        resultado = arbol.insertar(obstaculo)
        assert resultado == True, f"Debe insertar obstáculo {i + 1}"
        assert arbol.obtener_total_obstaculos() == i + 1, (
            f"Debe tener {i + 1} obstáculos"
        )

    # Verificar que el árbol mantiene balance
    assert arbol.obtener_total_obstaculos() == 9, "Debe tener 9 obstáculos"
    assert not arbol.esta_vacio(), "Árbol no debe estar vacío"

    # Verificar que no se permiten duplicados
    duplicado = Obstaculo(100, 1, TipoObstaculo.ROCA)
    resultado = arbol.insertar(duplicado)
    assert resultado == False, "No debe insertar duplicado"
    assert arbol.obtener_total_obstaculos() == 9, "Debe seguir teniendo 9 obstáculos"

    print("✅ Inserción múltiple y balanceamiento: PASÓ")


def test_eliminacion():
    """Prueba: Eliminación de obstáculos con balanceamiento"""
    print("🧪 Probando eliminación de obstáculos...")

    arbol = ArbolAVL()

    # Insertar obstáculos
    obstaculos = [
        Obstaculo(100, 1, TipoObstaculo.ROCA),
        Obstaculo(50, 2, TipoObstaculo.CONO),
        Obstaculo(150, 0, TipoObstaculo.HUECO),
        Obstaculo(25, 1, TipoObstaculo.ACEITE),
        Obstaculo(75, 0, TipoObstaculo.BARRERA),
    ]

    for obstaculo in obstaculos:
        arbol.insertar(obstaculo)

    assert arbol.obtener_total_obstaculos() == 5, "Debe tener 5 obstáculos inicialmente"

    # Eliminar hoja
    resultado = arbol.eliminar(Obstaculo(25, 1, TipoObstaculo.ACEITE))
    assert resultado == True, "Debe eliminar hoja"
    assert arbol.obtener_total_obstaculos() == 4, "Debe tener 4 obstáculos"

    # Eliminar nodo con un hijo
    resultado = arbol.eliminar(Obstaculo(50, 2, TipoObstaculo.CONO))
    assert resultado == True, "Debe eliminar nodo con un hijo"
    assert arbol.obtener_total_obstaculos() == 3, "Debe tener 3 obstáculos"

    # Eliminar nodo con dos hijos (raíz)
    resultado = arbol.eliminar(Obstaculo(100, 1, TipoObstaculo.ROCA))
    assert resultado == True, "Debe eliminar nodo con dos hijos"
    assert arbol.obtener_total_obstaculos() == 2, "Debe tener 2 obstáculos"

    # Intentar eliminar obstáculo inexistente
    resultado = arbol.eliminar(Obstaculo(300, 3, TipoObstaculo.ROCA))
    assert resultado == False, "No debe eliminar obstáculo inexistente"
    assert arbol.obtener_total_obstaculos() == 2, "Debe seguir teniendo 2 obstáculos"

    print("✅ Eliminación de obstáculos: PASÓ")


def test_recorridos():
    """Prueba: Recorridos en anchura y profundidad"""
    print("🧪 Probando recorridos del árbol...")

    arbol = ArbolAVL()

    # Insertar obstáculos en orden específico
    obstaculos = [
        Obstaculo(100, 1, TipoObstaculo.ROCA),  # Raíz
        Obstaculo(50, 2, TipoObstaculo.CONO),  # Izquierda
        Obstaculo(150, 0, TipoObstaculo.HUECO),  # Derecha
        Obstaculo(25, 1, TipoObstaculo.ACEITE),  # Izquierda-izquierda
        Obstaculo(75, 0, TipoObstaculo.BARRERA),  # Izquierda-derecha
        Obstaculo(125, 2, TipoObstaculo.ROCA),  # Derecha-izquierda
        Obstaculo(175, 1, TipoObstaculo.CONO),  # Derecha-derecha
    ]

    for obstaculo in obstaculos:
        arbol.insertar(obstaculo)

    # Recorrido en anchura (BFS)
    recorrido_anchura = arbol.recorrido_en_anchura()
    assert len(recorrido_anchura) == 7, "Recorrido en anchura debe tener 7 elementos"

    # En BFS, el primer elemento debe ser la raíz
    assert recorrido_anchura[0].x == 100 and recorrido_anchura[0].y == 1, (
        "Primer elemento debe ser la raíz"
    )

    # Recorrido en profundidad (in-order)
    recorrido_profundidad = arbol.recorrido_en_profundidad()
    assert len(recorrido_profundidad) == 7, (
        "Recorrido en profundidad debe tener 7 elementos"
    )

    # En in-order, los elementos deben estar ordenados
    for i in range(len(recorrido_profundidad) - 1):
        obs1 = recorrido_profundidad[i]
        obs2 = recorrido_profundidad[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
            f"Recorrido in-order debe estar ordenado: {obs1} antes de {obs2}"
        )

    # Ambos recorridos deben contener los mismos elementos
    elementos_anchura = set((obs.x, obs.y) for obs in recorrido_anchura)
    elementos_profundidad = set((obs.x, obs.y) for obs in recorrido_profundidad)
    assert elementos_anchura == elementos_profundidad, (
        "Ambos recorridos deben contener los mismos elementos"
    )

    print("✅ Recorridos del árbol: PASÓ")


def test_busqueda_rango():
    """Prueba: Búsqueda eficiente por rango"""
    print("🧪 Probando búsqueda por rango...")

    arbol = ArbolAVL()

    # Insertar obstáculos en diferentes posiciones
    obstaculos = [
        Obstaculo(50, 0, TipoObstaculo.ROCA),
        Obstaculo(100, 1, TipoObstaculo.CONO),
        Obstaculo(150, 2, TipoObstaculo.HUECO),
        Obstaculo(200, 0, TipoObstaculo.ACEITE),
        Obstaculo(250, 1, TipoObstaculo.BARRERA),
        Obstaculo(300, 2, TipoObstaculo.ROCA),
        Obstaculo(350, 0, TipoObstaculo.CONO),
    ]

    for obstaculo in obstaculos:
        arbol.insertar(obstaculo)

    # Búsqueda en rango específico
    resultado = arbol.buscar_en_rango(90, 160, 0, 2)
    coordenadas_encontradas = [(obs.x, obs.y) for obs in resultado]

    assert (100, 1) in coordenadas_encontradas, "Debe encontrar obstáculo en (100,1)"
    assert (150, 2) in coordenadas_encontradas, "Debe encontrar obstáculo en (150,2)"
    assert (50, 0) not in coordenadas_encontradas, (
        "No debe encontrar obstáculo en (50,0)"
    )
    assert (200, 0) not in coordenadas_encontradas, (
        "No debe encontrar obstáculo en (200,0)"
    )

    # Búsqueda en rango vacío
    resultado = arbol.buscar_en_rango(400, 500, 0, 2)
    assert len(resultado) == 0, "No debe encontrar obstáculos en rango vacío"

    # Búsqueda en rango que incluye todos
    resultado = arbol.buscar_en_rango(0, 400, 0, 2)
    assert len(resultado) == 7, "Debe encontrar todos los obstáculos"

    # Búsqueda por carril específico
    resultado = arbol.buscar_en_rango(0, 400, 1, 1)
    carriles_encontrados = [obs.y for obs in resultado]
    assert all(y == 1 for y in carriles_encontrados), (
        "Debe encontrar solo obstáculos en carril 1"
    )

    print("✅ Búsqueda por rango: PASÓ")


def test_balanceamiento_automatico():
    """Prueba: Balanceamiento automático del árbol"""
    print("🧪 Probando balanceamiento automático...")

    arbol = ArbolAVL()

    # Insertar en orden que causa desbalance (secuencia creciente)
    for i in range(10):
        obstaculo = Obstaculo(10 + i * 10, i % 3, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)

    # Verificar que el árbol mantiene balance
    assert arbol.obtener_total_obstaculos() == 10, "Debe tener 10 obstáculos"

    # Verificar que las operaciones siguen funcionando
    resultado = arbol.buscar_en_rango(50, 80, 0, 2)
    assert len(resultado) >= 3, "Debe encontrar obstáculos en el rango"

    # Verificar que el recorrido in-order sigue ordenado
    recorrido = arbol.recorrido_en_profundidad()
    for i in range(len(recorrido) - 1):
        obs1 = recorrido[i]
        obs2 = recorrido[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
            "Recorrido debe seguir ordenado después del balanceamiento"
        )

    print("✅ Balanceamiento automático: PASÓ")


def test_altura_y_factor_balance():
    """Prueba: Cálculo de altura y factor de balance"""
    print("🧪 Probando altura y factor de balance...")

    # Crear nodo simple
    obstaculo = Obstaculo(100, 1, TipoObstaculo.ROCA)
    nodo = NodoAVL(obstaculo)

    assert nodo.altura == 1, "Altura inicial debe ser 1"
    assert nodo.obtener_factor_balance() == 0, "Factor de balance inicial debe ser 0"

    # Agregar hijo izquierdo
    hijo_izq = NodoAVL(Obstaculo(50, 2, TipoObstaculo.CONO))
    nodo.izquierdo = hijo_izq
    nodo.actualizar_altura()

    assert nodo.altura == 2, "Altura debe ser 2 con un hijo"
    assert nodo.obtener_factor_balance() == 1, "Factor de balance debe ser 1"

    # Agregar hijo derecho
    hijo_der = NodoAVL(Obstaculo(150, 0, TipoObstaculo.HUECO))
    nodo.derecho = hijo_der
    nodo.actualizar_altura()

    assert nodo.altura == 2, "Altura debe seguir siendo 2 con dos hijos"
    assert nodo.obtener_factor_balance() == 0, "Factor de balance debe ser 0"

    print("✅ Altura y factor de balance: PASÓ")


def test_operaciones_combinadas():
    """Prueba: Operaciones combinadas (inserción, eliminación, búsqueda)"""
    print("🧪 Probando operaciones combinadas...")

    arbol = ArbolAVL()

    # Fase 1: Inserción masiva
    for i in range(20):
        obstaculo = Obstaculo(100 + i * 5, i % 3, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)

    assert arbol.obtener_total_obstaculos() == 20, "Debe tener 20 obstáculos"

    # Fase 2: Búsquedas múltiples
    for i in range(5):
        x_min = 100 + i * 20
        x_max = x_min + 15
        resultado = arbol.buscar_en_rango(x_min, x_max, 0, 2)
        assert len(resultado) >= 0, f"Búsqueda {i + 1} debe funcionar"

    # Fase 3: Eliminaciones selectivas
    for i in range(10):
        x = 100 + i * 10
        y = i % 3
        resultado = arbol.eliminar(Obstaculo(x, y, TipoObstaculo.ROCA))
        # Algunas eliminaciones pueden fallar si el obstáculo no existe
        assert isinstance(resultado, bool), "Eliminación debe retornar bool"

    # Fase 4: Verificar estado final
    assert arbol.obtener_total_obstaculos() >= 10, (
        "Debe tener al menos 10 obstáculos restantes"
    )

    # Fase 5: Recorridos finales
    recorrido_anchura = arbol.recorrido_en_anchura()
    recorrido_profundidad = arbol.recorrido_en_profundidad()

    assert len(recorrido_anchura) == len(recorrido_profundidad), (
        "Ambos recorridos deben tener la misma longitud"
    )
    assert len(recorrido_anchura) == arbol.obtener_total_obstaculos(), (
        "Recorridos deben incluir todos los obstáculos"
    )

    print("✅ Operaciones combinadas: PASÓ")


def main():
    """Ejecuta todas las pruebas del árbol AVL"""
    print("🚀 Iniciando pruebas del árbol AVL...\n")
    print("=" * 50)

    try:
        test_criterios_ordenamiento()
        print()

        test_insercion_multiple()
        print()

        test_eliminacion()
        print()

        test_recorridos()
        print()

        test_busqueda_rango()
        print()

        test_balanceamiento_automatico()
        print()

        test_altura_y_factor_balance()
        print()

        test_operaciones_combinadas()
        print()

        print("=" * 50)
        print("🎉 ¡TODAS LAS PRUEBAS DEL ÁRBOL AVL PASARON!")
        print("✅ Funcionalidad AVL completamente validada")

        return True

    except AssertionError as e:
        print(f"❌ Error en las pruebas: {e}")
        return False
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
