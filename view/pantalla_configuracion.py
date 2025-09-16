"""
Pantalla de configuración del juego donde se puede modificar el árbol AVL.
Responsabilidad: Interfaz para administrar obstáculos antes de iniciar el juego.
"""

import pygame
from pygame.locals import *
from typing import Optional, Tuple


class PantallaConfiguracion:
    """
    Pantalla que permite configurar el árbol de obstáculos antes de jugar.
    """

    def __init__(self, ancho=800, alto=600):
        """
        Inicializa la pantalla de configuración.

        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        self.gestor_juego = None  # Se asigna externamente

        # Áreas de la interfaz
        self.area_arbol = pygame.Rect(50, 100, 400, 400)
        self.area_controles = pygame.Rect(500, 100, 250, 400)

        # Estado de la interfaz
        self.obstaculo_seleccionado = None
        self.mostrando_recorrido = False
        self.tipo_recorrido_actual = None
        self.recorrido_actual = []

        # Controles de entrada
        self.campo_x = ""
        self.campo_y = ""
        self.tipo_seleccionado = "roca"
        self.campo_activo = None
        
        # Visualizador del árbol
        from .visualizador_arbol import VisualizadorArbol
        self.visualizador = VisualizadorArbol(400, 400)
        
        # Tipos de obstáculos disponibles
        self.tipos_obstaculos = ["roca", "cono", "hueco", "aceite", "barrera"]

    def dibujar(self, screen):
        """
        Dibuja toda la pantalla de configuración.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        self.dibujar_fondo(screen)
        self.dibujar_arbol(screen)
        self.dibujar_controles(screen)

    def dibujar_fondo(self, screen):
        """
        Dibuja el fondo y las divisiones de la pantalla.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        # Título
        screen.draw.text(
            "CONFIGURACION DEL JUEGO",
            (self.ancho // 2 - 150, 20),
            fontsize=24,
            color="white"
        )
        
        # Dibujar áreas
        screen.draw.rect(self.area_arbol, (100, 100, 100))
        screen.draw.rect(self.area_controles, (80, 80, 80))
        
        # Etiquetas de áreas
        screen.draw.text(
            "Vista del Arbol AVL",
            (self.area_arbol.x + 10, self.area_arbol.y - 25),
            fontsize=16,
            color="white"
        )
        
        screen.draw.text(
            "Controles",
            (self.area_controles.x + 10, self.area_controles.y - 25),
            fontsize=16,
            color="white"
        )

    def dibujar_arbol(self, screen):
        """
        Dibuja la visualización gráfica del árbol AVL.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        if self.gestor_juego and self.gestor_juego.arbol_obstaculos:
            self.visualizador.dibujar_arbol(
                screen, 
                self.gestor_juego.arbol_obstaculos,
                self.area_arbol.x,
                self.area_arbol.y
            )

    def dibujar_nodo(self, screen, nodo, x, y, nivel):
        """
        Dibuja un nodo individual del árbol.

        Args:
            screen: Superficie de pygame donde dibujar
            nodo: Nodo del árbol a dibujar
            x (int): Posición X del nodo
            y (int): Posición Y del nodo
            nivel (int): Nivel del nodo en el árbol
        """
        pass

    def dibujar_controles(self, screen):
        """
        Dibuja los controles de la interfaz (campos, botones).

        Args:
            screen: Superficie de pygame donde dibujar
        """
        x = self.area_controles.x + 10
        y = self.area_controles.y + 20
        
        # Título de controles
        screen.draw.text(
            "Agregar Obstaculo:",
            (x, y),
            fontsize=14,
            color="white"
        )
        y += 30
        
        # Campo X
        screen.draw.text("X:", (x, y), fontsize=12, color="white")
        self.dibujar_campo_texto(screen, self.campo_x, x + 30, y - 5, 60, self.campo_activo == "x")
        y += 30
        
        # Campo Y
        screen.draw.text("Y:", (x, y), fontsize=12, color="white")
        self.dibujar_campo_texto(screen, self.campo_y, x + 30, y - 5, 60, self.campo_activo == "y")
        y += 30
        
        # Tipo de obstáculo
        screen.draw.text("Tipo:", (x, y), fontsize=12, color="white")
        self.dibujar_boton(screen, self.tipo_seleccionado, x + 50, y - 5, 80, 20)
        y += 40
        
        # Botón agregar
        self.dibujar_boton(screen, "AGREGAR", x, y, 100, 30)
        y += 50
        
        # Botones de recorrido
        screen.draw.text("Recorridos:", (x, y), fontsize=14, color="white")
        y += 25
        
        self.dibujar_boton(screen, "RECORRIDO ANCHURA", x, y, 150, 25)
        y += 35
        
        self.dibujar_boton(screen, "RECORRIDO PROFUNDIDAD", x, y, 150, 25)
        y += 50
        
        # Botón iniciar juego
        self.dibujar_boton(screen, "INICIAR JUEGO", x, y, 120, 35)

    def dibujar_campo_texto(self, screen, texto, x, y, ancho, activo):
        """
        Dibuja un campo de texto.

        Args:
            screen: Superficie donde dibujar
            texto (str): Texto actual del campo
            x, y (int): Posición del campo
            ancho (int): Ancho del campo
            activo (bool): Si el campo está activo
        """
        color = (255, 255, 255) if activo else (200, 200, 200)
        screen.draw.rect(pygame.Rect(x, y, ancho, 20), color)
        screen.draw.text(texto, (x + 5, y + 2), fontsize=12, color="black")

    def dibujar_boton(self, screen, texto, x, y, ancho, alto, activo=True):
        """
        Dibuja un botón.

        Args:
            screen: Superficie donde dibujar
            texto (str): Texto del botón
            x, y (int): Posición del botón
            ancho, alto (int): Dimensiones del botón
            activo (bool): Si el botón está habilitado
        """
        color = (100, 150, 255) if activo else (100, 100, 100)
        screen.draw.filled_rect(pygame.Rect(x, y, ancho, alto), color)
        screen.draw.rect(pygame.Rect(x, y, ancho, alto), (255, 255, 255))
        
        # Centrar texto
        texto_x = x + (ancho - len(texto) * 6) // 2
        texto_y = y + (alto - 12) // 2
        screen.draw.text(texto, (texto_x, texto_y), fontsize=10, color="white")

    def dibujar_recorrido(self, screen):
        """
        Dibuja el recorrido actual si está activo.

        Args:
            screen: Superficie donde dibujar
        """
        pass

    def manejar_evento(self, evento):
        """
        Maneja los eventos de entrada del usuario.

        Args:
            evento: Evento de pygame

        Returns:
            str: Acción a realizar ('iniciar_juego', 'salir', None)
        """
        pass

    def manejar_clic_mouse(self, pos):
        """
        Maneja los clics del mouse en la interfaz.

        Args:
            pos (Tuple[int, int]): Posición del clic

        Returns:
            str: Acción a realizar o None
        """
        x, y = pos
        
        # Verificar clic en área del árbol
        if self.area_arbol.collidepoint(x, y):
            # Buscar nodo en esa posición
            nodo = self.visualizador.obtener_nodo_en_posicion(
                self.gestor_juego.arbol_obstaculos,
                x - self.area_arbol.x,
                y - self.area_arbol.y
            )
            if nodo:
                self.visualizador.establecer_nodo_seleccionado(nodo)
                return "seleccionar_nodo"
        
        # Verificar clic en controles
        if self.area_controles.collidepoint(x, y):
            return self._manejar_clic_controles(x, y)
        
        return None
    
    def _manejar_clic_controles(self, x, y):
        """Maneja clics en el área de controles."""
        # Coordenadas relativas al área de controles
        rel_x = x - self.area_controles.x
        rel_y = y - self.area_controles.y
        
        # Botón agregar (aproximado)
        if 10 <= rel_x <= 110 and 120 <= rel_y <= 150:
            return "agregar_obstaculo"
        
        # Botón recorrido anchura
        if 10 <= rel_x <= 160 and 200 <= rel_y <= 225:
            return "recorrido_anchura"
        
        # Botón recorrido profundidad
        if 10 <= rel_x <= 160 and 235 <= rel_y <= 260:
            return "recorrido_profundidad"
        
        # Botón iniciar juego
        if 10 <= rel_x <= 130 and 285 <= rel_y <= 320:
            return "iniciar_juego"
        
        # Campo X
        if 40 <= rel_x <= 100 and 45 <= rel_y <= 65:
            self.campo_activo = "x"
            return "activar_campo_x"
        
        # Campo Y
        if 40 <= rel_x <= 100 and 75 <= rel_y <= 95:
            self.campo_activo = "y"
            return "activar_campo_y"
        
        return None

    def manejar_tecla(self, tecla):
        """
        Maneja las teclas presionadas.

        Args:
            tecla: Tecla presionada (en pygame-zero es un objeto con propiedades)
        """
        # Usar strings directamente para las teclas en pygame-zero
        # Manejar entrada de texto en campos activos
        if self.campo_activo:
            if tecla == "backspace":
                if self.campo_activo == "x" and self.campo_x:
                    self.campo_x = self.campo_x[:-1]
                elif self.campo_activo == "y" and self.campo_y:
                    self.campo_y = self.campo_y[:-1]
            elif tecla == "return":
                if self.campo_activo == "x":
                    self.campo_activo = "y"
                elif self.campo_activo == "y":
                    self.agregar_obstaculo()
                    self.campo_activo = None
            elif tecla == "escape":
                self.campo_activo = None
            else:
                # Agregar dígito - en pygame-zero, las teclas numéricas son caracteres
                if hasattr(tecla, 'name') and tecla.name.isdigit():
                    if self.campo_activo == "x":
                        self.campo_x += tecla.name
                    elif self.campo_activo == "y":
                        self.campo_y += tecla.name
        
        # Teclas especiales
        if tecla == "enter":
            return "iniciar_juego"
        
        return None

    def agregar_obstaculo(self):
        """
        Intenta agregar un nuevo obstáculo con los datos ingresados.

        Returns:
            bool: True si se agregó correctamente
        """
        if not self.gestor_juego:
            return False
        
        # Validar entrada
        try:
            x = int(self.campo_x)
            y = int(self.campo_y)
        except ValueError:
            return False
        
        # Validar rango de Y (carriles 0-2)
        if y < 0 or y > 2:
            return False
        
        # Crear obstáculo
        from logic.obstaculo import TipoObstaculo
        tipo = TipoObstaculo(self.tipo_seleccionado)
        
        # Intentar agregar al árbol
        if self.gestor_juego.agregar_obstaculo(x, y, tipo):
            # Limpiar campos
            self.campo_x = ""
            self.campo_y = ""
            return True
        
        return False

    def eliminar_obstaculo_seleccionado(self):
        """
        Elimina el obstáculo actualmente seleccionado.

        Returns:
            bool: True si se eliminó correctamente
        """
        pass

    def mostrar_recorrido_anchura(self):
        """
        Activa la visualización del recorrido en anchura.
        """
        if self.gestor_juego:
            recorrido = self.gestor_juego.obtener_recorrido_anchura()
            self.visualizador.iniciar_animacion_recorrido(recorrido)
            self.mostrando_recorrido = True
            self.tipo_recorrido_actual = "anchura"

    def mostrar_recorrido_profundidad(self):
        """
        Activa la visualización del recorrido en profundidad.
        """
        if self.gestor_juego:
            recorrido = self.gestor_juego.obtener_recorrido_profundidad()
            self.visualizador.iniciar_animacion_recorrido(recorrido)
            self.mostrando_recorrido = True
            self.tipo_recorrido_actual = "profundidad"

    def limpiar_recorrido(self):
        """
        Limpia la visualización de recorridos.
        """
        self.visualizador.limpiar_seleccion()
        self.mostrando_recorrido = False
        self.tipo_recorrido_actual = None

    def validar_entrada_obstaculo(self, x, y):
        """
        Valida que las coordenadas ingresadas sean válidas.

        Args:
            x (str): Coordenada X como string
            y (str): Coordenada Y como string

        Returns:
            Tuple[bool, str]: (Es válido, mensaje de error)
        """
        pass

    def obtener_nodo_en_posicion(self, pos):
        """
        Obtiene el nodo del árbol que está en la posición especificada.

        Args:
            pos (Tuple[int, int]): Posición del mouse

        Returns:
            Optional: Nodo en esa posición o None
        """
        pass

    def calcular_posicion_nodo(self, nodo, nivel, indice_en_nivel):
        """
        Calcula la posición visual de un nodo en el árbol.

        Args:
            nodo: Nodo del árbol
            nivel (int): Nivel del nodo
            indice_en_nivel (int): Índice del nodo en su nivel

        Returns:
            Tuple[int, int]: Posición (x, y) del nodo
        """
        pass
