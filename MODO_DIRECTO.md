# 🚀 Modo de Juego Directo

Este archivo describe cómo utilizar el modo de juego directo, que te permite saltarte la pantalla de configuración e iniciar directamente el juego.

## Cómo Ejecutar el Modo Directo

```bash
# Usar Pygame Zero para ejecutar directamente el juego
python -m pgzero jugar_directo.py
```

## ¿Qué es el Modo Directo?

El modo directo es una forma alternativa de iniciar el juego que:

1. **Salta la configuración** - Inicia directamente en modo de juego
2. **Carga configuración predeterminada** - Usa los valores del archivo `data/configuracion.json`
3. **Enfoque en jugar** - Perfecto para pruebas rápidas o demostraciones

## Controles en Modo Directo

- **↑ / ↓**: Mover el carrito entre carriles
- **Espacio**: Saltar
- **P**: Pausar/Reanudar juego
- **T**: Mostrar/ocultar árbol AVL
- **H**: Mostrar/ocultar hitboxes (modo debug)
- **ESC**: Pausar/Salir

## Diferencias con el Modo Normal

| Característica | Modo Normal | Modo Directo |
|----------------|-------------|--------------|
| Pantalla inicial | Configuración | Juego |
| Modificar obstáculos | ✅ Sí | ❌ No |
| Personalizar árbol | ✅ Sí | ❌ No |
| Tiempo para jugar | ⏱️ Más lento | ⚡ Más rápido |

## Solución de Problemas

Si encuentras problemas al ejecutar el modo directo:

1. Asegúrate de tener pygame-zero instalado
2. Verifica que estás usando la sintaxis correcta para ejecutar
3. Confirma que todos los archivos del proyecto están presentes

## Código Fuente

El archivo `jugar_directo.py` contiene una versión simplificada del bucle principal del juego, que inicializa el gestor de juego y cambia directamente al estado `JUGANDO` sin pasar por la pantalla de configuración.