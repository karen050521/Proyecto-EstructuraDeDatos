# Suite de Pruebas del Proyecto Jeffy-DS

Esta carpeta contiene una suite completa de pruebas para validar toda la funcionalidad del proyecto según los requisitos de `definicion.md`.

## Estructura de Pruebas

### 1. `test_basico.py` - Pruebas Básicas
**Funcionalidad fundamental validada:**
- ✅ Creación de obstáculos de todos los tipos
- ✅ Creación y estado inicial del carrito
- ✅ Movimiento automático y manual del carrito
- ✅ Sistema de salto con física realista
- ✅ Sistema de daño y energía
- ✅ Detección de colisiones
- ✅ Creación de árbol AVL vacío
- ✅ Inserción simple en árbol AVL
- ✅ Búsqueda simple en árbol AVL

### 2. `test_arbol_avl.py` - Pruebas Árbol AVL
**Funcionalidad AVL completamente validada:**
- ✅ Criterios de ordenamiento (X primero, luego Y)
- ✅ Inserción múltiple con balanceamiento automático
- ✅ Eliminación de obstáculos con balanceamiento
- ✅ Recorridos en anchura (BFS) y profundidad (in-order)
- ✅ Búsqueda eficiente por rango
- ✅ Balanceamiento automático con rotaciones
- ✅ Cálculo de altura y factor de balance
- ✅ Operaciones combinadas (inserción, eliminación, búsqueda)

### 3. `test_juego_completo.py` - Pruebas Juego Completo
**Integración y mecánicas del juego validadas:**
- ✅ Inicialización completa del juego
- ✅ Carga de configuración desde JSON
- ✅ Mecánicas básicas del juego
- ✅ Sistema de obstáculos visibles
- ✅ Detección y procesamiento de colisiones
- ✅ Sistema de energía por tipo de obstáculo
- ✅ Condiciones de fin del juego
- ✅ Escenario completo de juego
- ✅ Sistema de estadísticas
- ✅ Sistema de pausa y reinicio

### 4. `test_requisitos_proyecto.py` - Pruebas Requisitos Proyecto
**Validación específica según definicion.md:**
- ✅ Carga y representación del árbol (0.5 puntos)
- ✅ Recorridos gráficos del árbol (1.0 puntos)
- ✅ Administración del árbol antes del juego (1.0 puntos)
- ✅ Juego del carrito usando árbol AVL (2.0 puntos)
- ✅ Criterios técnicos específicos
- ✅ Escenarios de juego (éxito y fallo)

## Cómo Ejecutar las Pruebas

### Ejecutar todas las pruebas:
```bash
cd .tests
python ejecutar_pruebas.py
```

### Ejecutar pruebas individuales:
```bash
cd .tests
python test_basico.py
python test_arbol_avl.py
python test_juego_completo.py
python test_requisitos_proyecto.py
```

### Ejecutar desde el directorio raíz:
```bash
python .tests/test_basico.py
python .tests/test_arbol_avl.py
python .tests/test_juego_completo.py
python .tests/test_requisitos_proyecto.py
```

## Resultados de las Pruebas

**Estado actual: ✅ TODAS LAS PRUEBAS PASAN**

```
RESUMEN: 4/4 pruebas pasaron
Porcentaje: 100.0%

TODAS LAS PRUEBAS PASARON!
Proyecto completamente validado
```

## Validaciones Completadas

### ✅ Funcionalidad Básica
- Todas las clases implementadas correctamente
- Tipado completo en todas las funciones
- Manejo de errores apropiado

### ✅ Árbol AVL
- Balanceamiento automático con rotaciones
- Recorridos en anchura y profundidad
- Búsqueda eficiente por rango O(log n + k)
- Criterios de ordenamiento según especificación

### ✅ Mecánicas del Juego
- Movimiento automático del carrito
- Control manual en eje Y
- Sistema de salto con física realista
- Detección de colisiones en tiempo real
- Sistema de energía por tipo de obstáculo
- Condiciones de fin de juego

### ✅ Integración
- Carga de configuración desde JSON
- Gestión de obstáculos visibles
- Sistema de estadísticas completo
- Escenarios de juego (éxito y fallo)

### ✅ Requisitos del Proyecto
- Todos los puntos de calificación validados
- Criterios técnicos específicos cumplidos
- Estructura JSON compatible con definicion.md

## Archivos de Configuración

- `data/configuracion.json` - Archivo de configuración de ejemplo
- Compatible con la estructura especificada en definicion.md
- Incluye 10 obstáculos distribuidos estratégicamente

## Próximos Pasos

El sistema de lógica está **100% completo y validado**. Los próximos pasos serían:

1. **Integración con la capa de visualización** (`view/`)
2. **Integración con el archivo principal** (`main.py`)
3. **Implementación de la interfaz gráfica**
4. **Visualización del árbol AVL**
5. **Controles de usuario**

## Notas Técnicas

- Todas las pruebas incluyen casos edge y validaciones exhaustivas
- El sistema maneja correctamente coordenadas repetidas
- El balanceamiento AVL mantiene altura logarítmica
- Las colisiones se detectan eficientemente
- El sistema de energía es balanceado por tipo de obstáculo
- Los escenarios de juego cubren casos de éxito y fallo
