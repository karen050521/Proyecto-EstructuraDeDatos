# Juego de Carrito con Obstáculos Dinámicos usando Árbol AVL

## 🎯 Objetivo del Proyecto
Desarrollar un videojuego 2D donde un carrito esquiva obstáculos organizados mediante un árbol AVL, demostrando la eficiencia de esta estructura de datos para consultas espaciales en tiempo real.

## 🏗️ Arquitectura del Proyecto

```
jeffy-ds/
├── logic/                    # Lógica de negocio y estructuras de datos
│   ├── arbol_avl.py         # Implementación del árbol AVL
│   ├── obstaculo.py         # Clase Obstáculo
│   ├── carrito.py           # Clase Carrito
│   └── gestor_juego.py      # Gestor principal del estado del juego
├── view/                     # Interfaz gráfica con pygame-zero
│   ├── pantalla_config.py   # Vista de configuración del árbol
│   ├── pantalla_juego.py    # Vista principal del juego
│   └── visualizador_arbol.py # Visualización gráfica del árbol AVL
├── data/                     # Archivos de configuración
│   └── configuracion.json   # Configuración inicial y obstáculos
├── images/                   # Sprites del juego
└── sounds/                   # Efectos de sonido
```

## 🎮 Mecánica del Juego

### Fase 1: Configuración
- **¿Por qué?** Permitir al usuario personalizar el nivel antes de jugar
- Cargar configuración desde JSON
- Visualizar árbol AVL gráficamente
- Permitir agregar/eliminar obstáculos manualmente
- Mostrar recorridos del árbol (anchura/profundidad)

### Fase 2: Ejecución
- **¿Por qué?** Demostrar la eficiencia del árbol AVL en consultas espaciales
- Carrito se mueve automáticamente (eje X)
- Consultar árbol AVL cada frame para obstáculos visibles
- Control del carrito (eje Y y salto)
- Sistema de colisiones y energía

## 📋 Plan de Desarrollo (0% → 100%)

### 🔧 Fase 0: Configuración Inicial (0% → 15%)
- [ ] **Configurar proyecto con uv**
  - *¿Por qué?* Gestión de dependencias reproducible
  - Instalar pygame-zero
  - Configurar pyproject.toml
  - Crear estructura de carpetas

### 🌳 Fase 1: Estructura de Datos (15% → 35%)
- [ ] **Implementar Nodo AVL**
  - *¿Por qué?* Base fundamental del árbol balanceado
  - Atributos: valor, altura, hijos, factor de balance
  - Métodos de comparación por coordenadas (x, y)

- [ ] **Implementar Árbol AVL**
  - *¿Por qué?* Consultas eficientes O(log n) vs O(n) lineal
  - Inserción con rotaciones automáticas
  - Búsqueda por rango de coordenadas
  - Recorridos (anchura, profundidad)
  - Eliminación de nodos

- [ ] **Crear clase Obstáculo**
  - *¿Por qué?* Encapsular propiedades y comportamiento
  - Coordenadas (x1, y1, x2, y2)
  - Tipo y daño asociado
  - Área de colisión rectangular

- [ ] **Crear clase Carrito**
  - *¿Por qué?* Separar lógica de movimiento del rendering
  - Posición, velocidad, energía
  - Estados: normal, saltando, colisionando
  - Métodos de movimiento y colisión

### 🎨 Fase 2: Interfaz Gráfica Base (35% → 55%)
- [ ] **Configurar pygame-zero**
  - *¿Por qué?* Framework simplificado para prototipado rápido
  - Crear main.py como punto de entrada
  - Configurar dimensiones de pantalla
  - Sistema de estados (configuración/juego)

- [ ] **Crear PantallaConfiguracion**
  - *¿Por qué?* Interfaz intuitiva para modificar el árbol
  - Visualización gráfica del árbol AVL
  - Controles para agregar/eliminar obstáculos
  - Botones para recorridos del árbol

- [ ] **Crear PantallaJuego**
  - *¿Por qué?* Separar lógica de rendering del juego
  - Dibujo del carrito y carretera
  - Rendering de obstáculos visibles únicamente
  - HUD con energía y controles

- [ ] **Implementar VisualizadorArbol**
  - *¿Por qué?* Demostrar estructura del árbol visualmente
  - Dibujo de nodos como círculos
  - Conexiones entre nodos padre-hijo
  - Posicionamiento automático de nodos

### 🎮 Fase 3: Lógica de Juego (55% → 80%)
- [ ] **Implementar GestorJuego**
  - *¿Por qué?* Coordinar todos los componentes del juego
  - Carga de configuración JSON
  - Transición entre estados
  - Loop principal del juego

- [ ] **Sistema de consultas espaciales**
  - *¿Por qué?* Demostrar eficiencia del árbol AVL
  - Consultar obstáculos en rango de visión
  - Optimización: solo dibujar obstáculos visibles
  - Métricas de rendimiento

- [ ] **Sistema de colisiones**
  - *¿Por qué?* Mecánica core del juego
  - Detección carrito-obstáculo
  - Reducción de energía por tipo
  - Estados de invulnerabilidad temporal

- [ ] **Controles y movimiento**
  - *¿Por qué?* Interactividad del usuario
  - Movimiento automático en X
  - Control manual en Y (↑↓)
  - Mecánica de salto (ESPACIO)

### 🎯 Fase 4: Pulido y Optimización (80% → 100%)
- [ ] **Assets gráficos básicos**
  - *¿Por qué?* Experiencia visual mínima
  - Sprite del carrito (2 estados: normal/saltando)
  - Sprites de obstáculos por tipo
  - Fondo de carretera simple

- [ ] **Sistema de configuración JSON**
  - *¿Por qué?* Flexibilidad sin recompilar
  - Parámetros del juego (velocidad, distancia)
  - Lista inicial de obstáculos
  - Validación de datos de entrada

- [ ] **Refinamiento de la interfaz**
  - *¿Por qué?* Usabilidad y presentación
  - Transiciones suaves entre pantallas
  - Feedback visual de acciones
  - Manejo de errores de usuario

## 🧪 Criterios de Aceptación

### Funcionalidad Mínima Viable (MVP):
1. ✅ **Árbol AVL funcional**: Inserción, consulta por rango, recorridos
2. ✅ **Juego básico**: Carrito que se mueve, obstáculos que aparecen
3. ✅ **Configuración**: Modificar árbol antes del juego
4. ✅ **Visualización**: Ver estructura del árbol gráficamente

### Métricas de Éxito:
- **Rendimiento**: Consultas del árbol < 1ms para 1000 obstáculos
- **Usabilidad**: Interfaz intuitiva sin manual
- **Correctitud**: Árbol AVL siempre balanceado
- **Jugabilidad**: Juego fluido a 60 FPS

## 🚀 Comandos de Desarrollo

```bash
# Instalar dependencias
uv sync

# Ejecutar juego
uv run python main.py

# Ejecutar con pygame-zero directamente
uv run pgzrun main.py
```

## 📝 Notas de Implementación

### Decisiones de Diseño:
- **pygame-zero**: Simplicidad sobre flexibilidad completa
- **Español**: Todas las variables, clases y métodos en español
- **Single Responsibility**: Máximo 200 LOC por clase
- **Modularidad**: Separación clara entre lógica y presentación

### Limitaciones Actuales:
- Sin persistencia de configuraciones personalizadas
- Sin sistema de puntuación o niveles
- Sin efectos de sonido (opcional)
- Sin animaciones complejas

---
*Este README es la guía maestra del proyecto. Actualizar conforme se complete cada fase.*
