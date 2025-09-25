#!/usr/bin/env python3
"""
Pruebas específicas para validar funcionalidad de interfaz gráfica
Simula operaciones que realizará la interfaz gráfica
"""

import sys
import os
import json
import tempfile

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.obstaculo import Obstaculo, TipoObstaculo
from logic.arbol_avl import ArbolAVL
from logic.carrito import Carrito, EstadoCarrito
from logic.gestor_juego import GestorJuego, EstadoJuego


def test_visualizacion_arbol_avl():
    """Prueba: Funcionalidad para visualización del árbol AVL"""
    print("🧪 Probando funcionalidad para visualización del árbol AVL...")

    gestor = GestorJuego()

    # Crear árbol con estructura interesante para visualizar
    obstaculos_visualizacion = [
        (100, 1, TipoObstaculo.ROCA),  # Raíz
        (50, 2, TipoObstaculo.CONO),  # Izquierda
        (150, 0, TipoObstaculo.HUECO),  # Derecha
        (25, 1, TipoObstaculo.ACEITE),  # Izquierda-izquierda
        (75, 0, TipoObstaculo.BARRERA),  # Izquierda-derecha
        (125, 2, TipoObstaculo.ROCA),  # Derecha-izquierda
        (175, 1, TipoObstaculo.CONO),  # Derecha-derecha
        (10, 0, TipoObstaculo.HUECO),  # Izquierda-izquierda-izquierda
        (200, 2, TipoObstaculo.ACEITE),  # Derecha-derecha-derecha
    ]

    for x, y, tipo in obstaculos_visualizacion:
        gestor.agregar_obstaculo(x, y, tipo)

    # Obtener datos para visualización
    total_obstaculos = gestor.arbol_obstaculos.obtener_total_obstaculos()
    assert total_obstaculos == 9, "Debe tener 9 obstáculos para visualización"

    # Recorrido en anchura para visualización por niveles
    recorrido_anchura = gestor.obtener_recorrido_anchura()
    assert len(recorrido_anchura) == 9, "Recorrido en anchura debe tener 9 elementos"

    # Recorrido en profundidad para visualización in-order
    recorrido_profundidad = gestor.obtener_recorrido_profundidad()
    assert len(recorrido_profundidad) == 9, (
        "Recorrido en profundidad debe tener 9 elementos"
    )

    # Verificar que los recorridos son diferentes (estructura no trivial)
    assert recorrido_anchura != recorrido_profundidad, (
        "Los recorridos deben ser diferentes"
    )

    # Verificar ordenamiento en profundidad
    for i in range(len(recorrido_profundidad) - 1):
        obs1 = recorrido_profundidad[i]
        obs2 = recorrido_profundidad[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), (
            "Recorrido en profundidad debe estar ordenado"
        )

    print("✅ Funcionalidad para visualización del árbol AVL: PASÓ")


def test_actualizacion_tiempo_real():
    """Prueba: Actualización en tiempo real para interfaz"""
    print("🧪 Probando actualización en tiempo real para interfaz...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar obstáculos distribuidos
    for i in range(20):
        x = 100 + i * 50
        y = i % 3
        tipo = list(TipoObstaculo)[i % 5]
        gestor.agregar_obstaculo(x, y, tipo)

    carrito = gestor.carrito

    # Simular actualización en tiempo real (como haría la interfaz)
    for frame in range(50):
        # Actualizar carrito (movimiento automático)
        carrito.mover_automaticamente()

        # Actualizar obstáculos visibles (como haría la interfaz)
        gestor.actualizar_obstaculos_visibles()

        # Obtener datos para renderizado
        obstaculos_visibles = gestor.obstaculos_visibles
        posicion_carrito = (carrito.x, carrito.y)
        estado_carrito = carrito.estado
        energia_porcentaje = carrito.obtener_porcentaje_energia()

        # Verificar que los datos están disponibles para la interfaz
        assert isinstance(obstaculos_visibles, list), (
            "Obstáculos visibles debe ser lista"
        )
        assert isinstance(posicion_carrito, tuple), "Posición carrito debe ser tupla"
        assert isinstance(estado_carrito, EstadoCarrito), "Estado carrito debe ser enum"
        assert isinstance(energia_porcentaje, float), (
            "Energía porcentaje debe ser float"
        )
        assert 0.0 <= energia_porcentaje <= 1.0, "Energía debe estar entre 0 y 1"

        # Verificar colisiones (como haría la interfaz)
        colisiones = gestor.verificar_colisiones()
        if colisiones:
            # Procesar colisión (como haría la interfaz)
            gestor.procesar_colision(colisiones[0])

        # Actualizar estadísticas (como haría la interfaz)
        gestor.distancia_recorrida = carrito.x - 50
        stats = gestor.obtener_estadisticas()

        # Verificar que las estadísticas están disponibles
        assert "distancia_recorrida" in stats, "Debe incluir distancia_recorrida"
        assert "energia_porcentaje" in stats, "Debe incluir energia_porcentaje"
        assert "obstaculos_visibles" in stats, "Debe incluir obstaculos_visibles"
        assert "estado_juego" in stats, "Debe incluir estado_juego"

    print("✅ Actualización en tiempo real para interfaz: PASÓ")


def test_controles_usuario():
    """Prueba: Simulación de controles de usuario"""
    print("🧪 Probando simulación de controles de usuario...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    carrito = gestor.carrito

    # Simular controles de usuario
    # Flecha arriba
    carrito.mover_arriba()
    assert carrito.y == 2, "Debe moverse al carril superior"

    # Flecha abajo
    carrito.mover_abajo()
    assert carrito.y == 1, "Debe moverse al carril medio"

    carrito.mover_abajo()
    assert carrito.y == 0, "Debe moverse al carril inferior"

    # Tecla espacio (salto)
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "Debe iniciar salto"

    # Simular frames de salto
    for _ in range(25):
        carrito.actualizar_salto()

    assert carrito.estado == EstadoCarrito.NORMAL, "Debe terminar salto"

    # Simular pausa del juego
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.PAUSADO, "Debe pausar juego"

    # Simular reanudar juego
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Debe reanudar juego"

    # Simular reinicio del juego
    gestor.reiniciar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Debe reiniciar juego"
    assert carrito.x == 50, "Carrito debe volver a posición inicial"
    assert carrito.y == 1, "Carrito debe volver a carril inicial"
    assert carrito.energia_actual == 100, "Carrito debe tener energía completa"

    print("✅ Simulación de controles de usuario: PASÓ")


def test_administracion_obstaculos_interfaz():
    """Prueba: Administración de obstáculos desde interfaz"""
    print("🧪 Probando administración de obstáculos desde interfaz...")

    gestor = GestorJuego()

    # Simular agregar obstáculos desde interfaz
    obstaculos_interfaz = [
        (100, 1, TipoObstaculo.ROCA),
        (200, 0, TipoObstaculo.CONO),
        (300, 2, TipoObstaculo.HUECO),
        (400, 1, TipoObstaculo.ACEITE),
        (500, 0, TipoObstaculo.BARRERA),
    ]

    for x, y, tipo in obstaculos_interfaz:
        resultado = gestor.agregar_obstaculo(x, y, tipo)
        assert resultado == True, f"Debe agregar obstáculo en ({x},{y})"

    # Verificar que se agregaron correctamente
    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 5, (
        "Debe tener 5 obstáculos"
    )

    # Simular eliminar obstáculos desde interfaz
    resultado = gestor.eliminar_obstaculo(200, 0)
    assert resultado == True, "Debe eliminar obstáculo existente"

    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 4, (
        "Debe tener 4 obstáculos"
    )

    # Simular intentar agregar obstáculo duplicado
    resultado = gestor.agregar_obstaculo(100, 1, TipoObstaculo.CONO)
    assert resultado == False, "No debe permitir obstáculo duplicado"

    assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 4, (
        "Debe seguir teniendo 4 obstáculos"
    )

    # Obtener datos para mostrar en interfaz
    recorrido_anchura = gestor.obtener_recorrido_anchura()
    recorrido_profundidad = gestor.obtener_recorrido_profundidad()

    assert len(recorrido_anchura) == 4, "Recorrido en anchura debe tener 4 elementos"
    assert len(recorrido_profundidad) == 4, (
        "Recorrido en profundidad debe tener 4 elementos"
    )

    print("✅ Administración de obstáculos desde interfaz: PASÓ")


def test_carga_guardado_configuracion():
    """Prueba: Carga y guardado de configuración para interfaz"""
    print("🧪 Probando carga y guardado de configuración para interfaz...")

    # Crear configuración de prueba
    config_prueba = {
        "configuracion": {
            "distancia_total": 1500,
            "velocidad_carrito": 8,
            "refresco_ms": 150,
            "altura_salto": 60,
            "color_carrito_inicial": "verde",
        },
        "obstaculos": [
            {"x": 100, "y": 0, "tipo": "roca"},
            {"x": 200, "y": 1, "tipo": "cono"},
            {"x": 300, "y": 2, "tipo": "hueco"},
            {"x": 400, "y": 0, "tipo": "aceite"},
            {"x": 500, "y": 1, "tipo": "barrera"},
        ],
    }

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_prueba, f, indent=2)
        temp_file = f.name

    try:
        # Cargar configuración
        gestor = GestorJuego(temp_file)
        resultado_carga = gestor.cargar_configuracion()

        assert resultado_carga == True, "Debe cargar configuración"
        assert gestor.distancia_total == 1500, "Debe cargar distancia_total"
        assert gestor.velocidad_carrito == 8, "Debe cargar velocidad_carrito"
        assert gestor.refresco_ms == 150, "Debe cargar refresco_ms"
        assert gestor.altura_salto == 60, "Debe cargar altura_salto"
        assert gestor.color_carrito_inicial == "verde", (
            "Debe cargar color_carrito_inicial"
        )

        # Verificar obstáculos cargados
        assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 5, (
            "Debe cargar 5 obstáculos"
        )

        # Simular guardado de configuración (como haría la interfaz)
        config_guardada = {
            "configuracion": {
                "distancia_total": gestor.distancia_total,
                "velocidad_carrito": gestor.velocidad_carrito,
                "refresco_ms": gestor.refresco_ms,
                "altura_salto": gestor.altura_salto,
                "color_carrito_inicial": gestor.color_carrito_inicial,
            },
            "obstaculos": [],
        }

        # Obtener obstáculos para guardar
        obstaculos = gestor.arbol_obstaculos.recorrido_en_profundidad()
        for obstaculo in obstaculos:
            config_guardada["obstaculos"].append(
                {"x": obstaculo.x, "y": obstaculo.y, "tipo": obstaculo.tipo.value}
            )

        # Verificar que la configuración se puede serializar
        json_str = json.dumps(config_guardada, indent=2)
        assert len(json_str) > 0, "Debe poder serializar configuración"

        # Verificar que se puede deserializar
        config_deserializada = json.loads(json_str)
        assert config_deserializada["configuracion"]["distancia_total"] == 1500, (
            "Debe poder deserializar configuración"
        )
        assert len(config_deserializada["obstaculos"]) == 5, (
            "Debe poder deserializar obstáculos"
        )

    finally:
        os.unlink(temp_file)

    print("✅ Carga y guardado de configuración para interfaz: PASÓ")


def test_estados_juego_interfaz():
    """Prueba: Estados del juego para interfaz gráfica"""
    print("🧪 Probando estados del juego para interfaz gráfica...")

    gestor = GestorJuego()

    # Estado inicial
    assert gestor.estado_actual == EstadoJuego.MENU_INICIAL, (
        "Estado inicial debe ser MENU_INICIAL"
    )

    # Inicializar juego
    gestor.inicializar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Debe estar en estado JUGANDO"

    # Pausar juego
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.PAUSADO, "Debe estar en estado PAUSADO"

    # Reanudar juego
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Debe volver a estado JUGANDO"

    # Simular fin de juego por energía
    carrito = gestor.carrito
    carrito.energia_actual = 0
    assert gestor.verificar_condiciones_fin_juego() == True, (
        "Debe detectar fin de juego"
    )

    # Simular fin de juego por distancia
    carrito.energia_actual = 100
    gestor.distancia_recorrida = gestor.distancia_total + 10
    assert gestor.verificar_condiciones_fin_juego() == True, (
        "Debe detectar fin de juego por distancia"
    )

    # Reiniciar juego
    gestor.reiniciar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, (
        "Debe estar en estado JUGANDO después de reiniciar"
    )
    assert carrito.energia_actual == 100, "Carrito debe tener energía completa"
    assert gestor.distancia_recorrida == 0, "Distancia debe ser 0"

    print("✅ Estados del juego para interfaz gráfica: PASÓ")


def test_datos_renderizado():
    """Prueba: Datos necesarios para renderizado"""
    print("🧪 Probando datos necesarios para renderizado...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Agregar obstáculos para renderizar
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)
    gestor.agregar_obstaculo(150, 0, TipoObstaculo.CONO)
    gestor.agregar_obstaculo(200, 2, TipoObstaculo.HUECO)

    carrito = gestor.carrito

    # Obtener datos para renderizado
    datos_renderizado = {
        "carrito": {
            "posicion": (carrito.x, carrito.y),
            "estado": carrito.estado.value,
            "energia_porcentaje": carrito.obtener_porcentaje_energia(),
            "sprite": carrito.obtener_sprite_nombre(),
            "color": carrito.color_actual,
        },
        "obstaculos_visibles": [],
        "estadisticas": gestor.obtener_estadisticas(),
        "estado_juego": gestor.estado_actual.value,
    }

    # Actualizar obstáculos visibles
    gestor.actualizar_obstaculos_visibles()

    # Agregar obstáculos visibles a datos de renderizado
    for obstaculo in gestor.obstaculos_visibles:
        datos_renderizado["obstaculos_visibles"].append(
            {
                "posicion": (obstaculo.x, obstaculo.y),
                "tipo": obstaculo.tipo.value,
                "sprite": obstaculo.obtener_sprite_nombre(),
                "rectangulo_colision": obstaculo.obtener_rectangulo_colision(),
            }
        )

    # Verificar que todos los datos están disponibles
    assert "carrito" in datos_renderizado, "Debe incluir datos del carrito"
    assert "obstaculos_visibles" in datos_renderizado, (
        "Debe incluir obstáculos visibles"
    )
    assert "estadisticas" in datos_renderizado, "Debe incluir estadísticas"
    assert "estado_juego" in datos_renderizado, "Debe incluir estado del juego"

    # Verificar datos del carrito
    carrito_data = datos_renderizado["carrito"]
    assert "posicion" in carrito_data, "Debe incluir posición del carrito"
    assert "estado" in carrito_data, "Debe incluir estado del carrito"
    assert "energia_porcentaje" in carrito_data, "Debe incluir energía del carrito"
    assert "sprite" in carrito_data, "Debe incluir sprite del carrito"
    assert "color" in carrito_data, "Debe incluir color del carrito"

    # Verificar datos de obstáculos
    for obstaculo_data in datos_renderizado["obstaculos_visibles"]:
        assert "posicion" in obstaculo_data, "Debe incluir posición del obstáculo"
        assert "tipo" in obstaculo_data, "Debe incluir tipo del obstáculo"
        assert "sprite" in obstaculo_data, "Debe incluir sprite del obstáculo"
        assert "rectangulo_colision" in obstaculo_data, (
            "Debe incluir rectángulo de colisión"
        )

    print("✅ Datos necesarios para renderizado: PASÓ")


def test_colisiones_tiempo_real():
    """Prueba: Detección de colisiones en tiempo real"""
    print("🧪 Probando detección de colisiones en tiempo real...")

    gestor = GestorJuego()
    gestor.inicializar_juego()

    # Crear obstáculos estratégicos
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)
    gestor.agregar_obstaculo(150, 0, TipoObstaculo.CONO)
    gestor.agregar_obstaculo(200, 2, TipoObstaculo.HUECO)

    carrito = gestor.carrito

    # Simular movimiento y detección de colisiones
    colisiones_detectadas = []

    for paso in range(50):
        # Mover carrito
        carrito.mover_automaticamente()

        # Actualizar obstáculos visibles
        gestor.actualizar_obstaculos_visibles()

        # Detectar colisiones
        colisiones = gestor.verificar_colisiones()

        if colisiones:
            colisiones_detectadas.extend(colisiones)

            # Procesar colisiones
            for colision in colisiones:
                gestor.procesar_colision(colision)

        # Verificar que el carrito sigue funcionando
        assert carrito.esta_vivo() or carrito.energia_actual <= 0, (
            "Carrito debe estar vivo o haber muerto correctamente"
        )

    # Verificar que se detectaron colisiones
    assert len(colisiones_detectadas) > 0, "Debe haber detectado colisiones"

    # Verificar que el carrito perdió energía
    assert carrito.energia_actual < 100, "Carrito debe haber perdido energía"

    print("✅ Detección de colisiones en tiempo real: PASÓ")


def main():
    """Ejecuta todas las pruebas de interfaz gráfica"""
    print("🚀 Iniciando pruebas de interfaz gráfica...\n")
    print("=" * 60)

    try:
        test_visualizacion_arbol_avl()
        print()

        test_actualizacion_tiempo_real()
        print()

        test_controles_usuario()
        print()

        test_administracion_obstaculos_interfaz()
        print()

        test_carga_guardado_configuracion()
        print()

        test_estados_juego_interfaz()
        print()

        test_datos_renderizado()
        print()

        test_colisiones_tiempo_real()
        print()

        print("=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS DE INTERFAZ GRÁFICA PASARON!")
        print("✅ El sistema está listo para integración con interfaz gráfica")
        print("🚀 Todas las funcionalidades necesarias están validadas")

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
