#!/usr/bin/env python3
"""
Data Analytics Dashboard - Advanced Version
Sistema avanzado de análisis de datos empresariales con pandas, SQLite y más funcionalidades
"""

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
import uvicorn
import pandas as pd
import numpy as np

from database import DatabaseManager

app = FastAPI(
    title="Data Analytics Dashboard - Advanced",
    description="Sistema avanzado de análisis de datos empresariales con pandas y SQLite",
    version="2.0.0"
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicializar base de datos
db = DatabaseManager()

@app.on_event("startup")
async def startup_event():
    """Inicializar datos de muestra al arrancar"""
    print("Inicializando base de datos...")
    db.generate_sample_data(1000)  # Generar 1000 registros de muestra
    print("Base de datos inicializada correctamente")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Servir el dashboard principal"""
    with open("static/dashboard_advanced.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/data")
async def get_analytics_data():
    """Obtener todos los datos de análisis"""
    try:
        data = db.get_analytics_summary()
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sales")
async def get_sales_data(
    start_date: Optional[str] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    product: Optional[str] = Query(None, description="Filtrar por producto"),
    region: Optional[str] = Query(None, description="Filtrar por región")
):
    """Obtener datos de ventas con filtros opcionales"""
    try:
        df = db.get_sales_data(start_date, end_date)
        
        # Aplicar filtros adicionales
        if product and product != "":
            df = df[df['product'] == product]
        
        if region and region != "":
            df = df[df['region'] == region]
        
        return {"success": True, "data": df.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products")
async def get_products_data():
    """Obtener datos de productos"""
    try:
        data = db.get_analytics_summary()
        return {"success": True, "data": data["product_data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regions")
async def get_regions_data():
    """Obtener datos de regiones"""
    try:
        data = db.get_analytics_summary()
        return {"success": True, "data": data["region_data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics")
async def get_metrics():
    """Obtener métricas generales"""
    try:
        data = db.get_analytics_summary()
        return {"success": True, "data": data["metrics"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/csv/{table_name}")
async def export_csv(table_name: str):
    """Exportar datos a CSV"""
    try:
        if table_name not in ['sales', 'products', 'regions']:
            raise HTTPException(status_code=400, detail="Tabla no válida")
        
        filename = db.export_to_csv(table_name)
        return FileResponse(
            filename, 
            media_type='text/csv',
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/excel")
async def export_excel():
    """Exportar todos los datos a Excel"""
    try:
        filename = db.export_to_excel()
        return FileResponse(
            filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filters")
async def get_filter_options():
    """Obtener opciones para filtros"""
    try:
        # Obtener fechas disponibles
        sales_df = db.get_sales_data()
        
        # Verificar que hay datos
        if len(sales_df) == 0:
            return {
                "success": True,
                "data": {
                    "dates": {
                        "min": None,
                        "max": None,
                        "available": []
                    },
                    "products": [],
                    "regions": []
                }
            }
        
        dates = sorted(sales_df['date'].unique().tolist())
        
        # Obtener productos únicos
        products = sorted(sales_df['product'].unique().tolist())
        
        # Obtener regiones únicas
        regions = sorted(sales_df['region'].unique().tolist())
        
        return {
            "success": True,
            "data": {
                "dates": {
                    "min": min(dates) if dates else None,
                    "max": max(dates) if dates else None,
                    "available": dates
                },
                "products": products,
                "regions": regions
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends")
async def get_trends_analysis():
    """Obtener análisis de tendencias"""
    try:
        sales_df = db.get_sales_data()
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        
        # Análisis de tendencias por producto
        product_trends = {}
        for product in sales_df['product'].unique():
            product_data = sales_df[sales_df['product'] == product]
            monthly_sales = product_data.groupby(product_data['date'].dt.to_period('M'))['sales_amount'].sum()
            
            # Calcular tendencia (pendiente de regresión lineal simple)
            if len(monthly_sales) > 1:
                x = np.arange(len(monthly_sales))
                y = monthly_sales.values
                trend = np.polyfit(x, y, 1)[0]  # Pendiente
                product_trends[product] = {
                    'trend': round(trend, 2),
                    'direction': 'up' if trend > 0 else 'down',
                    'strength': 'strong' if abs(trend) > 1000 else 'weak'
                }
        
        return {"success": True, "data": product_trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check del sistema"""
    try:
        # Verificar conexión a base de datos
        db.get_analytics_summary()
        return {
            "status": "healthy", 
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "version": "2.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

if __name__ == "__main__":
    print("Iniciando Data Analytics Dashboard - Advanced Version...")
    print("Dashboard: http://localhost:8002")
    print("API Docs: http://localhost:8002/docs")
    print("Features: Pandas + SQLite + Export + Filters + Trends")
    uvicorn.run(app, host="0.0.0.0", port=8002)
