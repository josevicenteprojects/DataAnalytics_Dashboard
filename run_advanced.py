#!/usr/bin/env python3
"""
Script de inicio avanzado para Data Analytics Dashboard
Incluye opciones para desarrollo, testing y producción
"""

import subprocess
import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Data Analytics Dashboard - Advanced')
    parser.add_argument('--mode', choices=['dev', 'test', 'prod'], default='dev',
                       help='Modo de ejecución (dev/test/prod)')
    parser.add_argument('--port', type=int, default=8002,
                       help='Puerto para ejecutar la aplicación')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("    Data Analytics Dashboard - Advanced Version")
    print("=" * 60)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app_advanced.py"):
        print("❌ Error: No se encuentra app_advanced.py")
        print("Asegurate de estar en el directorio correcto")
        return
    
    if args.mode == 'test':
        print("Modo: Testing")
        print("Ejecutando tests unitarios...")
        print()
        
        try:
            result = subprocess.run([sys.executable, "test_app.py"], check=True)
            print("Tests completados exitosamente")
        except subprocess.CalledProcessError as e:
            print(f"Error en tests: {e}")
            return
        except FileNotFoundError:
            print("Error: No se encuentra test_app.py")
            return
    
    elif args.mode == 'prod':
        print("Modo: Produccion")
        print("Iniciando con Docker...")
        print()
        
        try:
            subprocess.run(["docker-compose", "up", "--build"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error con Docker: {e}")
            print("Asegurate de tener Docker instalado")
            return
        except FileNotFoundError:
            print("Error: Docker no esta instalado")
            return
    
    else:  # dev mode
        print("Modo: Desarrollo")
        print("Instalando dependencias...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True, capture_output=True)
            print("Dependencias instaladas correctamente")
        except subprocess.CalledProcessError as e:
            print(f"Error instalando dependencias: {e}")
            return
        
        print()
        print("Iniciando servidor...")
        print()
        print("Dashboard: http://localhost:8002")
        print("API Docs: http://localhost:8002/docs")
        print("Health Check: http://localhost:8002/health")
        print()
        print("Caracteristicas avanzadas:")
        print("  • Base de datos SQLite con pandas")
        print("  • Filtros dinamicos")
        print("  • Exportacion CSV/Excel")
        print("  • Analisis de tendencias")
        print("  • Tests unitarios")
        print()
        print("Presiona Ctrl+C para detener el servidor")
        print("=" * 60)
        print()
        
        # Ejecutar la aplicación
        try:
            subprocess.run([sys.executable, "app_advanced.py"], check=True)
        except KeyboardInterrupt:
            print("\nServidor detenido")
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando la aplicacion: {e}")

if __name__ == "__main__":
    main()
