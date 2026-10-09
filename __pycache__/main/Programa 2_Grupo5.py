# ==============================================================================
# UNIVERSIDAD AMERICANA (UAM)
# Asignatura: Álgebra Lineal (MTM0120)
# Proyecto Integrador: Calculadora de Álgebra Lineal - Programa 2
# Archivo Principal de Ejecución (Main)
# ==============================================================================

import sys

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