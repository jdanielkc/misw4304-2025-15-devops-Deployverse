#!/usr/bin/env python3
"""
Punto de entrada para AWS Elastic Beanstalk
"""

import sys
import os

# Agregar el directorio actual al Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.app import create_app
    
    # Crear la aplicación
    application = create_app()
    
    # Para compatibilidad, también exponer como 'app'
    app = application
    
except ImportError as e:
    print(f"Error importing application: {e}")
    raise

# Elastic Beanstalk espera la variable 'application'
if __name__ == "__main__":
    # En desarrollo local, usar la misma configuración que src/app.py
    application.run(host="0.0.0.0", port=5000, debug=False)