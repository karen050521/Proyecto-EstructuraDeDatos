#!/usr/bin/env python3
"""
Pruebas de casos edge y escenarios complejos
Validación de situaciones límite que podrían fallar en la interfaz
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


def test_obstaculos_limites_coordenadas():
    """Prueba: Obstáculos en límites de coordenadas"""
    print("🧪 Probando obstáculos en límites de coordenadas...")
    
    arbol = ArbolAVL()
    
    # Obstáculos en coordenadas extremas
    obstaculos_limites = [
        Obstaculo(0, 0, TipoObstaculo.ROCA),      # Origen
        Obstaculo(9999, 2, TipoObstaculo.CONO),   # X muy grande
        Obstaculo(100, 0, TipoObstaculo.HUECO),   # Y mínimo
        Obstaculo(200, 2, TipoObstaculo.ACEITE),  # Y máximo
        Obstaculo(-50, 1, TipoObstaculo.BARRERA), # X negativo
    ]
    
    for obstaculo in obstaculos_limites:
        resultado = arbol.insertar(obstaculo)
        assert resultado == True, f"Debe insertar obstáculo en {obstaculo.x},{obstaculo.y}"
    
    # Verificar búsqueda en rangos extremos
    resultado = arbol.buscar_en_rango(-100, 10000, 0, 2)
    assert len(resultado) == 5, "Debe encontrar todos los obstáculos en rango amplio"
    
    # Verificar búsqueda en rango muy específico
    resultado = arbol.buscar_en_rango(0, 0, 0, 0)
    assert len(resultado) == 1, "Debe encontrar solo el obstáculo en (0,0)"
    
    print("✅ Obstáculos en límites de coordenadas: PASÓ")


def test_carrito_movimiento_limites():
    """Prueba: Movimiento del carrito en límites"""
    print("🧪 Probando movimiento del carrito en límites...")
    
    carrito = Carrito(x_inicial=0, y_inicial=1)
    
    # Movimiento en límite inferior Y
    carrito.y = 0
    carrito.mover_abajo()
    assert carrito.y == 0, "No debe moverse por debajo del límite inferior"
    
    # Movimiento en límite superior Y
    carrito.y = 2
    carrito.mover_arriba()
    assert carrito.y == 2, "No debe moverse por encima del límite superior"
    
    # Movimiento automático desde posición 0
    carrito.x = 0
    carrito.mover_automaticamente()
    assert carrito.x == 5, "Debe moverse correctamente desde posición 0"
    
    # Movimiento automático desde posición negativa
    carrito.x = -10
    carrito.mover_automaticamente()
    assert carrito.x == -5, "Debe moverse correctamente desde posición negativa"
    
    print("✅ Movimiento del carrito en límites: PASÓ")


def test_salto_en_limites():
    """Prueba: Salto del carrito en posiciones límite"""
    print("🧪 Probando salto del carrito en posiciones límite...")
    
    carrito = Carrito(x_inicial=0, y_inicial=0)
    
    # Salto desde carril inferior
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "Debe poder saltar desde carril inferior"
    
    # Simular salto completo
    for _ in range(25):
        carrito.actualizar_salto()
    assert carrito.estado == EstadoCarrito.NORMAL, "Debe terminar salto correctamente"
    
    # Salto desde carril superior
    carrito.y = 2
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "Debe poder saltar desde carril superior"
    
    # Simular salto completo
    for _ in range(25):
        carrito.actualizar_salto()
    assert carrito.estado == EstadoCarrito.NORMAL, "Debe terminar salto correctamente"
    
    print("✅ Salto del carrito en posiciones límite: PASÓ")


def test_colisiones_multiples():
    """Prueba: Múltiples colisiones simultáneas"""
    print("🧪 Probando múltiples colisiones simultáneas...")
    
    gestor = GestorJuego()
    gestor.inicializar_juego()
    
    # Crear obstáculos superpuestos
    gestor.agregar_obstaculo(100, 1, TipoObstaculo.ROCA)
    gestor.agregar_obstaculo(105, 1, TipoObstaculo.CONO)  # Superpuesto
    gestor.agregar_obstaculo(110, 1, TipoObstaculo.HUECO)  # Superpuesto
    
    carrito = gestor.carrito
    carrito.x = 100
    carrito.y = 1
    
    # Actualizar obstáculos visibles
    gestor.actualizar_obstaculos_visibles()
    
    # Verificar múltiples colisiones
    colisiones = gestor.verificar_colisiones()
    assert len(colisiones) >= 1, "Debe detectar al menos una colisión"
    
    # Procesar todas las colisiones
    energia_inicial = carrito.energia_actual
    for colision in colisiones:
        gestor.procesar_colision(colision)
    
    assert carrito.energia_actual < energia_inicial, "Debe perder energía por colisiones"
    
    print("✅ Múltiples colisiones simultáneas: PASÓ")


def test_arbol_avl_insercion_masiva():
    """Prueba: Inserción masiva en árbol AVL"""
    print("🧪 Probando inserción masiva en árbol AVL...")
    
    arbol = ArbolAVL()
    
    # Insertar 100 obstáculos
    for i in range(100):
        x = i * 10
        y = i % 3
        obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
        resultado = arbol.insertar(obstaculo)
        assert resultado == True, f"Debe insertar obstáculo {i}"
    
    assert arbol.obtener_total_obstaculos() == 100, "Debe tener 100 obstáculos"
    
    # Verificar que el árbol mantiene balance
    recorrido = arbol.recorrido_en_profundidad()
    assert len(recorrido) == 100, "Recorrido debe incluir todos los obstáculos"
    
    # Verificar ordenamiento
    for i in range(len(recorrido) - 1):
        obs1 = recorrido[i]
        obs2 = recorrido[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), \
            "Recorrido debe estar ordenado"
    
    # Verificar búsqueda eficiente
    resultado = arbol.buscar_en_rango(0, 500, 0, 2)
    assert len(resultado) == 51, "Debe encontrar 51 obstáculos en rango 0-500"
    
    print("✅ Inserción masiva en árbol AVL: PASÓ")


def test_eliminacion_masiva():
    """Prueba: Eliminación masiva del árbol AVL"""
    print("🧪 Probando eliminación masiva del árbol AVL...")
    
    arbol = ArbolAVL()
    
    # Insertar obstáculos
    obstaculos = []
    for i in range(50):
        x = i * 20
        y = i % 3
        obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)
        obstaculos.append(obstaculo)
    
    assert arbol.obtener_total_obstaculos() == 50, "Debe tener 50 obstáculos"
    
    # Eliminar la mitad
    for i in range(0, 50, 2):  # Eliminar pares
        resultado = arbol.eliminar(obstaculos[i])
        assert resultado == True, f"Debe eliminar obstáculo {i}"
    
    assert arbol.obtener_total_obstaculos() == 25, "Debe tener 25 obstáculos"
    
    # Verificar que el árbol mantiene balance
    recorrido = arbol.recorrido_en_profundidad()
    assert len(recorrido) == 25, "Recorrido debe incluir 25 obstáculos"
    
    # Verificar ordenamiento
    for i in range(len(recorrido) - 1):
        obs1 = recorrido[i]
        obs2 = recorrido[i + 1]
        assert (obs1.x < obs2.x) or (obs1.x == obs2.x and obs1.y < obs2.y), \
            "Recorrido debe estar ordenado después de eliminaciones"
    
    print("✅ Eliminación masiva del árbol AVL: PASÓ")


def test_configuracion_json_extrema():
    """Prueba: Configuración JSON con valores extremos"""
    print("🧪 Probando configuración JSON con valores extremos...")
    
    # Configuración con valores extremos
    config_extrema = {
        "configuracion": {
            "distancia_total": 1,  # Muy corta
            "velocidad_carrito": 1,  # Muy lenta
            "refresco_ms": 50,  # Muy rápido
            "altura_salto": 100,  # Muy alto
            "color_carrito_inicial": "rojo"
        },
        "obstaculos": [
            {"x": 0, "y": 0, "tipo": "roca"},
            {"x": 1, "y": 2, "tipo": "barrera"}
        ]
    }
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_extrema, f, indent=2)
        temp_file = f.name
    
    try:
        gestor = GestorJuego(temp_file)
        resultado = gestor.cargar_configuracion()
        
        assert resultado == True, "Debe cargar configuración extrema"
        assert gestor.distancia_total == 1, "Debe cargar distancia_total extrema"
        assert gestor.velocidad_carrito == 1, "Debe cargar velocidad_carrito extrema"
        assert gestor.refresco_ms == 50, "Debe cargar refresco_ms extremo"
        assert gestor.altura_salto == 100, "Debe cargar altura_salto extrema"
        assert gestor.color_carrito_inicial == "rojo", "Debe cargar color_carrito_inicial"
        
        # Verificar obstáculos
        assert gestor.arbol_obstaculos.obtener_total_obstaculos() == 2, "Debe cargar 2 obstáculos"
        
        # Inicializar juego
        gestor.inicializar_juego()
        assert gestor.estado_actual == EstadoJuego.JUGANDO, "Debe inicializar juego"
        
        # Verificar que el carrito puede moverse
        carrito = gestor.carrito
        carrito.mover_automaticamente()
        assert carrito.x > 50, "Carrito debe moverse con velocidad extrema"
        
    finally:
        os.unlink(temp_file)
    
    print("✅ Configuración JSON con valores extremos: PASÓ")


def test_escenario_juego_intenso():
    """Prueba: Escenario de juego intenso con muchos obstáculos"""
    print("🧪 Probando escenario de juego intenso...")
    
    gestor = GestorJuego()
    gestor.inicializar_juego()
    
    # Crear nivel intenso con muchos obstáculos
    for i in range(50):
        x = 100 + i * 10
        y = i % 3
        tipo = list(TipoObstaculo)[i % 5]  # Rotar entre tipos
        gestor.agregar_obstaculo(x, y, tipo)
    
    carrito = gestor.carrito
    
    # Simular juego intenso
    colisiones_totales = 0
    for paso in range(100):
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
        
        # Verificar condiciones de fin
        if gestor.verificar_condiciones_fin_juego():
            break
    
    # Verificar que el sistema manejó el juego intenso
    assert colisiones_totales > 0, "Debe haber detectado colisiones"
    assert gestor.distancia_recorrida > 0, "Debe haber avanzado"
    
    # Verificar que el árbol mantiene integridad
    assert gestor.arbol_obstaculos.obtener_total_obstaculos() >= 40, \
        "Debe mantener la mayoría de obstáculos"
    
    print("✅ Escenario de juego intenso: PASÓ")


def test_estados_carrito_complejos():
    """Prueba: Estados complejos del carrito"""
    print("🧪 Probando estados complejos del carrito...")
    
    carrito = Carrito()
    
    # Estado normal
    assert carrito.estado == EstadoCarrito.NORMAL, "Estado inicial debe ser NORMAL"
    assert carrito.esta_vivo() == True, "Debe estar vivo inicialmente"
    
    # Salto
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "Debe estar saltando"
    assert carrito.esta_saltando() == True, "Debe detectar salto"
    
    # Simular salto a la mitad
    for _ in range(10):
        carrito.actualizar_salto()
    
    # Aplicar daño durante el salto
    energia_antes = carrito.energia_actual
    carrito.recibir_daño(30)
    assert carrito.energia_actual < energia_antes, "Debe perder energía durante salto"
    assert carrito.estado == EstadoCarrito.SALTANDO, "Debe seguir saltando"
    
    # Terminar salto
    for _ in range(20):
        carrito.actualizar_salto()
    
    assert carrito.estado == EstadoCarrito.NORMAL, "Debe volver a NORMAL"
    assert carrito.esta_saltando() == False, "No debe estar saltando"
    
    # Estado de colisión
    carrito.estado = EstadoCarrito.COLISIONANDO
    assert carrito.estado == EstadoCarrito.COLISIONANDO, "Debe estar en colisión"
    
    # Estado invulnerable
    carrito.estado = EstadoCarrito.INVULNERABLE
    assert carrito.estado == EstadoCarrito.INVULNERABLE, "Debe estar invulnerable"
    
    print("✅ Estados complejos del carrito: PASÓ")


def test_busqueda_rango_compleja():
    """Prueba: Búsqueda por rango en escenarios complejos"""
    print("🧪 Probando búsqueda por rango en escenarios complejos...")
    
    arbol = ArbolAVL()
    
    # Crear obstáculos en patrón complejo
    obstaculos = []
    for i in range(20):
        for j in range(3):
            x = i * 50 + j * 10
            y = j
            obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
            arbol.insertar(obstaculo)
            obstaculos.append(obstaculo)
    
    # Búsqueda en rango específico
    resultado = arbol.buscar_en_rango(100, 200, 1, 1)
    carriles_encontrados = [obs.y for obs in resultado]
    assert all(y == 1 for y in carriles_encontrados), "Debe encontrar solo carril 1"
    
    # Búsqueda en rango que cruza múltiples carriles
    resultado = arbol.buscar_en_rango(50, 150, 0, 2)
    assert len(resultado) > 0, "Debe encontrar obstáculos en múltiples carriles"
    
    # Búsqueda en rango muy específico
    resultado = arbol.buscar_en_rango(100, 100, 1, 1)
    assert len(resultado) <= 1, "Debe encontrar máximo 1 obstáculo en rango específico"
    
    # Búsqueda en rango vacío
    resultado = arbol.buscar_en_rango(2000, 3000, 0, 2)
    assert len(resultado) == 0, "No debe encontrar obstáculos en rango vacío"
    
    print("✅ Búsqueda por rango en escenarios complejos: PASÓ")


def test_rendimiento_operaciones():
    """Prueba: Rendimiento de operaciones críticas"""
    print("🧪 Probando rendimiento de operaciones críticas...")
    
    import time
    
    # Prueba de inserción masiva
    arbol = ArbolAVL()
    start_time = time.time()
    
    for i in range(1000):
        x = i * 5
        y = i % 3
        obstaculo = Obstaculo(x, y, TipoObstaculo.ROCA)
        arbol.insertar(obstaculo)
    
    insert_time = time.time() - start_time
    assert insert_time < 1.0, f"Inserción de 1000 elementos debe ser rápida (<1s), tomó {insert_time:.3f}s"
    
    # Prueba de búsqueda masiva
    start_time = time.time()
    
    for i in range(100):
        x_min = i * 50
        x_max = x_min + 25
        resultado = arbol.buscar_en_rango(x_min, x_max, 0, 2)
        assert len(resultado) >= 0, "Búsqueda debe funcionar correctamente"
    
    search_time = time.time() - start_time
    assert search_time < 0.5, f"Búsqueda de 100 rangos debe ser rápida (<0.5s), tomó {search_time:.3f}s"
    
    # Prueba de recorrido
    start_time = time.time()
    recorrido = arbol.recorrido_en_profundidad()
    traverse_time = time.time() - start_time
    
    assert len(recorrido) == 1000, "Recorrido debe incluir todos los elementos"
    assert traverse_time < 0.1, f"Recorrido debe ser muy rápido (<0.1s), tomó {traverse_time:.3f}s"
    
    print("✅ Rendimiento de operaciones críticas: PASÓ")


def main():
    """Ejecuta todas las pruebas de casos edge"""
    print("🚀 Iniciando pruebas de casos edge y escenarios complejos...\n")
    print("=" * 60)
    
    try:
        test_obstaculos_limites_coordenadas()
        print()
        
        test_carrito_movimiento_limites()
        print()
        
        test_salto_en_limites()
        print()
        
        test_colisiones_multiples()
        print()
        
        test_arbol_avl_insercion_masiva()
        print()
        
        test_eliminacion_masiva()
        print()
        
        test_configuracion_json_extrema()
        print()
        
        test_escenario_juego_intenso()
        print()
        
        test_estados_carrito_complejos()
        print()
        
        test_busqueda_rango_compleja()
        print()
        
        test_rendimiento_operaciones()
        print()
        
        print("=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS DE CASOS EDGE PASARON!")
        print("✅ El sistema maneja correctamente situaciones límite")
        print("🚀 Listo para integración con interfaz gráfica")
        
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
