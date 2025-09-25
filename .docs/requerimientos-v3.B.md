
### Pantalla de Juego Principal
- ✅ Estructura básica de la pantalla
- ✅ Dibujo del fondo y carretera
- ✅ División en carriles visuales
- 🔧 Renderizado del carrito (básico)
- ⬜ Sistema de cámara que sigue al carrito
    - 👨‍💻 **Archivo:** `view/pantalla_juego.py` | **Método:** `dibujar()`
    - **Acción:** Calcular un `offset_camara` basado en la `distancia_recorrida` y aplicarlo al dibujar todos los elementos del juego.
- ⬜ Renderizado de obstáculos en tiempo real
    - 👨‍💻 **Archivo:** `view/pantalla_juego.py` | **Método:** `dibujar_obstaculos()`
    - **Acción:** Iterar sobre la lista `obstaculos_visibles` del `GestorJuego` y dibujarlos en pantalla aplicando el `offset_camara`.
- ⬜ HUD con información del juego (energía, distancia, puntos)
    - 👨‍💻 **Archivo:** `view/pantalla_juego.py` | **Método:** `dibujar_hud()`
    - **Acción:** Obtener los datos de `energía`, `distancia` y `puntuación` del `GestorJuego` y mostrarlos en la parte superior de la pantalla.

### Visualización del Árbol AVL
- ✅ Clase VisualizadorArbol básica
- ✅ Cálculo de posiciones de nodos
- ✅ Dibujo de nodos y conexiones
- 🔧 Recorridos animados (estructura presente, falta animación)
    - 👨‍💻 **Archivo:** `view/visualizador_arbol.py` | **Método:** `update()`
    - **Acción:** Usar un temporizador para mostrar los nodos del recorrido uno por uno, en lugar de todos a la vez.
- ⬜ Ventana emergente para mostrar el árbol
    - 👨‍💻 **Archivo:** `main.py` | **Funciones:** `draw()`, `on_key_down()`
    - **Acción:** Usar una tecla (ej. 'T') para activar un modo `mostrar_arbol` que dibuje la visualización del árbol sobre la pantalla actual.
- ⬜ Controles para diferentes tipos de recorrido
    - 👨‍💻 **Archivo:** `view/visualizador_arbol.py`
    - **Acción:** Añadir botones o teclas para seleccionar si se desea visualizar el recorrido BFS, Preorden, Inorden o Postorden.

---

## 🔗 5. INTEGRACIÓN Y LÓGICA DE JUEGO

> **Definición de Terminado (DoD):** La integración es exitosa cuando el input del usuario se traduce en acciones del carrito, el `GestorJuego` actualiza el estado del mundo (posición, colisiones) consultando el árbol AVL en tiempo real, y la `PantallaJuego` refleja visualmente dicho estado, todo de forma sincronizada y fluida.

### Conexión entre Componentes
- 🔧 Gestor conectado con pantallas (parcial)
- ⬜ Sincronización entre lógica y vista
    - 👨‍💻 **Archivo:** `main.py` | **Funciones:** `update()`, `draw()`
    - **Acción:** Asegurar que `update()` se encarga de toda la lógica y `draw()` solo de dibujar el estado actual, sin modificarlo.
- ⬜ Sistema de eventos entre módulos
    - **Acción:** Para funcionalidades complejas, se podría implementar un sistema simple de publicador/suscriptor, pero para este proyecto es opcional. La comunicación directa a través del `GestorJuego` es suficiente.

### Sistema de Colisiones
- ⬜ Definir hitboxes para el carrito (rectángulo)
    - 👨‍💻 **Archivo:** `logic/carrito.py` | **Método:** `get_hitbox()`
- ⬜ Definir hitboxes para obstáculos (por tipo)
    - 👨‍💻 **Archivo:** `logic/obstaculo.py` | **Método:** `get_hitbox()`
- ⬜ Algoritmo de detección de intersección
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método a crear:** `_verificar_colisiones()`
    - **Acción:** Usar `pygame.Rect.colliderect()` para comparar el hitbox del carrito con el de cada obstáculo visible.
- ⬜ Manejo de evento de colisión
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `_verificar_colisiones()`
    - **Acción:** Si hay colisión, llamar al método `recibir_daño()` del carrito.
- ⬜ Aplicación de daño por colisión
    - 👨‍💻 **Archivo:** `logic/carrito.py` | **Método a crear:** `recibir_daño(self, cantidad)`
    - **Acción:** Reducir la energía del carrito y posiblemente cambiar su estado a `DAÑADO` por un corto tiempo.

### Consultas del Árbol en Tiempo Real
- ⬜ Consulta de obstáculos en rango visible
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método a crear:** `_actualizar_obstaculos_visibles()`
    - **Acción:** Llamar a `arbol_obstaculos.buscar_en_rango()` con las coordenadas de la cámara.
- ⬜ Optimización para consultas frecuentes
    - **Acción:** En lugar de llamar a la búsqueda en cada frame, hacerlo solo cuando el carrito haya avanzado una cierta distancia.

### Input del Usuario
- ⬜ Manejo de teclas de flecha (↑↓) para movimiento Y
    - 👨‍💻 **Archivo:** `main.py` | **Función:** `update()`
    - **Acción:** Comprobar `keyboard.up` y `keyboard.down` para llamar a `gestor_juego.carrito.mover()`.
- ⬜ Manejo de tecla ESPACIO para salto
    - 👨‍💻 **Archivo:** `main.py` | **Función:** `on_key_down()`
    - **Acción:** Comprobar si `key == keys.SPACE` para llamar a `gestor_juego.carrito.saltar()`.
- ⬜ Sistema de input responsivo
    - **Acción:** Asegurarse de que las acciones solo se procesen si `gestor_juego.estado_actual == EstadoJuego.JUGANDO`.

---

## 🚀 6. FUNCIONALIDADES AVANZADAS

> **Definición de Terminado (DoD):** Las funcionalidades avanzadas están completas cuando el juego se siente "pulido". Esto incluye animaciones suaves para el jugador y la interfaz, un sistema de puntuación que recompensa la habilidad, y la capacidad de personalizar la experiencia del juego.

### Animaciones
- ⬜ Animación suave del salto del carrito
    - 👨‍💻 **Archivo:** `logic/carrito.py` | **Método:** `update()`
    - **Acción:** Implementar una física de salto basada en gravedad y velocidad inicial para un movimiento curvo.
- ⬜ Efectos de partículas para colisiones
    - **Acción:** Crear una clase `Particula` y un sistema que las genere cuando ocurre una colisión.
- ⬜ Animación del fondo en movimiento
    - **Acción:** Usar un fondo con efecto parallax para dar sensación de velocidad.

### Sistema de Puntuación
- ⬜ Puntos por distancia recorrida
- ⬜ Puntos por obstáculos evitados
    - 👨‍💻 **Archivo:** `logic/gestor_juego.py` | **Método:** `update()`
    - **Acción:** Incrementar la puntuación cuando un obstáculo sale de la pantalla por la izquierda sin haber colisionado.
- ⬜ Display de puntuación en HUD

### Funcionalidades Extras
- ⬜ Poder insertar obstáculos manualmente antes del juego
    - 👨‍💻 **Archivo:** `view/pantalla_configuracion.py`
    - **Acción:** Añadir una interfaz visual para hacer clic y añadir obstáculos, que llame a `arbol_obstaculos.insertar()`.
- ⬜ Eliminar obstáculos desde la interfaz
- ⬜ Sonidos y efectos de audio
    - **Acción:** Usar `pygame.mixer` para cargar y reproducir sonidos para el salto, colisiones y música de fondo.

---

## 📚 7. DOCUMENTACIÓN Y TESTING

> **Definición de Terminado (DoD):** El proyecto está listo para la entrega cuando el código está bien documentado con `docstrings`, hay una suite de tests que valida la lógica principal (especialmente el árbol AVL), y se ha creado un manual de usuario y un video demostrativo.

### Documentación Técnica
- ⬜ Documentación de la API del árbol AVL con `docstrings`.
- ⬜ Diagramas de clases UML.
- ⬜ Manual técnico del proyecto (`README.md` detallado).

### Manual de Usuario
- ⬜ Instrucciones de instalación y ejecución.
- ⬜ Guía de controles del juego.
- ⬜ Tutorial de configuración.

### Testing
- ⬜ Tests unitarios para el árbol AVL
    - 👨‍💻 **Framework:** `pytest` | **Archivo a crear:** `tests/test_arbol_avl.py`
    - **Acción:** Probar inserciones, rotaciones, balance y recorridos.
- ⬜ Tests de integración para el gestor
    - 👨‍💻 **Framework:** `pytest` | **Archivo a crear:** `tests/test_gestor_juego.py`
    - **Acción:** Probar la carga de configuración y la lógica de estados sin la UI.
- ⬜ Tests de la lógica de colisiones

### Video y Entrega Final
- ⬜ Script del videotutorial.
- ⬜ Grabación del gameplay.
- ⬜ Preparación del repositorio para entrega (limpiar archivos, `README.md` final).

---

## 🎯 SIGUIENTE SPRINT SUGERIDO

Para finalizar rápidamente un MVP funcional, se sugiere completar en orden:

1.  **Integración Básica** (2-3 horas)
    -   ⬜ Conectar completamente gestor con pantallas
    -   ⬜ Implementar transiciones de estado
2.  **Input y Movimiento** (2-3 horas)
    -   ⬜ Input de usuario funcionando
    -   ⬜ Salto básico del carrito
3.  **Colisiones Básicas** (3-4 horas)
    -   ⬜ Detección de colisiones rectangulares
    -   ⬜ Aplicación de daño
4.  **Visualización Completa** (2-3 horas)
    -   ⬜ Obstáculos renderizados en pantalla
    -   ⬜ HUD básico funcionando

**Total estimado para MVP: 10-13 horas de trabajo**

---

*Última actualización: 25 de septiembre, 2025*
*Estado del proyecto: 65% completado - En desarrollo activo*