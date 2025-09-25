# 🚀 Cómo Ejecutar el Proyecto

## Instalación Rápida

```bash
# 1. Instalar dependencias
uv sync

# 2. Ejecutar el juego
uv run python -m pgzero main.py
```

## ¿Qué Verás?

### Al Ejecutar:
1. **Ventana de 800x600** con fondo azul oscuro
2. **Texto de debug** mostrando el estado actual
3. **Estado inicial: "configuracion"**
4. **Contador de obstáculos** en el árbol

### Controles Actuales:
- **ESC**: Salir (desde configuración) o volver a configuración (desde juego)
- **Flechas ↑↓**: Mover carrito (cuando esté jugando)
- **ESPACIO**: Saltar (cuando esté jugando)
- **P**: Pausar (cuando esté jugando)

## Estado Actual del Proyecto

### ✅ Completado (MVP):
- [x] **Estructura del proyecto** con pygame-zero
- [x] **Todas las clases definidas** (métodos sin implementar)
- [x] **Sistema de estados** (configuración/juego/pausa)
- [x] **Configuración JSON** cargable
- [x] **Main.py funcional** con pygame-zero
- [x] **README detallado** como guía de implementación

### 🚧 Próximos Pasos (Por Prioridad):

#### 1. **Implementar Árbol AVL** (Crítico)
```python
# Archivos a implementar:
- logic/nodo_avl.py      # Nodo individual con balance
- logic/arbol_avl.py     # Árbol con inserción/búsqueda/rotaciones
```

#### 2. **Implementar Clases de Juego** (Alto)
```python
- logic/obstaculo.py     # Obstáculo con colisiones
- logic/carrito.py       # Carrito con movimiento
- logic/gestor_juego.py  # Coordinador principal
```

#### 3. **Implementar Interfaces** (Medio)
```python
- view/pantalla_configuracion.py  # Pantalla para modificar árbol
- view/pantalla_juego.py          # Pantalla principal del juego
- view/visualizador_arbol.py      # Visualización del árbol
```

## Arquitectura del Código

```
main.py                 # Punto de entrada con pygame-zero
├── logic/             # Lógica pura (sin pygame)
│   ├── arbol_avl.py   # ⭐ Estructura de datos principal
│   ├── carrito.py     # Estado y movimiento del jugador
│   ├── obstaculo.py   # Entidad de obstáculo
│   └── gestor_juego.py # Coordinador general
└── view/              # Interfaces gráficas
    ├── pantalla_*.py  # Pantallas del juego
    └── visualizador_arbol.py # Visualización del AVL
```

## Comandos Útiles

```bash
# Ejecutar con pygame-zero
uv run python -m pgzero main.py

# Ejecutar Python normal (solo muestra info)
uv run python main.py

# Instalar nuevas dependencias
uv add nombre-paquete

# Ver estructura del proyecto
tree . /F   # Windows
ls -la      # Linux/Mac
```

## Debugging

Si algo no funciona:

1. **Verificar que uv esté instalado**: `uv --version`
2. **Instalar dependencias**: `uv sync`
3. **Verificar pygame-zero**: `uv run python -c "import pgzero; print('OK')"`

## Siguiente Sesión de Desarrollo

**Prioridad 1**: Implementar `ArbolAVL.insertar()` y `ArbolAVL.buscar_en_rango()`
- Esto es lo que demuestra la eficiencia del proyecto
- Sin esto, el juego no tiene sentido académico

**Prioridad 2**: Implementar `Carrito` básico para que se mueva
- Permite probar el juego interactivamente
- Validar que pygame-zero funciona correctamente

---
*Este archivo es tu guía rápida. El README.md tiene el plan completo.*
