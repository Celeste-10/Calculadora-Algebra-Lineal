# ==============================================================================
# UNIVERSIDAD AMERICANA (UAM)
# Asignatura: Álgebra Lineal (MTM0120)
# Proyecto Integrador: Calculadora de Álgebra Lineal - Programa 2
# Archivo Principal de Ejecución (Main)
# ==============================================================================

import sys
import os

# Garantizar que Python reconozca la carpeta raíz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from PyQt6.QtWidgets import QApplication
except ImportError:
    from PyQt5.QtWidgets import QApplication

from gui.interfaz_gui import CalculadoraGaussJordan

def main():
    app = QApplication(sys.argv)
    ventana = CalculadoraGaussJordan()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()