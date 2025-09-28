#!/usr/bin/env python3
"""
Test script to verify that the AVL tree is properly reset when the game restarts.
"""

from logic.gestor_juego import GestorJuego, EstadoJuego
from logic.obstaculo import TipoObstaculo

def test_tree_reset_on_restart():
    """Test that the AVL tree is properly reset when the game restarts."""
    print("🧪 Testing AVL tree reset on game restart...")
    
    # Initialize game manager
    gestor = GestorJuego()
    gestor.cargar_configuracion()
    gestor.inicializar_juego()
    
    # Get initial obstacle count
    initial_count = gestor.arbol_obstaculos.obtener_total_obstaculos()
    print(f"✅ Initial obstacle count: {initial_count}")
    
    # Simulate game progress - remove some obstacles by simulating collision
    obstacles_before_removal = initial_count
    
    # Let's remove a few obstacles to simulate gameplay
    all_obstacles = gestor.arbol_obstaculos.recorrido_en_profundidad()
    obstacles_to_remove = all_obstacles[:3] if len(all_obstacles) >= 3 else all_obstacles[:1]
    
    for obstacle in obstacles_to_remove:
        gestor.arbol_obstaculos.eliminar(obstacle)
        
    remaining_count = gestor.arbol_obstaculos.obtener_total_obstaculos()
    print(f"✅ After removing obstacles: {remaining_count} (removed {obstacles_before_removal - remaining_count})")
    
    # Verify obstacles were actually removed
    assert remaining_count < initial_count, "Obstacles should have been removed"
    
    # Now restart the game
    print("🔄 Restarting game...")
    gestor.estado_actual = EstadoJuego.JUEGO_TERMINADO  # Simulate game over
    gestor.reiniciar_juego()
    
    # Check that tree is restored to original state
    final_count = gestor.arbol_obstaculos.obtener_total_obstaculos()
    print(f"✅ After restart: {final_count}")
    
    # Verify tree is restored
    assert final_count == initial_count, f"Tree should be restored to original state. Expected {initial_count}, got {final_count}"
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Game should be in JUGANDO state"
    assert gestor.distancia_recorrida == 0, "Distance should be reset"
    assert gestor.puntuacion == 0, "Score should be reset"
    assert gestor.tiempo_juego == 0, "Time should be reset"
    
    # Verify that we can still query the tree correctly
    obstacles_after_restart = gestor.arbol_obstaculos.recorrido_en_profundidad()
    assert len(obstacles_after_restart) == initial_count, "All original obstacles should be back"
    
    print("🎉 All AVL tree reset tests passed!")
    print(f"✅ Tree successfully restored from {remaining_count} to {final_count} obstacles")

def test_restart_multiple_times():
    """Test that multiple restarts work correctly."""
    print("🔄 Testing multiple restarts...")
    
    gestor = GestorJuego()
    gestor.cargar_configuracion()
    initial_count = gestor.arbol_obstaculos.obtener_total_obstaculos()
    
    for i in range(3):
        print(f"  Restart #{i+1}")
        gestor.inicializar_juego()
        
        # Remove some obstacles
        all_obstacles = gestor.arbol_obstaculos.recorrido_en_profundidad()
        if all_obstacles:
            gestor.arbol_obstaculos.eliminar(all_obstacles[0])
            
        # Restart
        gestor.estado_actual = EstadoJuego.JUEGO_TERMINADO
        gestor.reiniciar_juego()
        
        # Verify restoration
        current_count = gestor.arbol_obstaculos.obtener_total_obstaculos()
        assert current_count == initial_count, f"Restart #{i+1} failed: expected {initial_count}, got {current_count}"
        
    print("✅ Multiple restarts work correctly")

if __name__ == "__main__":
    test_tree_reset_on_restart()
    print()
    test_restart_multiple_times()
    print("\n🎉 All tests passed! Tree reset functionality works perfectly!")