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

### Archivo JSON y Carga de Configuración
- ✅ Estructura básica del JSON implementada
- ✅ Carga de configuración desde archivo
- ✅ Carga de obstáculos predefinidos
- ⬜ Validación de datos del JSON al cargar
- ⬜ Manejo de errores detallado para archivos corruptos
- ⬜ Guardar configuración modificada de vuelta al JSON

### Configuraciones del Juego
- ✅ Distancia total configurable
- ✅ Velocidad del carrito configurable
- ✅ Tiempo de refresco configurable
- ✅ Altura de salto configurable
- ✅ Color inicial del carrito configurable
- ⬜ Configuración de tipos de obstáculos y daño
- ⬜ Configuración de energía inicial del carrito

---

## 🌳 2. ÁRBOL AVL Y ESTRUCTURA DE DATOS

### Implementación del Árbol AVL
- ✅ Clase NodoAVL con balance y altura
- ✅ Clase ArbolAVL con inserción balanceada
- ✅ Eliminación de nodos manteniendo balance
- ✅ Rotaciones simples y dobles
- ✅ Búsqueda de obstáculos por coordenadas
- ✅ Recorridos en profundidad (preorden, inorden, postorden)
- ✅ Recorrido en anchura (BFS)
- ⬜ Optimización de consultas por rango (x_min, x_max, y_min, y_max)

### Estructura de Obstáculos
- ✅ Clase Obstaculo con coordenadas y tipo
- ✅ Enum TipoObstaculo con diferentes tipos
- ✅ Sistema de comparación para inserción en AVL
- ✅ Validación de coordenadas únicas
- ⬜ Definición de áreas de colisión por obstáculo
- ⬜ Sistema de daño por tipo de obstáculo

### Estructura del Carrito
- ✅ Clase Carrito con posición y estado
- ✅ Estados del carrito (normal, saltando, dañado)
- ✅ Sistema de energía básico
- ⬜ Área de colisión del carrito definida
- ⬜ Sistema de puntuación integrado

---

## 🎯 3. SISTEMA DE JUEGO BÁSICO

### Estados del Juego
- ✅ Enum EstadoJuego definido
- ✅ GestorJuego con cambio de estados
- 🔧 Transiciones entre estados (necesita completarse)
- ⬜ Lógica de pausa y reanudación
- ⬜ Condiciones de victoria (llegar a la meta)
- ⬜ Condiciones de derrota (energía = 0)

### Movimiento del Carrito
- ✅ Avance automático en X
- 🔧 Control manual en Y (parcialmente implementado)
- ⬜ Implementar mecánica de salto completa
- ⬜ Cambio de color durante el salto
- ⬜ Animación de aterrizaje del salto
- ⬜ Limitaciones de movimiento (no salir de la carretera)

### Sistema de Tiempo y Física
- ✅ Control de tiempo de refresco
- ⬜ Calculadora de distancia recorrida
- ⬜ Sistema de velocidad variable
- ⬜ Física básica para el salto (parábola)
- ⬜ Sincronización entre avance y aparición de obstáculos

---

## 🖼️ 4. INTERFAZ GRÁFICA

### Pantalla de Configuración
- ✅ Componentes básicos de UI (botones, campos de texto)
- ✅ Pantalla de configuración estructurada
- 🔧 Integración con el gestor de juego (parcial)
- ⬜ Validación de entrada de usuario en tiempo real
- ⬜ Preview de configuración antes de aplicar
- ⬜ Reset a valores por defecto

### Pantalla de Juego Principal
- ✅ Estructura básica de la pantalla
- ✅ Dibujo del fondo y carretera
- ✅ División en carriles visuales
- 🔧 Renderizado del carrito (básico)
- ⬜ Sistema de cámara que sigue al carrito
- ⬜ Renderizado de obstáculos en tiempo real
- ⬜ HUD con información del juego (energía, distancia, puntos)

### Visualización del Árbol AVL
- ✅ Clase VisualizadorArbol básica
- ✅ Cálculo de posiciones de nodos
- ✅ Dibujo de nodos y conexiones
- 🔧 Recorridos animados (estructura presente, falta animación)
- ⬜ Ventana emergente para mostrar el árbol
- ⬜ Resaltado de nodos durante recorridos
- ⬜ Controles para diferentes tipos de recorrido

---

## 🔗 5. INTEGRACIÓN Y LÓGICA DE JUEGO

### Conexión entre Componentes
- 🔧 Gestor conectado con pantallas (parcial)
- ⬜ Sincronización entre lógica y vista
- ⬜ Comunicación bidireccional entre componentes
- ⬜ Sistema de eventos entre módulos

### Sistema de Colisiones
- ⬜ Definir hitboxes para el carrito (rectángulo)
- ⬜ Definir hitboxes para obstáculos (por tipo)
- ⬜ Algoritmo de detección de intersección
- ⬜ Manejo de evento de colisión
- ⬜ Aplicación de daño por colisión
- ⬜ Efectos visuales de colisión

### Consultas del Árbol en Tiempo Real
- ⬜ Consulta de obstáculos en rango visible
- ⬜ Optimización para consultas frecuentes
- ⬜ Cache de obstáculos cercanos
- ⬜ Actualización eficiente de obstáculos visibles

### Input del Usuario
- ⬜ Manejo de teclas de flecha (↑↓) para movimiento Y
- ⬜ Manejo de tecla ESPACIO para salto
- ⬜ Prevención de inputs durante animaciones
- ⬜ Sistema de input responsivo

---

## 🚀 6. FUNCIONALIDADES AVANZADAS

### Animaciones
- ⬜ Animación suave del salto del carrito
- ⬜ Cambio gradual de color durante el salto
- ⬜ Animación de los recorridos del árbol
- ⬜ Efectos de partículas para colisiones
- ⬜ Animación del fondo en movimiento

### Sistema de Puntuación
- ⬜ Puntos por distancia recorrida
- ⬜ Puntos por obstáculos evitados
- ⬜ Bonificaciones por tiempo
- ⬜ Display de puntuación en HUD
- ⬜ Sistema de high scores

### Funcionalidades Extras
- ⬜ Poder insertar obstáculos manualmente antes del juego
- ⬜ Eliminar obstáculos desde la interfaz
- ⬜ Diferentes niveles de dificultad
- ⬜ Sonidos y efectos de audio
- ⬜ Configuración de controles

---

## 📚 7. DOCUMENTACIÓN Y TESTING

### Documentación Técnica
- ⬜ Documentación de la API del árbol AVL
- ⬜ Diagramas de clases UML
- ⬜ Documentación de la arquitectura
- ⬜ Manual técnico del proyecto

### Manual de Usuario
- ⬜ Instrucciones de instalación
- ⬜ Guía de controles del juego
- ⬜ Tutorial de configuración
- ⬜ Solución de problemas comunes

### Testing
- ⬜ Tests unitarios para el árbol AVL
- ⬜ Tests de integración para el gestor
- ⬜ Tests de la lógica de colisiones
- ⬜ Tests de carga y rendimiento

### Video y Entrega Final
- ⬜ Script del videotutorial
- ⬜ Grabación del gameplay
- ⬜ Explicación técnica en el video
- ⬜ Preparación del repositorio para entrega

---

## ⚠️ NOTAS TÉCNICAS IMPORTANTES

### Decisiones Pendientes
1. **Sistema de Colisiones**: Decidir si usar rectángulos simples o formas más complejas
2. **Rendimiento**: Evaluar si necesitamos optimizaciones adicionales para el árbol
3. **Animaciones**: Definir duración y estilo de las animaciones
4. **Audio**: Decidir si agregar sonidos básicos o enfocarse solo en lo visual

### Tareas Críticas para el Funcionamiento Mínimo
1. Completar la integración entre pantallas y gestor
2. Implementar el sistema básico de colisiones
3. Hacer funcionar el input del usuario
4. Conectar la visualización del árbol con la pantalla de juego

### Tareas que Agregan Valor pero No Son Críticas
1. Animaciones elaboradas
2. Sistema de puntuación complejo
3. Múltiples niveles de dificultad
4. Efectos visuales avanzados

---

## 🎯 SIGUIENTE SPRINT SUGERIDO

Para finalizar rápidamente un MVP funcional, se sugiere completar en orden:

1. **Integración Básica** (2-3 horas)
   - ⬜ Conectar completamente gestor con pantallas
   - ⬜ Implementar transiciones de estado

2. **Input y Movimiento** (2-3 horas)
   - ⬜ Input de usuario funcionando
   - ⬜ Salto básico del carrito

3. **Colisiones Básicas** (3-4 horas)
   - ⬜ Detección de colisiones rectangulares
   - ⬜ Aplicación de daño

4. **Visualización Completa** (2-3 horas)
   - ⬜ Obstáculos renderizados en pantalla
   - ⬜ HUD básico funcionando

**Total estimado para MVP: 10-13 horas de trabajo**

---

*Última actualización: 25 de septiembre, 2025*
*Estado del proyecto: 65% completado - En desarrollo activo*