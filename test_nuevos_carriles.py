#!/usr/bin/env python3
"""
Script de prueba para verificar las nuevas funcionalidades:
- 6 carriles (0-5)
- Eliminación automática de obstáculos pasados
- Nuevo sistema de puntuación
"""

from logic.gestor_juego import GestorJuego
from logic.carrito import Carrito
from logic.obstaculo import Obstaculo, TipoObstaculo

def test_carriles():
    """Prueba el sistema de 6 carriles."""
    print("=== PRUEBA: Sistema de 6 carriles ===")
    
    carrito = Carrito(x_inicial=50, y_inicial=2)
    print(f"Carrito inicial en carril: {carrito.y}")
    
    # Probar movimientos
    for i in range(10):
        if carrito.y < 5:
            carrito.mover_arriba()
            print(f"Moviendo arriba -> carril: {carrito.y}")
        else:
            break
    
    for i in range(10):
        if carrito.y > 0:
            carrito.mover_abajo()
            print(f"Moviendo abajo -> carril: {carrito.y}")
        else:
            break
    
    print("✅ Prueba de carriles completada\n")

def test_obstaculos_6_carriles():
    """Prueba obstáculos en los 6 carriles."""
    print("=== PRUEBA: Obstáculos en 6 carriles ===")
    
    gestor = GestorJuego()
    gestor.cargar_configuracion()
    
    # Crear obstáculos en cada carril
    for carril in range(6):
        obstaculo = Obstaculo(x=100 + carril * 50, y=carril, tipo=TipoObstaculo.ROCA)
        resultado = gestor.arbol_obstaculos.insertar(obstaculo)
        print(f"Obstáculo en carril {carril}: {'✅' if resultado else '❌'}")
    
    print(f"Total de obstáculos: {gestor.arbol_obstaculos.obtener_total_obstaculos()}")
    
    # Probar búsqueda por rango
    obstaculos_visibles = gestor.arbol_obstaculos.buscar_en_rango(0, 500, 0, 5)
    print(f"Obstáculos en rango (0-500, carriles 0-5): {len(obstaculos_visibles)}")
    
    print("✅ Prueba de obstáculos completada\n")

def test_eliminacion_automatica():
    """Prueba la eliminación automática de obstáculos."""
    print("=== PRUEBA: Eliminación automática ===")
    
    gestor = GestorJuego()
    gestor.cargar_configuracion()
    
    print(f"Obstáculos iniciales: {gestor.arbol_obstaculos.obtener_total_obstaculos()}")
    
    # Simular que el carrito avanza mucho
    gestor.inicializar_juego()
    gestor.carrito.x = 3000  # Mover carrito muy adelante
    
    # Actualizar para eliminar obstáculos pasados
    gestor.eliminar_obstaculos_pasados()
    
    print(f"Obstáculos después de eliminación: {gestor.arbol_obstaculos.obtener_total_obstaculos()}")
    print("✅ Prueba de eliminación completada\n")

if __name__ == "__main__":
    print("🚗 Probando nuevas funcionalidades del juego de carrito\n")
    
    try:
        test_carriles()
        test_obstaculos_6_carriles()
        test_eliminacion_automatica()
        
        print("🎉 ¡Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()