#!/usr/bin/env python3
"""
Database module for Data Analytics Dashboard
Manejo de base de datos SQLite con pandas
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar la base de datos con tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                product TEXT NOT NULL,
                region TEXT NOT NULL,
                sales_amount REAL NOT NULL,
                profit REAL NOT NULL,
                quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                cost REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de regiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                country TEXT NOT NULL,
                population INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_sample_data(self, num_records: int = 1000):
        """Generar datos de muestra realistas usando pandas"""
        np.random.seed(42)
        
        # Productos
        products = [
            "Laptop Pro", "Smartphone X", "Tablet Air", "Monitor 4K", 
            "Keyboard RGB", "Mouse Wireless", "Headphones Pro", "Webcam HD",
            "Speaker Bluetooth", "Charger Fast"
        ]
        
        # Regiones
        regions = ["Norte", "Sur", "Este", "Oeste", "Centro"]
        
        # Categorías
        categories = ["Electronics", "Computing", "Audio", "Accessories"]
        
        # Generar fechas (últimos 12 meses)
        start_date = datetime.now() - timedelta(days=365)
        dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
        
        # Generar datos
        data = []
        for _ in range(num_records):
            date = pd.to_datetime(np.random.choice(dates)).strftime('%Y-%m-%d')
            product = np.random.choice(products)
            region = np.random.choice(regions)
            
            # Precios realistas
            base_price = np.random.uniform(50, 2000)
            quantity = np.random.randint(1, 10)
            sales_amount = base_price * quantity
            profit = sales_amount * np.random.uniform(0.1, 0.4)
            
            data.append({
                'date': date,
                'product': product,
                'region': region,
                'sales_amount': round(sales_amount, 2),
                'profit': round(profit, 2),
                'quantity': quantity
            })
        
        # Crear DataFrame
        df = pd.DataFrame(data)
        
        # Insertar en base de datos
        conn = sqlite3.connect(self.db_path)
        df.to_sql('sales', conn, if_exists='replace', index=False)
        
        # Insertar productos
        product_data = []
        for i, product in enumerate(products):
            product_data.append({
                'name': product,
                'category': categories[i % len(categories)],
                'price': np.random.uniform(50, 2000),
                'cost': np.random.uniform(30, 1200)
            })
        
        product_df = pd.DataFrame(product_data)
        product_df.to_sql('products', conn, if_exists='replace', index=False)
        
        # Insertar regiones
        region_data = []
        for region in regions:
            region_data.append({
                'name': region,
                'country': 'España',
                'population': np.random.randint(100000, 2000000)
            })
        
        region_df = pd.DataFrame(region_data)
        region_df.to_sql('regions', conn, if_exists='replace', index=False)
        
        conn.close()
        return df
    
    def get_sales_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Obtener datos de ventas con filtros"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM sales"
        params = []
        
        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        elif start_date:
            query += " WHERE date >= ?"
            params.append(start_date)
        elif end_date:
            query += " WHERE date <= ?"
            params.append(end_date)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_analytics_summary(self):
        """Obtener resumen analítico usando pandas"""
        conn = sqlite3.connect(self.db_path)
        
        # Datos de ventas
        sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        
        # Métricas generales
        total_sales = sales_df['sales_amount'].sum()
        total_profit = sales_df['profit'].sum()
        total_customers = sales_df['quantity'].sum()
        avg_order_value = sales_df['sales_amount'].mean()
        
        # Crecimiento (comparar últimos 3 meses vs anteriores)
        current_date = datetime.now()
        three_months_ago = current_date - timedelta(days=90)
        six_months_ago = current_date - timedelta(days=180)
        
        recent_sales = sales_df[sales_df['date'] >= three_months_ago]['sales_amount'].sum()
        previous_sales = sales_df[
            (sales_df['date'] >= six_months_ago) & 
            (sales_df['date'] < three_months_ago)
        ]['sales_amount'].sum()
        
        growth_rate = ((recent_sales - previous_sales) / previous_sales * 100) if previous_sales > 0 else 0
        
        # Ventas por mes (últimos 12 meses)
        monthly_sales = sales_df.groupby(sales_df['date'].dt.to_period('M'))['sales_amount'].sum()
        monthly_profit = sales_df.groupby(sales_df['date'].dt.to_period('M'))['profit'].sum()
        
        # Productos más vendidos
        product_sales = sales_df.groupby('product').agg({
            'sales_amount': 'sum',
            'quantity': 'sum'
        }).sort_values('sales_amount', ascending=False)
        
        # Ventas por región
        region_sales = sales_df.groupby('region').agg({
            'sales_amount': 'sum',
            'quantity': 'sum'
        }).sort_values('sales_amount', ascending=False)
        
        conn.close()
        
        return {
            'metrics': {
                'total_sales': round(total_sales, 2),
                'total_profit': round(total_profit, 2),
                'total_customers': int(total_customers),
                'avg_order_value': round(avg_order_value, 2),
                'growth_rate': round(growth_rate, 1)
            },
            'monthly_data': {
                'months': [str(period) for period in monthly_sales.index],
                'sales': [round(x, 2) for x in monthly_sales.values],
                'profit': [round(x, 2) for x in monthly_profit.values]
            },
            'product_data': {
                'products': product_sales.index.tolist(),
                'sales': [round(x, 2) for x in product_sales['sales_amount'].values],
                'quantity': [int(x) for x in product_sales['quantity'].values]
            },
            'region_data': {
                'regions': region_sales.index.tolist(),
                'sales': [round(x, 2) for x in region_sales['sales_amount'].values],
                'customers': [int(x) for x in region_sales['quantity'].values]
            }
        }
    
    def export_to_csv(self, table_name: str, filename: str = None):
        """Exportar datos a CSV"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        
        if filename is None:
            filename = f"{table_name}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df.to_csv(filename, index=False)
        return filename
    
    def export_to_excel(self, filename: str = None):
        """Exportar todos los datos a Excel"""
        conn = sqlite3.connect(self.db_path)
        
        with pd.ExcelWriter(filename or f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx") as writer:
            # Hoja de ventas
            sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
            sales_df.to_excel(writer, sheet_name='Ventas', index=False)
            
            # Hoja de productos
            products_df = pd.read_sql_query("SELECT * FROM products", conn)
            products_df.to_excel(writer, sheet_name='Productos', index=False)
            
            # Hoja de regiones
            regions_df = pd.read_sql_query("SELECT * FROM regions", conn)
            regions_df.to_excel(writer, sheet_name='Regiones', index=False)
            
            # Hoja de resumen
            summary = self.get_analytics_summary()
            summary_df = pd.DataFrame([summary['metrics']])
            summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        conn.close()
        return filename
