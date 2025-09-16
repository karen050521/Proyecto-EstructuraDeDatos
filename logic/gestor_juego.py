"""
Gestor principal del estado y lógica del juego.
Responsabilidad: Coordinar todos los componentes y manejar el ciclo de vida del juego.
"""

import json
from enum import Enum
from typing import List, Dict, Any, Optional
from .arbol_avl import ArbolAVL
from .carrito import Carrito, EstadoCarrito
from .obstaculo import Obstaculo, TipoObstaculo


class EstadoJuego(Enum):
    """Estados posibles del juego."""

    MENU_INICIAL = "menu_inicial"
    CONFIGURACION = "configuracion"
    JUGANDO = "jugando"
    PAUSADO = "pausado"
    JUEGO_TERMINADO = "juego_terminado"


class GestorJuego:
    """
    Controla el estado general del juego y coordina todos los componentes.
    """

    def __init__(self, archivo_configuracion: str = "data/configuracion.json") -> None:
        """
        Inicializa el gestor del juego.

        Args:
            archivo_configuracion (str): Ruta al archivo de configuración JSON
        """
        self.estado_actual: EstadoJuego = EstadoJuego.MENU_INICIAL
        self.arbol_obstaculos: ArbolAVL = ArbolAVL()
        self.carrito: Optional[Carrito] = None
        self.archivo_configuracion: str = archivo_configuracion

        # Configuración del juego
        self.distancia_total: int = 2000  # metros
        self.velocidad_carrito: int = 10  # metros por segundo
        self.refresco_ms: int = 200  # milisegundos entre frames
        self.altura_salto: int = 50  # píxeles
        self.color_carrito_inicial: str = "azul"

        # Estado del juego
        self.distancia_recorrida: int = 0
        self.obstaculos_visibles: List[Obstaculo] = []
        self.rango_vision: int = 150  # píxeles hacia adelante
        self.puntuacion: int = 0
        self.tiempo_juego: float = 0

    def cargar_configuracion(self) -> bool:
        """
        Carga la configuración inicial desde el archivo JSON.

        Returns:
            bool: True si se cargó correctamente
        """
        try:
            with open(self.archivo_configuracion, "r", encoding="utf-8") as archivo:
                config = json.load(archivo)

                # Cargar configuración del juego (soporta estructura anidada)
                configuracion = config.get(
                    "configuracion", config
                )  # Usar sección configuracion o el objeto completo
                self.distancia_total = configuracion.get("distancia_total", 2000)
                self.velocidad_carrito = configuracion.get("velocidad_carrito", 10)
                self.refresco_ms = configuracion.get("refresco_ms", 200)
                self.altura_salto = configuracion.get("altura_salto", 50)
                self.color_carrito_inicial = configuracion.get(
                    "color_carrito_inicial", "azul"
                )

                # Cargar obstáculos predefinidos
                obstaculos_config = config.get("obstaculos", [])
                for obs_data in obstaculos_config:
                    obstaculo = self._crear_obstaculo_desde_dict(obs_data)
                    self.arbol_obstaculos.insertar(obstaculo)

                return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error cargando configuración: {e}")
            return False

    def guardar_configuracion(self) -> bool:
        """
        Guarda la configuración actual en el archivo JSON.

        Returns:
            bool: True si se guardó correctamente
        """
        try:
            config = {
                "distancia_total": self.distancia_total,
                "velocidad_carrito": self.velocidad_carrito,
                "refresco_ms": self.refresco_ms,
                "altura_salto": self.altura_salto,
                "color_carrito_inicial": self.color_carrito_inicial,
                "obstaculos": [],
            }

            # Guardar obstáculos actuales
            obstaculos = self.arbol_obstaculos.recorrido_en_profundidad()
            for obstaculo in obstaculos:
                config["obstaculos"].append(
                    {
                        "x": obstaculo.x,
                        "y": obstaculo.y,
                        "tipo": obstaculo.tipo.value,
                        "ancho": obstaculo.ancho,
                        "alto": obstaculo.alto,
                    }
                )

            with open(self.archivo_configuracion, "w", encoding="utf-8") as archivo:
                json.dump(config, archivo, indent=2, ensure_ascii=False)

            return True
        except (IOError, json.JSONEncodeError) as e:
            print(f"Error guardando configuración: {e}")
            return False

    def inicializar_juego(self) -> None:
        """
        Inicializa todos los componentes necesarios para empezar a jugar.
        """
        # Crear carrito
        self.carrito = Carrito(x_inicial=50, y_inicial=1, energia_maxima=100)

        # Reiniciar estado del juego
        self.distancia_recorrida = 0
        self.obstaculos_visibles = []
        self.puntuacion = 0
        self.tiempo_juego = 0

        # Cambiar estado
        self.estado_actual = EstadoJuego.JUGANDO

    def cambiar_estado(self, nuevo_estado: EstadoJuego) -> None:
        """
        Cambia el estado actual del juego.

        Args:
            nuevo_estado (EstadoJuego): Nuevo estado a establecer
        """
        self.estado_actual = nuevo_estado

    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza la lógica del juego cada frame.

        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        if self.estado_actual != EstadoJuego.JUGANDO:
            return

        if self.carrito is None:
            return

        # Actualizar carrito
        self.carrito.actualizar(delta_tiempo)

        # Actualizar distancia recorrida
        self.distancia_recorrida = self.carrito.x - 50  # Posición inicial

        # Actualizar obstáculos visibles
        self.actualizar_obstaculos_visibles()

        # Verificar colisiones
        obstaculos_colisionados = self.verificar_colisiones()
        for obstaculo in obstaculos_colisionados:
            self.procesar_colision(obstaculo)

        # Verificar condiciones de fin de juego
        if self.verificar_condiciones_fin_juego():
            self.estado_actual = EstadoJuego.JUEGO_TERMINADO

        # Actualizar tiempo de juego
        self.tiempo_juego += delta_tiempo

    def actualizar_obstaculos_visibles(self) -> None:
        """
        Consulta el árbol AVL para obtener obstáculos en el rango de visión.
        Esta es la función clave que demuestra la eficiencia del árbol.
        """
        if self.carrito is None:
            return

        # Definir rango de visión basado en la posición del carrito
        x_actual = self.carrito.x
        x_min = x_actual
        x_max = x_actual + self.rango_vision
        y_min = 0  # Todos los carriles
        y_max = 2

        # Usar la búsqueda eficiente del árbol AVL
        self.obstaculos_visibles = self.arbol_obstaculos.buscar_en_rango(
            x_min, x_max, y_min, y_max
        )

    def verificar_colisiones(self) -> List[Obstaculo]:
        """
        Verifica colisiones entre el carrito y los obstáculos visibles.

        Returns:
            List[Obstaculo]: Lista de obstáculos con los que colisionó
        """
        if self.carrito is None:
            return []

        obstaculos_colisionados = []
        for obstaculo in self.obstaculos_visibles:
            if self.carrito.colisiona_con(obstaculo):
                obstaculos_colisionados.append(obstaculo)

        return obstaculos_colisionados

    def procesar_colision(self, obstaculo: Obstaculo) -> None:
        """
        Procesa una colisión entre el carrito y un obstáculo.

        Args:
            obstaculo (Obstaculo): Obstáculo que colisionó
        """
        if self.carrito is None:
            return

        # Aplicar daño al carrito
        daño = obstaculo.obtener_daño()
        self.carrito.recibir_daño(daño)

        # Cambiar estado del carrito
        self.carrito.estado = EstadoCarrito.COLISIONANDO

        # Actualizar puntuación (penalización por colisión)
        self.puntuacion = max(0, self.puntuacion - daño)

        # Remover obstáculo del árbol (opcional, dependiendo del tipo)
        if obstaculo.tipo in [TipoObstaculo.CONO, TipoObstaculo.ACEITE]:
            self.arbol_obstaculos.eliminar(obstaculo)

    def verificar_condiciones_fin_juego(self) -> bool:
        """
        Verifica si se cumplieron las condiciones para terminar el juego.

        Returns:
            bool: True si el juego debe terminar
        """
        if self.carrito is None:
            return True

        # El juego termina si:
        # 1. El carrito se queda sin energía
        if not self.carrito.esta_vivo():
            return True

        # 2. Se alcanza la distancia total
        if self.distancia_recorrida >= self.distancia_total:
            return True

        return False

    def agregar_obstaculo(self, x: int, y: int, tipo: TipoObstaculo) -> bool:
        """
        Agrega un nuevo obstáculo al árbol AVL.

        Args:
            x (int): Posición X
            y (int): Posición Y (carril)
            tipo (TipoObstaculo): Tipo de obstáculo

        Returns:
            bool: True si se agregó correctamente
        """
        obstaculo = Obstaculo(x, y, tipo)
        return self.arbol_obstaculos.insertar(obstaculo)

    def eliminar_obstaculo(self, x: int, y: int) -> bool:
        """
        Elimina un obstáculo del árbol AVL.

        Args:
            x (int): Posición X del obstáculo
            y (int): Posición Y del obstáculo

        Returns:
            bool: True si se eliminó correctamente
        """
        # Crear un obstáculo temporal para buscar y eliminar
        obstaculo_temp = Obstaculo(
            x, y, TipoObstaculo.ROCA
        )  # Tipo no importa para búsqueda
        return self.arbol_obstaculos.eliminar(obstaculo_temp)

    def obtener_recorrido_anchura(self) -> List[Obstaculo]:
        """
        Obtiene el recorrido en anchura del árbol de obstáculos.

        Returns:
            List[Obstaculo]: Obstáculos en orden de anchura
        """
        return self.arbol_obstaculos.recorrido_en_anchura()

    def obtener_recorrido_profundidad(self) -> List[Obstaculo]:
        """
        Obtiene el recorrido en profundidad del árbol de obstáculos.

        Returns:
            List[Obstaculo]: Obstáculos en orden de profundidad
        """
        return self.arbol_obstaculos.recorrido_en_profundidad()

    def reiniciar_juego(self) -> None:
        """
        Reinicia el juego a su estado inicial.
        """
        if self.carrito is not None:
            self.carrito.reiniciar()

        self.distancia_recorrida = 0
        self.obstaculos_visibles = []
        self.puntuacion = 0
        self.tiempo_juego = 0
        self.estado_actual = EstadoJuego.JUGANDO

    def pausar_juego(self) -> None:
        """
        Pausa o despausa el juego.
        """
        if self.estado_actual == EstadoJuego.JUGANDO:
            self.estado_actual = EstadoJuego.PAUSADO
        elif self.estado_actual == EstadoJuego.PAUSADO:
            self.estado_actual = EstadoJuego.JUGANDO

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene las estadísticas actuales del juego.

        Returns:
            dict: Diccionario con estadísticas del juego
        """
        energia_porcentaje = 0.0
        if self.carrito is not None:
            energia_porcentaje = self.carrito.obtener_porcentaje_energia()

        return {
            "distancia_recorrida": self.distancia_recorrida,
            "distancia_total": self.distancia_total,
            "progreso_porcentaje": (self.distancia_recorrida / self.distancia_total)
            * 100,
            "puntuacion": self.puntuacion,
            "tiempo_juego": self.tiempo_juego,
            "energia_porcentaje": energia_porcentaje * 100,
            "obstaculos_visibles": len(self.obstaculos_visibles),
            "total_obstaculos": self.arbol_obstaculos.obtener_total_obstaculos(),
            "estado_juego": self.estado_actual.value,
        }

    def _crear_obstaculo_desde_dict(self, datos_obstaculo: Dict[str, Any]) -> Obstaculo:
        """
        Crea un obstáculo a partir de un diccionario de configuración.

        Args:
            datos_obstaculo (dict): Datos del obstáculo desde JSON

        Returns:
            Obstaculo: Nuevo obstáculo creado
        """
        x = datos_obstaculo["x"]
        y = datos_obstaculo["y"]
        tipo_str = datos_obstaculo["tipo"]
        ancho = datos_obstaculo.get("ancho", 30)
        alto = datos_obstaculo.get("alto", 30)

        # Convertir string a enum
        tipo = TipoObstaculo(tipo_str)

        return Obstaculo(x, y, tipo, ancho, alto)
