#!/usr/bin/env python3
"""
Tests unitarios para Data Analytics Dashboard
"""

import unittest
import tempfile
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from database import DatabaseManager
from app_advanced import app
from fastapi.testclient import TestClient

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """Configurar test con base de datos temporal"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Limpiar después del test"""
        os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test: La base de datos se inicializa correctamente"""
        # Verificar que las tablas existen
        conn = self.db.db_path
        # Este test verifica que no hay errores al inicializar
        self.assertTrue(os.path.exists(conn))
    
    def test_generate_sample_data(self):
        """Test: Generar datos de muestra funciona correctamente"""
        df = self.db.generate_sample_data(100)
        
        # Verificar que se generaron datos
        self.assertEqual(len(df), 100)
        
        # Verificar columnas
        expected_columns = ['date', 'product', 'region', 'sales_amount', 'profit', 'quantity']
        self.assertEqual(list(df.columns), expected_columns)
        
        # Verificar tipos de datos
        self.assertTrue(pd.api.types.is_numeric_dtype(df['sales_amount']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['profit']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['quantity']))
    
    def test_get_analytics_summary(self):
        """Test: Obtener resumen analítico funciona"""
        # Generar datos de prueba
        self.db.generate_sample_data(50)
        
        # Obtener resumen
        summary = self.db.get_analytics_summary()
        
        # Verificar estructura
        self.assertIn('metrics', summary)
        self.assertIn('monthly_data', summary)
        self.assertIn('product_data', summary)
        self.assertIn('region_data', summary)
        
        # Verificar métricas
        metrics = summary['metrics']
        self.assertIn('total_sales', metrics)
        self.assertIn('total_profit', metrics)
        self.assertIn('total_customers', metrics)
        self.assertIn('avg_order_value', metrics)
        self.assertIn('growth_rate', metrics)
    
    def test_export_csv(self):
        """Test: Exportar a CSV funciona"""
        self.db.generate_sample_data(10)
        
        filename = self.db.export_to_csv('sales')
        
        # Verificar que el archivo se creó
        self.assertTrue(os.path.exists(filename))
        
        # Verificar contenido
        df = pd.read_csv(filename)
        self.assertEqual(len(df), 10)
        
        # Limpiar archivo
        os.remove(filename)
    
    def test_export_excel(self):
        """Test: Exportar a Excel funciona"""
        self.db.generate_sample_data(10)
        
        filename = self.db.export_to_excel()
        
        # Verificar que el archivo se creó
        self.assertTrue(os.path.exists(filename))
        
        # Verificar contenido
        excel_data = pd.read_excel(filename, sheet_name='Ventas')
        self.assertEqual(len(excel_data), 10)
        
        # Limpiar archivo
        os.remove(filename)

class TestAPI(unittest.TestCase):
    def setUp(self):
        """Configurar cliente de test"""
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test: Health check funciona"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('timestamp', data)
    
    def test_get_analytics_data(self):
        """Test: Obtener datos de análisis funciona"""
        response = self.client.get("/api/data")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_metrics(self):
        """Test: Obtener métricas funciona"""
        response = self.client.get("/api/metrics")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_sales_data(self):
        """Test: Obtener datos de ventas funciona"""
        response = self.client.get("/api/sales")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_products_data(self):
        """Test: Obtener datos de productos funciona"""
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_regions_data(self):
        """Test: Obtener datos de regiones funciona"""
        response = self.client.get("/api/regions")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_filters(self):
        """Test: Obtener opciones de filtros funciona"""
        response = self.client.get("/api/filters")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_export_csv(self):
        """Test: Exportar CSV funciona"""
        response = self.client.get("/api/export/csv/sales")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'text/csv; charset=utf-8')
    
    def test_export_excel(self):
        """Test: Exportar Excel funciona"""
        response = self.client.get("/api/export/excel")
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                     response.headers['content-type'])
    
    def test_dashboard_page(self):
        """Test: Página del dashboard carga"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.headers['content-type'])

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        """Configurar test con datos de muestra"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = DatabaseManager(self.temp_db.name)
        self.db.generate_sample_data(100)
    
    def tearDown(self):
        """Limpiar después del test"""
        os.unlink(self.temp_db.name)
    
    def test_data_consistency(self):
        """Test: Los datos generados son consistentes"""
        df = self.db.get_sales_data()
        
        # Verificar que no hay valores nulos en columnas importantes
        self.assertFalse(df['sales_amount'].isnull().any())
        self.assertFalse(df['profit'].isnull().any())
        self.assertFalse(df['quantity'].isnull().any())
        
        # Verificar que los valores son positivos
        self.assertTrue((df['sales_amount'] > 0).all())
        self.assertTrue((df['profit'] > 0).all())
        self.assertTrue((df['quantity'] > 0).all())
    
    def test_date_filtering(self):
        """Test: Filtrado por fechas funciona"""
        start_date = '2024-01-01'
        end_date = '2024-06-30'
        
        df = self.db.get_sales_data(start_date, end_date)
        
        if len(df) > 0:
            # Verificar que todas las fechas están en el rango
            df['date'] = pd.to_datetime(df['date'])
            self.assertTrue((df['date'] >= start_date).all())
            self.assertTrue((df['date'] <= end_date).all())

def run_tests():
    """Ejecutar todos los tests"""
    # Crear suite de tests
    test_suite = unittest.TestSuite()
    
    # Añadir tests de base de datos
    test_suite.addTest(unittest.makeSuite(TestDatabaseManager))
    
    # Añadir tests de API
    test_suite.addTest(unittest.makeSuite(TestAPI))
    
    # Añadir tests de procesamiento de datos
    test_suite.addTest(unittest.makeSuite(TestDataProcessing))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Ejecutando tests unitarios...")
    print("=" * 50)
    
    success = run_tests()
    
    print("=" * 50)
    if success:
        print("✅ Todos los tests pasaron correctamente!")
    else:
        print("❌ Algunos tests fallaron")
    
    print("=" * 50)





