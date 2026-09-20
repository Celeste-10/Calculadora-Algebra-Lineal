# ==============================================================================
# INTERFAZ GRÁFICA BALANCEADA - PROGRAMA 3 (ACENTOS NAVY & DEEP BLUES)
# ==============================================================================

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
    QMessageBox, QTabWidget, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from logica.vectores_matrices import (
    sumar_matrices, restar_matrices, escalar_por_matriz, multiplicar_matrices,
    sumar_vectores, restar_vectores, escalar_por_vector,
    es_combinacion_lineal, resolver_ecuacion_matricial
)
from logica.algebra_lineal import formato_matriz_html

# Estilo con fondo claro y acentos en la paleta Navy & Deep Blues
ESTILO_MODERNO = """
    QMainWindow, QWidget {
        background-color: #F0F6FF;
        color: #1F2937;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
    }
    
    /* Pestañas */
    QTabWidget::pane {
        border: 1px solid #BFD8FF;
        background-color: #FFFFFF;
        border-radius: 8px;
    }
    QTabBar::tab {
        background-color: #E6F0FF;
        color: #3B82F6;
        padding: 8px 18px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        font-weight: bold;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background-color: #4A90E2;
        color: #FFFFFF;
    }

    /* Marcos y Secciones */
    QGroupBox {
        border: 1px solid #A9CCFF;
        border-radius: 8px;
        margin-top: 12px;
        font-weight: bold;
        color: #4A90E2;
        background-color: #FFFFFF;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }

    /* Botones con los azules más vibrantes de la paleta */
    QPushButton {
        background-color: #4A90E2;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 8px 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #609DE6;
    }
    QPushButton:pressed {
        background-color: #7BAEF7;
    }

    /* Tablas de Entrada */
    QTableWidget {
        background-color: #FFFFFF;
        gridline-color: #DCEBFF;
        color: #1F2937;
        border: 1px solid #BFD8FF;
        border-radius: 6px;
    }
    QHeaderView::section {
        background-color: #4A90E2;
        color: #FFFFFF;
        font-weight: bold;
        border: none;
        padding: 4px;
    }

    /* Inputs numéricos y Consola de Resultados */
    QSpinBox, QDoubleSpinBox {
        background-color: #FFFFFF;
        color: #1F2937;
        border: 1px solid #A9CCFF;
        border-radius: 4px;
        padding: 4px;
    }
    QTextEdit {
        background-color: #FFFFFF;
        color: #1F2937;
        border: 1px solid #DCEBFF;
        border-radius: 6px;
        padding: 8px;
    }
    /* Estilo corregido para liberar el área de clic de las flechas */
    QSpinBox, QDoubleSpinBox {
        background-color: #FFFFFF;
        color: #1F2937;
        border: 1px solid #A9CCFF;
        border-radius: 4px;
        padding-top: 2px;
        padding-bottom: 2px;
        padding-left: 4px;
        padding-right: 18px; /* Hace espacio para las flechas nativas */
        min-height: 24px;
        font-weight: bold;
    }
"""

class InterfazPrograma3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAM | ÁLGEBRA LINEAL - PROGRAMA 3")
        self.resize(1100, 750)
        self.setStyleSheet(ESTILO_MODERNO)
        self.init_ui()

    def init_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_main = QVBoxLayout(widget_central)

        # Encabezado Oficial
        lbl_titulo = QLabel("ÁLGEBRA LINEAL: OPERACIONES EN Rⁿ, MATRICES Y COMBINACIONES")
        lbl_titulo.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet("color: #4A90E2; margin-bottom: 5px;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_main.addWidget(lbl_titulo)

        tabs = QTabWidget()
        tabs.addTab(self.tab_vectores(), "Vectores en Rⁿ")
        tabs.addTab(self.tab_matrices(), "Operaciones Matriciales")
        tabs.addTab(self.tab_combinaciones(), "Combinación Lineal")
        tabs.addTab(self.tab_ecuaciones(), "Ecuación Ax = b")

        layout_main.addWidget(tabs)

    # --------------------------------------------------------------------------
    # PESTAÑA 1: VECTORES
    # --------------------------------------------------------------------------
    def tab_vectores(self):
        w = QWidget()
        l = QHBoxLayout(w)
        
        left = QVBoxLayout()
        grp = QGroupBox("Configuración de Vectores (u y v)")
        gl = QVBoxLayout(grp)
        
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Dimensión (n):"))
        self.spin_n_vec = QSpinBox(); self.spin_n_vec.setValue(3); self.spin_n_vec.setRange(1, 10)
        ctrl.addWidget(self.spin_n_vec)
        btn = QPushButton("Generar")
        btn.clicked.connect(self.gen_tablas_vec)
        ctrl.addWidget(btn)
        gl.addLayout(ctrl)

        ctrl_esc = QHBoxLayout()
        ctrl_esc.addWidget(QLabel("Escalar (c):"))
        self.spin_c_vec = QDoubleSpinBox(); self.spin_c_vec.setValue(2.0); self.spin_c_vec.setRange(-100, 100)
        ctrl_esc.addWidget(self.spin_c_vec)
        gl.addLayout(ctrl_esc)

        self.tabla_u = QTableWidget()
        self.tabla_v = QTableWidget()
        gl.addWidget(QLabel("Vector u:"))
        gl.addWidget(self.tabla_u)
        gl.addWidget(QLabel("Vector v:"))
        gl.addWidget(self.tabla_v)
        left.addWidget(grp)

        b_layout = QHBoxLayout()
        b1 = QPushButton("u + v"); b1.clicked.connect(self.calc_suma_vec)
        b2 = QPushButton("u - v"); b2.clicked.connect(self.calc_resta_vec)
        b3 = QPushButton("c · u"); b3.clicked.connect(self.calc_esc_vec)
        b_layout.addWidget(b1); b_layout.addWidget(b2); b_layout.addWidget(b3)
        left.addLayout(b_layout)

        self.txt_res_vec = QTextEdit(); self.txt_res_vec.setReadOnly(True)
        l.addLayout(left, 5)
        l.addWidget(self.txt_res_vec, 5)

        self.gen_tablas_vec()
        return w

    def gen_tablas_vec(self):
        n = self.spin_n_vec.value()
        for t in [self.tabla_u, self.tabla_v]:
            t.setRowCount(1); t.setColumnCount(n)
            for j in range(n):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                t.setItem(0, j, item)

    def _get_vec(self, t):
        return [float(t.item(0, j).text()) if t.item(0, j) else 0.0 for j in range(t.columnCount())]

    def calc_suma_vec(self):
        res = sumar_vectores(self._get_vec(self.tabla_u), self._get_vec(self.tabla_v))
        self.txt_res_vec.setHtml(f"<h3>Resultado u + v:</h3><p>{res}</p>")

    def calc_resta_vec(self):
        res = restar_vectores(self._get_vec(self.tabla_u), self._get_vec(self.tabla_v))
        self.txt_res_vec.setHtml(f"<h3>Resultado u - v:</h3><p>{res}</p>")

    def calc_esc_vec(self):
        c = self.spin_c_vec.value()
        res = escalar_por_vector(c, self._get_vec(self.tabla_u))
        self.txt_res_vec.setHtml(f"<h3>Resultado {c} · u:</h3><p>{res}</p>")

    # --------------------------------------------------------------------------
    # PESTAÑA 2: OPERACIONES MATRICIALES
    # --------------------------------------------------------------------------
    def tab_matrices(self):
        w = QWidget()
        l = QHBoxLayout(w)
        left = QVBoxLayout()

        # Matriz A
        grpA = QGroupBox("Matriz A")
        lA = QVBoxLayout(grpA)
        cA = QHBoxLayout()
        cA.addWidget(QLabel("m:"))
        
        self.mA = QSpinBox()
        self.mA.setRange(1, 100)
        self.mA.setValue(2)
        cA.addWidget(self.mA)
        
        cA.addWidget(QLabel("n:"))
        self.nA = QSpinBox()
        self.nA.setRange(1, 100)
        self.nA.setValue(2)
        cA.addWidget(self.nA)
        
        bA = QPushButton("Ok")
        bA.clicked.connect(self.genA)
        cA.addWidget(bA)
        lA.addLayout(cA)
        self.tabA = QTableWidget()
        lA.addWidget(self.tabA)

        # Matriz B
        grpB = QGroupBox("Matriz B")
        lB = QVBoxLayout(grpB)
        cB = QHBoxLayout()
        cB.addWidget(QLabel("m:"))
        
        self.mB = QSpinBox()
        self.mB.setRange(1, 100)
        self.mB.setValue(2)
        cB.addWidget(self.mB)
        
        cB.addWidget(QLabel("n:"))
        self.nB = QSpinBox()
        self.nB.setRange(1, 100)
        self.nB.setValue(2)
        cB.addWidget(self.nB)
        
        bB = QPushButton("Ok")
        bB.clicked.connect(self.genB)
        cB.addWidget(bB)
        lB.addLayout(cB)
        self.tabB = QTableWidget()
        lB.addWidget(self.tabB)

        left.addWidget(grpA)
        left.addWidget(grpB)

        b_layout = QHBoxLayout()
        b_sum = QPushButton("A + B"); b_sum.clicked.connect(self.calc_sum_mat)
        b_res = QPushButton("A - B"); b_res.clicked.connect(self.calc_res_mat)
        b_mul = QPushButton("A × B"); b_mul.clicked.connect(self.calc_mul_mat)
        b_layout.addWidget(b_sum); b_layout.addWidget(b_res); b_layout.addWidget(b_mul)
        left.addLayout(b_layout)

        self.txt_res_mat = QTextEdit(); self.txt_res_mat.setReadOnly(True)
        l.addLayout(left, 5); l.addWidget(self.txt_res_mat, 5)

        self.genA(); self.genB()
        return w
    def genA(self): self._fill_mat(self.tabA, self.mA.value(), self.nA.value())
    def genB(self): self._fill_mat(self.tabB, self.mB.value(), self.nB.value())

    def _fill_mat(self, t, m, n):
        t.setRowCount(m); t.setColumnCount(n)
        for i in range(m):
            for j in range(n):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                t.setItem(i, j, item)

    def _get_mat(self, t):
        return [[float(t.item(i, j).text() if t.item(i, j) else 0) for j in range(t.columnCount())] for i in range(t.rowCount())]

    def calc_sum_mat(self):
        try:
            r = sumar_matrices(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(formato_matriz_html(r, "Resultado A + B"))
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def calc_res_mat(self):
        try:
            r = restar_matrices(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(formato_matriz_html(r, "Resultado A - B"))
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def calc_mul_mat(self):
        try:
            r = multiplicar_matrices(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(formato_matriz_html(r, "Resultado A × B"))
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    # --------------------------------------------------------------------------
    # PESTAÑA 3: COMBINACIONES LINEALES
    # --------------------------------------------------------------------------
    def tab_combinaciones(self):
        w = QWidget(); l = QVBoxLayout(w)
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Dimensión (n):"))
        self.spin_dim_c = QSpinBox(); self.spin_dim_c.setRange(1, 100); self.spin_dim_c.setValue(3); ctrl.addWidget(self.spin_dim_c)
        ctrl.addWidget(QLabel("Vectores (k):"))
        self.spin_k_c = QSpinBox(); self.spin_k_c.setRange(1, 100); self.spin_k_c.setValue(3); ctrl.addWidget(self.spin_k_c)
        btn = QPushButton("Generar Matriz"); btn.clicked.connect(self.gen_comb); ctrl.addWidget(btn)
        l.addLayout(ctrl)

        self.tab_c = QTableWidget(); l.addWidget(self.tab_c)
        btn_eval = QPushButton("Evaluar Combinación Lineal"); btn_eval.clicked.connect(self.eval_comb); l.addWidget(btn_eval)
        self.txt_res_c = QTextEdit(); self.txt_res_c.setReadOnly(True); l.addWidget(self.txt_res_c)

        self.gen_comb()
        return w

    def gen_comb(self):
        n, k = self.spin_dim_c.value(), self.spin_k_c.value()
        self.tab_c.setRowCount(n); self.tab_c.setColumnCount(k + 1)
        self.tab_c.setHorizontalHeaderLabels([f"v{j+1}" for j in range(k)] + ["b"])
        for i in range(n):
            for j in range(k + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tab_c.setItem(i, j, item)

    def eval_comb(self):
        try:
            n, k = self.spin_dim_c.value(), self.spin_k_c.value()
            mat = self._get_mat(self.tab_c)
            conjunto = [[mat[i][j] for i in range(n)] for j in range(k)]
            b = [mat[i][k] for i in range(n)]
            _, pasos, res = es_combinacion_lineal(conjunto, b)
            self.txt_res_c.setHtml(f"<h3>Resultado:</h3>{res}<br><b>Pasos:</b><br>" + "<br>".join(pasos))
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    # --------------------------------------------------------------------------
    # PESTAÑA 4: ECUACIONES MATRICIALES (Ax = b)
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # PESTAÑA 4: ECUACIONES MATRICIALES (Ax = b) - ESTRUCTURA DIVIDIDA
    # --------------------------------------------------------------------------
    def tab_ecuaciones(self):
        w = QWidget()
        layout_principal = QHBoxLayout(w)

        # Panel Izquierdo: Entradas y Tabla
        panel_izquierdo = QVBoxLayout()
        
        grp_dim = QGroupBox("1. Dimensiones del Sistema [m × n]")
        l_dim = QHBoxLayout(grp_dim)
        l_dim.addWidget(QLabel("Ecuaciones (m):"))
        self.spin_m_e = QSpinBox(); self.spin_m_e.setRange(1, 100); self.spin_m_e.setValue(3)
        l_dim.addWidget(self.spin_m_e)
        
        l_dim.addWidget(QLabel("Variables (n):"))
        self.spin_n_e = QSpinBox(); self.spin_n_e.setRange(1, 100); self.spin_n_e.setValue(3)
        l_dim.addWidget(self.spin_n_e)
        
        btn_gen = QPushButton("Generar Sistema")
        btn_gen.clicked.connect(self.gen_eq)
        l_dim.addWidget(btn_gen)
        panel_izquierdo.addWidget(grp_dim)

        grp_mat = QGroupBox("2. Coeficientes de la Matriz Aumentada [A|b]")
        l_mat = QVBoxLayout(grp_mat)
        self.tab_e = QTableWidget()
        l_mat.addWidget(self.tab_e)
        panel_izquierdo.addWidget(grp_mat)

        btn_res = QPushButton("Resolver Ax = b")
        btn_res.clicked.connect(self.res_eq)
        panel_izquierdo.addWidget(btn_res)

        # Panel Derecho: Salidas divididas
        panel_derecho = QVBoxLayout()

        grp_pasos = QGroupBox("3. Procedimiento Paso a Paso")
        l_pasos = QVBoxLayout(grp_pasos)
        self.txt_pasos_e = QTextEdit()
        self.txt_pasos_e.setReadOnly(True)
        l_pasos.addWidget(self.txt_pasos_e)
        panel_derecho.addWidget(grp_pasos, 6)  # Proporción vertical

        grp_res = QGroupBox("4. Resultados, Pivotes y Solución Final")
        l_res = QVBoxLayout(grp_res)
        self.txt_sol_e = QTextEdit()
        self.txt_sol_e.setReadOnly(True)
        l_res.addWidget(self.txt_sol_e)
        panel_derecho.addWidget(grp_res, 4)   # Proporción vertical

        # Ensamblar paneles
        layout_principal.addLayout(panel_izquierdo, 4)
        layout_principal.addLayout(panel_derecho, 6)

        self.gen_eq()
        return w

    def res_eq(self):
        try:
            m, n = self.spin_m_e.value(), self.spin_n_e.value()
            mat = self._get_mat(self.tab_e)
            A = [fila[:n] for fila in mat]
            b = [fila[n] for fila in mat]
            
            # Ejecutar lógica backend
            _, pasos, res = resolver_ecuacion_matricial(A, b)
            
            # Mostrar el procedimiento paso a paso arriba
            self.txt_pasos_e.setHtml("<b>Pasos de Reducción:</b><br><br>" + "<br><br>".join(pasos))
            
            # Mostrar pivotes y solución final abajo
            self.txt_sol_e.setHtml(f"<h3>Resumen de la Solución:</h3>{res}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def gen_eq(self):
        m, n = self.spin_m_e.value(), self.spin_n_e.value()
        self.tab_e.setRowCount(m); self.tab_e.setColumnCount(n + 1)
        self.tab_e.setHorizontalHeaderLabels([f"x{j+1}" for j in range(n)] + ["b"])
        for i in range(m):
            for j in range(n + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tab_e.setItem(i, j, item)

    