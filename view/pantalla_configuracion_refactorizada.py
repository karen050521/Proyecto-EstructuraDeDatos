"""
Pantalla de configuración del juego refactorizada.
Responsabilidad: Coordinar la interfaz de configuración usando componentes UI.
"""

import pygame
from typing import Optional, Tuple
from .visualizador_arbol import VisualizadorArbol
from .components import BotonModerno, CampoTexto, SelectorTipo


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
        self.gestor_juego = None

        # Áreas de la interfaz
        self.area_arbol = pygame.Rect(50, 100, 400, 400)
        self.area_controles = pygame.Rect(500, 100, 250, 400)

        # Visualizador del árbol
        self.visualizador = VisualizadorArbol(400, 400)

        # Componentes UI
        self._crear_componentes_ui()

    def _crear_componentes_ui(self):
        """Crea todos los componentes UI."""
        x = self.area_controles.x + 15
        y = self.area_controles.y + 20

        # Campos de texto
        self.campo_x = CampoTexto(
            x + 20, y + 60, 80, 28, "Posición X", self._validar_coordenada_x
        )

        self.campo_y = CampoTexto(
            x + 20, y + 110, 80, 28, "Carril Y (0-2)", self._validar_coordenada_y
        )

        # Selector de tipo
        tipos = ["roca", "cono", "hueco", "aceite", "barrera"]
        self.selector_tipo = SelectorTipo(x + 20, y + 160, 120, 28, tipos, "roca")

        # Botones
        self.boton_agregar = BotonModerno(
            "➕ AGREGAR", x, y + 220, 120, 35, (76, 175, 80), self._agregar_obstaculo
        )

        self.boton_anchura = BotonModerno(
            "🔍 RECORRIDO ANCHURA",
            x,
            y + 320,
            180,
            30,
            (33, 150, 243),
            self._mostrar_recorrido_anchura,
        )

        self.boton_profundidad = BotonModerno(
            "🔍 RECORRIDO PROFUNDIDAD",
            x,
            y + 360,
            180,
            30,
            (33, 150, 243),
            self._mostrar_recorrido_profundidad,
        )

        self.boton_iniciar = BotonModerno(
            "🚀 INICIAR JUEGO", x, y + 450, 150, 40, (255, 152, 0), self._iniciar_juego
        )

    def _validar_coordenada_x(self, texto: str) -> bool:
        """Valida la coordenada X."""
        try:
            x = int(texto)
            return x >= 0
        except ValueError:
            return False

    def _validar_coordenada_y(self, texto: str) -> bool:
        """Valida la coordenada Y."""
        try:
            y = int(texto)
            return 0 <= y <= 2
        except ValueError:
            return False

    def _agregar_obstaculo(self):
        """Agrega un obstáculo al árbol."""
        if not self.gestor_juego:
            print("Error: No hay gestor de juego")
            return

        if not self.campo_x.valido or not self.campo_y.valido:
            print("Error: Campos inválidos")
            return

        try:
            x = int(self.campo_x.obtener_texto())
            y = int(self.campo_y.obtener_texto())
            tipo_str = self.selector_tipo.obtener_opcion_actual()

            from logic.obstaculo import TipoObstaculo

            tipo = TipoObstaculo(tipo_str)

            if self.gestor_juego.agregar_obstaculo(x, y, tipo):
                print(f"Obstáculo agregado: ({x}, {y}) tipo {tipo_str}")
                self.campo_x.limpiar()
                self.campo_y.limpiar()
            else:
                print(f"Error: Ya existe un obstáculo en ({x}, {y})")

        except Exception as e:
            print(f"Error al agregar obstáculo: {e}")

    def _mostrar_recorrido_anchura(self):
        """Muestra el recorrido en anchura."""
        if self.gestor_juego and not self.gestor_juego.arbol_obstaculos.esta_vacio():
            recorrido = self.gestor_juego.obtener_recorrido_anchura()
            self.visualizador.iniciar_animacion_recorrido(recorrido)
            print("Recorrido en anchura iniciado")

    def _mostrar_recorrido_profundidad(self):
        """Muestra el recorrido en profundidad."""
        if self.gestor_juego and not self.gestor_juego.arbol_obstaculos.esta_vacio():
            recorrido = self.gestor_juego.obtener_recorrido_profundidad()
            self.visualizador.iniciar_animacion_recorrido(recorrido)
            print("Recorrido en profundidad iniciado")

    def _iniciar_juego(self):
        """Inicia el juego."""
        print("Iniciando juego...")

    def dibujar(self, screen):
        """
        Dibuja toda la pantalla de configuración.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        self._dibujar_fondo(screen)
        self._dibujar_arbol(screen)
        self._dibujar_controles(screen)

    def _dibujar_fondo(self, screen):
        """Dibuja el fondo de la pantalla."""
        # Fondo principal
        screen.draw.filled_rect(pygame.Rect(0, 0, self.ancho, self.alto), (15, 20, 30))

        # Título principal
        titulo_rect = pygame.Rect(self.ancho // 2 - 220, 5, 440, 60)
        screen.draw.filled_rect(titulo_rect, (30, 40, 60))
        screen.draw.rect(titulo_rect, (80, 120, 180))

        screen.draw.text(
            "🎮 CONFIGURACIÓN DEL JUEGO",
            (self.ancho // 2 - 160, 20),
            fontsize=22,
            color=(255, 255, 255),
        )

        screen.draw.text(
            "🌳 Árbol AVL de Obstáculos",
            (self.ancho // 2 - 120, 40),
            fontsize=14,
            color=(200, 220, 255),
        )

        # Áreas
        self._dibujar_area_arbol(screen)
        self._dibujar_area_controles(screen)

    def _dibujar_area_arbol(self, screen):
        """Dibuja el área del árbol."""
        # Sombra
        sombra_rect = pygame.Rect(
            self.area_arbol.x + 4,
            self.area_arbol.y + 4,
            self.area_arbol.width,
            self.area_arbol.height,
        )
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 80))

        # Fondo
        screen.draw.filled_rect(self.area_arbol, (25, 30, 40))
        screen.draw.rect(self.area_arbol, (60, 80, 120))

        # Etiqueta
        label_rect = pygame.Rect(self.area_arbol.x + 5, self.area_arbol.y - 30, 150, 25)
        screen.draw.filled_rect(label_rect, (60, 60, 60))
        screen.draw.text(
            "🌳 Vista del Árbol AVL",
            (self.area_arbol.x + 10, self.area_arbol.y - 25),
            fontsize=14,
            color=(255, 255, 255),
        )

    def _dibujar_area_controles(self, screen):
        """Dibuja el área de controles."""
        # Sombra
        sombra_rect = pygame.Rect(
            self.area_controles.x + 4,
            self.area_controles.y + 4,
            self.area_controles.width,
            self.area_controles.height,
        )
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 80))

        # Fondo
        screen.draw.filled_rect(self.area_controles, (30, 35, 45))
        screen.draw.rect(self.area_controles, (70, 90, 130))

        # Etiqueta
        label_rect = pygame.Rect(
            self.area_controles.x + 5, self.area_controles.y - 30, 120, 25
        )
        screen.draw.filled_rect(label_rect, (60, 60, 60))
        screen.draw.text(
            "⚙️ Controles",
            (self.area_controles.x + 10, self.area_controles.y - 25),
            fontsize=14,
            color=(255, 255, 255),
        )

    def _dibujar_arbol(self, screen):
        """Dibuja la visualización del árbol."""
        if self.gestor_juego and self.gestor_juego.arbol_obstaculos:
            self.visualizador.dibujar_arbol(
                screen,
                self.gestor_juego.arbol_obstaculos,
                self.area_arbol.x,
                self.area_arbol.y,
            )

    def _dibujar_controles(self, screen):
        """Dibuja todos los controles."""
        x = self.area_controles.x + 15
        y = self.area_controles.y + 20

        # Títulos de sección
        self._dibujar_titulo_seccion(screen, "AGREGAR OBSTÁCULO", x, y)
        y += 40

        # Etiquetas
        screen.draw.text("Posición X:", (x, y), fontsize=11, color=(200, 200, 200))
        screen.draw.text(
            "Carril Y (0-2):", (x, y + 50), fontsize=11, color=(200, 200, 200)
        )
        screen.draw.text(
            "Tipo de obstáculo:", (x, y + 100), fontsize=11, color=(200, 200, 200)
        )

        # Componentes
        self.campo_x.dibujar(screen)
        self.campo_y.dibujar(screen)
        self.selector_tipo.dibujar(screen)
        self.boton_agregar.dibujar(screen)

        # Separador
        y += 120
        screen.draw.line((x, y), (x + 200, y), (100, 100, 100))
        y += 20

        # Recorridos
        self._dibujar_titulo_seccion(screen, "RECORRIDOS DEL ÁRBOL", x, y)
        y += 35

        self.boton_anchura.dibujar(screen)
        self.boton_profundidad.dibujar(screen)

        # Separador
        y += 80
        screen.draw.line((x, y), (x + 200, y), (100, 100, 100))
        y += 20

        # Iniciar juego
        self.boton_iniciar.dibujar(screen)

        # Información del árbol
        y += 60
        self._dibujar_info_arbol(screen, x, y)

    def _dibujar_titulo_seccion(self, screen, texto, x, y):
        """Dibuja un título de sección."""
        screen.draw.filled_rect(
            pygame.Rect(x - 5, y - 5, len(texto) * 8 + 10, 25), (45, 45, 45)
        )
        screen.draw.text(texto, (x, y), fontsize=12, color=(255, 255, 255))

    def _dibujar_info_arbol(self, screen, x, y):
        """Dibuja información sobre el árbol."""
        if self.gestor_juego and self.gestor_juego.arbol_obstaculos:
            total = self.gestor_juego.arbol_obstaculos.obtener_total_obstaculos()
            altura = self.gestor_juego.arbol_obstaculos.obtener_altura(
                self.gestor_juego.arbol_obstaculos.raiz
            )
            info_texto = f"Obstáculos: {total} | Altura: {altura}"
            screen.draw.text(info_texto, (x, y), fontsize=10, color=(150, 150, 150))
        else:
            screen.draw.text("Árbol vacío", (x, y), fontsize=10, color=(150, 150, 150))

    def manejar_clic_mouse(self, pos):
        """
        Maneja los clics del mouse.

        Args:
            pos (tuple): Posición del clic

        Returns:
            str: Acción a realizar o None
        """
        x, y = pos

        # Verificar clic en área del árbol
        if self.area_arbol.collidepoint(x, y):
            if self.gestor_juego and self.gestor_juego.arbol_obstaculos:
                nodo = self.visualizador.obtener_nodo_en_posicion(
                    self.gestor_juego.arbol_obstaculos,
                    x - self.area_arbol.x,
                    y - self.area_arbol.y,
                )
                if nodo:
                    self.visualizador.establecer_nodo_seleccionado(nodo)
                    return "seleccionar_nodo"

        # Verificar clic en controles
        if self.area_controles.collidepoint(x, y):
            return self._manejar_clic_controles(pos)

        return None

    def _manejar_clic_controles(self, pos):
        """Maneja clics en el área de controles."""
        # Componentes
        if self.campo_x.verificar_clic(pos):
            self.campo_x.activar()
            self.campo_y.desactivar()
            return None

        if self.campo_y.verificar_clic(pos):
            self.campo_y.activar()
            self.campo_x.desactivar()
            return None

        if self.selector_tipo.manejar_clic(pos):
            return None

        if self.boton_agregar.manejar_clic(pos):
            return None

        if self.boton_anchura.manejar_clic(pos):
            return None

        if self.boton_profundidad.manejar_clic(pos):
            return None

        if self.boton_iniciar.manejar_clic(pos):
            return "iniciar_juego"

        # Desactivar campos si se hace clic fuera
        self.campo_x.desactivar()
        self.campo_y.desactivar()

        return None

    def manejar_tecla(self, tecla):
        """
        Maneja las teclas presionadas.

        Args:
            tecla: Tecla presionada
        """
        # Manejar entrada de texto
        if self.campo_x.activo or self.campo_y.activo:
            campo_activo = self.campo_x if self.campo_x.activo else self.campo_y

            if tecla == "backspace":
                campo_activo.borrar_caracter()
            elif tecla == "return":
                if self.campo_x.activo:
                    self.campo_x.desactivar()
                    self.campo_y.activar()
                else:
                    self._agregar_obstaculo()
                    self.campo_x.desactivar()
                    self.campo_y.desactivar()
            elif tecla == "escape":
                self.campo_x.desactivar()
                self.campo_y.desactivar()
            else:
                if hasattr(tecla, "name") and tecla.name.isdigit():
                    campo_activo.agregar_caracter(tecla.name)

        # Teclas especiales
        if tecla == "enter":
            return "iniciar_juego"

        return None
