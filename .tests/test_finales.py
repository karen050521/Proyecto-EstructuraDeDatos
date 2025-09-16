#!/usr/bin/env python3
"""
Pruebas finales - Validación general y exhaustiva del sistema completo
Pruebas que validan la generalidad y robustez total del proyecto
"""

import sys
import os
import json
import tempfile
import random
import time

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.obstaculo import Obstaculo, TipoObstaculo
from logic.nodo_avl import NodoAVL
from logic.arbol_avl import ArbolAVL
from logic.carrito import Carrito, EstadoCarrito
from logic.gestor_juego import GestorJuego, EstadoJuego


def test_validacion_general_sistema():
    """Prueba: Validación general del sistema completo"""
    print("🧪 Probando validación general del sistema...")

    # Crear sistema completo
    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Verificar que todos los componentes están inicializados
    assert gestor.carrito is not None, "Carrito debe estar inicializado"
    assert gestor.arbol_obstaculos is not None, "Árbol AVL debe estar inicializado"
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Estado debe ser JUGANDO"

    # Verificar propiedades del carrito
    carrito = gestor.carrito
    assert carrito.x == 50, "Carrito debe estar en posición inicial X"
    assert carrito.y == 1, "Carrito debe estar en carril medio"
    assert carrito.energia_actual == 100, "Carrito debe tener energía completa"
    assert carrito.esta_vivo() == True, "Carrito debe estar vivo"

    # Verificar árbol AVL
    assert gestor.arbol_obstaculos.esta_vacio() == True, (
        "Árbol debe estar vacío inicialmente"
    )
    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 0, (
        "Debe tener 0 obstáculos"
    )

    # Verificar configuración por defecto
    assert gestor.distancia_total == 2000, "Distancia total por defecto debe ser 2000"
    assert gestor.velocidad_carrito == 10, "Velocidad por defecto debe ser 10"
    assert gestor.refresco_ms == 200, "Refresco por defecto debe ser 200"
    assert gestor.altura_salto == 50, "Altura de salto por defecto debe ser 50"

    print("✅ Validación general del sistema: PASÓ")


def test_operaciones_completas_avl():
    """Prueba: Operaciones completas del árbol AVL"""
    print("🧪 Probando operaciones completas del árbol AVL...")

    arbol = ArbolAVL()

    # Fase 1: Inserción masiva
    obstaculos_insertados = 0
    for i in range(200):
        x = random.randint(0, 10000)
        y = random.randint(0, 2)
        tipo = random.choice(list(TipoObstaculo))
        obstaculo = Obstaculo(x, y, tipo)

        if arbol.insertar(obstaculo):
            obstaculos_insertados += 1

    assert arbol.obtener_total_obstaculos() == obstaculos_insertados, (
        "Número de obstáculos debe coincidir"
    )

    # Fase 2: Búsquedas múltiples
    for i in range(50):
        x_min = random.randint(0, 5000)
        x_max = x_min + random.randint(100, 1000)
        resultado = arbol.buscar_en_rango(x_min, x_max, 0, 2)

        # Verificar que todos los resultados están en el rango
        for obs in resultado:
            assert x_min <= obs.x <= x_max, "Obstáculo fuera del rango de búsqueda"
            assert 0 <= obs.y <= 2, "Y fuera del rango válido"

    # Fase 3: Recorridos
    recorrido_anchura = arbol.recorrido_en_anchura()
    recorrido_profundidad = arbol.recorrido_en_profundidad()

    assert len(recorrido_anchura) == obstaculos_insertados, (
        "Recorrido en anchura debe incluir todos los obstáculos"
    )
    assert len(recorrido_profundidad) == obstaculos_insertados, (
        "Recorrido en profundidad debe incluir todos los obstáculos"
    )

    # Verificar que el recorrido en profundidad está ordenado
    for i in range(len(recorrido_profundidad) - 1):
        obs1 = recorrido_profundidad[i]
        obs2 = recorrido_profundidad[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
            "Recorrido en profundidad debe estar ordenado"
        )

    # Fase 4: Eliminaciones selectivas
    obstaculos_eliminados = 0
    for obs in recorrido_profundidad[:50]:  # Eliminar los primeros 50
        if arbol.eliminar(obs):
            obstaculos_eliminados += 1

    assert (
        arbol.obtener_total_obstaculos()
        == obstaculos_insertados - obstaculos_eliminados
    ), "Número de obstáculos después de eliminación debe ser correcto"

    print(
        f"✅ Operaciones completas AVL: {obstaculos_insertados} insertados, {obstaculos_eliminados} eliminados"
    )


def test_mecanicas_completas_juego():
    """Prueba: Mecánicas completas del juego"""
    print("🧪 Probando mecánicas completas del juego...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Crear nivel complejo
    for i in range(30):
        x = 100 + (i * 50)
        y = i % 3
        tipo = random.choice(list(TipoObstaculo))
        gestor.agregar_obstaculo(x, y, tipo)

    carrito = gestor.carrito

    # Simular juego completo con todas las mecánicas
    pasos = 0
    colisiones = 0
    saltos = 0

    while pasos < 100:
        # Mecánica 1: Movimiento automático
        carrito.mover_automaticamente()

        # Mecánica 2: Actualización de obstáculos visibles
        gestor.actualizar_obstaculos_visibles()

        # Mecánica 3: Detección de colisiones
        colisiones_detectadas = gestor.verificar_colisiones()

        if colisiones_detectadas:
            # Mecánica 4: Estrategia de evasión
            obstaculo = colisiones_detectadas[0]

            if obstaculo.y == 1:  # Obstáculo en carril medio
                if carrito.y == 1:
                    carrito.mover_arriba()
            elif obstaculo.y == 0:  # Obstáculo en carril abajo
                if carrito.y == 0:
                    carrito.mover_arriba()
            elif obstaculo.y == 2:  # Obstáculo en carril arriba
                if carrito.y == 2:
                    carrito.mover_abajo()

            # Mecánica 5: Salto como alternativa
            if random.random() < 0.3:  # 30% de probabilidad de saltar
                carrito.saltar()
                saltos += 1

                # Simular salto
                for _ in range(25):
                    carrito.actualizar_salto()

            # Mecánica 6: Procesamiento de colisiones
            colisiones_restantes = gestor.verificar_colisiones()
            if colisiones_restantes:
                gestor.procesar_colision(colisiones_restantes[0])
                colisiones += 1

        # Mecánica 7: Actualización de distancia
        gestor.distancia_recorrida = carrito.x - 50

        # Mecánica 8: Verificación de condiciones de fin
        if gestor.verificar_condiciones_fin_juego():
            break

        pasos += 1

    # Verificar que todas las mecánicas funcionaron
    assert pasos > 0, "Debe haber procesado pasos"
    assert carrito.x > 50, "Carrito debe haber avanzado"
    assert gestor.distancia_recorrida > 0, "Debe haber recorrido distancia"

    print(
        f"✅ Mecánicas completas: {pasos} pasos, {colisiones} colisiones, {saltos} saltos"
    )


def test_rendimiento_sistema():
    """Prueba: Rendimiento del sistema completo"""
    print("🧪 Probando rendimiento del sistema...")

    # Medir tiempo de inicialización
    start_time = time.time()

    gestor = GestorJuego()
    gestor.inicializar_juego()

    init_time = time.time() - start_time

    # Medir tiempo de inserción masiva
    start_time = time.time()

    for i in range(500):
        x = random.randint(0, 10000)
        y = random.randint(0, 2)
        tipo = random.choice(list(TipoObstaculo))
        gestor.agregar_obstaculo(x, y, tipo)

    insertion_time = time.time() - start_time

    # Medir tiempo de búsquedas
    start_time = time.time()

    for i in range(100):
        x_min = random.randint(0, 5000)
        x_max = x_min + random.randint(100, 1000)
        gestor.arbol_obstaculos.buscar_en_rango(x_min, x_max, 0, 2)

    search_time = time.time() - start_time

    # Medir tiempo de simulación de juego
    start_time = time.time()

    carrito = gestor.carrito
    for i in range(100):
        carrito.mover_automaticamente()
        gestor.actualizar_obstaculos_visibles()
        gestor.verificar_colisiones()

    game_time = time.time() - start_time

    # Verificar que los tiempos son razonables
    assert init_time < 1.0, f"Inicialización muy lenta: {init_time:.3f}s"
    assert insertion_time < 3.0, f"Inserción muy lenta: {insertion_time:.3f}s"
    assert search_time < 2.0, f"Búsqueda muy lenta: {search_time:.3f}s"
    assert game_time < 1.0, f"Simulación muy lenta: {game_time:.3f}s"

    print(
        f"✅ Rendimiento: Init {init_time:.3f}s, Insert {insertion_time:.3f}s, Search {search_time:.3f}s, Game {game_time:.3f}s"
    )


def test_robustez_sistema():
    """Prueba: Robustez del sistema ante condiciones extremas"""
    print("🧪 Probando robustez del sistema...")

    # Prueba 1: Sistema con configuración extrema
    gestor = GestorJuego()
    gestor.distancia_total = 1  # Distancia mínima
    gestor.velocidad_carrito = 1  # Velocidad mínima
    gestor.altura_salto = 1  # Salto mínimo
    gestor.inicializar_juego()

    assert gestor.carrito is not None, "Sistema debe funcionar con configuración mínima"

    # Prueba 2: Sistema con muchos obstáculos
    gestor = GestorJuego()
    gestor.inicializar_juego()

    for i in range(1000):
        x = i * 10
        y = i % 3
        gestor.agregar_obstaculo(x, y, TipoObstaculo.ROCA)

    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 1000, (
        "Sistema debe manejar muchos obstáculos"
    )

    # Prueba 3: Sistema bajo estrés de operaciones
    carrito = gestor.carrito

    for i in range(500):
        carrito.mover_automaticamente()
        gestor.actualizar_obstaculos_visibles()
        gestor.verificar_colisiones()

        # Verificar que el sistema sigue funcionando
        assert carrito.x >= 50, "Sistema debe mantener consistencia"
        assert 0 <= carrito.y <= 2, "Sistema debe mantener límites"

    print("✅ Robustez del sistema: PASÓ")


def test_validacion_requisitos_completa():
    """Prueba: Validación completa de todos los requisitos"""
    print("🧪 Probando validación completa de requisitos...")

    # Requisito 1: Carga y representación del árbol
    config_json = {
        "configuracion": {
            "distancia_total": 2000,
            "velocidad_carrito": 10,
            "refresco_ms": 200,
            "altura_salto": 50,
            "color_carrito_inicial": "azul",
        },
        "obstaculos": [
            {"x": 150, "y": 0, "tipo": "roca"},
            {"x": 320, "y": 1, "tipo": "cono"},
            {"x": 500, "y": 2, "tipo": "hueco"},
        ],
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_json, f, indent=2)
        temp_file = f.name

    try:
        gestor = GestorJuego(temp_file)
        assert gestor.cargar_configuracion() == True, "Debe cargar configuración"
        assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 3, (
            "Debe cargar obstáculos"
        )
    finally:
        os.unlink(temp_file)

    # Requisito 2: Recorridos gráficos del árbol
    arbol = ArbolAVL()
    for i in range(10):
        obstaculo = Obstaculo(i * 100, i % 3, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)

    recorrido_anchura = arbol.recorrido_en_anchura()
    recorrido_profundidad = arbol.recorrido_en_profundidad()

    assert len(recorrido_anchura) == 10, (
        "Recorrido en anchura debe incluir todos los elementos"
    )
    assert len(recorrido_profundidad) == 10, (
        "Recorrido en profundidad debe incluir todos los elementos"
    )

    # Verificar ordenamiento del recorrido en profundidad
    for i in range(len(recorrido_profundidad) - 1):
        obs1 = recorrido_profundidad[i]
        obs2 = recorrido_profundidad[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
            "Recorrido en profundidad debe estar ordenado"
        )

    # Requisito 3: Administración del árbol antes del juego
    gestor = GestorJuego()

    # Inserción manual
    assert gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA) == True, (
        "Debe insertar obstáculo"
    )
    assert gestor.agregar_obstaculo(100, 1, TipoObstaculo.CONO) == False, (
        "No debe insertar duplicado"
    )

    # Eliminación
    assert gestor.eliminar_obstaculo(100, 1) == True, "Debe eliminar obstáculo"
    assert gestor.eliminar_obstaculo(100, 1) == False, (
        "No debe eliminar obstáculo inexistente"
    )

    # Requisito 4: Juego del carrito usando árbol AVL
    gestor.inicializar_juego()
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)

    carrito = gestor.carrito

    # Movimiento automático
    carrito.mover_automaticamente()
    assert carrito.x > 50, "Carrito debe moverse automáticamente"

    # Control manual
    carrito.mover_arriba()
    assert carrito.y == 2, "Carrito debe moverse manualmente"

    # Sistema de salto
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "Carrito debe poder saltar"

    # Consulta eficiente de obstáculos
    carrito.x = 90
    gestor.actualizar_obstaculos_visibles()
    assert len(gestor.obstaculos_visibles) > 0, "Debe encontrar obstáculos visibles"

    # Detección de colisiones
    carrito.x = 100
    carrito.y = 1
    colisiones = gestor.verificar_colisiones()
    assert len(colisiones) > 0, "Debe detectar colisiones"

    # Sistema de energía
    energia_inicial = carrito.energia_actual
    gestor.procesar_colision(colisiones[0])
    assert carrito.energia_actual < energia_inicial, "Carrito debe perder energía"

    # Condiciones de fin de juego
    carrito.energia_actual = 0
    assert gestor.verificar_condiciones_fin_juego() == True, "Debe terminar sin energía"

    print("✅ Validación completa de requisitos: PASÓ")


def test_estabilidad_largo_plazo():
    """Prueba: Estabilidad del sistema a largo plazo"""
    print("🧪 Probando estabilidad a largo plazo...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Simular juego prolongado
    carrito = gestor.carrito
    pasos_totales = 0
    operaciones_avl = 0

    for ciclo in range(10):  # 10 ciclos de juego
        # Agregar obstáculos en cada ciclo
        for i in range(20):
            x = 100 + (ciclo * 200) + (i * 10)
            y = i % 3
            tipo = random.choice(list(TipoObstaculo))
            gestor.agregar_obstaculo(x, y, tipo)
            operaciones_avl += 1

        # Simular juego en cada ciclo
        for paso in range(50):
            carrito.mover_automaticamente()
            gestor.actualizar_obstaculos_visibles()

            colisiones = gestor.verificar_colisiones()
            if colisiones:
                gestor.procesar_colision(colisiones[0])

            gestor.distancia_recorrida = carrito.x - 50
            pasos_totales += 1

            # Verificar estabilidad del sistema
            assert carrito.x >= 50, "Sistema debe mantener consistencia en X"
            assert 0 <= carrito.y <= 2, "Sistema debe mantener límites en Y"
            assert 0 <= carrito.energia_actual <= carrito.energia_maxima, (
                "Sistema debe mantener energía válida"
            )
            assert gestor.arbol_obstaculos.obtener_total_obstaculos() >= 0, (
                "Sistema debe mantener número válido de obstáculos"
            )

    print(
        f"✅ Estabilidad a largo plazo: {pasos_totales} pasos, {operaciones_avl} operaciones AVL"
    )


def main():
    """Ejecuta todas las pruebas finales"""
    print("🚀 Iniciando pruebas finales y validación general...\n")
    print("=" * 60)

    try:
        test_validacion_general_sistema()
        print()

        test_operaciones_completas_avl()
        print()

        test_mecanicas_completas_juego()
        print()

        test_rendimiento_sistema()
        print()

        test_robustez_sistema()
        print()

        test_validacion_requisitos_completa()
        print()

        test_estabilidad_largo_plazo()
        print()

        print("=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS FINALES PASARON!")
        print("✅ El sistema es completamente robusto y cumple todos los requisitos")
        print("🚀 Proyecto listo para producción")

        return True

    except AssertionError as e:
        print(f"❌ Error en las pruebas finales: {e}")
        return False
    except Exception as e:
        print(f"💥 Error inesperado en pruebas finales: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
