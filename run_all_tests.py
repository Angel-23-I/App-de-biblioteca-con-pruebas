"""Script para ejecutar todos los niveles de pruebas"""
import unittest
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """Ejecuta todas las suites de pruebas"""
    
    # Crear test loader
    loader = unittest.TestLoader()
    
    # Crear test suite
    suite = unittest.TestSuite()
    
    # Cargar pruebas de cada nivel
    print("=" * 70)
    print("EJECUTANDO TODAS LAS PRUEBAS DEL SISTEMA DE BIBLIOTECA")
    print("=" * 70)
    
    print("\n1. Pruebas Unitarias...")
    suite.addTests(loader.discover('tests', pattern='test_unitarias.py'))
    
    print("2. Pruebas de Integración...")
    suite.addTests(loader.discover('tests', pattern='test_integracion.py'))
    
    print("3. Pruebas de Sistema...")
    suite.addTests(loader.discover('tests', pattern='test_sistema.py'))
    
    print("4. Pruebas de Aceptación...")
    suite.addTests(loader.discover('tests', pattern='test_aceptacion.py'))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE PRUEBAS")
    print("=" * 70)
    print(f"Total de pruebas ejecutadas: {result.testsRun}")
    print(f"Pruebas exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Pruebas fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
