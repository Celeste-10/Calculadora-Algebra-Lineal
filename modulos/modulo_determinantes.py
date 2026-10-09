"""
MÓDULO DE CÁLCULO DE DETERMINANTES Y REGLA DE CRAMER
Implementa el cálculo de determinantes por expansión de cofactores, Método de Sarrus (3x3), 
reducción a matriz triangular superior y la resolución de sistemas lineales por Regla de Cramer.

Asignatura: Álgebra Lineal 
"""

from logica.operaciones import resolver_gauss_jordan, formato_matriz_html, decimal_a_fraccion
# ------------------------------------------------------------------------------
# DETERMINANTES (SARRUS, COFACTORES Y CRAMER)
# ------------------------------------------------------------------------------

def calcular_submatriz(A, fila, col):
    return [f[:col] + f[col+1:] for i, f in enumerate(A) if i != fila]

def determinante_cofactores(A):
    n = len(A)
    if n == 1: return A[0][0]
    if n == 2: return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    det = 0.0
    for j in range(n):
        det += ((-1)**j) * A[0][j] * determinante_cofactores(calcular_submatriz(A, 0, j))
    return det

def reporte_determinantes_y_cramer(A, B):
    """Genera el reporte detallado de Cofactores paso a paso, Sarrus (evaluando si aplica o no) y Regla de Cramer."""
    mA, nA = len(A), len(A[0])
    html = "<h2>1. Determinante por Expansión de Cofactores (Paso a Paso)</h2>"

    if mA != nA:
        html += f"<p style='color:#C0392B;'><b>ERROR:</b> La Matriz A no es cuadrada ({mA}×{nA}). No se puede calcular el determinante.</p>"
    else:
        # --- DESGLOSE PASO A PASO DE COFACTORES ---
        detA = determinante_cofactores(A)
        html += f"<p><b>Fórmula de Expansión por la Fila 1:</b> det(A) = ∑ a₁ⱼ · C₁ⱼ , donde C₁ⱼ = (-1)¹⁺ʲ · det(M₁ⱼ)</p>"
        html += "<ul>"
        
        if nA == 2:
            a, b = A[0][0], A[0][1]
            c, d = A[1][0], A[1][1]
            html += f"<li><b>Fórmula para 2×2:</b> det(A) = (a₁₁ · a₂₂) - (a₁₂ · a₂₁)</li>"
            html += f"<li><b>Sustitución:</b> ({decimal_a_fraccion(a)} × {decimal_a_fraccion(d)}) - ({decimal_a_fraccion(b)} × {decimal_a_fraccion(c)}) = <b>{decimal_a_fraccion(detA)}</b></li>"
        else:
            terminos_pasos = []
            for j in range(nA):
                elem = A[0][j]
                signo = (-1) ** (0 + j)
                signo_str = "+" if signo > 0 else "-"
                submat = calcular_submatriz(A, 0, j)
                det_sub = determinante_cofactores(submat)
                cofactor_val = signo * det_sub
                
                html += f"<li><b>Elemento a₁{j+1} = {decimal_a_fraccion(elem)}:</b> Signo (-1)¹⁺{j+1} = {signo_str}1 | "
                html += f"Menor M₁{j+1} det = {decimal_a_fraccion(det_sub)} | Cofactor C₁{j+1} = {decimal_a_fraccion(cofactor_val)}</li>"
                
                terminos_pasos.append(f"({decimal_a_fraccion(elem)} × {decimal_a_fraccion(cofactor_val)})")
            
            html += f"</ul><p><b>Suma de Términos:</b> det(A) = {' + '.join(terminos_pasos)} = <b>{decimal_a_fraccion(detA)}</b></p>"

        # --- EVALUACIÓN EXPLICITA DEL MÉTODO DE SARRUS ---
        html += "<hr><h2>2. Método de Sarrus</h2>"
        if nA == 3:
            d1 = A[0][0]*A[1][1]*A[2][2] + A[0][1]*A[1][2]*A[2][0] + A[0][2]*A[1][0]*A[2][1]
            d2 = A[0][2]*A[1][1]*A[2][0] + A[0][0]*A[1][2]*A[2][1] + A[0][1]*A[1][0]*A[2][2]
            det_sarrus = d1 - d2
            html += f"""
            <blockquote style="background-color: #EBF5FB; border-left: 4px solid #3498DB; padding: 10px;">
                <b style="color: #2980B9;">✔ EL MÉTODO DE SARRUS SÍ ES APLICABLE (Matriz 3×3)</b><br>
                &bull; Diagonales Principales (+): ({A[0][0]}·{A[1][1]}·{A[2][2]}) + ({A[0][1]}·{A[1][2]}·{A[2][0]}) + ({A[0][2]}·{A[1][0]}·{A[2][1]}) = <b>{decimal_a_fraccion(d1)}</b><br>
                &bull; Diagonales Secundarias (-): ({A[0][2]}·{A[1][1]}·{A[2][0]}) + ({A[0][0]}·{A[1][2]}·{A[2][1]}) + ({A[0][1]}·{A[1][0]}·{A[2][2]}) = <b>{decimal_a_fraccion(d2)}</b><br>
                &bull; <b>det(A) = {decimal_a_fraccion(d1)} - ({decimal_a_fraccion(d2)}) = {decimal_a_fraccion(det_sarrus)}</b>
            </blockquote>
            """
        else:
            html += f"""
            <blockquote style="background-color: #FDEDEC; border-left: 4px solid #E74C3C; padding: 10px;">
                <b style="color: #C0392B;">✘ EL MÉTODO DE SARRUS NO ES APLICABLE</b><br>
                <i>Razón: La Regla de Sarrus es un algoritmo exclusivo para matrices de orden 3×3. La Matriz A ingresada es de dimensión {nA}×{nA}.</i>
            </blockquote>
            """

    # --- REGLA DE CRAMER ---
    html += "<hr><h2>3. Solución de Sistema por Regla de Cramer (Ax = b)</h2>"
    if mA == nA and len(B) == mA:
        b = [B[i][0] for i in range(mA)]
        detA = determinante_cofactores(A)
        if abs(detA) < 1e-9:
            html += "<p style='color:#C0392B;'><b>DICTAMEN:</b> El sistema no tiene solución única por Cramer porque det(A) = 0 (Matriz Singular).</p>"
        else:
            html += f"<p>Tomando la Columna 1 de la Matriz B como el vector constante <b>b = {b}</b>:</p><ul>"
            for j in range(nA):
                # Sustituir la columna j por el vector b
                Aj = [fila[:] for fila in A]
                for i in range(mA):
                    Aj[i][j] = b[i]
                detAj = determinante_cofactores(Aj)
                xj = detAj / detA
                html += f"<li><b>Variable x<sub>{j+1}</sub>:</b> det(A<sub>{j+1}</sub>) / det(A) = {decimal_a_fraccion(detAj)} / ({decimal_a_fraccion(detA)}) = <b>{decimal_a_fraccion(xj)}</b></li>"
            html += "</ul>"
    else:
        html += f"<p style='color:#7F8C8D;'>Para aplicar Cramer, la Matriz A debe ser cuadrada y el número de filas de B ({len(B)}) debe coincidir con las dimensiones de A ({mA}).</p>"

    return html