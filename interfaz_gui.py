# ==============================================================================
# MÓDULO DE INTERFAZ GRÁFICA (PYQT)
# ==============================================================================

try:
    from PyQt6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QMessageBox, QHeaderView
    )
    from PyQt6.QtCore import Qt
except ImportError:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QMessageBox, QHeaderView
    )
    from PyQt5.QtCore import Qt

from logica.algebra_lineal import resolver_gauss_jordan, formato_matriz_html

class CalculadoraGaussJordan(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAM - Calculadora de Álgebra Lineal | Gauss-Jordan")
        self.resize(1100, 700)
        self.aplicar_estilos()
        self.init_ui()

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #F4F6F7; }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #BDC3C7;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                background-color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #1B4F72;
            }
            QLabel { font-size: 12px; color: #2C3E50; }
            QPushButton {
                background-color: #1B4F72;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover { background-color: #2E86C1; }
            QPushButton:pressed { background-color: #154360; }
            QTableWidget {
                border: 1px solid #BDC3C7;
                gridline-color: #EAEDED;
                background-color: #FFFFFF;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #EAECEE;
                font-weight: bold;
                color: #2C3E50;
                border: 1px solid #D5D8DC;
            }
            QTextEdit {
                border: 1px solid #BDC3C7;
                background-color: #FFFFFF;
                font-family: Consolas, Monospace, Courier;
                font-size: 12px;
            }
        """)

    def init_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central)

        # ----------------------------------------------------------------------
        # PANEL IZQUIERDO: Entradas y Configuración
        # ----------------------------------------------------------------------
        panel_izq = QVBoxLayout()

        group_dimensiones = QGroupBox("1. Dimensiones del Sistema [m × n]")
        layout_dim = QHBoxLayout()

        layout_dim.addWidget(QLabel("Ecuaciones (m):"))
        self.spin_m = QSpinBox()
        self.spin_m.setRange(1, 10)
        self.spin_m.setValue(3)
        layout_dim.addWidget(self.spin_m)

        layout_dim.addWidget(QLabel("Variables (n):"))
        self.spin_n = QSpinBox()
        self.spin_n.setRange(1, 10)
        self.spin_n.setValue(3)
        layout_dim.addWidget(self.spin_n)

        btn_generar = QPushButton("Generar Matriz")
        btn_generar.clicked.connect(self.generar_tabla)
        layout_dim.addWidget(btn_generar)

        group_dimensiones.setLayout(layout_dim)
        panel_izq.addWidget(group_dimensiones)

        group_matriz = QGroupBox("2. Coeficientes de la Matriz Aumentada [A|b]")
        layout_matriz = QVBoxLayout()

        self.tabla_matriz = QTableWidget()
        layout_matriz.addWidget(self.tabla_matriz)

        btn_resolver = QPushButton("Calcular Gauss-Jordan")
        btn_resolver.setFixedHeight(40)
        btn_resolver.clicked.connect(self.procesar_sistema)
        layout_matriz.addWidget(btn_resolver)

        group_matriz.setLayout(layout_matriz)
        panel_izq.addWidget(group_matriz)

        layout_principal.addLayout(panel_izq, stretch=4)

        # ----------------------------------------------------------------------
        # PANEL DERECHO: Procedimiento y Resultados
        # ----------------------------------------------------------------------
        panel_der = QVBoxLayout()

        group_pasos = QGroupBox("3. Procedimiento Paso a Paso")
        layout_pasos = QVBoxLayout()

        self.txt_pasos = QTextEdit()
        self.txt_pasos.setReadOnly(True)
        layout_pasos.addWidget(self.txt_pasos)

        group_pasos.setLayout(layout_pasos)
        panel_der.addWidget(group_pasos, stretch=3)

        group_resultados = QGroupBox("4. Resultados, Pivotes y Solución Final")
        layout_res = QVBoxLayout()

        self.txt_resultados = QTextEdit()
        self.txt_resultados.setReadOnly(True)
        self.txt_resultados.setMaximumHeight(180)
        layout_res.addWidget(self.txt_resultados)

        group_resultados.setLayout(layout_res)
        panel_der.addWidget(group_resultados, stretch=2)

        layout_principal.addLayout(panel_der, stretch=6)

        self.generar_tabla()

    def generar_tabla(self):
        m = self.spin_m.value()
        n = self.spin_n.value()

        self.tabla_matriz.setRowCount(m)
        self.tabla_matriz.setColumnCount(n + 1)

        # Importar el formateador de subíndices Unicode
        from logica.algebra_lineal import var_subind

        # Asignar los encabezados de las variables con subíndice (ej. x₁, x₂, x₃)
        encabezados = [var_subind(j+1) for j in range(n)] + ["b (Indep.)"]
        self.tabla_matriz.setHorizontalHeaderLabels(encabezados)

        header = self.tabla_matriz.horizontalHeader()
        for j in range(n + 1):
            header.setSectionResizeMode(j, QHeaderView.ResizeMode.Stretch)

        for i in range(m):
            for j in range(n + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_matriz.setItem(i, j, item)

    def procesar_sistema(self):
        m = self.spin_m.value()
        n = self.spin_n.value()
        matriz_orig = []

        try:
            for i in range(m):
                fila = []
                for j in range(n + 1):
                    item = self.tabla_matriz.item(i, j)
                    texto = item.text() if item else "0"
                    val = float(texto)
                    fila.append(val)
                matriz_orig.append(fila)
        except ValueError:
            QMessageBox.critical(self, "Error de Entrada", "Por favor ingrese valores numéricos válidos en la matriz.")
            return

        matriz_rref, pasos_log, resumen_txt = resolver_gauss_jordan(matriz_orig, m, n)
        self.txt_pasos.setHtml("<br>".join(pasos_log))
        rref_html = formato_matriz_html(matriz_rref, "Matriz Escalonada Reducida Final (RREF):")
        self.txt_resultados.setHtml(resumen_txt + "<br>" + rref_html)