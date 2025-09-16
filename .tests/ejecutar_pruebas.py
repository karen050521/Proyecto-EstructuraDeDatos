#!/usr/bin/env python3
"""
Script simple para ejecutar todas las pruebas individualmente
"""

import subprocess
import sys
import os


def ejecutar_prueba(nombre_archivo):
    """Ejecuta una prueba individual"""
    print(f"\n{'=' * 60}")
    print(f"EJECUTANDO: {nombre_archivo}")
    print(f"{'=' * 60}")

    try:
        # Cambiar al directorio de las pruebas
        test_dir = os.path.dirname(__file__)
        os.chdir(test_dir)

        # Ejecutar la prueba
        result = subprocess.run(
            [sys.executable, nombre_archivo],
            capture_output=False,  # Mostrar salida directamente
            text=True,
        )

        if result.returncode == 0:
            print(f"\nPASO: {nombre_archivo}")
            return True
        else:
            print(f"\nFALLO: {nombre_archivo} (codigo: {result.returncode})")
            return False

    except Exception as e:
        print(f"Error ejecutando {nombre_archivo}: {e}")
        return False


def main():
    """Ejecuta todas las pruebas"""
    print("INICIANDO PRUEBAS DEL PROYECTO")
    print("Validacion completa segun definicion.md")

    pruebas = [
        "test_basico.py",
        "test_arbol_avl.py",
        "test_juego_completo.py",
        "test_requisitos_proyecto.py",
        "test_estres.py",
        "test_integracion_completa.py",
        "test_finales.py",
    ]

    resultados = []

    for prueba in pruebas:
        if os.path.exists(prueba):
            resultado = ejecutar_prueba(prueba)
            resultados.append((prueba, resultado))
        else:
            print(f"Archivo no encontrado: {prueba}")
            resultados.append((prueba, False))

    # Reporte final
    print(f"\n{'=' * 80}")
    print("REPORTE FINAL")
    print(f"{'=' * 80}")

    pasaron = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)

    for prueba, resultado in resultados:
        estado = "PASO" if resultado else "FALLO"
        print(f"{estado}: {prueba}")

    print(f"\nRESUMEN: {pasaron}/{total} pruebas pasaron")
    print(f"Porcentaje: {(pasaron / total * 100):.1f}%")

    if pasaron == total:
        print("\nTODAS LAS PRUEBAS PASARON!")
        print("Proyecto completamente validado")
        return True
    else:
        print(f"\n{pasaron} de {total} pruebas pasaron")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
