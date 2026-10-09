"""
MÓDULO DE TEOREMAS Y FUNDAMENTOS DE ÁLGEBRA LINEAL
Compendio organizado por Módulos (Vectores, Matrices, Inversa y Determinantes) que presenta 
los teoremas clave, equivalencias del Teorema de la Matriz Invertible y propiedades de clase.

Asignatura: Álgebra Lineal 
"""

try:
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
    from PyQt6.QtGui import QFont
    from PyQt6.QtCore import Qt
except ImportError:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
    from PyQt5.QtGui import QFont
    from PyQt5.QtCore import Qt

class PantallaTeoremas(QWidget):
    def __init__(self, callback_volver):
        super().__init__()
        self.callback_volver = callback_volver
        self.init_ui()

    def init_ui(self):
        layout_main = QVBoxLayout(self)

        # Barra Superior con botón para regresar al Menú Principal
        top_bar = QHBoxLayout()
        btn_volver = QPushButton("← Menú Principal")
        btn_volver.setFixedWidth(160)
        btn_volver.clicked.connect(self.callback_volver)
        top_bar.addWidget(btn_volver)

        lbl_titulo = QLabel("ÁLGEBRA LINEAL: COMPENDIO DE TEOREMAS POR MÓDULO")
        lbl_titulo.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold if hasattr(QFont, 'Weight') else QFont.Bold))
        lbl_titulo.setStyleSheet("color: #4A90E2;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter)
        
        top_bar.addWidget(lbl_titulo, 1)
        layout_main.addLayout(top_bar)

        # Visor del resumen de teoremas estructurado por Módulos
        txt_teoremas = QTextEdit()
        txt_teoremas.setReadOnly(True)
        
        contenido_html = """
        <h2 style='color:#1B4F72;'>📘 COMPENDIO DE TEOREMAS DE ÁLGEBRA LINEAL</h2>
        <hr style='border: 1px solid #4A90E2;'>

        <!-- ================================================================= -->
        <!-- MÓDULO I: VECTORES Y COMBINACIONES LINEALES -->
        <!-- ================================================================= -->
        <h3 style='color:#2980B9;'>MÓDULO I: VECTORES EN Rⁿ Y COMBINACIONES LINEALES</h3>
        
        <h4>1. Independencia y Dependencia Lineal</h4>
        <p><b>Definición:</b> Un conjunto de vectores {v₁, v₂, ..., vₖ} en ℝⁿ es <b>Linealmente Independiente (L.I.)</b> si la ecuación c₁v₁ + c₂v₂ + ... + cₖvₖ = 0 solo admite la solución trivial (c₁ = c₂ = ... = cₖ = 0).</p>
        <ul>
            <li><b>Teorema de la Cantidad:</b> Si k > n (más vectores que componentes/dimensiones), el conjunto es obligatoriamente <b>Linealmente Dependiente (L.D.)</b>.</li>
            <li><b>Vector Nulo:</b> Todo conjunto de vectores que contenga al vector cero (0) es L.D.</li>
        </ul>

        <h4>2. Propiedades de la Multiplicación Matriz-Vector (Ax)</h4>
        <p>Para cualquier matriz A de m×n y vectores u, v en ℝⁿ:</p>
        <ul>
            <li><b>A(u + v) = Au + Av</b> (Propiedad Aditiva).</li>
            <li><b>A(c·u) = c(Au)</b> para cualquier escalar c (Propiedad Homogénea).</li>
        </ul>

        <hr style='border: 1px solid #BDC3C7;'>

        <!-- ================================================================= -->
        <!-- MÓDULO II: OPERACIONES MATRICIALES Y ALGEBRA DE MATRICES -->
        <!-- ================================================================= -->
        <h3 style='color:#2980B9;'>MÓDULO II: ÁLGEBRA DE MATRICES</h3>

        <h4>1. Propiedades de la Suma de Matrices y Escalares</h4>
        <p>Dadas A, B, C de m×n y escalares r, s:</p>
        <ul>
            <li><b>Conmutativa:</b> A + B = B + A</li>
            <li><b>Asociativa:</b> (A + B) + C = A + (B + C)</li>
            <li><b>Neutro Aditivo:</b> A + 0 = A</li>
            <li><b>Distributiva de Escalar:</b> r(A + B) = rA + rB</li>
            <li><b>Distributiva de Suma de Escalares:</b> (r + s)A = rA + sA</li>
            <li><b>Asociativa de Escalares:</b> r(sA) = (rs)A</li>
        </ul>

        <h4>2. Propiedades de la Multiplicación de Matrices</h4>
        <ul>
            <li><b>Ley Asociativa:</b> A(BC) = (AB)C</li>
            <li><b>Ley Distributiva Izquierda:</b> A(B + C) = AB + AC</li>
            <li><b>Ley Distributiva Derecha:</b> (B + C)A = BA + CA</li>
            <li><b>Producto por Escalar:</b> r(AB) = (rA)B = A(rB)</li>
            <li><b>Matriz Identidad:</b> Iₘ A = A = A I♁</li>
        </ul>

        <h4>3. Propiedades de la Transpuesta</h4>
        <ul>
            <li><b>(Aᵀ)ᵀ = A</b></li>
            <li><b>(A + B)ᵀ = Aᵀ + Bᵀ</b></li>
            <li><b>(rA)ᵀ = r Aᵀ</b></li>
            <li><b>(AB)ᵀ = Bᵀ Aᵀ</b> (El orden del producto se invierte).</li>
        </ul>

        <hr style='border: 1px solid #BDC3C7;'>

        <!-- ================================================================= -->
        <!-- MÓDULO III: MATRIZ INVERSA, DETERMINANTES Y CRAMER (TAREA 5) -->
        <!-- ================================================================= -->
        <h3 style='color:#2980B9;'>MÓDULO III: MATRIZ INVERSA, DETERMINANTES Y REGLA DE CRAMER</h3>

        <h4>1. Teorema de la Matriz Invertible (Equivalencias)</h4>
        <p>Sea A una matriz cuadrada de n×n. Las siguientes proposiciones son lógicamente equivalentes:</p>
        <ul>
            <li><b>a)</b> A es una matriz invertible (no singular).</li>
            <li><b>b)</b> det(A) ≠ 0.</li>
            <li><b>c)</b> A tiene n posiciones pivote (Rango(A) = n).</li>
            <li><b>d)</b> El sistema Ax = 0 tiene únicamente la solución trivial.</li>
            <li><b>e)</b> Las columnas de A forman un conjunto Linealmente Independiente (L.I.).</li>
            <li><b>f)</b> Las columnas de A generan el espacio ℝⁿ.</li>
            <li><b>g)</b> Ax = b tiene solución única para cualquier vector b en ℝⁿ.</li>
        </ul>

        <h4>2. Propiedades Principales de la Matriz Inversa</h4>
        <ul>
            <li><b>Inversa de la Inversa:</b> (A⁻¹)⁻¹ = A</li>
            <li><b>Inversa del Producto:</b> (AB)⁻¹ = B⁻¹ A⁻¹</li>
            <li><b>Inversa de la Transpuesta:</b> (Aᵀ)⁻¹ = (A⁻¹)ᵀ</li>
            <li><b>Inversa del Escalar:</b> (kA)⁻¹ = (1/k) A⁻¹  (con k ≠ 0)</li>
            <li><b>Determinante de la Inversa:</b> det(A⁻¹) = 1 / det(A)</li>
        </ul>

        <h4>3. Métodos para el Cálculo de la Inversa</h4>
        <ul>
            <li><b>Gauss-Jordan:</b> Reducción de la matriz aumentada [A | I] hasta llegar a [I | A⁻¹].</li>
            <li><b>Matriz Adjunta:</b> A⁻¹ = (1 / det(A)) · adj(A), donde adj(A) = (Cofactores(A))ᵀ.</li>
        </ul>

        <h4>4. Teoremas de Determinantes y Regla de Cramer</h4>
        <ul>
            <li><b>Regla de Sarrus:</b> Válida únicamente para matrices cuadradas de orden 3×3.</li>
            <li><b>Efecto de Operaciones de Fila:</b>
                <ul>
                    <li>Intercambio de dos filas: multiplica det(A) por -1.</li>
                    <li>Reemplazo (Fᵢ → Fᵢ + k Fⱼ): NO altera el valor de det(A).</li>
                    <li>Multiplicación por escalar k (Fᵢ → k Fᵢ): multiplica det(A) por k.</li>
                </ul>
            </li>
            <li><b>Matriz Triangular:</b> El determinante es igual al producto de los elementos de su diagonal principal.</li>
            <li><b>Regla de Cramer:</b> Para un sistema Ax = b con det(A) ≠ 0, la solución es xᵢ = det(Aᵢ) / det(A), reemplazando la columna i por el vector constante b.</li>
        </ul>
        """
        
        txt_teoremas.setHtml(contenido_html)
        layout_main.addWidget(txt_teoremas)

        return self