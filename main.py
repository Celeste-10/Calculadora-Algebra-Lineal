"""
PUNTO DE ENTRADA PRINCIPAL DE LA CALCULADORA DE ÁLGEBRA LINEAL
Inicializa la aplicación PyQt, carga los estilos CSS del sistema e integra los módulos
operativos y la pantalla de resumen de teoremas.

Asignatura: Álgebra Lineal 
"""
import sys
from PyQt6.QtWidgets import QApplication
from gui.gui_window import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())