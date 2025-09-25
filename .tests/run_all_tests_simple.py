#!/usr/bin/env python3
"""
Ejecutor de todas las pruebas - Versión simple sin emojis para Windows
Ejecuta todas las suites de pruebas en orden
"""

import sys
import os
import subprocess
import time


def run_test_suite(test_file, description):
    """Ejecuta una suite de pruebas y reporta el resultado"""
    print(f"\n{'=' * 60}")
    print(f"EJECUTANDO: {description}")
    print(f"Archivo: {test_file}")
    print(f"{'=' * 60}")

    try:
        # Ejecutar el archivo de pruebas
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__),
        )

        # Mostrar salida
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"PASO - {description}")
            return True
        else:
            print(f"FALLO - {description} (codigo: {result.returncode})")
            return False

    except Exception as e:
        print(f"Error ejecutando {test_file}: {e}")
        return False


def main():
    """Ejecuta todas las suites de pruebas en orden"""
    print("INICIANDO SUITE COMPLETA DE PRUEBAS")
    print("Validacion completa del proyecto segun definicion.md")
    print(f"Inicio: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Definir suites de pruebas en orden de complejidad
    test_suites = [
        ("test_basico.py", "Pruebas Basicas - Funcionalidad Fundamental"),
        ("test_arbol_avl.py", "Pruebas Arbol AVL - Funcionalidad AVL Completa"),
        ("test_juego_completo.py", "Pruebas Juego Completo - Integracion y Mecanicas"),
        (
            "test_requisitos_proyecto.py",
            "Pruebas Requisitos Proyecto - Validacion Especifica",
        ),
    ]

    results = []
    start_time = time.time()

    # Ejecutar cada suite
    for test_file, description in test_suites:
        test_path = os.path.join(os.path.dirname(__file__), test_file)

        if not os.path.exists(test_path):
            print(f"Archivo no encontrado: {test_path}")
            results.append((description, False, "Archivo no encontrado"))
            continue

        success = run_test_suite(test_path, description)
        results.append((description, success, ""))

        # Pausa entre suites
        time.sleep(1)

    # Calcular tiempo total
    end_time = time.time()
    total_time = end_time - start_time

    # Reporte final
    print(f"\n{'=' * 80}")
    print("REPORTE FINAL DE PRUEBAS")
    print(f"{'=' * 80}")
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    passed = 0
    failed = 0

    for description, success, error in results:
        status = "PASO" if success else "FALLO"
        print(f"{status} - {description}")
        if error:
            print(f"    {error}")

        if success:
            passed += 1
        else:
            failed += 1

    print()
    print(f"RESUMEN:")
    print(f"   Pruebas pasadas: {passed}")
    print(f"   Pruebas fallidas: {failed}")
    print(f"   Total: {passed + failed}")
    print(f"   Porcentaje exito: {(passed / (passed + failed) * 100):.1f}%")

    if failed == 0:
        print()
        print("TODAS LAS PRUEBAS PASARON!")
        print("El proyecto esta completamente validado")
        print("Listo para integracion con la capa de visualizacion")
        print()
        print("VALIDACIONES COMPLETADAS:")
        print("   - Funcionalidad basica de todas las clases")
        print("   - Arbol AVL con balanceamiento automatico")
        print("   - Recorridos en anchura y profundidad")
        print("   - Busqueda eficiente por rango")
        print("   - Mecanicas completas del juego")
        print("   - Sistema de colisiones y energia")
        print("   - Carga de configuracion desde JSON")
        print("   - Escenarios de juego (exito y fallo)")
        print("   - Todos los requisitos de definicion.md")

        return True
    else:
        print()
        print("ALGUNAS PRUEBAS FALLARON")
        print("Revisar los errores antes de continuar")

        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
