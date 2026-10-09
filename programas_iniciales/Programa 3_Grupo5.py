# ==============================================================================
# UNIVERSIDAD AMERICANA (UAM)
# Asignatura: Álgebra Lineal (MTM0120)
# Proyecto Integrador: Calculadora de Álgebra Lineal - Programa 3
# Archivo Principal de Ejecución (Main)
# ==============================================================================

import sys
import os

# Configuración de ruta dinámica para evitar errores de importación
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from PyQt6.QtWidgets import QApplication
except ImportError:
    from PyQt6.QtWidgets import QApplication

from gui.interfaz_programa3 import InterfazPrograma3

def main():
    app = QApplication(sys.argv)
    ventana = InterfazPrograma3()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()