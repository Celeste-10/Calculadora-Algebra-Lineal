import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QStackedWidget)
from PyQt6.QtCore import Qt

from modulos.modulo_sistemas import VentanaModuloSistemas
from modulos.modulo_vectores import VentanaModuloVectores
from modulos.modulo_matrices import VentanaModuloMatrices

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MatrixX - Calculadora de Álgebra Lineal")
        self.setGeometry(100, 100, 750, 600)
        
        # Estilo oscuro estilo MatrixX 🟢
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QLabel { color: #00FF66; font-family: Consolas, monospace; font-size: 14px; }
            QPushButton { 
                background-color: #1E1E1E; 
                color: #00FF66; 
                border: 2px solid #00FF66; 
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #00FF66; 
                color: #121212; 
            }
            QTableWidget {
                background-color: #1B1B1B;
                color: #00FF66;
                gridline-color: #00FF66;
            }
            QTextEdit {
                background-color: #0A0A0A;
                color: #00FF66;
                font-family: Consolas, monospace;
            }
        """)

        # Gestor de pantallas (Stack)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instanciar cada vista
        self.pantalla_menu = self.crear_menu_principal()
        self.pantalla_m1 = VentanaModuloSistemas(self.volver_al_menu)
        self.pantalla_m2 = VentanaModuloVectores(self.volver_al_menu)
        self.pantalla_m3 = VentanaModuloMatrices(self.volver_al_menu)

        # Agregar al Stack
        self.stack.addWidget(self.pantalla_menu) # Índice 0
        self.stack.addWidget(self.pantalla_m1)   # Índice 1
        self.stack.addWidget(self.pantalla_m2)   # Índice 2
        self.stack.addWidget(self.pantalla_m3)   # Índice 3

    def crear_menu_principal(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo = QLabel("┌─────────────────────────────────────────┐\n"
                        "│                MatrixX                  │\n"
                        "│       Calculadora de Álgebra Lineal     │\n"
                        "└─────────────────────────────────────────┘")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_m1 = QPushButton(" Módulo 1: Sistemas de Ecuaciones Lineales (SEL)")
        btn_m2 = QPushButton(" Módulo 2: Vectores e Independencia Lineal")
        btn_m3 = QPushButton(" Módulo 3: Álgebra de Matrices e Inversa")
        btn_salir = QPushButton(" Salir")

        # Conexiones de botones a sus respectivas pantallas
        btn_m1.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_m2.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_m3.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_salir.clicked.connect(self.close)

        layout.addWidget(titulo)
        layout.addSpacing(25)
        layout.addWidget(btn_m1)
        layout.addWidget(btn_m2)
        layout.addWidget(btn_m3)
        layout.addSpacing(15)
        layout.addWidget(btn_salir)

        widget.setLayout(layout)
        return widget

    def volver_al_menu(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())