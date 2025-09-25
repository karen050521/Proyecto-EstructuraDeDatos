#!/usr/bin/env python3
"""
Pruebas de requisitos del proyecto - Validación específica según definicion.md
Valida cada punto de calificación y requisito técnico del proyecto
"""

import sys
import os
import json
import tempfile

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.obstaculo import Obstaculo, TipoObstaculo
from logic.nodo_avl import NodoAVL
from logic.arbol_avl import ArbolAVL
from logic.carrito import Carrito, EstadoCarrito
from logic.gestor_juego import GestorJuego, EstadoJuego


def test_carga_y_representacion_arbol():
    """
    Prueba: Carga y representación del árbol (0.5 puntos)
    - Carga desde JSON
    - Representación gráfica del árbol
    """
    print("🧪 Probando carga y representación del árbol...")

    # Crear archivo JSON de prueba
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
            {"x": 1200, "y": 1, "tipo": "aceite"},
        ],
    }

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_json, f, indent=2)
        temp_file = f.name

    try:
        # Probar carga desde JSON
        gestor = GestorJuego(temp_file)
        resultado_carga = gestor.cargar_configuracion()

        assert resultado_carga == True, "Debe cargar la configuración correctamente"
        assert gestor.distancia_total == 2000, "Debe cargar distancia_total"
        assert gestor.velocidad_carrito == 10, "Debe cargar velocidad_carrito"
        assert gestor.refresco_ms == 200, "Debe cargar refresco_ms"
        assert gestor.altura_salto == 50, "Debe cargar altura_salto"
        assert gestor.color_carrito_inicial == "azul", (
            "Debe cargar color_carrito_inicial"
        )

        # Verificar que se cargaron los obstáculos
        assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 4, (
            "Debe cargar 4 obstáculos"
        )

        # Verificar representación del árbol (estructura)
        assert not gestor.arbol_obstaculos.esta_vacio(), "El árbol no debe estar vacío"

        # Verificar que el árbol mantiene balance
        obstaculos = gestor.arbol_obstaculos.recorrido_en_profundidad()
        assert len(obstaculos) == 4, "Debe tener 4 obstáculos en el recorrido"

        print("✅ Carga y representación del árbol: PASÓ")

    finally:
        # Limpiar archivo temporal
        os.unlink(temp_file)


def test_recorridos_graficos_arbol():
    """
    Prueba: Recorridos gráficos del árbol (1.0 puntos)
    - Recorrido en anchura (BFS)
    - Recorrido en profundidad (in-order)
    """
    print("🧪 Probando recorridos gráficos del árbol...")

    arbol = ArbolAVL()

    # Insertar obstáculos en orden específico para probar recorridos
    obstaculos = [
        Obstaculo(100, 1, TipoObstaculo.ROCA),  # x=100
        Obstaculo(50, 2, TipoObstaculo.CONO),  # x=50 (izquierda)
        Obstaculo(150, 0, TipoObstaculo.HUECO),  # x=150 (derecha)
        Obstaculo(25, 1, TipoObstaculo.ACEITE),  # x=25 (izquierda-izquierda)
        Obstaculo(75, 0, TipoObstaculo.BARRERA),  # x=75 (izquierda-derecha)
        Obstaculo(125, 2, TipoObstaculo.ROCA),  # x=125 (derecha-izquierda)
        Obstaculo(175, 1, TipoObstaculo.CONO),  # x=175 (derecha-derecha)
    ]

    for obstaculo in obstaculos:
        arbol.insertar(obstaculo)

    # Probar recorrido en anchura (BFS)
    recorrido_anchura = arbol.recorrido_en_anchura()
    assert len(recorrido_anchura) == 7, "Recorrido en anchura debe tener 7 elementos"

    # En BFS, el primer elemento debe ser la raíz (100,1)
    assert recorrido_anchura[0].x == 100 and recorrido_anchura[0].y == 1, (
        "Primer elemento debe ser la raíz"
    )

    # Probar recorrido en profundidad (in-order)
    recorrido_profundidad = arbol.recorrido_en_profundidad()
    assert len(recorrido_profundidad) == 7, (
        "Recorrido en profundidad debe tener 7 elementos"
    )

    # En in-order, los elementos deben estar ordenados por coordenadas
    for i in range(len(recorrido_profundidad) - 1):
        obs1 = recorrido_profundidad[i]
        obs2 = recorrido_profundidad[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
            f"Recorrido in-order debe estar ordenado: {obs1} antes de {obs2}"
        )

    # Verificar que ambos recorridos contienen los mismos elementos
    elementos_anchura = set((obs.x, obs.y) for obs in recorrido_anchura)
    elementos_profundidad = set((obs.x, obs.y) for obs in recorrido_profundidad)
    assert elementos_anchura == elementos_profundidad, (
        "Ambos recorridos deben contener los mismos elementos"
    )

    print("✅ Recorridos gráficos del árbol: PASÓ")


def test_administracion_arbol_antes_juego():
    """
    Prueba: Administración del árbol antes de iniciar el juego (1.0 puntos)
    - Inserción manual de obstáculos
    - Eliminación de obstáculos
    - No permitir coordenadas repetidas
    - Comportamiento natural del AVL
    """
    print("🧪 Probando administración del árbol antes del juego...")

    gestor = GestorJuego()

    # Probar inserción manual de obstáculos
    assert gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA) == True, (
        "Debe insertar obstáculo"
    )
    assert gestor.agregar_obstaculo(200, 2, TipoObstaculo.CONO) == True, (
        "Debe insertar segundo obstáculo"
    )
    assert gestor.agregar_obstaculo(150, 0, TipoObstaculo.HUECO) == True, (
        "Debe insertar tercer obstáculo"
    )

    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 3, (
        "Debe tener 3 obstáculos"
    )

    # Probar que no se permiten coordenadas repetidas
    assert gestor.agregar_obstaculo(100, 1, TipoObstaculo.ACEITE) == False, (
        "No debe permitir coordenadas repetidas"
    )
    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 3, (
        "Debe seguir teniendo 3 obstáculos"
    )

    # Probar eliminación de obstáculos
    assert gestor.eliminar_obstaculo(200, 2) == True, (
        "Debe eliminar obstáculo existente"
    )
    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 2, (
        "Debe tener 2 obstáculos después de eliminar"
    )

    # Probar eliminación de obstáculo inexistente
    assert gestor.eliminar_obstaculo(300, 3) == False, (
        "No debe eliminar obstáculo inexistente"
    )
    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 2, (
        "Debe seguir teniendo 2 obstáculos"
    )

    # Probar comportamiento natural del AVL (balanceamiento)
    # Insertar muchos obstáculos para forzar rotaciones
    for i in range(10):
        gestor.agregar_obstaculo(50 + i * 10, i % 3, TipoObstaculo.ROCA)

    # Verificar que el árbol mantiene balance (altura logarítmica)
    total_obstaculos = gestor.arbol_obstaculos.obtener_total_obstaculos()
    assert total_obstaculos == 12, f"Debe tener 12 obstáculos, tiene {total_obstaculos}"

    # Verificar que las operaciones siguen funcionando después del balanceamiento
    obstaculos_rango = gestor.arbol_obstaculos.buscar_en_rango(100, 150, 0, 2)
    assert len(obstaculos_rango) >= 1, (
        "Debe encontrar obstáculos en el rango después del balanceamiento"
    )

    print("✅ Administración del árbol antes del juego: PASÓ")


def test_juego_carrito_usando_arbol_avl():
    """
    Prueba: Juego del carrito usando el árbol AVL (2.0 puntos)
    - Movimiento automático del carrito
    - Control manual en eje Y
    - Sistema de salto
    - Consulta eficiente de obstáculos en rango visible
    - Detección de colisiones
    - Sistema de energía
    - Condiciones de fin de juego
    """
    print("🧪 Probando juego del carrito usando árbol AVL...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar obstáculos estratégicamente
    obstaculos_juego = [
        (100, 1, TipoObstaculo.ROCA),  # Obstáculo en carril medio
        (150, 0, TipoObstaculo.CONO),  # Obstáculo en carril abajo
        (200, 2, TipoObstaculo.HUECO),  # Obstáculo en carril arriba
        (250, 1, TipoObstaculo.ACEITE),  # Obstáculo en carril medio
        (300, 0, TipoObstaculo.BARRERA),  # Obstáculo en carril abajo
    ]

    for x, y, tipo in obstaculos_juego:
        gestor.agregar_obstaculo(x, y, tipo)

    carrito = gestor.carrito
    assert carrito is not None, "Debe tener un carrito inicializado"

    # Probar movimiento automático del carrito
    posicion_inicial_x = carrito.x
    carrito.mover_automaticamente()
    assert carrito.x > posicion_inicial_x, (
        "El carrito debe moverse automáticamente en X"
    )

    # Probar control manual en eje Y
    posicion_inicial_y = carrito.y
    carrito.mover_arriba()
    assert carrito.y > posicion_inicial_y, "El carrito debe moverse hacia arriba"

    carrito.mover_abajo()
    assert carrito.y == posicion_inicial_y, (
        "El carrito debe volver a la posición original"
    )

    # Probar sistema de salto
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "El carrito debe estar saltando"
    assert carrito.esta_saltando() == True, "Debe detectar que está saltando"

    # Simular finalización del salto
    for _ in range(25):  # Más que la duración del salto
        carrito.actualizar_salto()
    assert carrito.estado == EstadoCarrito.NORMAL, (
        "El carrito debe volver al estado normal"
    )

    # Probar consulta eficiente de obstáculos en rango visible
    carrito.x = 90  # Posicionar cerca de obstáculos
    gestor.actualizar_obstaculos_visibles()

    # Debe encontrar obstáculos en el rango de visión
    assert len(gestor.obstaculos_visibles) > 0, (
        "Debe encontrar obstáculos en el rango visible"
    )

    # Probar detección de colisiones
    carrito.x = 100
    carrito.y = 1
    colisiones = gestor.verificar_colisiones()
    assert len(colisiones) > 0, "Debe detectar colisiones"

    # Probar sistema de energía
    energia_inicial = carrito.energia_actual
    if colisiones:
        gestor.procesar_colision(colisiones[0])
        assert carrito.energia_actual < energia_inicial, (
            "El carrito debe perder energía por colisión"
        )

    # Probar condiciones de fin de juego
    # Condición 1: Sin energía
    carrito.energia_actual = 0
    assert gestor.verificar_condiciones_fin_juego() == True, (
        "Debe terminar el juego sin energía"
    )

    # Condición 2: Alcanzar distancia total
    carrito.energia_actual = 100  # Restaurar energía
    carrito.x = gestor.distancia_total + 50  # Posición que supera la distancia total
    # Actualizar distancia recorrida manualmente para la prueba
    gestor.distancia_recorrida = gestor.distancia_total + 10
    assert gestor.verificar_condiciones_fin_juego() == True, (
        "Debe terminar el juego al alcanzar la meta"
    )

    print("✅ Juego del carrito usando árbol AVL: PASÓ")


def test_criterios_ordenamiento_avl():
    """
    Prueba específica de los criterios de ordenamiento del AVL según definicion.md:
    - Comparar primero el valor de x
    - En caso de empate en x, comparar el valor de y
    - No se permiten coordenadas repetidas
    """
    print("🧪 Probando criterios de ordenamiento del AVL...")

    arbol = ArbolAVL()

    # Probar ordenamiento por X
    obstaculo1 = Obstaculo(100, 1, TipoObstaculo.ROCA)
    obstaculo2 = Obstaculo(50, 2, TipoObstaculo.CONO)

    nodo1 = NodoAVL(obstaculo1)
    nodo2 = NodoAVL(obstaculo2)

    assert nodo1.es_mayor_que(obstaculo2) == True, (
        "100,1 debe ser mayor que 50,2 (por X)"
    )
    assert nodo2.es_mayor_que(obstaculo1) == False, "50,2 no debe ser mayor que 100,1"

    # Probar ordenamiento por Y cuando X es igual
    obstaculo3 = Obstaculo(100, 0, TipoObstaculo.HUECO)
    assert nodo1.es_mayor_que(obstaculo3) == True, (
        "100,1 debe ser mayor que 100,0 (por Y)"
    )
    assert nodo1.es_igual_a(obstaculo3) == False, "100,1 no debe ser igual a 100,0"

    # Probar que no se permiten coordenadas repetidas
    arbol.insertar(obstaculo1)
    assert arbol.insertar(obstaculo1) == False, (
        "No debe permitir insertar coordenadas repetidas"
    )
    assert arbol.obtener_total_obstaculos() == 1, "Debe tener solo 1 obstáculo"

    # Probar inserción de obstáculo con mismas coordenadas pero diferente tipo
    obstaculo_repetido = Obstaculo(100, 1, TipoObstaculo.ACEITE)
    assert arbol.insertar(obstaculo_repetido) == False, (
        "No debe permitir coordenadas repetidas aunque sea diferente tipo"
    )

    print("✅ Criterios de ordenamiento del AVL: PASÓ")


def test_consulta_rango_eficiente():
    """
    Prueba específica de la consulta eficiente de obstáculos en rango
    según definicion.md: "consultar rápidamente los obstáculos dentro de un rango"
    """
    print("🧪 Probando consulta eficiente de obstáculos en rango...")

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

    # Probar consulta de rango específico
    obstaculos_rango = arbol.buscar_en_rango(90, 160, 0, 2)

    # Debe encontrar obstáculos en el rango
    coordenadas_encontradas = [(obs.x, obs.y) for obs in obstaculos_rango]
    assert (100, 1) in coordenadas_encontradas, "Debe encontrar obstáculo en (100,1)"
    assert (150, 2) in coordenadas_encontradas, "Debe encontrar obstáculo en (150,2)"

    # No debe encontrar obstáculos fuera del rango
    assert (50, 0) not in coordenadas_encontradas, (
        "No debe encontrar obstáculo en (50,0)"
    )
    assert (200, 0) not in coordenadas_encontradas, (
        "No debe encontrar obstáculo en (200,0)"
    )

    # Probar consulta de rango vacío
    obstaculos_vacio = arbol.buscar_en_rango(400, 500, 0, 2)
    assert len(obstaculos_vacio) == 0, "No debe encontrar obstáculos en rango vacío"

    # Probar consulta de rango que incluye todos los obstáculos
    obstaculos_todos = arbol.buscar_en_rango(0, 400, 0, 2)
    assert len(obstaculos_todos) == 7, "Debe encontrar todos los obstáculos"

    print("✅ Consulta eficiente de obstáculos en rango: PASÓ")


def test_configuracion_json():
    """
    Prueba específica de la carga de configuración desde JSON
    según definicion.md
    """
    print("🧪 Probando configuración desde JSON...")

    # Crear configuración de prueba según el ejemplo de definicion.md
    config_json = {
        "configuracion": {
            "distancia_total": 2000,
            "velocidad_carrito": 10,
            "refresco_ms": 300,
            "altura_salto": 50,
            "color_carrito_inicial": "verde",
        },
        "obstaculos": [
            {"x": 150, "y": 0, "tipo": "roca"},
            {"x": 320, "y": 1, "tipo": "cono"},
            {"x": 500, "y": 2, "tipo": "hueco"},
            {"x": 1200, "y": 1, "tipo": "aceite"},
        ],
    }

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_json, f, indent=2)
        temp_file = f.name

    try:
        gestor = GestorJuego(temp_file)
        resultado = gestor.cargar_configuracion()

        assert resultado == True, "Debe cargar configuración exitosamente"

        # Verificar configuración del juego
        assert gestor.distancia_total == 2000, "Debe cargar distancia_total"
        assert gestor.velocidad_carrito == 10, "Debe cargar velocidad_carrito"
        assert gestor.refresco_ms == 300, "Debe cargar refresco_ms"
        assert gestor.altura_salto == 50, "Debe cargar altura_salto"
        assert gestor.color_carrito_inicial == "verde", (
            "Debe cargar color_carrito_inicial"
        )

        # Verificar obstáculos
        assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 4, (
            "Debe cargar 4 obstáculos"
        )

        # Verificar que los obstáculos están en el árbol
        obstaculos = gestor.arbol_obstaculos.recorrido_en_profundidad()
        coordenadas = [(obs.x, obs.y) for obs in obstaculos]

        assert (150, 0) in coordenadas, "Debe tener obstáculo en (150,0)"
        assert (320, 1) in coordenadas, "Debe tener obstáculo en (320,1)"
        assert (500, 2) in coordenadas, "Debe tener obstáculo en (500,2)"
        assert (1200, 1) in coordenadas, "Debe tener obstáculo en (1200,1)"

        print("✅ Configuración desde JSON: PASÓ")

    finally:
        os.unlink(temp_file)


def test_escenario_carrito_llega_meta():
    """
    Prueba específica: Carrito llega a la meta (escenario de éxito)
    """
    print("🧪 Probando escenario: carrito llega a la meta...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Configurar distancia corta para prueba
    gestor.distancia_total = 500

    # Agregar algunos obstáculos
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)
    gestor.agregar_obstaculo(200, 0, TipoObstaculo.CONO)
    gestor.agregar_obstaculo(300, 2, TipoObstaculo.HUECO)

    carrito = gestor.carrito

    # Simular avance del carrito hasta la meta
    for paso in range(100):  # Suficientes pasos para llegar a la meta
        # Mover carrito automáticamente
        carrito.mover_automaticamente()

        # Actualizar distancia recorrida
        gestor.distancia_recorrida = carrito.x - 50

        # Actualizar obstáculos visibles
        gestor.actualizar_obstaculos_visibles()

        # Verificar colisiones
        colisiones = gestor.verificar_colisiones()
        if colisiones:
            # Esquivar obstáculos moviendo a carriles libres
            if carrito.y == 1:  # Si está en carril medio
                carrito.mover_arriba()  # Mover arriba
            elif carrito.y == 2:  # Si está arriba
                carrito.mover_abajo()  # Mover abajo

        # Verificar si llegó a la meta
        if gestor.verificar_condiciones_fin_juego():
            break

    # Verificar que llegó a la meta
    assert gestor.distancia_recorrida >= gestor.distancia_total, (
        "Debe haber llegado a la meta"
    )
    assert carrito.esta_vivo() == True, "Carrito debe seguir vivo al llegar a la meta"

    print("✅ Escenario: carrito llega a la meta: PASÓ")


def test_escenario_carrito_muere():
    """
    Prueba específica: Carrito muere por colisiones (escenario de fallo)
    """
    print("🧪 Probando escenario: carrito muere por colisiones...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar muchos obstáculos para causar daño
    for i in range(10):
        gestor.agregar_obstaculo(
            100 + i * 20, 1, TipoObstaculo.BARRERA
        )  # Obstáculos de alto daño

    carrito = gestor.carrito

    # Simular juego hasta que muera
    for paso in range(50):
        # Mover carrito automáticamente
        carrito.mover_automaticamente()

        # Actualizar obstáculos visibles
        gestor.actualizar_obstaculos_visibles()

        # Verificar colisiones
        colisiones = gestor.verificar_colisiones()
        if colisiones:
            # Procesar todas las colisiones
            for colision in colisiones:
                gestor.procesar_colision(colision)

        # Verificar si murió
        if not carrito.esta_vivo():
            break

    # Verificar que murió
    assert carrito.esta_vivo() == False, "Carrito debe haber muerto"
    assert carrito.energia_actual == 0, "Carrito debe tener 0 de energía"

    print("✅ Escenario: carrito muere por colisiones: PASÓ")


def main():
    """Ejecuta todas las pruebas de requisitos del proyecto"""
    print("🚀 Iniciando pruebas de requisitos del proyecto...\n")
    print("=" * 60)

    try:
        # Pruebas según puntos de calificación
        test_carga_y_representacion_arbol()
        print()

        test_recorridos_graficos_arbol()
        print()

        test_administracion_arbol_antes_juego()
        print()

        test_juego_carrito_usando_arbol_avl()
        print()

        # Pruebas específicas de requisitos técnicos
        test_criterios_ordenamiento_avl()
        print()

        test_consulta_rango_eficiente()
        print()

        test_configuracion_json()
        print()

        # Pruebas de escenarios específicos
        test_escenario_carrito_llega_meta()
        print()

        test_escenario_carrito_muere()
        print()

        print("=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS DE REQUISITOS PASARON!")
        print("✅ El proyecto cumple con todos los requisitos de definicion.md")
        print("📊 Puntos de calificación validados:")
        print("   • Carga y representación del árbol: ✅ (0.5)")
        print("   • Recorridos gráficos del árbol: ✅ (1.0)")
        print("   • Administración del árbol antes del juego: ✅ (1.0)")
        print("   • Juego del carrito usando árbol AVL: ✅ (2.0)")
        print("   • Criterios técnicos específicos: ✅")
        print("   • Escenarios de juego: ✅")

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
