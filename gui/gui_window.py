"""
INTERFAZ GRÁFICA DE LA CALCULADORA DE ÁLGEBRA LINEAL
Construye la ventana principal con PyQt, pestañas de navegación para cada módulo temático,
tablas dinámicas de entrada de datos y paneles de visualización de procedimientos paso a paso.

Asignatura: Álgebra Lineal 
"""

try:
    from PyQt6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QMessageBox, QTabWidget, QDoubleSpinBox, QHeaderView, QStackedWidget, QGraphicsDropShadowEffect
    )
    from PyQt6.QtGui import QFont, QPixmap
    from PyQt6.QtCore import Qt
except ImportError:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QMessageBox, QTabWidget, QDoubleSpinBox, QHeaderView, QStackedWidget
    )
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont

from modulos.modulo_vectores import (
    sumar_vectores_pasos, restar_vectores_pasos, escalar_por_vector_pasos,
    es_combinacion_lineal, evaluar_independencia_lineal, evaluar_combinacion_lineal_gauss_jordan, multiplicar_escalar_u_y_v,
    verificar_propiedades_ax, multiplicar_matrices, multiplicar_matriz_vector
)

from modulos.modulo_matrices import (
    sumar_matrices_pasos, restar_matrices_pasos, multiplicar_matrices_pasos, traspuestas_ambas_matrices_pasos, 
    inversas_ambas_matrices_pasos, verificar_propiedades_suma, verificar_propiedades_multiplicacion, verificar_propiedades_transpuesta
)

from modulos.modulo_sistemas import (
    resolver_ecuacion_matricial
)

from teoremas.resumen_teoremas import PantallaTeoremas

from logica.operaciones import formato_matriz_html

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

    /* Marcos y Secciones Principales */
    QGroupBox {
        border: 1px solid #A9CCFF;
        border-radius: 8px;
        margin-top: 10px;
        font-weight: bold;
        color: #4A90E2;
        background-color: #FFFFFF;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }

    /* Contenedores Internos para Vectores */
    QGroupBox#grp_vector {
        border: 1px solid #BFD8FF;
        border-radius: 6px;
        margin-top: 8px;
        font-weight: bold;
        color: #2C3E50;
        background-color: #F4F8FF;
    }
    QGroupBox#grp_vector::title {
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px;
        color: #2C3E50;
    }

    /* Botones */
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
        padding-top: 2px;
        padding-bottom: 2px;
        padding-left: 4px;
        padding-right: 18px; /* Espacio necesario para las flechas */
        min-height: 24px;
        font-weight: bold;
    }
    QTextEdit {
        background-color: #FFFFFF;
        color: #1F2937;
        border: 1px solid #DCEBFF;
        border-radius: 6px;
        padding: 8px;
    }
"""

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAM | ÁLGEBRA LINEAL ")
        self.resize(1100, 750)
        self.setStyleSheet(ESTILO_MODERNO)
        self.init_ui()

    def init_ui(self):
        # Contenedor de vistas principales (Menú Inicio <-> Calculadora)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Crear las dos vistas
        self.pagina_inicio = self.crear_pantalla_inicio()
        self.pagina_calculadora = self.crear_pantalla_calculadora()

        # --- NUEVA PANTALLA DE TEOREMAS ---
        self.pagina_teoremas = PantallaTeoremas(
            callback_volver=lambda: self.stacked_widget.setCurrentIndex(0)
        )

        # Agregar páginas al stacked_widget
        self.stacked_widget.addWidget(self.pagina_inicio)      # Índice 0
        self.stacked_widget.addWidget(self.pagina_calculadora) # Índice 1
        self.stacked_widget.addWidget(self.pagina_teoremas)    # índice 2

    # --------------------------------------------------------------------------
    # PANTALLA DE INICIO / MENÚ PRINCIPAL
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # PANTALLA DE INICIO / MENÚ PRINCIPAL
    # --------------------------------------------------------------------------
    def crear_pantalla_inicio(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)  # Asigna directamente el layout al widget principal
        
        # Definición de alineación para evitar NameError
        align_center = Qt.AlignmentFlag.AlignCenter
        layout.setAlignment(align_center)

        # --- LOGO EN IMAGEN ---
        lbl_logo = QLabel()
        pixmap = QPixmap("assets/MatrixX.png")
        
        if not pixmap.isNull():
            lbl_logo.setPixmap(pixmap.scaledToWidth(420, Qt.TransformationMode.SmoothTransformation))
        else:
            lbl_logo.setText("MatrixX")  # Texto de respaldo si no encuentra la imagen
            lbl_logo.setFont(QFont("Georgia", 36, QFont.Weight.Bold if hasattr(QFont, 'Weight') else QFont.Bold))
        
        lbl_logo.setAlignment(align_center)
        lbl_logo.setStyleSheet("background: transparent;")
        layout.addWidget(lbl_logo)

        # --- SUBTÍTULO ---
        lbl_subtitulo = QLabel("Calculadora y Solucionador Modular")
        lbl_subtitulo.setFont(QFont("Segoe UI", 13))
        lbl_subtitulo.setStyleSheet("color: #7F8C8D; margin-bottom: 25px;")
        lbl_subtitulo.setAlignment(align_center)

        # Panel para los botones del menú
        group_box = QGroupBox("Selecciona un Módulo para comenzar:")
        group_box.setFixedWidth(480)
        box_layout = QVBoxLayout()
        box_layout.setSpacing(12)

        # Botones de módulos
        btn_sistemas = QPushButton("1. Sistemas de Ecuaciones Lineales (Ax = b)")
        btn_vectores = QPushButton("2. Operaciones con Vectores en Rⁿ")
        btn_matrices = QPushButton("3. Operaciones Matriciales e Inversa")
        btn_determinantes = QPushButton("4. Combinaciones y Propiedades Ax")
        btn_teoremas = QPushButton("5. Resumen de Teoremas y Fundamentos")

        botones = [btn_sistemas, btn_vectores, btn_matrices, btn_determinantes, btn_teoremas]

        mapa_pestanas = [3, 0, 1, 2]  # Pestañas correspondientes a los primeros 4 botones

        for idx, btn in enumerate(botones):
            btn.setFixedHeight(45)
            btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold if hasattr(QFont, 'Weight') else QFont.Bold))
            
            # Si es uno de los 4 primeros botones (módulos de calculadora)
            if idx < 4:
                target_tab = mapa_pestanas[idx]
                btn.clicked.connect(lambda _, tab=target_tab: self.abrir_modulo(tab))
            else:
                # Si es el 5º botón (Resumen de Teoremas), cambia directamente al Índice 2 del StackedWidget
                btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
                
            box_layout.addWidget(btn)

        group_box.setLayout(box_layout)

        # Añadir los componentes al layout principal
        layout.addWidget(lbl_subtitulo)
        layout.addWidget(group_box, alignment=align_center)

        return widget
    def abrir_modulo(self, indice_pestana):
        """Cambia a la vista de la calculadora y abre la pestaña seleccionada."""
        self.stacked_widget.setCurrentIndex(1)
        self.tabs.setCurrentIndex(indice_pestana)

    def crear_pantalla_calculadora(self):
        """Contenedor de la calculadora con tus pestañas originales."""
        widget = QWidget()
        layout_main = QVBoxLayout(widget)

        # Barra Superior: Botón para volver al Menú + Encabezado
        top_bar = QHBoxLayout()
        btn_volver = QPushButton("← Menú Principal")
        btn_volver.setFixedWidth(160)
        btn_volver.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        top_bar.addWidget(btn_volver)

        lbl_titulo = QLabel("ÁLGEBRA LINEAL: OPERACIONES EN Rⁿ, MATRICES Y COMBINACIONES")
        lbl_titulo.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold if hasattr(QFont, 'Weight') else QFont.Bold))
        lbl_titulo.setStyleSheet("color: #4A90E2;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter)
        
        top_bar.addWidget(lbl_titulo, 1)
        layout_main.addLayout(top_bar)

        # Tus Pestañas Originales
        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab_vectores(), "Vectores en Rⁿ")
        self.tabs.addTab(self.tab_matrices(), "Operaciones Matriciales")
        self.tabs.addTab(self.tab_combinaciones(), "Combinación Lineal")
        self.tabs.addTab(self.tab_ecuaciones(), "Ecuación Ax = b")
        self.tabs.addTab(self.tab_propiedades_ax(), "Propiedades Ax")

        layout_main.addWidget(self.tabs)
        return widget

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

        # Layout de botones de operaciones en Rn
        b_layout = QHBoxLayout()
        
        b1 = QPushButton("u + v")
        b1.clicked.connect(self.calc_suma_vec)
        
        b2 = QPushButton("u - v")
        b2.clicked.connect(self.calc_resta_vec)
        
        # 1. Cambiamos el texto y la conexión para escalar u y v
        b3 = QPushButton("c · u  y  c · v")
        b3.clicked.connect(self.calc_esc_vec)
        
        # 2. NUEVO BOTÓN: Combinación Lineal
        b4 = QPushButton("Independencia Lineal")
        b4.clicked.connect(self.calc_independencia_vec)
        
        b_layout.addWidget(b1)
        b_layout.addWidget(b2)
        b_layout.addWidget(b3)
        b_layout.addWidget(b4)  # Se agrega al layout
        
        left.addLayout(b_layout)

        self.txt_res_vec = QTextEdit(); self.txt_res_vec.setReadOnly(True)
        l.addLayout(left, 5)
        l.addWidget(self.txt_res_vec, 5)

        self.gen_tablas_vec()
        return w

    def gen_tablas_vec(self):
        n = self.spin_n_vec.value()
        align_center = Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter
        for t in [self.tabla_u, self.tabla_v]:
            t.setRowCount(1); t.setColumnCount(n)
            for j in range(n):
                item = QTableWidgetItem("0")
                item.setTextAlignment(align_center)
                t.setItem(0, j, item)

    def _get_vec(self, t):
        return [float(t.item(0, j).text()) if t.item(0, j) else 0.0 for j in range(t.columnCount())]

    def calc_suma_vec(self):
        _, pasos = sumar_vectores_pasos(self._get_vec(self.tabla_u), self._get_vec(self.tabla_v))
        self.txt_res_vec.setHtml(pasos)

    def calc_resta_vec(self):
        _, pasos = restar_vectores_pasos(self._get_vec(self.tabla_u), self._get_vec(self.tabla_v))
        self.txt_res_vec.setHtml(pasos)

    def obtener_vector_u(self):
        """Lee todos los valores de la tabla del vector u."""
        return [
            float(self.tabla_u.item(0, j).text()) if self.tabla_u.item(0, j) else 0.0 
            for j in range(self.tabla_u.columnCount())
        ]

    def obtener_vector_v(self):
        """Lee todos los valores de la tabla del vector v."""
        return [
            float(self.tabla_v.item(0, j).text()) if self.tabla_v.item(0, j) else 0.0 
            for j in range(self.tabla_v.columnCount())
        ]

    def calc_esc_vec(self):
        """Calcula el producto por escalar para u y para v."""
        try:
            u = self.obtener_vector_u()
            v = self.obtener_vector_v()
            c = float(self.spin_c_vec.value())  # Nombre correcto del control del escalar
            
            # Llamar a la función importada de modulo_vectores
            cu, cv, texto_pasos = multiplicar_escalar_u_y_v(u, v, c)
            
            # Mostrar resultado en el cuadro de texto correcto
            self.txt_res_vec.setPlainText(texto_pasos)

        except Exception as e:
            self.txt_res_vec.setPlainText(f"Error al calcular: {str(e)}")

    def calc_independencia_vec(self):
        """Evalúa si el conjunto formado por {u, v} es L.I. o L.D."""
        try:
            u = self.obtener_vector_u()
            v = self.obtener_vector_v()
            vectores = [u, v]

            # Evaluación con la función ya importada en tu módulo
            matriz_rref, pasos, resumen, es_li = evaluar_independencia_lineal(vectores)
            
            # Muestra el resultado formateado en HTML en el visor lateral
            self.txt_res_vec.setHtml(resumen)

        except Exception as e:
            self.txt_res_vec.setPlainText(f"Error al evaluar independencia lineal: {str(e)}")

    
    def accion_multiplicar_escalar(self):
        # Obtener u, v y c desde la interfaz
        u = self.obtener_vector_u()
        v = self.obtener_vector_v()
        c = float(self.input_escalar.text())
        
        # Calcular ambos productos
        cu, cv, texto_pasos = multiplicar_escalar_u_y_v(u, v, c)
        
        # Mostrar el procedimiento completo en el panel de la derecha
        self.txt_procedimiento.setText(texto_pasos)
    def accion_evaluar_combinacion_lineal(self):
        # 1. Leer vectores desde la UI (ejemplo u y v como conjunto)
        u = self.obtener_vector_u()
        v = self.obtener_vector_v()
        vectores = [u, v]
        
        # 2. Leer el vector b
        vector_b = self.obtener_vector_b()
        
        # 3. Evaluar con Gauss-Jordan
        es_comb, pasos_texto, pesos = evaluar_combinacion_lineal_gauss_jordan(vectores, vector_b)
        
        # 4. Mostrar en la caja de procedimiento
        self.txt_procedimiento.setText(pasos_texto)

    # --------------------------------------------------------------------------
    # PESTAÑA 2: OPERACIONES MATRICIALES
    # --------------------------------------------------------------------------
    def tab_matrices(self):
        w = QWidget()
        l = QHBoxLayout(w)
        left = QVBoxLayout()

        # Configuración de Escalares r y s
        grp_esc = QGroupBox("Escalares")
        l_esc = QHBoxLayout(grp_esc)
        l_esc.addWidget(QLabel("Escalar r:"))
        self.spin_r = QDoubleSpinBox()
        self.spin_r.setRange(-100, 100)
        self.spin_r.setValue(2.0)
        l_esc.addWidget(self.spin_r)

        l_esc.addWidget(QLabel("Escalar s:"))
        self.spin_s = QDoubleSpinBox()
        self.spin_s.setRange(-100, 100)
        self.spin_s.setValue(3.0)
        l_esc.addWidget(self.spin_s)
        left.addWidget(grp_esc)

        # Matriz A
        grpA = QGroupBox("Matriz A")
        lA = QVBoxLayout(grpA)
        cA = QHBoxLayout()
        cA.addWidget(QLabel("m:"))
        self.mA = QSpinBox(); self.mA.setRange(1, 100); self.mA.setValue(2)
        cA.addWidget(self.mA)
        cA.addWidget(QLabel("n:"))
        self.nA = QSpinBox(); self.nA.setRange(1, 100); self.nA.setValue(2)
        cA.addWidget(self.nA)
        bA = QPushButton("Ok"); bA.clicked.connect(self.genA)
        cA.addWidget(bA)
        lA.addLayout(cA)
        self.tabA = QTableWidget()
        self.tabA.setMaximumHeight(140)
        lA.addWidget(self.tabA)

        # Matriz B
        grpB = QGroupBox("Matriz B")
        lB = QVBoxLayout(grpB)
        cB = QHBoxLayout()
        cB.addWidget(QLabel("m:"))
        self.mB = QSpinBox(); self.mB.setRange(1, 100); self.mB.setValue(2)
        cB.addWidget(self.mB)
        cB.addWidget(QLabel("n:"))
        self.nB = QSpinBox(); self.nB.setRange(1, 100); self.nB.setValue(2)
        cB.addWidget(self.nB)
        bB = QPushButton("Ok"); bB.clicked.connect(self.genB)
        cB.addWidget(bB)
        lB.addLayout(cB)
        self.tabB = QTableWidget()
        self.tabB.setMaximumHeight(140)
        lB.addWidget(self.tabB)

        # Matriz C
        grpC = QGroupBox("Matriz C")
        lC = QVBoxLayout(grpC)
        cC = QHBoxLayout()
        cC.addWidget(QLabel("m:"))
        self.mC = QSpinBox(); self.mC.setRange(1, 100); self.mC.setValue(2)
        cC.addWidget(self.mC)
        cC.addWidget(QLabel("n:"))
        self.nC = QSpinBox(); self.nC.setRange(1, 100); self.nC.setValue(2)
        cC.addWidget(self.nC)
        bC = QPushButton("Ok"); bC.clicked.connect(self.genC)
        cC.addWidget(bC)
        lC.addLayout(cC)
        self.tabC = QTableWidget()
        self.tabC.setMaximumHeight(140)
        lC.addWidget(self.tabC)

        left.addWidget(grpA)
        left.addWidget(grpB)
        left.addWidget(grpC)

        # Fila 1: Operaciones Básicas
        b_layout = QHBoxLayout()
        b_sum = QPushButton("A + B"); b_sum.clicked.connect(self.calc_sum_mat)
        b_res = QPushButton("A - B"); b_res.clicked.connect(self.calc_res_mat)
        b_mul = QPushButton("A × B"); b_mul.clicked.connect(self.calc_mul_mat)
        b_trasp = QPushButton("Aᵀ y Bᵀ"); b_trasp.clicked.connect(self.calc_trasp_mat)
        b_inv = QPushButton("A⁻¹ y B⁻¹"); b_inv.clicked.connect(self.calc_inv_mat)

        b_layout.addWidget(b_sum)
        b_layout.addWidget(b_res)
        b_layout.addWidget(b_mul)
        b_layout.addWidget(b_trasp)
        b_layout.addWidget(b_inv)
        left.addLayout(b_layout)

        # Fila 2: Botones de Teoremas Completos
        b_teoremas_layout = QHBoxLayout()
        b_prop_suma = QPushButton("Teoremas Suma")
        b_prop_suma.clicked.connect(self.calc_propiedades_suma)
        
        b_prop_mul = QPushButton("Propiedades Multiplicación")
        b_prop_mul.clicked.connect(self.calc_propiedades_multiplicacion)
        
        b_prop_trans = QPushButton("Propiedades Transpuesta")
        b_prop_trans.clicked.connect(self.calc_propiedades_transpuesta)

        b_det_cramer = QPushButton("Determinantes y Cramer")
        b_det_cramer.clicked.connect(self.calc_det_cramer)

        b_verificador = QPushButton("Verificador de Propiedades")
        b_verificador.clicked.connect(self.calc_verificador_propiedades)

        b_teoremas_layout.addWidget(b_prop_suma)
        b_teoremas_layout.addWidget(b_prop_mul)
        b_teoremas_layout.addWidget(b_prop_trans)
        b_teoremas_layout.addWidget(b_det_cramer)
        b_teoremas_layout.addWidget(b_verificador)
        left.addLayout(b_teoremas_layout)

        left.addStretch()

        self.txt_res_mat = QTextEdit()
        self.txt_res_mat.setReadOnly(True)

        l.addLayout(left, 5)
        l.addWidget(self.txt_res_mat, 5)

        self.genA()
        self.genB()
        self.genC()
        return w

    def genA(self): self._fill_mat(self.tabA, self.mA.value(), self.nA.value())
    def genB(self): self._fill_mat(self.tabB, self.mB.value(), self.nB.value())
    def genC(self): self._fill_mat(self.tabC, self.mC.value(), self.nC.value())

    def _fill_mat(self, t, m, n):
        t.setRowCount(m); t.setColumnCount(n)
        align_center = Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter
        for i in range(m):
            for j in range(n):
                item = QTableWidgetItem("0")
                item.setTextAlignment(align_center)
                t.setItem(i, j, item)

    def _get_mat(self, t):
        return [[float(t.item(i, j).text() if t.item(i, j) else 0) for j in range(t.columnCount())] for i in range(t.rowCount())]

    def calc_sum_mat(self):
        try:
            _, pasos = sumar_matrices_pasos(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(pasos)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_res_mat(self):
        try:
            _, pasos = restar_matrices_pasos(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(pasos)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_mul_mat(self):
        try:
            _, pasos = multiplicar_matrices_pasos(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(pasos)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_trasp_mat(self):
        try:
            _, pasos = traspuestas_ambas_matrices_pasos(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(pasos)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_inv_mat(self):
        try:
            _, pasos = inversas_ambas_matrices_pasos(self._get_mat(self.tabA), self._get_mat(self.tabB))
            self.txt_res_mat.setHtml(pasos)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_comb_lineal(self):
        try:
            u = self.obtener_vector_u()
            v = self.obtener_vector_v()
            vectores = [u, v]
            dim = len(u)
            
            # ... lectura del vector b ...
            
            es_comb, pasos_html, pesos = evaluar_combinacion_lineal_gauss_jordan(vectores, b)
            
            # Usamos setHtml para renderizar las tablas y estilos HTML
            self.txt_res_vec.setHtml(pasos_html)

        except Exception as e:
            self.txt_res_vec.setPlainText(f"Error: {str(e)}")

    # --------------------------------------------------------------------------
    # PESTAÑA 3: COMBINACIONES LINEALES
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
        panel_derecho.addWidget(grp_pasos, 6)

        grp_res = QGroupBox("4. Resultados, Pivotes y Solución Final")
        l_res = QVBoxLayout(grp_res)
        self.txt_sol_e = QTextEdit()
        self.txt_sol_e.setReadOnly(True)
        l_res.addWidget(self.txt_sol_e)
        panel_derecho.addWidget(grp_res, 4)

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
            
            _, pasos, res = resolver_ecuacion_matricial(A, b)
            self.txt_pasos_e.setHtml("<b>Pasos de Reducción:</b><br><br>" + "<br><br>".join(pasos))
            self.txt_sol_e.setHtml(f"<h3>Resumen de la Solución:</h3>{res}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def gen_eq(self):
        m, n = self.spin_m_e.value(), self.spin_n_e.value()
        self.tab_e.setRowCount(m); self.tab_e.setColumnCount(n + 1)
        self.tab_e.setHorizontalHeaderLabels([f"x{j+1}" for j in range(n)] + ["b"])
        align_center = Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter
        for i in range(m):
            for j in range(n + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(align_center)
                self.tab_e.setItem(i, j, item)
    
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
        align_center = Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter
        for i in range(n):
            for j in range(k + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(align_center)
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
    # PESTAÑA 4: ECUACIONES MATRICIALES (Ax = b) - ESTRUCTURA DIVIDIDA
    # --------------------------------------------------------------------------
    def tab_propiedades_ax(self):
        w = QWidget()
        l_main = QHBoxLayout(w)

        p_izq = QVBoxLayout()
        grp_dim = QGroupBox("1. Dimensiones de la Matriz A [m × n]")
        l_dim = QHBoxLayout(grp_dim)
        l_dim.addWidget(QLabel("Filas (m):"))
        self.spin_m_prop = QSpinBox()
        self.spin_m_prop.setRange(1, 100)
        self.spin_m_prop.setValue(3)
        l_dim.addWidget(self.spin_m_prop)

        l_dim.addWidget(QLabel("Columnas (n):"))
        self.spin_n_prop = QSpinBox()
        self.spin_n_prop.setRange(1, 100)
        self.spin_n_prop.setValue(3)
        l_dim.addWidget(self.spin_n_prop)

        btn_gen = QPushButton("Generar Tablas")
        btn_gen.clicked.connect(self.gen_propiedades_ax)
        l_dim.addWidget(btn_gen)
        p_izq.addWidget(grp_dim)

        grp_entradas = QGroupBox("2. Matriz A, Vectores u, v y Escalar c")
        l_entradas = QVBoxLayout(grp_entradas)
        self.tab_A_prop = QTableWidget()
        l_entradas.addWidget(QLabel("Matriz A (m × n):"))
        l_entradas.addWidget(self.tab_A_prop)

        layout_vecs = QHBoxLayout()
        v_u, v_v = QVBoxLayout(), QVBoxLayout()
        self.tab_u_prop, self.tab_v_prop = QTableWidget(), QTableWidget()
        v_u.addWidget(QLabel("Vector u (n × 1):"))
        v_u.addWidget(self.tab_u_prop)
        v_v.addWidget(QLabel("Vector v (n × 1):"))
        v_v.addWidget(self.tab_v_prop)
        layout_vecs.addLayout(v_u)
        layout_vecs.addLayout(v_v)
        l_entradas.addLayout(layout_vecs)

        layout_esc = QHBoxLayout()
        layout_esc.addWidget(QLabel("Escalar (c):"))
        self.spin_c_prop = QDoubleSpinBox()
        self.spin_c_prop.setRange(-100, 100)
        self.spin_c_prop.setValue(2.0)
        layout_esc.addWidget(self.spin_c_prop)
        l_entradas.addLayout(layout_esc)
        p_izq.addWidget(grp_entradas)

        btn_verificar = QPushButton("Verificar Propiedades A(u + v) y A(c·u)")
        btn_verificar.clicked.connect(self.res_propiedades_ax)
        p_izq.addWidget(btn_verificar)

        p_der = QVBoxLayout()
        self.txt_pasos_prop = QTextEdit()
        self.txt_pasos_prop.setReadOnly(True)
        self.txt_sol_prop = QTextEdit()
        self.txt_sol_prop.setReadOnly(True)

        grp_pasos = QGroupBox("3. Comprobación Paso a Paso")
        QVBoxLayout(grp_pasos).addWidget(self.txt_pasos_prop)
        grp_res = QGroupBox("4. Dictamen Final del Teorema")
        QVBoxLayout(grp_res).addWidget(self.txt_sol_prop)

        p_der.addWidget(grp_pasos, 6)
        p_der.addWidget(grp_res, 4)

        l_main.addLayout(p_izq, 5)
        l_main.addLayout(p_der, 5)

        self.gen_propiedades_ax()
        return w

    def gen_propiedades_ax(self):
        m, n = self.spin_m_prop.value(), self.spin_n_prop.value()
        self._fill_mat(self.tab_A_prop, m, n)
        self.tab_A_prop.setHorizontalHeaderLabels([f"x{j+1}" for j in range(n)])
        self._fill_mat(self.tab_u_prop, n, 1)
        self.tab_u_prop.setHorizontalHeaderLabels(["u"])
        self._fill_mat(self.tab_v_prop, n, 1)
        self.tab_v_prop.setHorizontalHeaderLabels(["v"])

    def res_propiedades_ax(self):
        try:
            n = self.spin_n_prop.value()
            A = self._get_mat(self.tab_A_prop)
            u = [
                float(
                    self.tab_u_prop.item(i, 0).text()
                    if self.tab_u_prop.item(i, 0)
                    else 0
                )
                for i in range(n)
            ]
            v = [
                float(
                    self.tab_v_prop.item(i, 0).text()
                    if self.tab_v_prop.item(i, 0)
                    else 0
                )
                for i in range(n)
            ]
            c = float(self.spin_c_prop.value())

            pasos_html, resumen_html = verificar_propiedades_ax(A, u, v, c)
            self.txt_pasos_prop.setHtml(pasos_html)
            self.txt_sol_prop.setHtml(resumen_html)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_propiedades_suma(self):
        try:
            A = self._get_mat(self.tabA)
            B = self._get_mat(self.tabB)
            C = self._get_mat(self.tabC)
            r = float(self.spin_r.value())
            s = float(self.spin_s.value())
            html = verificar_propiedades_suma(A, B, C, r, s)
            self.txt_res_mat.setHtml(html)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_propiedades_multiplicacion(self):
        try:
            A = self._get_mat(self.tabA)
            B = self._get_mat(self.tabB)
            C = self._get_mat(self.tabC)
            r = float(self.spin_r.value())
            html = verificar_propiedades_multiplicacion(A, B, C, r)
            self.txt_res_mat.setHtml(html)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_propiedades_transpuesta(self):
        try:
            A = self._get_mat(self.tabA)
            B = self._get_mat(self.tabB)
            r = float(self.spin_r.value())
            html = verificar_propiedades_transpuesta(A, B, r)
            self.txt_res_mat.setHtml(html)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_inv_mat(self):
        try:
            from modulos.modulo_matrices import verificar_propiedades_inversa_pasos
            A = self._get_mat(self.tabA)
            B = self._get_mat(self.tabB)
            r = float(self.spin_r.value())
            
            # Ejecuta la inversa y la verificación completa de las 5 propiedades
            _, pasos = verificar_propiedades_inversa_pasos(A, B, r)
            self.txt_res_mat.setHtml(pasos)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_det_cramer(self):
        try:
            from modulos.modulo_determinantes import reporte_determinantes_y_cramer
            A = self._get_mat(self.tabA)
            B = self._get_mat(self.tabB)
            
            pasos = reporte_determinantes_y_cramer(A, B)
            self.txt_res_mat.setHtml(pasos)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calc_verificador_propiedades(self):
        """Ejecuta la comprobación paso a paso de las 6 propiedades exigidas en la Guía 5."""
        try:
            from modulos.modulo_matrices import verificar_propiedades_guia_tarea5
            A = self._get_mat(self.tabA)
            B = self._get_mat(self.tabB)
            r = float(self.spin_r.value())
            
            # Llama a la función del verificador en modulo_matrices
            html = verificar_propiedades_guia_tarea5(A, B, k_escalar=r)
            self.txt_res_mat.setHtml(html)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el Verificador: {str(e)}")