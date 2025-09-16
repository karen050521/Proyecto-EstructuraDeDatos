"""
Clase que representa el carrito del jugador.
Responsabilidad: Gestionar posición, movimiento, estado y colisiones del carrito.
"""

from enum import Enum

class EstadoCarrito(Enum):
    """Estados posibles del carrito durante el juego."""
    NORMAL = "normal"
    SALTANDO = "saltando"
    COLISIONANDO = "colisionando"
    INVULNERABLE = "invulnerable"

class Carrito:
    """
    Representa el carrito controlado por el jugador.
    Maneja movimiento automático en X y control manual en Y.
    """
    
    def __init__(self, x_inicial=50, y_inicial=1, energia_maxima=100):
        """
        Inicializa el carrito en la posición especificada.
        
        Args:
            x_inicial (int): Posición X inicial
            y_inicial (int): Carril inicial (0=abajo, 1=medio, 2=arriba)
            energia_maxima (int): Energía máxima del carrito
        """
        self.x = x_inicial
        self.y = y_inicial
        self.energia_actual = energia_maxima
        self.energia_maxima = energia_maxima
        self.estado = EstadoCarrito.NORMAL
        
        # Configuración de movimiento
        self.velocidad_x = 5  # metros por frame
        self.velocidad_y = 0  # velocidad vertical actual
        self.altura_salto = 50  # altura máxima del salto
        self.tiempo_salto = 0  # tiempo actual de salto
        self.duracion_salto = 20  # frames que dura el salto
        
        # Configuración visual
        self.ancho = 40
        self.alto = 30
        self.color_normal = "azul"
        self.color_saltando = "amarillo"
        self.color_actual = self.color_normal
    
    def actualizar(self, delta_tiempo):
        """
        Actualiza el estado del carrito cada frame.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        pass
    
    def mover_automaticamente(self):
        """
        Mueve el carrito automáticamente hacia adelante en el eje X.
        """
        pass
    
    def mover_arriba(self):
        """
        Mueve el carrito un carril hacia arriba (si es posible).
        """
        pass
    
    def mover_abajo(self):
        """
        Mueve el carrito un carril hacia abajo (si es posible).
        """
        pass
    
    def saltar(self):
        """
        Inicia el salto del carrito si no está ya saltando.
        """
        pass
    
    def actualizar_salto(self):
        """
        Actualiza la lógica del salto (altura y duración).
        """
        pass
    
    def recibir_daño(self, cantidad_daño):
        """
        Reduce la energía del carrito por una colisión.
        
        Args:
            cantidad_daño (int): Cantidad de energía a reducir
            
        Returns:
            bool: True si el carrito sigue vivo, False si se quedó sin energía
        """
        pass
    
    def obtener_rectangulo_colision(self):
        """
        Obtiene el rectángulo de colisión actual del carrito.
        
        Returns:
            dict: Diccionario con 'x', 'y', 'ancho', 'alto'
        """
        pass
    
    def colisiona_con(self, obstaculo):
        """
        Verifica si el carrito está colisionando con un obstáculo.
        
        Args:
            obstaculo (Obstaculo): Obstáculo a verificar
            
        Returns:
            bool: True si hay colisión
        """
        pass
    
    def esta_saltando(self):
        """
        Verifica si el carrito está en estado de salto.
        
        Returns:
            bool: True si está saltando
        """
        pass
    
    def esta_vivo(self):
        """
        Verifica si el carrito tiene energía suficiente para continuar.
        
        Returns:
            bool: True si tiene energía > 0
        """
        pass
    
    def obtener_porcentaje_energia(self):
        """
        Obtiene el porcentaje actual de energía.
        
        Returns:
            float: Porcentaje de energía (0.0 a 1.0)
        """
        pass
    
    def reiniciar(self, x_inicial=50, y_inicial=1):
        """
        Reinicia el carrito a su estado inicial.
        
        Args:
            x_inicial (int): Nueva posición X inicial
            y_inicial (int): Nuevo carril inicial
        """
        pass
    
    def obtener_sprite_nombre(self):
        """
        Obtiene el nombre del sprite actual según el estado.
        
        Returns:
            str: Nombre del archivo de sprite
        """
        pass
    
    def __str__(self):
        """
        Representación en string del carrito para debugging.
        
        Returns:
            str: Información del estado actual
        """
        pass
