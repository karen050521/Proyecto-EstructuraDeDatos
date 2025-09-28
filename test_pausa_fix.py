#!/usr/bin/env python3
"""
Test script to verify that the pause/unpause functionality is working correctly.
"""

from logic.gestor_juego import GestorJuego, EstadoJuego

def test_pause_unpause():
    """Test that the pause/unpause mechanism works correctly."""
    print("🧪 Testing pause/unpause functionality...")
    
    # Initialize game
    gestor = GestorJuego()
    gestor.inicializar_juego()
    
    # Verify initial state
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Game should start in JUGANDO state"
    print("✅ Initial state: JUGANDO")
    
    # Test pause
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.PAUSADO, "Game should be PAUSADO after first pause call"
    print("✅ After pause: PAUSADO")
    
    # Test unpause
    gestor.pausar_juego()
    assert gestor.estado_actual == EstadoJuego.JUGANDO, "Game should return to JUGANDO after second pause call"
    print("✅ After unpause: JUGANDO")
    
    # Test multiple pauses
    for i in range(5):
        current_state = gestor.estado_actual
        gestor.pausar_juego()
        expected_state = EstadoJuego.PAUSADO if current_state == EstadoJuego.JUGANDO else EstadoJuego.JUGANDO
        assert gestor.estado_actual == expected_state, f"State toggle failed on iteration {i}"
    
    print("✅ Multiple pause/unpause cycles work correctly")
    
    print("🎉 All pause/unpause tests passed!")

if __name__ == "__main__":
    test_pause_unpause()