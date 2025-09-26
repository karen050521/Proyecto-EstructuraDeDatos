"""
Punto de entrada alternativo que inicia el juego directamente sin pasar por configuración.
Ejecutar con: python -m pgzero jugar_directo.py
"""

import pygame
import pgzero
from pgzero.constants import keys
from logic.gestor_juego import GestorJuego, EstadoJuego
from view.pantalla_juego import PantallaJuego

# Configuración de pygame-zero
WIDTH = 800
HEIGHT = 600
TITLE = "Carrito con Obstaculos Dinamicos - Modo Directo"

# Centrar la ventana
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Instancias globales para pygame-zero
gestor_juego = None
pantalla_juego = None


def inicializar_juego():
    """
    Inicializa todos los componentes del juego y comienza directamente.
    """
    global gestor_juego, pantalla_juego

    # Crear el gestor principal
    gestor_juego = GestorJuego()
    gestor_juego.cargar_configuracion()
    
    # Crear la pantalla de juego
    pantalla_juego = PantallaJuego(WIDTH, HEIGHT)
    pantalla_juego.gestor_juego = gestor_juego

    # Inicializar juego directamente
    gestor_juego.inicializar_juego()
    gestor_juego.cambiar_estado(EstadoJuego.JUGANDO)

    print("Juego inicializado en modo directo")
    print("¡Comienza a jugar!")


def draw():
    """
    Función de dibujo principal llamada por pygame-zero.
    """
    if gestor_juego is None:
        inicializar_juego()
        return

    # Limpiar pantalla
    screen.fill((50, 50, 100))  # Azul oscuro

    # Dibujar pantalla de juego
    if gestor_juego.estado_actual in [EstadoJuego.JUGANDO, EstadoJuego.PAUSADO, EstadoJuego.JUEGO_TERMINADO]:
        pantalla_juego.dibujar(screen)
        
        # Dibujar overlay de pausa si está pausado
        if gestor_juego.estado_actual == EstadoJuego.PAUSADO:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))  # Negro semitransparente
            screen.blit(s, (0, 0))
            screen.draw.text(
                "PAUSA",
                (WIDTH // 2 - 50, HEIGHT // 2 - 30),
                fontsize=40,
                color="white"
            )
            
        # Dibujar overlay de fin de juego
        if gestor_juego.estado_actual == EstadoJuego.JUEGO_TERMINADO:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))  # Negro más oscuro semitransparente
            screen.blit(s, (0, 0))
            screen.draw.text(
                "FIN DEL JUEGO",
                (WIDTH // 2 - 100, HEIGHT // 2 - 50),
                fontsize=40,
                color="white"
            )
            
            # Mostrar puntuación final
            stats = gestor_juego.obtener_estadisticas()
            screen.draw.text(
                f"Puntuación final: {stats['puntuacion']}",
                (WIDTH // 2 - 90, HEIGHT // 2),
                fontsize=24,
                color="white"
            )
            screen.draw.text(
                f"Distancia recorrida: {stats['distancia_recorrida']} / {stats['distancia_total']}",
                (WIDTH // 2 - 150, HEIGHT // 2 + 40),
                fontsize=24,
                color="white"
            )
            screen.draw.text(
                "Presiona ESC para volver",
                (WIDTH // 2 - 120, HEIGHT // 2 + 100),
                fontsize=20,
                color="yellow"
            )

    # Dibujar información de debug
    screen.draw.text(
        f"Estado: {gestor_juego.estado_actual.value}",
        (10, 10),
        fontsize=20,
        color="white",
    )


def update(dt):
    """
    Función de actualización llamada por pygame-zero.

    Args:
        dt (float): Delta time desde el último frame
    """
    if gestor_juego is None:
        return

    # Actualizar el gestor principal
    gestor_juego.actualizar(dt)


def on_key_down(key):
    """
    Maneja las teclas presionadas.

    Args:
        key: Tecla presionada
    """
    if gestor_juego is None:
        return

    # Controles globales
    if key == keys.ESCAPE:
        if gestor_juego.estado_actual == EstadoJuego.JUGANDO:
            gestor_juego.pausar_juego()
        elif gestor_juego.estado_actual == EstadoJuego.PAUSADO:
            gestor_juego.pausar_juego()  # Despausa
        elif gestor_juego.estado_actual == EstadoJuego.JUEGO_TERMINADO:
            # En modo directo, reiniciar el juego
            inicializar_juego()
            
    # Controles del juego (corregidos para no estar invertidos)
    if gestor_juego.estado_actual == EstadoJuego.JUGANDO:
        if key == keys.UP:
            gestor_juego.carrito.mover_abajo()
        elif key == keys.DOWN:
            gestor_juego.carrito.mover_arriba()
        elif key == keys.SPACE:
            gestor_juego.carrito.saltar()
        elif key == keys.P:
            gestor_juego.pausar_juego()
        elif key == keys.T:
            pantalla_juego.mostrar_arbol = not pantalla_juego.mostrar_arbol
        elif key == keys.H:  # Mostrar/ocultar hitboxes
            pantalla_juego.mostrar_hitbox = not pantalla_juego.mostrar_hitbox
        elif key == keys.B:  # Mostrar recorrido en anchura
            if pantalla_juego.visualizador_arbol and pantalla_juego.mostrar_arbol:
                pantalla_juego.visualizador_arbol.iniciar_recorrido_anchura(gestor_juego.arbol_obstaculos)
        elif key == keys.D:  # Mostrar recorrido en profundidad
            if pantalla_juego.visualizador_arbol and pantalla_juego.mostrar_arbol:
                pantalla_juego.visualizador_arbol.iniciar_recorrido_profundidad(gestor_juego.arbol_obstaculos)


if __name__ == "__main__":
    # Si se ejecuta directamente este archivo sin pgzrun
    print("Iniciando Juego de Carrito en modo directo")
    print("Estructura de datos: Arbol AVL")
    print("Para ejecutar correctamente: uv run pgzrun jugar_directo.py")
    # Pygame Zero ejecutará las funciones draw(), update(), etc.