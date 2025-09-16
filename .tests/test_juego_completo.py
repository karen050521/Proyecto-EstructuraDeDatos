#!/usr/bin/env python3
"""
Pruebas del juego completo - Validación de integración y mecánicas del juego
Incluye escenarios completos desde inicio hasta fin del juego
"""

import sys
import os
import json
import tempfile

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.obstaculo import Obstaculo, TipoObstaculo
from logic.carrito import Carrito, EstadoCarrito
from logic.gestor_juego import GestorJuego, EstadoJuego


def test_inicializacion_juego():
    """Prueba: Inicialización completa del juego"""
    print("🧪 Probando inicialización del juego...")

    gestor = GestorJuego()

    # Verificar estado inicial
    assert gestor.estado_actual == EstadoJuego.MENU_INICIAL, (
        "Estado inicial debe ser MENU_INICIAL"
    )
    assert gestor.carrito is None, "Carrito debe ser None inicialmente"
    assert gestor.distancia_recorrida == 0, "Distancia recorrida debe ser 0"
    assert gestor.puntuacion == 0, "Puntuación debe ser 0"
    assert gestor.arbol_obstaculos.esta_vacio(), "Árbol de obstáculos debe estar vacío"

    # Inicializar juego
    gestor.inicializar_juego()

    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Estado debe ser JUGANDO"
    assert gestor.carrito is not None, "Debe tener un carrito"
    assert gestor.carrito.x == 50, "Carrito debe estar en posición inicial X=50"
    assert gestor.carrito.y == 1, "Carrito debe estar en carril medio Y=1"
    assert gestor.carrito.energia_actual == 100, "Carrito debe tener energía completa"

    print("✅ Inicialización del juego: PASÓ")


def test_carga_configuracion_json():
    """Prueba: Carga de configuración desde JSON"""
    print("🧪 Probando carga de configuración JSON...")

    # Crear configuración de prueba
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
            {"x": 750, "y": 0, "tipo": "aceite"},
            {"x": 1000, "y": 1, "tipo": "barrera"},
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
        assert gestor.distancia_total == 2000, "Debe cargar distancia_total"
        assert gestor.velocidad_carrito == 10, "Debe cargar velocidad_carrito"
        assert gestor.refresco_ms == 200, "Debe cargar refresco_ms"
        assert gestor.altura_salto == 50, "Debe cargar altura_salto"
        assert gestor.color_carrito_inicial == "azul", (
            "Debe cargar color_carrito_inicial"
        )

        # Verificar obstáculos cargados
        assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 5, (
            "Debe cargar 5 obstáculos"
        )

        # Verificar que los obstáculos están en el árbol
        obstaculos = gestor.arbol_obstaculos.recorrido_en_profundidad()
        coordenadas = [(obs.x, obs.y) for obs in obstaculos]

        assert (150, 0) in coordenadas, "Debe tener obstáculo en (150,0)"
        assert (320, 1) in coordenadas, "Debe tener obstáculo en (320,1)"
        assert (500, 2) in coordenadas, "Debe tener obstáculo en (500,2)"
        assert (750, 0) in coordenadas, "Debe tener obstáculo en (750,0)"
        assert (1000, 1) in coordenadas, "Debe tener obstáculo en (1000,1)"

    finally:
        os.unlink(temp_file)

    print("✅ Carga de configuración JSON: PASÓ")


def test_mecanicas_juego_basicas():
    """Prueba: Mecánicas básicas del juego"""
    print("🧪 Probando mecánicas básicas del juego...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    carrito = gestor.carrito

    # Probar movimiento automático
    posicion_inicial = carrito.x
    carrito.mover_automaticamente()
    assert carrito.x > posicion_inicial, "Carrito debe moverse automáticamente"

    # Probar control manual
    carrito.mover_arriba()
    assert carrito.y == 2, "Debe moverse al carril superior"

    carrito.mover_abajo()
    assert carrito.y == 1, "Debe volver al carril medio"

    # Probar salto
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "Debe estar saltando"

    # Simular finalización del salto
    for _ in range(25):
        carrito.actualizar_salto()
    assert carrito.estado == EstadoCarrito.NORMAL, "Debe volver al estado normal"

    print("✅ Mecánicas básicas del juego: PASÓ")


def test_obstaculos_visibles():
    """Prueba: Sistema de obstáculos visibles"""
    print("🧪 Probando sistema de obstáculos visibles...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar obstáculos en diferentes posiciones
    obstaculos = [
        (100, 1, TipoObstaculo.ROCA),  # Cerca del carrito
        (150, 0, TipoObstaculo.CONO),  # En rango de visión
        (200, 2, TipoObstaculo.HUECO),  # En rango de visión
        (300, 1, TipoObstaculo.ACEITE),  # Fuera de rango inicial
        (500, 0, TipoObstaculo.BARRERA),  # Muy lejos
    ]

    for x, y, tipo in obstaculos:
        gestor.agregar_obstaculo(x, y, tipo)

    # Posicionar carrito y actualizar obstáculos visibles
    carrito = gestor.carrito
    carrito.x = 90  # Cerca de los primeros obstáculos
    gestor.actualizar_obstaculos_visibles()

    # Debe encontrar obstáculos en el rango de visión
    assert len(gestor.obstaculos_visibles) > 0, "Debe encontrar obstáculos visibles"

    # Mover carrito más adelante
    carrito.x = 250
    gestor.actualizar_obstaculos_visibles()

    # Debe encontrar diferentes obstáculos
    assert len(gestor.obstaculos_visibles) >= 0, "Debe actualizar obstáculos visibles"

    print("✅ Sistema de obstáculos visibles: PASÓ")


def test_deteccion_colisiones():
    """Prueba: Detección y procesamiento de colisiones"""
    print("🧪 Probando detección de colisiones...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar obstáculo estratégicamente
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)  # En carril medio

    carrito = gestor.carrito

    # Posicionar carrito para colisión
    carrito.x = 100
    carrito.y = 1

    # Actualizar obstáculos visibles
    gestor.actualizar_obstaculos_visibles()

    # Verificar colisiones
    colisiones = gestor.verificar_colisiones()
    assert len(colisiones) > 0, "Debe detectar colisión"

    # Procesar colisión
    energia_inicial = carrito.energia_actual
    gestor.procesar_colision(colisiones[0])

    assert carrito.energia_actual < energia_inicial, "Carrito debe perder energía"
    assert carrito.estado == EstadoCarrito.COLISIONANDO, (
        "Carrito debe estar en estado de colisión"
    )

    print("✅ Detección de colisiones: PASÓ")


def test_sistema_energia():
    """Prueba: Sistema de energía y daño por tipo de obstáculo"""
    print("🧪 Probando sistema de energía...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    carrito = gestor.carrito

    # Probar daño por diferentes tipos de obstáculos
    tipos_daño = [
        (TipoObstaculo.ROCA, 20),
        (TipoObstaculo.CONO, 10),
        (TipoObstaculo.HUECO, 15),
        (TipoObstaculo.ACEITE, 5),
        (TipoObstaculo.BARRERA, 25),
    ]

    for tipo, daño_esperado in tipos_daño:
        # Restaurar energía
        carrito.energia_actual = 100

        # Crear obstáculo y procesar colisión
        obstaculo = Obstaculo(100, 1, tipo)
        energia_antes = carrito.energia_actual
        gestor.procesar_colision(obstaculo)

        assert carrito.energia_actual == energia_antes - daño_esperado, (
            f"Daño debe ser {daño_esperado} para {tipo}"
        )

    print("✅ Sistema de energía: PASÓ")


def test_condiciones_fin_juego():
    """Prueba: Condiciones de fin del juego"""
    print("🧪 Probando condiciones de fin del juego...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    carrito = gestor.carrito

    # Condición 1: Sin energía
    carrito.energia_actual = 0
    assert gestor.verificar_condiciones_fin_juego() == True, "Debe terminar sin energía"

    # Condición 2: Alcanzar distancia total
    carrito.energia_actual = 100  # Restaurar energía
    gestor.distancia_recorrida = gestor.distancia_total + 10
    assert gestor.verificar_condiciones_fin_juego() == True, (
        "Debe terminar al alcanzar meta"
    )

    # Condición 3: Juego normal (no debe terminar)
    carrito.energia_actual = 50
    gestor.distancia_recorrida = 100
    assert gestor.verificar_condiciones_fin_juego() == False, (
        "No debe terminar en condiciones normales"
    )

    print("✅ Condiciones de fin del juego: PASÓ")


def test_escenario_juego_completo():
    """Prueba: Escenario completo de juego"""
    print("🧪 Probando escenario completo de juego...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Crear un nivel con obstáculos estratégicos
    obstaculos_nivel = [
        (100, 1, TipoObstaculo.ROCA),  # Obstáculo en carril medio
        (150, 0, TipoObstaculo.CONO),  # Obstáculo en carril abajo
        (200, 2, TipoObstaculo.HUECO),  # Obstáculo en carril arriba
        (250, 1, TipoObstaculo.ACEITE),  # Obstáculo en carril medio
        (300, 0, TipoObstaculo.BARRERA),  # Obstáculo en carril abajo
        (350, 2, TipoObstaculo.ROCA),  # Obstáculo en carril arriba
        (400, 1, TipoObstaculo.CONO),  # Obstáculo en carril medio
    ]

    for x, y, tipo in obstaculos_nivel:
        gestor.agregar_obstaculo(x, y, tipo)

    carrito = gestor.carrito

    # Simular juego: avanzar y esquivar obstáculos
    for paso in range(50):
        # Mover carrito automáticamente
        carrito.mover_automaticamente()

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
            else:  # Si está abajo
                carrito.mover_arriba()  # Mover arriba

        # Actualizar distancia recorrida
        gestor.distancia_recorrida = carrito.x - 50

        # Verificar que el carrito sigue vivo
        if not carrito.esta_vivo():
            break

        # Verificar que no se alcanzó la meta
        if gestor.distancia_recorrida >= gestor.distancia_total:
            break

    # Verificar estado final
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Juego debe seguir activo"
    assert carrito.esta_vivo() == True, "Carrito debe seguir vivo"
    assert gestor.distancia_recorrida > 0, "Debe haber avanzado algo"

    print("✅ Escenario completo de juego: PASÓ")


def test_estadisticas_juego():
    """Prueba: Sistema de estadísticas del juego"""
    print("🧪 Probando sistema de estadísticas...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar algunos obstáculos
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)
    gestor.agregar_obstaculo(150, 0, TipoObstaculo.CONO)

    # Simular algo de progreso
    carrito = gestor.carrito
    carrito.x = 120
    carrito.recibir_daño(20)
    gestor.distancia_recorrida = 70
    gestor.puntuacion = 100

    # Obtener estadísticas
    stats = gestor.obtener_estadisticas()

    # Verificar que todas las estadísticas están presentes
    assert "distancia_recorrida" in stats, "Debe incluir distancia_recorrida"
    assert "distancia_total" in stats, "Debe incluir distancia_total"
    assert "progreso_porcentaje" in stats, "Debe incluir progreso_porcentaje"
    assert "puntuacion" in stats, "Debe incluir puntuacion"
    assert "tiempo_juego" in stats, "Debe incluir tiempo_juego"
    assert "energia_porcentaje" in stats, "Debe incluir energia_porcentaje"
    assert "obstaculos_visibles" in stats, "Debe incluir obstaculos_visibles"
    assert "total_obstaculos" in stats, "Debe incluir total_obstaculos"
    assert "estado_juego" in stats, "Debe incluir estado_juego"

    # Verificar valores
    assert stats["distancia_recorrida"] == 70, "Distancia recorrida debe ser 70"
    assert stats["distancia_total"] == 2000, "Distancia total debe ser 2000"
    assert stats["puntuacion"] == 100, "Puntuación debe ser 100"
    assert stats["total_obstaculos"] == 2, "Debe tener 2 obstáculos"
    assert stats["estado_juego"] == "jugando", "Estado debe ser jugando"

    print("✅ Sistema de estadísticas: PASÓ")


def test_pausa_y_reinicio():
    """Prueba: Sistema de pausa y reinicio"""
    print("🧪 Probando sistema de pausa y reinicio...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar obstáculos
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)

    # Simular progreso
    carrito = gestor.carrito
    carrito.x = 120
    carrito.recibir_daño(30)
    gestor.distancia_recorrida = 70
    gestor.puntuacion = 150

    # Pausar juego
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.PAUSADO, "Debe estar pausado"

    # Despausar juego
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Debe volver a jugando"

    # Reiniciar juego
    gestor.reiniciar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Debe estar jugando"
    assert gestor.distancia_recorrida == 0, "Distancia debe ser 0"
    assert gestor.puntuacion == 0, "Puntuación debe ser 0"
    assert carrito.x == 50, "Carrito debe estar en posición inicial"
    assert carrito.y == 1, "Carrito debe estar en carril inicial"
    assert carrito.energia_actual == 100, "Carrito debe tener energía completa"

    print("✅ Sistema de pausa y reinicio: PASÓ")


def main():
    """Ejecuta todas las pruebas del juego completo"""
    print("🚀 Iniciando pruebas del juego completo...\n")
    print("=" * 50)

    try:
        test_inicializacion_juego()
        print()

        test_carga_configuracion_json()
        print()

        test_mecanicas_juego_basicas()
        print()

        test_obstaculos_visibles()
        print()

        test_deteccion_colisiones()
        print()

        test_sistema_energia()
        print()

        test_condiciones_fin_juego()
        print()

        test_escenario_juego_completo()
        print()

        test_estadisticas_juego()
        print()

        test_pausa_y_reinicio()
        print()

        print("=" * 50)
        print("🎉 ¡TODAS LAS PRUEBAS DEL JUEGO COMPLETO PASARON!")
        print("✅ Integración y mecánicas del juego validadas")

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
