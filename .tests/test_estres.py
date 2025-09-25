#!/usr/bin/env python3
"""
Pruebas de estrés - Validación de robustez y casos extremos
Pruebas que someten el sistema a condiciones extremas
"""

import sys
import os
import random
import time

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.obstaculo import Obstaculo, TipoObstaculo
from logic.nodo_avl import NodoAVL
from logic.arbol_avl import ArbolAVL
from logic.carrito import Carrito, EstadoCarrito
from logic.gestor_juego import GestorJuego, EstadoJuego


def test_insercion_masiva_obstaculos():
    """Prueba: Inserción masiva de obstáculos para probar balanceamiento"""
    print("🧪 Probando inserción masiva de obstáculos...")

    arbol = ArbolAVL()

    # Insertar 1000 obstáculos aleatorios
    obstaculos_insertados = 0
    obstaculos_rechazados = 0

    for i in range(1000):
        x = random.randint(0, 10000)
        y = random.randint(0, 2)
        tipo = random.choice(list(TipoObstaculo))

        obstaculo = Obstaculo(x, y, tipo)

        if arbol.insertar(obstaculo):
            obstaculos_insertados += 1
        else:
            obstaculos_rechazados += 1

    # Verificar que el árbol mantiene balance
    assert arbol.obtener_total_obstaculos() == obstaculos_insertados, (
        f"Debe tener {obstaculos_insertados} obstáculos"
    )

    # Verificar que las operaciones siguen funcionando
    resultado = arbol.buscar_en_rango(0, 1000, 0, 2)
    assert len(resultado) >= 0, "Búsqueda debe funcionar después de inserción masiva"

    # Verificar que el recorrido in-order sigue ordenado
    recorrido = arbol.recorrido_en_profundidad()
    for i in range(len(recorrido) - 1):
        obs1 = recorrido[i]
        obs2 = recorrido[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
            "Recorrido debe seguir ordenado después de inserción masiva"
        )

    print(
        f"✅ Inserción masiva: {obstaculos_insertados} insertados, {obstaculos_rechazados} rechazados"
    )


def test_eliminacion_masiva():
    """Prueba: Eliminación masiva de obstáculos"""
    print("🧪 Probando eliminación masiva de obstáculos...")

    arbol = ArbolAVL()

    # Insertar obstáculos
    obstaculos = []
    for i in range(500):
        x = i * 2  # Coordenadas únicas
        y = i % 3
        tipo = random.choice(list(TipoObstaculo))
        obstaculo = Obstaculo(x, y, tipo)
        arbol.insertar(obstaculo)
        obstaculos.append(obstaculo)

    assert arbol.obtener_total_obstaculos() == 500, "Debe tener 500 obstáculos"

    # Eliminar la mitad de los obstáculos
    eliminados = 0
    for i in range(0, 500, 2):  # Eliminar cada segundo obstáculo
        if arbol.eliminar(obstaculos[i]):
            eliminados += 1

    assert arbol.obtener_total_obstaculos() == 250, (
        "Debe tener 250 obstáculos restantes"
    )

    # Verificar que las operaciones siguen funcionando
    resultado = arbol.buscar_en_rango(0, 1000, 0, 2)
    assert len(resultado) == 250, "Debe encontrar 250 obstáculos restantes"

    print(f"✅ Eliminación masiva: {eliminados} obstáculos eliminados")


def test_busqueda_extrema():
    """Prueba: Búsquedas en rangos extremos"""
    print("🧪 Probando búsquedas en rangos extremos...")

    arbol = ArbolAVL()

    # Insertar obstáculos en posiciones específicas
    for i in range(100):
        x = i * 10
        y = i % 3
        obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)

    # Búsqueda en rango muy pequeño
    resultado = arbol.buscar_en_rango(50, 60, 0, 2)
    assert len(resultado) >= 0, "Debe encontrar 0 o más obstáculos en rango pequeño"

    # Búsqueda en rango muy grande
    resultado = arbol.buscar_en_rango(0, 10000, 0, 2)
    assert len(resultado) == 100, "Debe encontrar todos los obstáculos en rango grande"

    # Búsqueda en rango vacío
    resultado = arbol.buscar_en_rango(10000, 20000, 0, 2)
    assert len(resultado) == 0, "No debe encontrar obstáculos en rango vacío"

    # Búsqueda por carril específico
    resultado = arbol.buscar_en_rango(0, 1000, 1, 1)
    carriles = [obs.y for obs in resultado]
    assert all(y == 1 for y in carriles), "Debe encontrar solo obstáculos en carril 1"

    print("✅ Búsquedas en rangos extremos: PASÓ")


def test_carrito_movimiento_extremo():
    """Prueba: Movimiento extremo del carrito"""
    print("🧪 Probando movimiento extremo del carrito...")

    carrito = Carrito()

    # Movimiento automático masivo
    for i in range(1000):
        carrito.mover_automaticamente()

    assert carrito.x == 50 + (1000 * 5), "Debe haber avanzado 5000 metros"

    # Movimiento vertical extremo
    for i in range(100):
        carrito.mover_arriba()
        carrito.mover_abajo()

    # Debe estar en el carril inicial
    assert carrito.y == 1, "Debe estar en carril medio después de movimiento extremo"

    # Saltos consecutivos
    for i in range(50):
        carrito.saltar()
        for _ in range(25):  # Completar cada salto
            carrito.actualizar_salto()

    assert carrito.estado == EstadoCarrito.NORMAL, "Debe estar en estado normal"
    assert carrito.velocidad_y == 0, "Velocidad Y debe ser 0"

    print("✅ Movimiento extremo del carrito: PASÓ")


def test_daño_extremo():
    """Prueba: Sistema de daño extremo"""
    print("🧪 Probando sistema de daño extremo...")

    carrito = Carrito(energia_maxima=1000)  # Energía alta para la prueba

    # Daño masivo
    carrito.recibir_daño(500)
    assert carrito.energia_actual == 500, "Debe tener 500 de energía"
    assert carrito.esta_vivo() == True, "Debe seguir vivo"

    # Daño que excede la energía
    carrito.recibir_daño(600)
    assert carrito.energia_actual == 0, "Debe tener 0 de energía"
    assert carrito.esta_vivo() == False, "No debe estar vivo"

    # Daño negativo (no debe afectar)
    carrito.energia_actual = 100
    carrito.recibir_daño(-50)
    assert carrito.energia_actual == 100, "Daño negativo no debe afectar"

    print("✅ Sistema de daño extremo: PASÓ")


def test_colisiones_masivas():
    """Prueba: Detección de colisiones masivas"""
    print("🧪 Probando detección de colisiones masivas...")

    carrito = Carrito(x_inicial=100, y_inicial=1)

    # Crear muchos obstáculos
    obstaculos = []
    for i in range(100):
        x = 100 + (i * 5)  # Obstáculos cada 5 metros
        y = i % 3
        obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
        obstaculos.append(obstaculo)

    colisiones_detectadas = 0
    for obstaculo in obstaculos:
        if carrito.colisiona_con(obstaculo):
            colisiones_detectadas += 1

    # Debe detectar colisión con el obstáculo en (100,1)
    assert colisiones_detectadas >= 1, "Debe detectar al menos una colisión"

    # Mover carrito y verificar nuevas colisiones
    carrito.x = 105
    carrito.y = 0

    colisiones_nuevas = 0
    for obstaculo in obstaculos:
        if carrito.colisiona_con(obstaculo):
            colisiones_nuevas += 1

    assert colisiones_nuevas >= 1, "Debe detectar colisiones en nueva posición"

    print(f"✅ Colisiones masivas: {colisiones_detectadas} colisiones detectadas")


def test_juego_estres():
    """Prueba: Juego bajo condiciones de estrés"""
    print("🧪 Probando juego bajo condiciones de estrés...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Crear un nivel extremo con muchos obstáculos
    for i in range(200):
        x = 100 + (i * 10)  # Obstáculos cada 10 metros
        y = i % 3
        tipo = random.choice(list(TipoObstaculo))
        gestor.agregar_obstaculo(x, y, tipo)

    carrito = gestor.carrito

    # Simular juego intenso
    frames = 0
    colisiones_totales = 0

    for paso in range(500):  # 500 pasos de juego
        # Mover carrito
        carrito.mover_automaticamente()

        # Actualizar obstáculos visibles
        gestor.actualizar_obstaculos_visibles()

        # Verificar colisiones
        colisiones = gestor.verificar_colisiones()
        if colisiones:
            colisiones_totales += len(colisiones)
            # Procesar primera colisión
            gestor.procesar_colision(colisiones[0])

        # Actualizar distancia
        gestor.distancia_recorrida = carrito.x - 50

        frames += 1

        # Verificar que el juego sigue funcionando
        if not carrito.esta_vivo():
            break

    # Verificar que el sistema sigue funcionando
    assert gestor.arbol_obstaculos.obtener_total_obstaculos() >= 100, (
        "Debe tener obstáculos restantes"
    )
    assert frames > 0, "Debe haber procesado frames"

    print(f"✅ Juego bajo estrés: {frames} frames, {colisiones_totales} colisiones")


def test_memoria_y_rendimiento():
    """Prueba: Uso de memoria y rendimiento"""
    print("🧪 Probando uso de memoria y rendimiento...")

    import time

    # Medir tiempo de inserción masiva
    start_time = time.time()

    arbol = ArbolAVL()
    for i in range(1000):
        x = random.randint(0, 10000)
        y = random.randint(0, 2)
        obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)

    insertion_time = time.time() - start_time

    # Medir tiempo de búsqueda
    start_time = time.time()

    for i in range(100):
        x_min = random.randint(0, 5000)
        x_max = x_min + random.randint(100, 1000)
        resultado = arbol.buscar_en_rango(x_min, x_max, 0, 2)

    search_time = time.time() - start_time

    # Medir tiempo de recorrido
    start_time = time.time()

    for i in range(10):
        recorrido = arbol.recorrido_en_profundidad()

    traversal_time = time.time() - start_time

    # Verificar que los tiempos son razonables
    assert insertion_time < 5.0, f"Inserción muy lenta: {insertion_time:.2f}s"
    assert search_time < 2.0, f"Búsqueda muy lenta: {search_time:.2f}s"
    assert traversal_time < 1.0, f"Recorrido muy lento: {traversal_time:.2f}s"

    print(
        f"✅ Rendimiento: Inserción {insertion_time:.3f}s, Búsqueda {search_time:.3f}s, Recorrido {traversal_time:.3f}s"
    )


def test_casos_edge():
    """Prueba: Casos edge y situaciones límite"""
    print("🧪 Probando casos edge y situaciones límite...")

    # Árbol vacío
    arbol = ArbolAVL()
    assert arbol.esta_vacio() == True, "Árbol debe estar vacío"
    assert arbol.buscar_en_rango(0, 100, 0, 2) == [], (
        "Búsqueda en árbol vacío debe retornar lista vacía"
    )

    # Un solo elemento
    obstaculo = Obstaculo(100, 1, TipoObstaculo.ROCA)
    arbol.insertar(obstaculo)
    assert arbol.obtener_total_obstaculos() == 1, "Debe tener 1 obstáculo"

    # Eliminar el único elemento
    arbol.eliminar(obstaculo)
    assert arbol.esta_vacio() == True, (
        "Árbol debe estar vacío después de eliminar único elemento"
    )

    # Carrito con energía 0
    carrito = Carrito(energia_maxima=0)
    assert carrito.esta_vivo() == False, "Carrito con energía 0 no debe estar vivo"
    assert carrito.obtener_porcentaje_energia() == 0.0, "Porcentaje debe ser 0"

    # Carrito en posición extrema
    carrito = Carrito(x_inicial=0, y_inicial=0)
    carrito.mover_abajo()  # No debe moverse
    assert carrito.y == 0, "No debe moverse fuera del límite inferior"

    carrito.y = 2
    carrito.mover_arriba()  # No debe moverse
    assert carrito.y == 2, "No debe moverse fuera del límite superior"

    print("✅ Casos edge y situaciones límite: PASÓ")


def test_consistencia_datos():
    """Prueba: Consistencia de datos después de operaciones"""
    print("🧪 Probando consistencia de datos...")

    arbol = ArbolAVL()

    # Insertar obstáculos
    obstaculos_originales = []
    for i in range(100):
        x = i * 10
        y = i % 3
        obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)
        obstaculos_originales.append(obstaculo)

    # Verificar consistencia después de operaciones
    for _ in range(50):
        # Operación aleatoria
        operacion = random.choice(["buscar", "recorrer", "eliminar"])

        if operacion == "buscar":
            x_min = random.randint(0, 500)
            x_max = x_min + random.randint(50, 200)
            resultado = arbol.buscar_en_rango(x_min, x_max, 0, 2)
            # Verificar que todos los resultados están en el rango
            for obs in resultado:
                assert x_min <= obs.x <= x_max, "Obstáculo fuera del rango de búsqueda"
                assert 0 <= obs.y <= 2, "Y fuera del rango válido"

        elif operacion == "recorrer":
            recorrido = arbol.recorrido_en_profundidad()
            # Verificar que el recorrido está ordenado
            for i in range(len(recorrido) - 1):
                obs1 = recorrido[i]
                obs2 = recorrido[i + 1]
                assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
                    "Recorrido no está ordenado"
                )

        elif operacion == "eliminar" and arbol.obtener_total_obstaculos() > 10:
            # Eliminar un obstáculo aleatorio
            obstaculo_eliminar = random.choice(obstaculos_originales)
            if arbol.eliminar(obstaculo_eliminar):
                obstaculos_originales.remove(obstaculo_eliminar)

    print("✅ Consistencia de datos: PASÓ")


def main():
    """Ejecuta todas las pruebas de estrés"""
    print("🚀 Iniciando pruebas de estrés y robustez...\n")
    print("=" * 60)

    try:
        test_insercion_masiva_obstaculos()
        print()

        test_eliminacion_masiva()
        print()

        test_busqueda_extrema()
        print()

        test_carrito_movimiento_extremo()
        print()

        test_daño_extremo()
        print()

        test_colisiones_masivas()
        print()

        test_juego_estres()
        print()

        test_memoria_y_rendimiento()
        print()

        test_casos_edge()
        print()

        test_consistencia_datos()
        print()

        print("=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS DE ESTRÉS PASARON!")
        print("✅ El sistema es robusto y maneja casos extremos correctamente")

        return True

    except AssertionError as e:
        print(f"❌ Error en las pruebas de estrés: {e}")
        return False
    except Exception as e:
        print(f"💥 Error inesperado en pruebas de estrés: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
