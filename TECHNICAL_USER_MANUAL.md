# TECHNICAL AND USER MANUAL
## Dynamic Obstacle Cart Game using AVL Tree

**Version:** 1.0  
**Date:** September 2025  
**Authors:** Data Structures Project Team  
**Framework:** Pygame Zero  
**Language:** Python 3.12+

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [Technical Documentation](#2-technical-documentation)
3. [Installation Guide](#3-installation-guide)
4. [User Manual](#4-user-manual)
5. [Gameplay Guide](#5-gameplay-guide)
6. [Configuration Manual](#6-configuration-manual)
7. [Troubleshooting](#7-troubleshooting)
8. [Developer Guide](#8-developer-guide)
9. [Technical Specifications](#9-technical-specifications)

---

## 1. PROJECT OVERVIEW

### 1.1 Description
The **Dynamic Obstacle Cart Game** is an educational project that demonstrates the practical implementation of an **AVL Tree** data structure. Players control a cart that navigates through a dynamic environment filled with obstacles, where the AVL tree efficiently manages obstacle queries and automatic cleanup based on the cart's position.

### 1.2 Key Features
- **6-Lane Highway System**: Navigate through 3 upper lanes and 3 lower lanes
- **AVL Tree-Based Obstacle Management**: Efficient insertion, search, and deletion operations
- **Dynamic Obstacle Types**: 5 different obstacle types with unique properties
- **Intelligent Collision System**: Jump over barriers, avoid other obstacles
- **Real-time Visualization**: Optional AVL tree visualization during gameplay
- **Configuration Interface**: Modify game parameters and obstacle placement
- **Automatic Cleanup**: Passed obstacles are automatically removed from the AVL tree

### 1.3 Educational Objectives
- Demonstrate AVL tree operations in a real-world scenario
- Show efficient range queries for obstacle detection
- Illustrate automatic balancing and tree maintenance
- Provide visual feedback of tree structure and traversals

---

## 2. TECHNICAL DOCUMENTATION

### 2.1 System Architecture

```
main.py                 # Entry point with Pygame Zero
├── logic/              # Pure game logic (no graphics)
│   ├── arbol_avl.py   # ⭐ Main data structure (AVL Tree)
│   ├── carrito.py     # Player cart logic and state
│   ├── obstaculo.py   # Obstacle entity and types
│   └── gestor_juego.py # Game coordinator and state manager
├── view/               # Graphical interfaces
│   ├── pantalla_configuracion.py # Configuration screen
│   ├── pantalla_juego.py         # Main game screen
│   ├── visualizador_arbol.py     # AVL tree visualizer
│   └── components/               # UI components
├── data/
│   └── configuracion.json        # Game configuration
└── images/                       # Game assets
    ├── carrito.png
    ├── obstaculos/
    └── hazzards/
```

### 2.2 Core Components

#### 2.2.1 AVL Tree Implementation (`arbol_avl.py`)
- **Purpose**: Manages obstacles with automatic balancing
- **Key Operations**:
  - `insertar(obstaculo)`: O(log n) insertion with balancing
  - `buscar_en_rango(x_min, x_max, y_min, y_max)`: Efficient range queries
  - `eliminar_obstaculos_en_rango()`: Batch deletion for cleanup
  - `obtener_recorrido_anchura()`: Breadth-first traversal
  - `obtener_recorrido_profundidad()`: Depth-first traversal

#### 2.2.2 Game Manager (`gestor_juego.py`)
- **Purpose**: Coordinates all game components and state
- **Key Functions**:
  - State management (Configuration, Playing, Paused, Game Over)
  - Obstacle visibility calculation using AVL tree queries
  - Collision detection and processing
  - Score and energy management
  - Automatic obstacle cleanup

#### 2.2.3 Cart Entity (`carrito.py`)
- **Purpose**: Player entity with movement and state
- **Features**:
  - 6-lane movement system (lanes 0-5)
  - Jump mechanics for barrier avoidance
  - Energy and collision state management
  - Smooth movement with boundary checking

#### 2.2.4 Obstacle System (`obstaculo.py`)
- **Purpose**: Defines obstacle types and properties
- **Obstacle Types**:
  - **Rock**: 20 damage, blocks movement
  - **Cone**: 10 damage, standard obstacle
  - **Hole**: 15 damage, ground hazard
  - **Oil**: 5 damage, slippery surface
  - **Barrier**: 25 damage, 2-lane height, jumpable

### 2.3 Data Flow

1. **Initialization**: Load configuration from JSON
2. **Configuration Phase**: Modify obstacles and game parameters
3. **Game Start**: Initialize cart and populate AVL tree
4. **Game Loop**:
   - Update cart position
   - Query AVL tree for visible obstacles
   - Check collisions
   - Remove passed obstacles
   - Update display
5. **Cleanup**: Automatic obstacle removal based on cart position

---

## 3. INSTALLATION GUIDE

### 3.1 System Requirements

**Minimum Requirements:**
- Python 3.12 or higher
- 4 GB RAM
- 100 MB free disk space
- Display resolution: 800x600 or higher

**Recommended:**
- Python 3.13
- 8 GB RAM
- Graphics support for smooth rendering

### 3.2 Installation Methods

#### Method 1: Using UV (Recommended)
```bash
# Clone the repository
git clone https://github.com/karen050521/Proyecto-EstructuraDeDatos.git
cd Proyecto-EstructuraDeDatos

# Install dependencies
uv sync

# Run the game
uv run python -m pgzero main.py
```

#### Method 2: Using PIP
```bash
# Clone the repository
git clone https://github.com/karen050521/Proyecto-EstructuraDeDatos.git
cd Proyecto-EstructuraDeDatos

# Install dependencies
pip install pgzero pygame

# Run the game
python -m pgzero main.py
```

#### Method 3: Direct Python Execution
```bash
# Install pygame-zero
pip install pgzero>=1.2.1 pygame>=2.0.0

# Run the game
python -m pgzero main.py
```

### 3.3 Verification
After installation, you should see:
1. A window titled "Carrito con Obstaculos Dinamicos - Arbol AVL"
2. Configuration screen with obstacle management controls
3. Debug information showing "Estado: configuracion"

---

## 4. USER MANUAL

### 4.1 Starting the Game

1. **Execute the game** using one of the installation methods above
2. **Configuration screen appears** - this is the initial state
3. **Review current obstacles** in the tree visualization
4. **Click "🚀 INICIAR JUEGO"** or **press ENTER** to start playing

### 4.2 Main Interface Elements

#### 4.2.1 Configuration Screen
- **Tree Visualization**: Shows current AVL tree structure
- **Obstacle Controls**: Add/remove obstacles
- **Game Parameters**: Modify energy and damage settings
- **Traversal Buttons**: View tree traversals
- **Start Game Button**: Begin playing

#### 4.2.2 Game Screen
- **6-Lane Highway**: 3 upper lanes (3,4,5) and 3 lower lanes (0,1,2)
- **Cart**: Player-controlled vehicle
- **Obstacles**: Various hazards with different properties
- **HUD**: Energy, score, distance, and debug information
- **Tree Visualization** (Optional): Real-time AVL tree display

### 4.3 Game Controls

#### Basic Movement
- **↑ (Up Arrow)**: Move to lower lane
- **↓ (Down Arrow)**: Move to upper lane
- **SPACE**: Jump (avoids barriers only)

#### Game Management
- **ESC**: Return to configuration / Exit game
- **P**: Pause game
- **T**: Toggle AVL tree visualization
- **H**: Toggle hitbox display (debug mode)

#### Tree Traversals (During Gameplay)
- **B**: Start breadth-first traversal visualization
- **D**: Start depth-first traversal visualization

### 4.4 Scoring System
- **+5 points** for each obstacle successfully passed
- **-[damage] points** for each collision
- **Energy loss** based on obstacle type
- **Game ends** when energy reaches 0

---

## 5. GAMEPLAY GUIDE

### 5.1 Objective
Navigate your cart through the highway while avoiding obstacles. The goal is to achieve the highest score possible by traveling the maximum distance without losing all your energy.

### 5.2 Lane System
The highway consists of **6 lanes** arranged as:
```
Upper Section: [Lane 5] [Lane 4] [Lane 3]
==== YELLOW DIVIDER ====
Lower Section: [Lane 2] [Lane 1] [Lane 0]
```

### 5.3 Obstacle Types and Strategies

#### 5.3.1 Rock (🗿)
- **Damage**: 20 points
- **Strategy**: Move to adjacent lane to avoid
- **Visual**: Brown circular obstacle

#### 5.3.2 Traffic Cone (🧡)
- **Damage**: 10 points  
- **Strategy**: Easy to avoid, good for practicing movement
- **Visual**: Orange triangular cone

#### 5.3.3 Hole (🕳️)
- **Damage**: 15 points
- **Strategy**: Cannot be jumped over, must change lanes
- **Visual**: Black circular hazard

#### 5.3.4 Oil Spill (🛢️)
- **Damage**: 5 points
- **Strategy**: Lowest damage, sometimes acceptable to hit
- **Visual**: Dark gray irregular shape

#### 5.3.5 Barrier (🚧)
- **Damage**: 25 points
- **Height**: Occupies 2 lane heights
- **Strategy**: **JUMP OVER** using SPACE key or change lanes
- **Visual**: Red and white striped barrier with reflectors

### 5.4 Advanced Techniques

#### 5.4.1 Lane Management
- Plan ahead using the tree visualization
- Keep track of upcoming obstacles
- Use the middle lanes (2,3) for maximum maneuverability

#### 5.4.2 Jumping Strategy
- Jump timing is crucial for barriers
- Only barriers can be jumped over
- Other obstacles will still cause collision even when jumping

#### 5.4.3 Score Optimization
- Minimize collisions to preserve score
- Focus on distance rather than risky maneuvers
- Use oil spills strategically (lowest damage) when necessary

---

## 6. CONFIGURATION MANUAL

### 6.1 Obstacle Management

#### 6.1.1 Adding Obstacles
1. **Position X Field**: Enter horizontal position (0-5000)
2. **Lane Y Field**: Select lane (0-5)
3. **Type Selector**: Choose obstacle type
4. **Click "➕ AGREGAR"**: Add to AVL tree

#### 6.1.2 Using Counter Buttons
- **+/- buttons**: Increment/decrement values quickly
- **Position X**: Adjust in steps of 50
- **Lane Y**: Cycle through lanes 0-5

#### 6.1.3 Obstacle Validation
The system automatically validates:
- X position must be ≥ 0
- Y position must be 0-5
- Duplicate positions are prevented

### 6.2 Tree Traversals

#### 6.2.1 Breadth-First Traversal
- **Click "🔍 ANCHURA"**: Start breadth-first visualization
- Shows level-by-level tree exploration
- Useful for understanding tree structure

#### 6.2.2 Depth-First Traversal  
- **Click "📊 PROFUNDIDAD"**: Start depth-first visualization
- Shows in-order traversal (sorted order)
- Demonstrates AVL tree sorting property

### 6.3 Configuration File

#### 6.3.1 JSON Structure (`data/configuracion.json`)
```json
{
    "obstaculos": [
        {
            "x": 300,
            "y": 0,
            "tipo": "roca",
            "daño": 20
        }
    ],
    "configuracion_juego": {
        "energia_inicial": 100,
        "velocidad_carrito": 8,
        "dano_por_tipo": {
            "roca": 20,
            "cono": 10,
            "hueco": 15,
            "aceite": 5,
            "barrera": 25
        }
    }
}
```

#### 6.3.2 Modifying Configuration
1. **Edit `data/configuracion.json`** with a text editor
2. **Restart the game** to load changes
3. **Or use the configuration interface** for real-time changes

---

## 7. TROUBLESHOOTING

### 7.1 Common Issues

#### 7.1.1 Game Won't Start
**Problem**: "The term 'uv' is not recognized"
```bash
# Solution: Use pip instead
pip install pgzero pygame
python -m pgzero main.py
```

**Problem**: "Module not found" errors
```bash
# Solution: Install missing dependencies
pip install pgzero>=1.2.1 pygame>=2.0.0
```

#### 7.1.2 Configuration Issues
**Problem**: Start button doesn't work
- **Check**: Button position is within the control area
- **Fix**: The button was automatically repositioned in recent updates

**Problem**: Obstacles not appearing
- **Check**: X position is within visible range (0-5000)
- **Check**: AVL tree has obstacles loaded
- **Fix**: Add obstacles using the configuration interface

#### 7.1.3 Performance Issues
**Problem**: Game runs slowly
- **Solution**: Disable tree visualization with 'T' key
- **Solution**: Reduce window size or resolution
- **Solution**: Close other applications

#### 7.1.4 Gameplay Issues
**Problem**: Can't jump over barriers
- **Check**: Press SPACE while approaching the barrier
- **Check**: Cart must be in jumping state
- **Note**: Only barriers can be jumped over

**Problem**: Controls feel inverted
- **Note**: UP arrow moves to lower-numbered lanes (down on screen)
- **Note**: DOWN arrow moves to higher-numbered lanes (up on screen)

### 7.2 Debug Mode

#### 7.2.1 Enabling Debug Features
- **H key**: Toggle hitbox visualization
- **T key**: Toggle tree visualization
- **Debug text**: Always visible in top-left corner

#### 7.2.2 Debug Information
- Current game state
- Cart position and lane
- Total obstacles in tree
- Collision detection results
- Tree operation results

### 7.3 Log Analysis

#### 7.3.1 Normal Operation Logs
```
Juego inicializado correctamente
Estado inicial: Configuracion
Total de obstáculos en el árbol: 30
```

#### 7.3.2 Error Logs
```
❌ Error cargando imágenes: [error details]
⚠️ Imagen no encontrada: [image path]
```

---

## 8. DEVELOPER GUIDE

### 8.1 Code Structure

#### 8.1.1 Separation of Concerns
- **`logic/`**: Pure Python logic, no graphics dependencies
- **`view/`**: Pygame Zero interface components
- **`data/`**: Configuration and game data
- **`images/`**: Visual assets

#### 8.1.2 Key Design Patterns
- **State Pattern**: Game states (Configuration, Playing, Paused)
- **Observer Pattern**: UI updates based on game state changes
- **Strategy Pattern**: Different obstacle behaviors
- **Factory Pattern**: Obstacle creation from JSON data

### 8.2 AVL Tree Implementation

#### 8.2.1 Node Structure (`nodo_avl.py`)
```python
class NodoAVL:
    def __init__(self, obstaculo: Obstaculo):
        self.obstaculo = obstaculo
        self.altura = 1
        self.izquierda = None
        self.derecha = None
```

#### 8.2.2 Tree Operations (`arbol_avl.py`)
- **Insertion**: Maintains balance after every insert
- **Range Queries**: Efficiently finds obstacles in view range
- **Deletion**: Batch removal for performance
- **Balancing**: Automatic rotations maintain O(log n) height

### 8.3 Extension Points

#### 8.3.1 Adding New Obstacle Types
1. **Add to `TipoObstaculo` enum**
2. **Define damage in `DAÑO_POR_TIPO`**
3. **Create visual assets**
4. **Update configuration interface**

#### 8.3.2 Adding New Game Mechanics
1. **Extend `EstadoCarrito` for new states**
2. **Modify collision detection in `gestor_juego.py`**
3. **Update UI in `pantalla_juego.py`**

### 8.4 Performance Considerations

#### 8.4.1 AVL Tree Optimization
- Batch operations for better performance
- Range queries instead of individual searches
- Lazy deletion for non-critical cleanup

#### 8.4.2 Rendering Optimization
- Only render visible obstacles
- Image caching and scaling
- Optional tree visualization to reduce overhead

---

## 9. TECHNICAL SPECIFICATIONS

### 9.1 Algorithm Complexity

#### 9.1.1 AVL Tree Operations
- **Insert**: O(log n)
- **Search**: O(log n)
- **Delete**: O(log n)
- **Range Query**: O(log n + k) where k = number of results
- **Traversal**: O(n)

#### 9.1.2 Game Operations
- **Collision Detection**: O(k) where k = visible obstacles
- **Obstacle Cleanup**: O(m log n) where m = obstacles to remove
- **Frame Update**: O(k + log n)

### 9.2 Memory Requirements

#### 9.2.1 Data Structures
- **AVL Tree**: O(n) where n = total obstacles
- **Visible Obstacles**: O(k) where k ≤ screen width / obstacle width
- **Image Assets**: ~500KB total
- **Game State**: O(1)

### 9.2.2 Performance Metrics
- **Target FPS**: 60
- **Maximum Obstacles**: 5000+
- **Memory Usage**: <100MB typical
- **Startup Time**: <3 seconds

### 9.3 File Formats

#### 9.3.1 Configuration (JSON)
- UTF-8 encoding
- Standard JSON format
- Validation on load
- Error reporting for malformed data

#### 9.3.2 Images (PNG)
- RGBA format with transparency
- Multiple sizes (30x30 to 60x100)
- Automatic scaling during runtime

### 9.4 Dependencies

#### 9.4.1 Required
- **Python**: 3.12+ (confirmed working on 3.13)
- **pygame-zero**: ≥1.2.1
- **pygame**: ≥2.0.0

#### 9.4.2 Optional
- **uv**: For dependency management
- **pytest**: For running test suite

---

## APPENDIX A: CONFIGURATION REFERENCE

### A.1 Complete JSON Schema
```json
{
    "obstaculos": [
        {
            "x": <integer 0-5000>,
            "y": <integer 0-5>,
            "tipo": <"roca"|"cono"|"hueco"|"aceite"|"barrera">,
            "daño": <integer>
        }
    ],
    "configuracion_juego": {
        "energia_inicial": <integer 1-200>,
        "velocidad_carrito": <integer 1-20>,
        "dano_por_tipo": {
            "roca": <integer>,
            "cono": <integer>,
            "hueco": <integer>,
            "aceite": <integer>,
            "barrera": <integer>
        }
    }
}
```

### A.2 Default Values
- **Energy**: 100
- **Speed**: 8
- **Damage**: Rock(20), Cone(10), Hole(15), Oil(5), Barrier(25)

---

## APPENDIX B: KEYBOARD REFERENCE

### B.1 All Controls
| Key | Action | Context |
|-----|--------|---------|
| ↑ | Move to lower lane | Game |
| ↓ | Move to upper lane | Game |
| SPACE | Jump (barriers only) | Game |
| ESC | Exit/Return to config | Always |
| P | Pause/Unpause | Game |
| T | Toggle tree visualization | Game |
| H | Toggle hitbox display | Game |
| B | Breadth-first traversal | Game |
| D | Depth-first traversal | Game |
| ENTER | Start game | Configuration |

---

## APPENDIX C: ERROR CODES

### C.1 System Errors
- **E001**: Python version incompatible
- **E002**: Missing pygame-zero
- **E003**: Configuration file corrupted

### C.2 Game Errors
- **G001**: Invalid obstacle position
- **G002**: AVL tree operation failed
- **G003**: Image loading failed

---

**© 2025 Data Structures Project Team. This manual covers version 1.0 of the Dynamic Obstacle Cart Game.**