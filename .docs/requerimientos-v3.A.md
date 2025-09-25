# 🎮 Requerimientos del Proyecto - Juego de Carrito con Árbol AVL

## 📋 Cómo usar esta lista
- ✅ = Completado y verificado
- ⬜ = Pendiente por hacer  
- 🔧 = En progreso
- ⚠️ = Requiere atención o decisión técnica

**Progreso general estimado: 65% completado**

---

## 📊 Resumen de Progreso por Categorías

| Categoría | Progreso | Estado |
|-----------|----------|--------|
| 🗃️ Configuración y Datos | 85% | Casi completo |
| 🌳 Árbol AVL y Estructura | 90% | Casi completo |
| 🎯 Sistema de Juego Básico | 60% | En progreso |
| 🖼️ Interfaz Gráfica | 55% | En progreso |
| 🔗 Integración y Lógica | 30% | Necesita trabajo |
| 🚀 Funcionalidades Avanzadas | 25% | Pendiente |
| 📚 Documentación y Testing | 20% | Pendiente |

---

## 🗃️ 1. CONFIGURACIÓN Y DATOS

> **Definición de Terminado (DoD):** La configuración se considera completa cuando el juego puede cargar y guardar todos los parámetros desde `configuracion.json`, incluyendo el daño por tipo de obstáculo y la energía inicial del carrito. El sistema debe validar los datos al cargar, manejar errores de formato de manera robusta, y reflejar cualquier cambio hecho en la UI de configuración una vez guardado.

### Archivo JSON y Carga de Configuración
- ✅ Estructura básica del JSON implementada
- ✅ Carga de configuración desde archivo
- ✅ Carga de obstáculos predefinidos
- ⬜ Validación de datos del JSON al cargar
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `cargar_configuracion()`
    - **Acción:** Añadir validaciones para los tipos y rangos de los valores cargados (e.g., `velocidad > 0`).
- ⬜ Manejo de errores detallado para archivos corruptos
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `cargar_configuracion()`
    - **Acción:** Mejorar el bloque `try-except` para capturar `json.JSONDecodeError` y `KeyError` de forma separada, informando al usuario del problema específico.
- ⬜ Guardar configuración modificada de vuelta al JSON
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `guardar_configuracion()`
    - **Acción:** Implementar la lógica para tomar los valores actuales del `GestorJuego` y escribirlos en el archivo `configuracion.json`.

### Configuraciones del Juego
- ✅ Distancia total configurable
- ✅ Velocidad del carrito configurable
- ✅ Tiempo de refresco configurable
- ✅ Altura de salto configurable
- ✅ Color inicial del carrito configurable
- ⬜ Configuración de tipos de obstáculos y daño
    - 👨‍💻 **Archivos:** `data/configuracion.json`, `logic/obstaculo.py`, `logic/gestor_juego.py`
    - **Acción:** Añadir una sección de `daño_obstaculos` al JSON y cargarla en el `GestorJuego` para que cada `TipoObstaculo` tenga un valor de daño asociado.
- ⬜ Configuración de energía inicial del carrito
    - 👨‍💻 **Archivos:** `data/configuracion.json`, `logic/carrito.py`, `logic/gestor_juego.py`
    - **Acción:** Añadir `energia_inicial` al JSON, leerla en el `GestorJuego` y pasarla al constructor del `Carrito`.

---

## 🌳 2. ÁRBOL AVL Y ESTRUCTURA DE DATOS

> **Definición de Terminado (DoD):** La estructura de datos está completa cuando el árbol AVL puede realizar búsquedas optimizadas por rango de coordenadas. Tanto el carrito como los obstáculos deben poder exponer sus áreas de colisión (`hitboxes`). El sistema debe poder asociar un valor de daño a cada tipo de obstáculo y el carrito debe tener un sistema para gestionar su puntuación.

### Implementación del Árbol AVL
- ✅ Clase NodoAVL con balance y altura
- ✅ Clase ArbolAVL con inserción balanceada
- ✅ Eliminación de nodos manteniendo balance
- ✅ Rotaciones simples y dobles
- ✅ Búsqueda de obstáculos por coordenadas
- ✅ Recorridos en profundidad (preorden, inorden, postorden)
- ✅ Recorrido en anchura (BFS)
- ⬜ Optimización de consultas por rango (x_min, x_max, y_min, y_max)
    - 👨‍💻 **Archivo:** `logic/arbol_avl.py` | **Método a crear:** `buscar_en_rango(self, x_min, x_max)`
    - **Acción:** Implementar un método que recorra el árbol podando las ramas que no se encuentren en el rango de `x` para acelerar la búsqueda de obstáculos visibles.

### Estructura de Obstáculos
- ✅ Clase Obstaculo con coordenadas y tipo
- ✅ Enum TipoObstaculo con diferentes tipos
- ✅ Sistema de comparación para inserción en AVL
- ✅ Validación de coordenadas únicas
- ⬜ Definición de áreas de colisión por obstáculo
    - 👨‍💻 **Archivo:** `logic/obstaculo.py` | **Clase:** `Obstaculo`
    - **Acción:** Añadir un método `get_hitbox(self)` que devuelva un `pygame.Rect` representando el área de colisión del obstáculo.
- ⬜ Sistema de daño por tipo de obstáculo
    - 👨‍💻 **Archivo:** `logic/obstaculo.py` | **Enum:** `TipoObstaculo`
    - **Acción:** Asociar un valor de daño a cada tipo, probablemente cargado desde el JSON y gestionado por el `GestorJuego`.

### Estructura del Carrito
- ✅ Clase Carrito con posición y estado
- ✅ Estados del carrito (normal, saltando, dañado)
- ✅ Sistema de energía básico
- ⬜ Área de colisión del carrito definida
    - 👨‍💻 **Archivo:** `logic/carrito.py` | **Clase:** `Carrito`
    - **Acción:** Añadir un método `get_hitbox(self)` que devuelva un `pygame.Rect` basado en la posición y tamaño actual del carrito.
- ⬜ Sistema de puntuación integrado
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Clase:** `GestorJuego`
    - **Acción:** Añadir un atributo `puntuacion` y la lógica para incrementarlo por distancia recorrida o por obstáculos esquivados.

---

## 🎯 3. SISTEMA DE JUEGO BÁSICO

> **Definición de Terminado (DoD):** El sistema de juego es funcional cuando el carrito puede moverse, saltar y permanecer dentro de los límites de la carretera. El `GestorJuego` debe controlar el ciclo de vida completo (jugar, pausar, ganar, perder) y la distancia recorrida debe determinar qué obstáculos se consultan y se muestran.

### Estados del Juego
- ✅ Enum EstadoJuego definido
- ✅ GestorJuego con cambio de estados
- 🔧 Transiciones entre estados (necesita completarse)
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `update()`
    - **Acción:** Implementar la lógica principal del juego solo cuando el estado sea `JUGANDO`.
- ⬜ Lógica de pausa y reanudación
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Métodos:** `pausar_juego()`, `reanudar_juego()`
    - **Acción:** Crear métodos para cambiar entre los estados `JUGANDO` y `PAUSADO`.
- ⬜ Condiciones de victoria (llegar a la meta)
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `update()`
    - **Acción:** Verificar si `distancia_recorrida >= distancia_total` para cambiar el estado a `JUEGO_TERMINADO`.
- ⬜ Condiciones de derrota (energía = 0)
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `update()`
    - **Acción:** Verificar si `carrito.energia <= 0` para cambiar el estado a `JUEGO_TERMINADO`.

### Movimiento del Carrito
- ✅ Avance automático en X
- 🔧 Control manual en Y (parcialmente implementado)
    - 👨‍💻 **Archivo:** `main.py` | **Función:** `update()` o `on_key_down()`
    - **Acción:** Capturar las teclas de flecha arriba/abajo para llamar al método `mover()` del carrito.
- ⬜ Implementar mecánica de salto completa
    - 👨‍💻 **Archivo:** `logic/carrito.py` | **Métodos:** `saltar()`, `update()`
    - **Acción:** En `saltar()`, iniciar una velocidad vertical. En `update()`, aplicar gravedad para crear un arco de salto.
- ⬜ Cambio de color durante el salto
    - 👨‍💻 **Archivo:** `view/pantalla_juego.py` | **Método:** `dibujar_carrito()`
    - **Acción:** Cambiar el color del carrito si `carrito.estado == EstadoCarrito.SALTANDO`.
- ⬜ Animación de aterrizaje del salto
    - 👨‍💻 **Archivo:** `logic/carrito.py` | **Método:** `update()`
    - **Acción:** Cuando el carrito toque el suelo (`y <= y_suelo`), cambiar su estado de `SALTANDO` a `NORMAL`.
- ⬜ Limitaciones de movimiento (no salir de la carretera)
    - 👨‍💻 **Archivo:** `logic/carrito.py` | **Método:** `mover()`
    - **Acción:** Añadir lógica para que la posición `y` del carrito no pueda ser mayor ni menor que los límites de los carriles.

### Sistema de Tiempo y Física
- ✅ Control de tiempo de refresco
- ⬜ Calculadora de distancia recorrida
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `update()`
    - **Acción:** Incrementar `self.distancia_recorrida` basado en la velocidad y el tiempo transcurrido.
- ⬜ Sincronización entre avance y aparición de obstáculos
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `_actualizar_obstaculos_visibles()`
    - **Acción:** Usar la `distancia_recorrida` para consultar en el árbol AVL los obstáculos que deberían estar visibles.

---

## 🖼️ 4. INTERFAZ GRÁFICA

> **Definición de Terminado (DoD):** La interfaz gráfica está completa cuando la pantalla de configuración puede modificar el estado del juego y guardarlo. La pantalla de juego debe mostrar una cámara que avanza, renderizando dinámicamente los obstáculos y un HUD actualizado en tiempo real. Debe ser posible abrir una ventana para visualizar el árbol AVL y sus recorridos en cualquier momento.

### Pantalla de Configuración
- ✅ Componentes básicos de UI (botones, campos de texto)
- ✅ Pantalla de configuración estructurada
- 🔧 Integración con el gestor de juego (parcial)
    - 👨‍💻 **Archivo:** `view/controlador_configuracion.py` | **Métodos:** `aplicar_cambios()`, `guardar_configuracion()`
    - **Acción:** Conectar los botones de la UI para que llamen a los métodos correspondientes en el `GestorJuego`.
- ⬜ Validación de entrada de usuario en tiempo real
    - 👨‍💻 **Archivo:** `view/components/campo_texto_simple.py`
    - **Acción:** Añadir lógica para validar que solo se ingresen números en campos numéricos.
- ⬜ Reset a valores por defecto
    - 👨‍💻 **Archivo:** `view/controlador_configuracion.py`
    - **Acción:** Implementar un botón "Reset" que llame a `gestor_juego.cargar_configuracion()` para restaurar los valores del JSON.
