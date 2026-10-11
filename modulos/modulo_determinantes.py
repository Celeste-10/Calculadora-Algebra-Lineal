"""
MÓDULO DE CÁLCULO DE DETERMINANTES Y REGLA DE CRAMER
Implementa el cálculo de determinantes por expansión de cofactores paso a paso, 
Método de Sarrus (evaluado para matrices 3x3) y la Regla de Cramer detallada.

Asignatura: Álgebra Lineal
"""

from logica.operaciones import formato_matriz_html, decimal_a_fraccion

def calcular_submatriz(A, fila, col):
    """Devuelve la submatriz eliminando la fila y columna indicadas."""
    return [f[:col] + f[col+1:] for i, f in enumerate(A) if i != fila]

def determinante_cofactores(A):
    """Calcula el determinante por expansión de cofactores de primer renglón."""
    n = len(A)
    if n == 1: return A[0][0]
    if n == 2: return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    det = 0.0
    for j in range(n):
        det += ((-1)**j) * A[0][j] * determinante_cofactores(calcular_submatriz(A, 0, j))
    return det

def reportar_determinantes_matriz_pasos(M, nombre="A"):
    """
    Genera el reporte detallado para una matriz M con alineación limpia:
    1. Expansión por Cofactores
    2. Método de Sarrus (Validando si aplica)
    """
    mM, nM = len(M), len(M[0])
    html = "<div style='margin-bottom: 25px; text-align: left;'>"
    html += f"<h2 style='color:#1B4F72; border-bottom: 2px solid #3498DB; padding-bottom: 5px; margin-top:0px;'>ANÁLISIS DE DETERMINANTE - MATRIZ {nombre} ({mM}×{nM})</h2>"

    if mM != nM:
        html += f"<p style='color:#C0392B; font-weight:bold;'>✘ ERROR: La Matriz {nombre} no es cuadrada ({mM}×{nM}). No tiene determinante.</p></div>"
        return html

    detM = determinante_cofactores(M)

    # 1. EXPANSIÓN POR COFACTORES
    html += "<h3 style='margin-left: 0px; color:#2C3E50;'>1. Determinante por Expansión de Cofactores (Paso a Paso)</h3>"
    html += f"<p><b>Fórmula de Expansión por Fila 1:</b> det({nombre}) = ∑ a₁ⱼ · C₁ⱼ , donde C₁ⱼ = (-1)¹⁺ʲ · det(M₁ⱼ)</p>"
    
    if nM == 2:
        a, b = M[0][0], M[0][1]
        c, d = M[1][0], M[1][0]
        html += "<ul style='line-height: 1.6; margin-left: 15px;'>"
        html += f"<li><b>Fórmula para 2×2:</b> det({nombre}) = (a₁₁ · a₂₂) - (a₁₂ · a₂₁)</li>"
        html += f"<li><b>Sustitución:</b> ({decimal_a_fraccion(a)} × {decimal_a_fraccion(d)}) - ({decimal_a_fraccion(b)} × {decimal_a_fraccion(c)}) = <b>{decimal_a_fraccion(detM)}</b></li>"
        html += "</ul>"
    else:
        html += "<ul style='line-height: 1.6; margin-left: 15px;'>"
        terminos_pasos = []
        for j in range(nM):
            elem = M[0][j]
            signo = (-1) ** (0 + j)
            signo_str = "+" if signo > 0 else "-"
            submat = calcular_submatriz(M, 0, j)
            det_sub = determinante_cofactores(submat)
            cofactor_val = signo * det_sub
            
            html += f"<li><b>Elemento a₁{j+1} = {decimal_a_fraccion(elem)}:</b> Signo (-1)¹⁺{j+1} = {signo_str}1 | "
            html += f"Menor M₁{j+1} det = {decimal_a_fraccion(det_sub)} | Cofactor C₁{j+1} = {decimal_a_fraccion(cofactor_val)}</li>"
            terminos_pasos.append(f"({decimal_a_fraccion(elem)} × {decimal_a_fraccion(cofactor_val)})")
        html += f"</ul><p><b>Suma de Términos:</b> det({nombre}) = {' + '.join(terminos_pasos)} = <b>{decimal_a_fraccion(detM)}</b></p>"

    # 2. MÉTODO DE SARRUS
    html += "<h3 style='margin-left: 0px; color:#2C3E50;'>2. Método de Sarrus</h3>"
    if nM == 3:
        d1 = M[0][0]*M[1][1]*M[2][2] + M[0][1]*M[1][2]*M[2][0] + M[0][2]*M[1][0]*M[2][1]
        d2 = M[0][2]*M[1][1]*M[2][0] + M[0][0]*M[1][2]*M[2][1] + M[0][1]*M[1][0]*M[2][2]
        det_sarrus = d1 - d2
        html += f"""
        <blockquote style="background-color: #EBF5FB; border-left: 4px solid #3498DB; padding: 10px; margin-left: 0px;">
            <b style="color: #2980B9;">✔ EL MÉTODO DE SARRUS SÍ ES APLICABLE (Matriz 3×3)</b><br>
            &bull; Diagonales Principales (+): ({M[0][0]}·{M[1][1]}·{M[2][2]}) + ({M[0][1]}·{M[1][2]}·{M[2][0]}) + ({M[0][2]}·{M[1][0]}·{M[2][1]}) = <b>{decimal_a_fraccion(d1)}</b><br>
            &bull; Diagonales Secundarias (-): ({M[0][2]}·{M[1][1]}·{M[2][0]}) + ({M[0][0]}·{M[1][2]}·{M[2][1]}) + ({M[0][1]}·{M[1][0]}·{M[2][2]}) = <b>{decimal_a_fraccion(d2)}</b><br>
            &bull; <b>det({nombre}) = {decimal_a_fraccion(d1)} - ({decimal_a_fraccion(d2)}) = {decimal_a_fraccion(det_sarrus)}</b>
        </blockquote>
        """
    else:
        html += f"""
        <blockquote style="background-color: #FDEDEC; border-left: 4px solid #E74C3C; padding: 10px; margin-left: 0px;">
            <b style="color: #C0392B;">✘ EL MÉTODO DE SARRUS NO ES APLICABLE</b><br>
            <i>Razón: La Regla de Sarrus es un algoritmo exclusivo para matrices de orden 3×3. La Matriz {nombre} es de dimensión {nM}×{nM}.</i>
        </blockquote>
        """
    html += "</div>"
    return html

def reporte_determinantes_tres_matrices(A, B, C):
    """Genera el reporte para las 3 matrices en la pestaña Operaciones Matriciales."""
    html = reportar_determinantes_matriz_pasos(A, "A")
    html += "<hr style='border: 1px dashed #BDC3C7; margin: 20px 0;'>"
    html += reportar_determinantes_matriz_pasos(B, "B")
    html += "<hr style='border: 1px dashed #BDC3C7; margin: 20px 0;'>"
    html += reportar_determinantes_matriz_pasos(C, "C")
    return html

def resolver_cramer_pestaña_sistemas_pasos(A, b):
    """
    Exclusivo para la pestaña 'Ecuación Ax = b':
    Lee directamente A y b del sistema ingresado y resuelve por Cramer paso a paso estilo pizarra,
    desglosando detalladamente el determinante principal |A| y los determinantes modificados.
    """
    mA, nA = len(A), len(A[0])
    html = "<div style='text-align: left; font-size: 13px;'>"
    html += "<h2 style='color:#1B4F72; border-bottom:2px solid #2980B9; padding-bottom:5px;'>SOLUCIÓN PASO A PASO POR REGLA DE CRAMER</h2>"

    if mA != nA:
        html += f"<p style='color:#C0392B; font-weight:bold;'><b>✘ ERROR:</b> La Regla de Cramer requiere que la matriz de coeficientes A sea cuadrada (n×n). La matriz del sistema es de {mA}×{nA}.</p></div>"
        return html, "<b style='color:#C0392B;'>El sistema no es cuadrado. Usar Gauss-Jordan.</b>"

    detA = determinante_cofactores(A)

    # Paso 1: Determinante Principal |A| desglosado paso a paso
    html += "<h3>1. Determinante Principal |A| (Desglose por Cofactores de la Fila 1):</h3>"
    
    if nA == 2:
        d1 = A[0][0] * A[1][1]
        d2 = A[0][1] * A[1][0]
        html += f"<p style='font-family:Consolas, monospace;'>&bull; |A| = ({decimal_a_fraccion(A[0][0])})({decimal_a_fraccion(A[1][1])}) - ({decimal_a_fraccion(A[0][1])})({decimal_a_fraccion(A[1][0])}) = ({decimal_a_fraccion(d1)}) - ({decimal_a_fraccion(d2)}) = <b style='font-size:15px; color:#1B4F72;'>{decimal_a_fraccion(detA)}</b></p>"
    else:
        html += "<ul style='line-height: 1.6; margin-left: 15px;'>"
        terminos_pasos_A = []
        for j in range(nA):
            elem = A[0][j]
            signo = (-1) ** (0 + j)
            signo_str = "+" if signo > 0 else "-"
            submat = calcular_submatriz(A, 0, j)
            det_sub = determinante_cofactores(submat)
            cofactor_val = signo * det_sub
            
            html += f"<li><b>Elemento a₁{j+1} = {decimal_a_fraccion(elem)}:</b> Signo (-1)¹⁺{j+1} = {signo_str}1 | Menor det(M₁{j+1}) = {decimal_a_fraccion(det_sub)} | Cofactor C₁{j+1} = {decimal_a_fraccion(cofactor_val)}</li>"
            terminos_pasos_A.append(f"({decimal_a_fraccion(elem)} × {decimal_a_fraccion(cofactor_val)})")
        
        suma_expr = ' + '.join(terminos_pasos_A)
        html += f"</ul><p><b>Suma de Cofactores:</b> |A| = {suma_expr} = <b style='font-size:15px; color:#1B4F72;'>{decimal_a_fraccion(detA)}</b></p>"

    if abs(detA) < 1e-9:
        html += "<blockquote style='background-color:#FDEDEC; border-left:4px solid #C0392B; padding:10px;'>"
        html += "<b style='color:#C0392B;'>✘ EL SISTEMA NO SE PUEDE RESOLVER POR CRAMER</b><br>"
        html += "<i>El determinante principal es cero (|A| = 0). La matriz es singular y el sistema no admite solución única.</i>"
        html += "</blockquote></div>"
        return html, "<b style='color:#C0392B;'>|A| = 0. No existe solución única por Cramer.</b>"

    # Paso 2: Desarrollo por variable estilo pizarra con desglose de sus determinantes
    html += "<hr style='border:1px solid #BDC3C7;'><h3>2. Determinantes Modificados y Sustitución de Variables:</h3>"
    
    nombres_var = [f"x<sub>{j+1}</sub>" for j in range(nA)]
    if nA == 2: nombres_var = ["x", "y"]
    elif nA == 3: nombres_var = ["x", "y", "z"]

    soluciones = []

    for j in range(nA):
        var = nombres_var[j]
        Aj = [fila[:] for fila in A]
        for i in range(mA):
            Aj[i][j] = b[i]

        detAj = determinante_cofactores(Aj)
        xj = detAj / detA
        soluciones.append(f"{var} = {decimal_a_fraccion(xj)}")

        html += "<div style='background-color:#F8F9F9; border:1px solid #D5D8DC; border-radius:6px; padding:10px; margin-bottom:15px;'>"
        html += f"<h4 style='color:#2980B9; margin-top:0px;'>Cálculo para {var}:</h4>"
        html += formato_matriz_html(Aj, f"Matriz |A<sub>{var}</sub>| (Columna {j+1} reemplazada por b):")

        if nA == 2:
            diag1 = Aj[0][0] * Aj[1][1]
            diag2 = Aj[0][1] * Aj[1][0]
            html += f"<p style='font-family:Consolas, monospace;'>&bull; |A<sub>{var}</sub>| = ({decimal_a_fraccion(Aj[0][0])})({decimal_a_fraccion(Aj[1][1])}) - ({decimal_a_fraccion(Aj[0][1])})({decimal_a_fraccion(Aj[1][0])}) = ({decimal_a_fraccion(diag1)}) - ({decimal_a_fraccion(diag2)}) = <b>{decimal_a_fraccion(detAj)}</b></p>"
        else:
            terminos_pasos_Aj = []
            for col in range(nA):
                elem = Aj[0][col]
                signo = (-1) ** (0 + col)
                submat = calcular_submatriz(Aj, 0, col)
                det_sub = determinante_cofactores(submat)
                cofactor_val = signo * det_sub
                terminos_pasos_Aj.append(f"({decimal_a_fraccion(elem)} × {decimal_a_fraccion(cofactor_val)})")
            
            suma_expr_Aj = ' + '.join(terminos_pasos_Aj)
            html += f"<p>&bull; |A<sub>{var}</sub>| por cofactores = {suma_expr_Aj} = <b>{decimal_a_fraccion(detAj)}</b></p>"

        det_aj_str = decimal_a_fraccion(detAj)
        det_a_str = decimal_a_fraccion(detA)
        xj_str = decimal_a_fraccion(xj)

        html += f"<p style='font-size:14px;'>&rArr; {var} = |A<sub>{var}</sub>| / |A| = ({det_aj_str}) / ({det_a_str}) &rArr; <span style='border:2px solid #27AE60; padding:3px 8px; background-color:#E8F8F5; border-radius:4px;'><b style='color:#27AE60;'>{var} = {xj_str}</b></span></p></div>"

    html += "</div>"
    resumen_final = f"<h3>Solución Final por Cramer:</h3><p style='font-size:15px; color:#27AE60;'><b>" + " &nbsp;&nbsp;|&nbsp;&nbsp; ".join(soluciones) + "</b></p>"
    
    return html, resumen_final