# CÓMO JUGAR

## Requisitos Previos
- Python 3.7 o superior
- Pygame-Zero (pgzero)

## Opciones para Iniciar el Juego

### 1. Modo Normal (con pantalla de configuración)
```
uv run python -m pgzero main.py
```
En este modo, inicias en la pantalla de configuración donde puedes ajustar parámetros y ver/modificar los obstáculos. Para comenzar el juego:
- Haz clic en el botón "Iniciar Juego" 
- O presiona la tecla Enter

### 2. Modo Directo (sin configuración)
```
uv run python -m pgzero jugar_directo.py
```
Este modo inicia el juego inmediatamente sin pasar por la pantalla de configuración.

## Controles del Juego

- **↑** : Mover el carrito hacia abajo un carril
- **↓** : Mover el carrito hacia arriba un carril
- **Espacio** : Hacer que el carrito salte
- **P** : Pausar/reanudar el juego
- **T** : Mostrar/ocultar visualización del árbol AVL
- **H** : Mostrar/ocultar hitboxes (modo debug)
- **B** : Mostrar recorrido en anchura (breadth-first) del árbol AVL
- **D** : Mostrar recorrido en profundidad (depth-first) del árbol AVL
- **Escape** : Volver a la pantalla de configuración o pausar

## Objetivo del Juego

El objetivo es recorrer toda la distancia configurada evitando los obstáculos que aparecen en la carretera. Puedes cambiar de carril o saltar para evitarlos. ¡Cuidado! El carrito pierde energía constantemente mientras avanza, por lo que debes llegar al final antes de quedarte sin energía.

## Pantalla de Configuración

En la pantalla de configuración puedes:
- Cambiar la distancia total del juego
- Modificar la velocidad del carrito
- Ajustar la energía inicial
- Ver y modificar los obstáculos

## Funcionalidades Especiales

- **Visualización del Árbol AVL**: Durante el juego puedes ver la estructura del árbol AVL que organiza los obstáculos. Los nodos resaltados corresponden a los obstáculos actualmente visibles en pantalla. El factor de balance (FB) se muestra en cada nodo, con colores diferentes según su valor:
  - Verde (FB=0): Nodo perfectamente balanceado
  - Amarillo (FB=-1 o FB=1): Nodo ligeramente desequilibrado pero dentro del límite AVL
  - Rojo (FB<-1 o FB>1): Nodo desbalanceado (temporal durante rotaciones)

- **Recorridos del Árbol**: 
  - Presiona **B** para ver el recorrido en anchura (breadth-first)
  - Presiona **D** para ver el recorrido en profundidad (depth-first)

- **Modo Debug (Hitboxes)**: Presiona **H** para ver las cajas de colisión del carrito y los obstáculos

- **Sistema de Energía**: El carrito pierde energía gradualmente mientras avanza. La velocidad de consumo es proporcional a la velocidad del carrito.

- **Sistema de Puntuación**:
  - Gana puntos automáticamente por distancia recorrida
  - Gana puntos extra por obstáculos evitados exitosamente (5 puntos por obstáculo)
  - Pierde puntos al colisionar con obstáculos (según el daño del obstáculo)

- **Actualización en tiempo real**: Observa cómo el árbol AVL se actualiza dinámicamente mientras juegas, destacando los obstáculos que están cerca del carrito y mostrando las rotaciones cuando ocurren.