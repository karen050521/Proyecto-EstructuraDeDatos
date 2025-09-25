"""
Pruebas básicas - Validación de funcionalidad fundamental
Desde lo más simple hasta lo más complejo según definicion.md
"""

import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.obstaculo import Obstaculo, TipoObstaculo
from logic.nodo_avl import NodoAVL
from logic.arbol_avl import ArbolAVL
from logic.carrito import Carrito, EstadoCarrito
from logic.gestor_juego import GestorJuego, EstadoJuego


def test_creacion_obstaculos():
    """Prueba básica: Crear obstáculos de diferentes tipos"""
    print("🧪 Probando creación de obstáculos...")

    # Crear obstáculos de todos los tipos
    tipos_obstaculos = [
        (TipoObstaculo.ROCA, 20),
        (TipoObstaculo.CONO, 10),
        (TipoObstaculo.HUECO, 15),
        (TipoObstaculo.ACEITE, 5),
        (TipoObstaculo.BARRERA, 25),
    ]

    for tipo, daño_esperado in tipos_obstaculos:
        obstaculo = Obstaculo(100, 1, tipo)
        assert obstaculo.tipo == tipo, f"Tipo debe ser {tipo}"
        assert obstaculo.obtener_daño() == daño_esperado, (
            f"Daño debe ser {daño_esperado} para {tipo}"
        )
        assert obstaculo.x == 100, "Coordenada X debe ser 100"
        assert obstaculo.y == 1, "Coordenada Y debe ser 1"

    print("✅ Creación de obstáculos: PASÓ")


def test_creacion_carrito():
    """Prueba básica: Crear carrito con estado inicial"""
    print("🧪 Probando creación de carrito...")

    carrito = Carrito(x_inicial=50, y_inicial=1, energia_maxima=100)

    # Verificar estado inicial
    assert carrito.x == 50, "Posición X inicial debe ser 50"
    assert carrito.y == 1, "Posición Y inicial debe ser 1"
    assert carrito.energia_actual == 100, "Energía inicial debe ser 100"
    assert carrito.energia_maxima == 100, "Energía máxima debe ser 100"
    assert carrito.estado == EstadoCarrito.NORMAL, "Estado inicial debe ser NORMAL"
    assert carrito.esta_vivo() == True, "Carrito debe estar vivo inicialmente"
    assert carrito.obtener_porcentaje_energia() == 1.0, (
        "Porcentaje de energía debe ser 100%"
    )

    print("✅ Creación de carrito: PASÓ")


def test_movimiento_carrito():
    """Prueba básica: Movimiento del carrito"""
    print("🧪 Probando movimiento del carrito...")

    carrito = Carrito(x_inicial=50, y_inicial=1)

    # Movimiento automático en X
    posicion_inicial_x = carrito.x
    carrito.mover_automaticamente()
    assert carrito.x == posicion_inicial_x + 5, "Debe avanzar 5 metros en X"

    # Movimiento manual en Y
    carrito.mover_arriba()
    assert carrito.y == 2, "Debe moverse al carril superior"

    carrito.mover_abajo()
    assert carrito.y == 1, "Debe volver al carril medio"

    carrito.mover_abajo()
    assert carrito.y == 0, "Debe moverse al carril inferior"

    # No debe moverse fuera de los límites
    carrito.mover_abajo()
    assert carrito.y == 0, "No debe moverse fuera del límite inferior"

    carrito.mover_arriba()
    carrito.mover_arriba()
    carrito.mover_arriba()
    assert carrito.y == 2, "No debe moverse fuera del límite superior"

    print("✅ Movimiento del carrito: PASÓ")


def test_salto_carrito():
    """Prueba básica: Sistema de salto del carrito"""
    print("🧪 Probando sistema de salto del carrito...")

    carrito = Carrito()

    # Iniciar salto
    carrito.saltar()
    assert carrito.estado == EstadoCarrito.SALTANDO, "Debe estar en estado SALTANDO"
    assert carrito.esta_saltando() == True, "Debe detectar que está saltando"
    assert carrito.color_actual == carrito.color_saltando, "Debe cambiar de color"

    # Simular frames del salto
    for frame in range(25):  # Más que la duración del salto
        carrito.actualizar_salto()
        if frame < 10:  # Durante la subida
            assert carrito.velocidad_y > 0, (
                f"Velocidad Y debe ser positiva durante subida (frame {frame})"
            )
        elif frame > 15:  # Durante la bajada
            assert carrito.velocidad_y <= 0, (
                f"Velocidad Y debe ser negativa durante bajada (frame {frame})"
            )

    # Verificar que terminó el salto
    assert carrito.estado == EstadoCarrito.NORMAL, "Debe volver al estado NORMAL"
    assert carrito.esta_saltando() == False, "No debe estar saltando"
    assert carrito.color_actual == carrito.color_normal, "Debe volver al color normal"
    assert carrito.velocidad_y == 0, "Velocidad Y debe ser 0 al finalizar"

    print("✅ Sistema de salto del carrito: PASÓ")


def test_daño_carrito():
    """Prueba básica: Sistema de daño del carrito"""
    print("🧪 Probando sistema de daño del carrito...")

    carrito = Carrito(energia_maxima=100)

    # Aplicar daño
    carrito.recibir_daño(30)
    assert carrito.energia_actual == 70, (
        "Debe tener 70 de energía después de 30 de daño"
    )
    assert carrito.esta_vivo() == True, "Debe seguir vivo con 70 de energía"
    assert carrito.obtener_porcentaje_energia() == 0.7, "Debe tener 70% de energía"

    # Aplicar más daño
    carrito.recibir_daño(50)
    assert carrito.energia_actual == 20, "Debe tener 20 de energía"
    assert carrito.esta_vivo() == True, "Debe seguir vivo con 20 de energía"

    # Aplicar daño fatal
    carrito.recibir_daño(25)
    assert carrito.energia_actual == 0, "Debe tener 0 de energía"
    assert carrito.esta_vivo() == False, "No debe estar vivo con 0 de energía"
    assert carrito.obtener_porcentaje_energia() == 0.0, "Debe tener 0% de energía"

    print("✅ Sistema de daño del carrito: PASÓ")


def test_deteccion_colisiones():
    """Prueba básica: Detección de colisiones"""
    print("🧪 Probando detección de colisiones...")

    carrito = Carrito(x_inicial=100, y_inicial=1)
    obstaculo = Obstaculo(100, 1, TipoObstaculo.ROCA)

    # Colisión directa
    assert carrito.colisiona_con(obstaculo) == True, "Debe detectar colisión directa"

    # Sin colisión - diferente X
    obstaculo.x = 150
    assert carrito.colisiona_con(obstaculo) == False, (
        "No debe detectar colisión con diferente X"
    )

    # Sin colisión - diferente Y (más separado)
    obstaculo.x = 100
    obstaculo.y = 50  # Muy separado en Y
    assert carrito.colisiona_con(obstaculo) == False, (
        "No debe detectar colisión con diferente Y"
    )

    # Colisión parcial
    obstaculo.x = 120  # Se superpone parcialmente
    obstaculo.y = 1
    assert carrito.colisiona_con(obstaculo) == True, "Debe detectar colisión parcial"

    print("✅ Detección de colisiones: PASÓ")


def test_creacion_arbol_vacio():
    """Prueba básica: Crear árbol AVL vacío"""
    print("🧪 Probando creación de árbol AVL vacío...")

    arbol = ArbolAVL()

    assert arbol.esta_vacio() == True, "Árbol debe estar vacío inicialmente"
    assert arbol.obtener_total_obstaculos() == 0, "Debe tener 0 obstáculos"
    assert arbol.raiz is None, "Raíz debe ser None"

    # Recorridos en árbol vacío
    assert arbol.recorrido_en_anchura() == [], (
        "Recorrido en anchura debe ser lista vacía"
    )
    assert arbol.recorrido_en_profundidad() == [], (
        "Recorrido en profundidad debe ser lista vacía"
    )
    assert arbol.buscar_en_rango(0, 100, 0, 2) == [], (
        "Búsqueda en rango debe ser lista vacía"
    )

    print("✅ Creación de árbol AVL vacío: PASÓ")


def test_insercion_simple():
    """Prueba básica: Inserción simple en árbol AVL"""
    print("🧪 Probando inserción simple en árbol AVL...")

    arbol = ArbolAVL()
    obstaculo = Obstaculo(100, 1, TipoObstaculo.ROCA)

    # Insertar primer obstáculo
    resultado = arbol.insertar(obstaculo)
    assert resultado == True, "Debe insertar obstáculo exitosamente"
    assert arbol.esta_vacio() == False, "Árbol no debe estar vacío"
    assert arbol.obtener_total_obstaculos() == 1, "Debe tener 1 obstáculo"
    assert arbol.raiz is not None, "Raíz no debe ser None"
    assert arbol.raiz.obstaculo == obstaculo, (
        "Raíz debe contener el obstáculo insertado"
    )

    # Intentar insertar duplicado
    obstaculo_duplicado = Obstaculo(100, 1, TipoObstaculo.CONO)
    resultado = arbol.insertar(obstaculo_duplicado)
    assert resultado == False, "No debe insertar obstáculo duplicado"
    assert arbol.obtener_total_obstaculos() == 1, "Debe seguir teniendo 1 obstáculo"

    print("✅ Inserción simple en árbol AVL: PASÓ")


def test_busqueda_simple():
    """Prueba básica: Búsqueda simple en árbol AVL"""
    print("🧪 Probando búsqueda simple en árbol AVL...")

    arbol = ArbolAVL()

    # Insertar varios obstáculos
    obstaculos = [
        Obstaculo(100, 1, TipoObstaculo.ROCA),
        Obstaculo(50, 2, TipoObstaculo.CONO),
        Obstaculo(150, 0, TipoObstaculo.HUECO),
    ]

    for obstaculo in obstaculos:
        arbol.insertar(obstaculo)

    # Búsqueda en rango que incluye todos
    resultado = arbol.buscar_en_rango(0, 200, 0, 2)
    assert len(resultado) == 3, "Debe encontrar 3 obstáculos en rango amplio"

    # Búsqueda en rango específico
    resultado = arbol.buscar_en_rango(90, 110, 0, 2)
    assert len(resultado) == 1, "Debe encontrar 1 obstáculo en rango específico"
    assert resultado[0].x == 100, "Debe encontrar el obstáculo en (100,1)"

    # Búsqueda en rango vacío
    resultado = arbol.buscar_en_rango(200, 300, 0, 2)
    assert len(resultado) == 0, "No debe encontrar obstáculos en rango vacío"

    print("✅ Búsqueda simple en árbol AVL: PASÓ")


def main():
    """Ejecuta todas las pruebas básicas"""
    print("🚀 Iniciando pruebas básicas...\n")
    print("=" * 50)

    try:
        test_creacion_obstaculos()
        print()

        test_creacion_carrito()
        print()

        test_movimiento_carrito()
        print()

        test_salto_carrito()
        print()

        test_daño_carrito()
        print()

        test_deteccion_colisiones()
        print()

        test_creacion_arbol_vacio()
        print()

        test_insercion_simple()
        print()

        test_busqueda_simple()
        print()

        print("=" * 50)
        print("🎉 ¡TODAS LAS PRUEBAS BÁSICAS PASARON!")
        print("✅ Funcionalidad fundamental validada")

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
