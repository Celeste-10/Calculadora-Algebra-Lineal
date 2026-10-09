"""
MÓDULO DE ÁLGEBRA DE MATRICES 
Implementa las operaciones con matrices (suma, resta, escalar, producto y transposición), 
inversa por Gauss-Jordan y Matriz Adjunta, comprobación A·A⁻¹=I y el Verificador de Propiedades.

Asignatura: Álgebra Lineal 
"""

from logica.operaciones import resolver_gauss_jordan, formato_matriz_html, decimal_a_fraccion
from modulos.modulo_determinantes import determinante_cofactores

# ------------------------------------------------------------------------------
# 2. MÓDULO DE OPERACIONES MATRICIALES BÁSICAS
# ------------------------------------------------------------------------------

def sumar_matrices(A, B):
    """
    Suma dos matrices A y B de dimensión m x n.
    Equivalente algebraico: Cᵢⱼ = Aᵢⱼ + Bᵢⱼ
    """
    m_A, n_A = len(A), len(A[0])
    m_B, n_B = len(B), len(B[0])

    if m_A != m_B or n_A != n_B:
        raise ValueError(f"Incompatibilidad de dimensiones: {m_A}x{n_A} no se puede sumar con {m_B}x{n_B}.")

    return [[A[i][j] + B[i][j] for j in range(n_A)] for i in range(m_A)]

def restar_matrices(A, B):
    """
    Resta dos matrices A y B de dimensión m x n.
    Equivalente algebraico: Cᵢⱼ = Aᵢⱼ - Bᵢⱼ
    """
    m_A, n_A = len(A), len(A[0])
    m_B, n_B = len(B), len(B[0])

    if m_A != m_B or n_A != n_B:
        raise ValueError(f"Incompatibilidad de dimensiones: {m_A}x{n_A} no se puede restar con {m_B}x{n_B}.")

    return [[A[i][j] - B[i][j] for j in range(n_A)] for i in range(m_A)]

def escalar_por_matriz(c, A):
    """
    Multiplica un escalar 'c' por una matriz A de m x n.
    Equivalente algebraico: (c·A)ᵢⱼ = c · Aᵢⱼ
    """
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiplicar_matrices(A, B):
    """
    Multiplica dos matrices A (m x n) y B (n x p).
    Equivalente algebraico: Cᵢⱼ = ∑ₖ Aᵢₖ · Bₖⱼ
    Usa tres bucles anidados respetando la restricción de Python puro.
    """
    m_A, n_A = len(A), len(A[0])
    m_B, n_B = len(B), len(B[0])

    if n_A != m_B:
        raise ValueError(f"Incompatibilidad de dimensiones: Columnas de A ({n_A}) != Filas de B ({m_B}).")

    # Inicializar matriz resultado C con ceros (m_A x n_B)
    C = [[0.0 for _ in range(n_B)] for _ in range(m_A)]

    # Algoritmo clásico de producto matricial
    for i in range(m_A):         # Fila de A
        for j in range(n_B):     # Columna de B
            suma_producto = 0.0
            for k in range(n_A): # Sumatoria de los productos
                suma_producto += A[i][k] * B[k][j]
            C[i][j] = suma_producto

    return C



def sumar_matrices_pasos(A, B):
    mA, nA = len(A), len(A[0])
    mB, nB = len(B), len(B[0])
    if mA != mB or nA != nB:
        raise ValueError(f"Incompatibilidad de dimensiones: {mA}x{nA} vs {mB}x{nB}.")

    res = [[A[i][j] + B[i][j] for j in range(nA)] for i in range(mA)]
    
    html = "<h3>Procedimiento Suma (A + B):</h3>"
    html += "<b>Detalle elemento por elemento:</b><br><ul>"
    for i in range(mA):
        for j in range(nA):
            html += f"<li>C<sub>{i+1}{j+1}</sub> = {decimal_a_fraccion(A[i][j])} + {decimal_a_fraccion(B[i][j])} = <b>{decimal_a_fraccion(res[i][j])}</b></li>"
    html += "</ul>"
    html += formato_matriz_html(res, "Matriz Resultante (A + B)")
    return res, html

def restar_matrices_pasos(A, B):
    mA, nA = len(A), len(A[0])
    mB, nB = len(B), len(B[0])
    if mA != mB or nA != nB:
        raise ValueError(f"Incompatibilidad de dimensiones: {mA}x{nA} vs {mB}x{nB}.")

    res = [[A[i][j] - B[i][j] for j in range(nA)] for i in range(mA)]
    
    html = "<h3>Procedimiento Resta (A - B):</h3>"
    html += "<b>Detalle elemento por elemento:</b><br><ul>"
    for i in range(mA):
        for j in range(nA):
            html += f"<li>C<sub>{i+1}{j+1}</sub> = {decimal_a_fraccion(A[i][j])} - ({decimal_a_fraccion(B[i][j])}) = <b>{decimal_a_fraccion(res[i][j])}</b></li>"
    html += "</ul>"
    html += formato_matriz_html(res, "Matriz Resultante (A - B)")
    return res, html

def multiplicar_matrices_pasos(A, B):
    mA, nA = len(A), len(A[0])
    mB, nB = len(B), len(B[0])
    if nA != mB:
        raise ValueError(f"Incompatibilidad de dimensiones: Columnas de A ({nA}) != Filas de B ({mB}).")

    C = [[0.0 for _ in range(nB)] for _ in range(mA)]
    html = "<h3>Procedimiento Multiplicación (A × B):</h3>"
    html += "<b>Cálculo de cada posición:</b><br><ul>"

    for i in range(mA):
        for j in range(nB):
            terminos = []
            suma = 0.0
            for k in range(nA):
                prod = A[i][k] * B[k][j]
                suma += prod
                terminos.append(f"({decimal_a_fraccion(A[i][k])} × {decimal_a_fraccion(B[k][j])})")
            C[i][j] = suma
            expr_str = " + ".join(terminos)
            html += f"<li>C<sub>{i+1}{j+1}</sub> = {expr_str} = <b>{decimal_a_fraccion(suma)}</b></li>"
    
    html += "</ul>"
    html += formato_matriz_html(C, "Matriz Resultante (A × B)")
    return C, html

def traspuestas_ambas_matrices_pasos(A, B):
    # Traspuesta de A
    mA, nA = len(A), len(A[0])
    AT = [[A[j][i] for j in range(mA)] for i in range(nA)]
    
    # Traspuesta de B
    mB, nB = len(B), len(B[0])
    BT = [[B[j][i] for j in range(mB)] for i in range(nB)]
    
    html = "<h3>1. Matriz Traspuesta de A (Aᵀ):</h3>"
    html += f"<p>Se intercambian filas por columnas (Dimensión original: {mA}x{nA} → Resultante: {nA}x{mA}):</p>"
    html += formato_matriz_html(AT, "Aᵀ")
    
    html += "<hr><h3>2. Matriz Traspuesta de B (Bᵀ):</h3>"
    html += f"<p>Se intercambian filas por columnas (Dimensión original: {mB}x{nB} → Resultante: {nB}x{mB}):</p>"
    html += formato_matriz_html(BT, "Bᵀ")
    
    return (AT, BT), html


def _procesar_inversa_individual(M, nombre):
    mM, nM = len(M), len(M[0])
    
    if mM != nM:
        return None, f"<h3>Matriz Inversa de {nombre} ({nombre}⁻¹):</h3><p style='color:#C0392B;'><b>NO EXISTE:</b> La matriz {nombre} no es cuadrada (Dimensión: {mM}x{nM}).</p>"

    # Caso 2x2 con fórmula estéticamente formateada para QTextEdit
    if mM == 2:
        a, b = M[0][0], M[0][1]
        c, d = M[1][0], M[1][1]
        det = (a * d) - (b * c)
        
        html = f"<h3>Matriz Inversa de {nombre} ({nombre}⁻¹):</h3>"
        html += f"<p><b>1. Determinante det({nombre}):</b> ({decimal_a_fraccion(a)})({decimal_a_fraccion(d)}) - ({decimal_a_fraccion(b)})({decimal_a_fraccion(c)}) = <b>{decimal_a_fraccion(det)}</b></p>"
        
        if abs(det) < 1e-9:
            html += f"<p style='color:#C0392B;'><b>DICTAMEN:</b> det({nombre}) = 0. La matriz {nombre} no es invertible (Es Singular).</p>"
            return None, html
            
        inv = [
            [ d / det, -b / det],
            [-c / det,  a / det]
        ]
        
        # Estructura matemática compatible con PyQt
        html += f"""
        <p><b>2. Aplicando la fórmula para matrices 2x2:</b></p>
        <blockquote style="font-size: 13px;">
            <b>Fórmula teórica:</b> {nombre}⁻¹ = (1 / det({nombre})) &middot; [ [d, -b], [-c, a] ]<br><br>
            <b>Sustituyendo valores:</b> {nombre}⁻¹ = (1 / {decimal_a_fraccion(det)}) &middot; [ [{decimal_a_fraccion(d)}, {decimal_a_fraccion(-b)}], [{decimal_a_fraccion(-c)}, {decimal_a_fraccion(a)}] ]
        </blockquote>
        """
        html += formato_matriz_html(inv, f"Matriz Inversa {nombre}⁻¹")
        return inv, html

    # Caso n x n mediante Método Gauss-Jordan [M | I]
    matriz_aumentada = []
    for i in range(mM):
        fila_I = [1.0 if i == j else 0.0 for j in range(nM)]
        matriz_aumentada.append(M[i][:] + fila_I)

    mat_rref, pasos_log, _ = resolver_gauss_jordan(matriz_aumentada, mM, nM * 2)

    es_invertible = True
    for i in range(mM):
        for j in range(nM):
            if abs(mat_rref[i][j] - (1.0 if i == j else 0.0)) > 1e-9:
                es_invertible = False
                break

    html = f"<h3>Matriz Inversa de {nombre} ({nombre}⁻¹) por Gauss-Jordan [{nombre} | I]:</h3>"
    html += "<b>Pasos de reducción por filas:</b><br><br>" + "<br><br>".join(pasos_log) + "<br><br>"

    if not es_invertible:
        html += f"<p style='color:#C0392B;'><b>DICTAMEN:</b> La matriz {nombre} no es invertible (Es Singular).</p>"
        return None, html

    inv = [[mat_rref[i][j + nM] for j in range(nM)] for i in range(mM)]
    html += formato_matriz_html(inv, f"Matriz Inversa {nombre}⁻¹")
    return inv, html


def inversas_ambas_matrices_pasos(A, B):
    invA, htmlA = _procesar_inversa_individual(A, "A")
    invB, htmlB = _procesar_inversa_individual(B, "B")
    
    html_total = htmlA + "<hr style='margin: 20px 0;'>" + htmlB
    return (invA, invB), html_total

# ==============================================================================
# TEOREMAS Y PROPIEDADES MATRICIALES (PASO A PASO)
# ==============================================================================

def crear_matriz_cero(m, n):
    return [[0.0 for _ in range(n)] for _ in range(m)]

def crear_matriz_identidad(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def obtener_transpuesta(A):
    m, n = len(A), len(A[0])
    return [[A[j][i] for j in range(m)] for i in range(n)]

def son_matrices_iguales(A, B, tol=1e-7):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False
    for i in range(len(A)):
        for j in range(len(A[0])):
            if abs(A[i][j] - B[i][j]) > tol:
                return False
    return True

# ------------------------------------------------------------------------------
# 1. Propiedades de la Suma y Escalares
# ------------------------------------------------------------------------------
def verificar_propiedades_suma(A, B, C, r, s):
    html = "<h2>Demostración de Propiedades de la Suma de Matrices</h2>"

    # 1. A + B = B + A
    try:
        AB = sumar_matrices(A, B)
        BA = sumar_matrices(B, A)
        html += "<h3>1. Propiedad Conmutativa: A + B = B + A</h3>"
        html += formato_matriz_html(AB, "Lado Izquierdo: A + B")
        html += formato_matriz_html(BA, "Lado Derecho: B + A")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(AB, BA) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>1. Propiedad Conmutativa: A + B = B + A</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p><hr>"

    # 2. (A + B) + C = A + (B + C)
    try:
        AB = sumar_matrices(A, B) if 'AB' not in locals() else AB
        BC = sumar_matrices(B, C)
        AB_C = sumar_matrices(AB, C)
        A_BC = sumar_matrices(A, BC)
        html += "<h3>2. Propiedad Asociativa: (A + B) + C = A + (B + C)</h3>"
        html += formato_matriz_html(AB_C, "Lado Izquierdo: (A + B) + C")
        html += formato_matriz_html(A_BC, "Lado Derecho: A + (B + C)")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(AB_C, A_BC) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>2. Propiedad Asociativa: (A + B) + C = A + (B + C)</h3><p style='color:red;'>No evaluable por dimensiones incompatibles: {e}</p><hr>"

    # 3. A + 0 = A
    try:
        O = crear_matriz_cero(len(A), len(A[0]))
        AO = sumar_matrices(A, O)
        html += "<h3>3. Neutro Aditivo: A + 0 = A</h3>"
        html += formato_matriz_html(AO, "Lado Izquierdo: A + 0")
        html += formato_matriz_html(A, "Lado Derecho: A")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(AO, A) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>3. Neutro Aditivo: A + 0 = A</h3><p style='color:red;'>Error: {e}</p><hr>"

    # 4. r(A + B) = rA + rB
    try:
        AB = sumar_matrices(A, B) if 'AB' not in locals() else AB
        r_AB = escalar_por_matriz(r, AB)
        rA_rB = sumar_matrices(escalar_por_matriz(r, A), escalar_por_matriz(r, B))
        html += "<h3>4. Distributiva respecto a la suma matricial: r(A + B) = rA + rB</h3>"
        html += formato_matriz_html(r_AB, f"Lado Izquierdo: {r}(A + B)")
        html += formato_matriz_html(rA_rB, f"Lado Derecho: {r}A + {r}B")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(r_AB, rA_rB) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>4. Distributiva respecto a la suma matricial: r(A + B) = rA + rB</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p><hr>"

    # 5. (r + s)A = rA + sA
    try:
        rs_A = escalar_por_matriz(r + s, A)
        rA_sA = sumar_matrices(escalar_por_matriz(r, A), escalar_por_matriz(s, A))
        html += "<h3>5. Distributiva respecto a la suma de escalares: (r + s)A = rA + sA</h3>"
        html += formato_matriz_html(rs_A, f"Lado Izquierdo: ({r} + {s})A")
        html += formato_matriz_html(rA_sA, f"Lado Derecho: {r}A + {s}A")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(rs_A, rA_sA) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>5. Distributiva respecto a la suma de escalares: (r + s)A = rA + sA</h3><p style='color:red;'>Error: {e}</p><hr>"

    # 6. r(sA) = (rs)A
    try:
        r_sA = escalar_por_matriz(r, escalar_por_matriz(s, A))
        rsA = escalar_por_matriz(r * s, A)
        html += "<h3>6. Propiedad Asociativa de la Multiplicación por Escalar: r(sA) = (rs)A</h3>"
        html += formato_matriz_html(r_sA, f"Lado Izquierdo: {r}({s}A)")
        html += formato_matriz_html(rsA, f"Lado Derecho: ({r}·{s})A")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(r_sA, rsA) else '✘ No cumple'}</p>"
    except Exception as e:
        html += f"<h3>6. Propiedad Asociativa de la Multiplicación por Escalar: r(sA) = (rs)A</h3><p style='color:red;'>Error: {e}</p>"

    return html

# ------------------------------------------------------------------------------
# 2. Propiedades de la Multiplicación
# ------------------------------------------------------------------------------
def verificar_propiedades_multiplicacion(A, B, C, r):
    html = "<h2>Demostración de Propiedades de la Multiplicación de Matrices</h2>"

    # 1. A(BC) = (AB)C
    try:
        A_BC = multiplicar_matrices(A, multiplicar_matrices(B, C))
        AB_C = multiplicar_matrices(multiplicar_matrices(A, B), C)
        html += "<h3>1. Ley Asociativa: A(BC) = (AB)C</h3>"
        html += formato_matriz_html(A_BC, "Lado Izquierdo: A(BC)")
        html += formato_matriz_html(AB_C, "Lado Derecho: (AB)C")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(A_BC, AB_C) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>1. Ley Asociativa: A(BC) = (AB)C</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p><hr>"

    # 2. A(B + C) = AB + AC
    try:
        A_BplusC = multiplicar_matrices(A, sumar_matrices(B, C))
        AB_plus_AC = sumar_matrices(multiplicar_matrices(A, B), multiplicar_matrices(A, C))
        html += "<h3>2. Ley Distributiva Izquierda: A(B + C) = AB + AC</h3>"
        html += formato_matriz_html(A_BplusC, "Lado Izquierdo: A(B + C)")
        html += formato_matriz_html(AB_plus_AC, "Lado Derecho: AB + AC")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(A_BplusC, AB_plus_AC) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>2. Ley Distributiva Izquierda: A(B + C) = AB + AC</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p><hr>"

    # 3. (B + C)A = BA + CA
    try:
        BplusC_A = multiplicar_matrices(sumar_matrices(B, C), A)
        BA_plus_CA = sumar_matrices(multiplicar_matrices(B, A), multiplicar_matrices(C, A))
        html += "<h3>3. Ley Distributiva Derecha: (B + C)A = BA + CA</h3>"
        html += formato_matriz_html(BplusC_A, "Lado Izquierdo: (B + C)A")
        html += formato_matriz_html(BA_plus_CA, "Lado Derecho: BA + CA")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(BplusC_A, BA_plus_CA) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>3. Ley Distributiva Derecha: (B + C)A = BA + CA</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p><hr>"

    # 4. r(AB) = (rA)B = A(rB)
    try:
        AB = multiplicar_matrices(A, B)
        r_AB = escalar_por_matriz(r, AB)
        rA_B = multiplicar_matrices(escalar_por_matriz(r, A), B)
        A_rB = multiplicar_matrices(A, escalar_por_matriz(r, B))
        html += "<h3>4. Multiplicación con Escalar: r(AB) = (rA)B = A(rB)</h3>"
        html += formato_matriz_html(r_AB, f"r(AB) con r={r}")
        html += formato_matriz_html(rA_B, "(rA)B")
        html += formato_matriz_html(A_rB, "A(rB)")
        cumple = son_matrices_iguales(r_AB, rA_B) and son_matrices_iguales(r_AB, A_rB)
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if cumple else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>4. Multiplicación con Escalar: r(AB) = (rA)B = A(rB)</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p><hr>"

    # 5. Im A = A = A In
    try:
        m, n = len(A), len(A[0])
        Im = crear_matriz_identidad(m)
        In = crear_matriz_identidad(n)
        Im_A = multiplicar_matrices(Im, A)
        A_In = multiplicar_matrices(A, In)
        html += "<h3>5. Identidad para la Multiplicación: Iₘ A = A = A Iₙ</h3>"
        html += formato_matriz_html(Im_A, "Iₘ A")
        html += formato_matriz_html(A, "A")
        html += formato_matriz_html(A_In, "A Iₙ")
        cumple = son_matrices_iguales(Im_A, A) and son_matrices_iguales(A, A_In)
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if cumple else '✘ No cumple'}</p>"
    except Exception as e:
        html += f"<h3>5. Identidad para la Multiplicación: Iₘ A = A = A Iₙ</h3><p style='color:red;'>Error: {e}</p>"

    return html

# ------------------------------------------------------------------------------
# 3. Propiedades de la Transpuesta
# ------------------------------------------------------------------------------
def verificar_propiedades_transpuesta(A, B, r):
    html = "<h2>Demostración de Propiedades de la Transpuesta de Matrices</h2>"

    # 1. (Aᵀ)ᵀ = A
    AT = obtener_transpuesta(A)
    ATT = obtener_transpuesta(AT)
    html += "<h3>1. Transpuesta de la Transpuesta: (Aᵀ)ᵀ = A</h3>"
    html += formato_matriz_html(ATT, "Lado Izquierdo: (Aᵀ)ᵀ")
    html += formato_matriz_html(A, "Lado Derecho: A")
    html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(ATT, A) else '✘ No cumple'}</p><hr>"

    # 2. (A + B)ᵀ = Aᵀ + Bᵀ
    try:
        A_plus_B_T = obtener_transpuesta(sumar_matrices(A, B))
        AT_plus_BT = sumar_matrices(AT, obtener_transpuesta(B))
        html += "<h3>2. Transpuesta de la Suma: (A + B)ᵀ = Aᵀ + Bᵀ</h3>"
        html += formato_matriz_html(A_plus_B_T, "Lado Izquierdo: (A + B)ᵀ")
        html += formato_matriz_html(AT_plus_BT, "Lado Derecho: Aᵀ + Bᵀ")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(A_plus_B_T, AT_plus_BT) else '✘ No cumple'}</p><hr>"
    except Exception as e:
        html += f"<h3>2. Transpuesta de la Suma: (A + B)ᵀ = Aᵀ + Bᵀ</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p><hr>"

    # 3. (rA)ᵀ = r Aᵀ
    rA_T = obtener_transpuesta(escalar_por_matriz(r, A))
    r_AT = escalar_por_matriz(r, AT)
    html += "<h3>3. Transpuesta del Producto por Escalar: (rA)ᵀ = r Aᵀ</h3>"
    html += formato_matriz_html(rA_T, f"Lado Izquierdo: ({r}A)ᵀ")
    html += formato_matriz_html(r_AT, f"Lado Derecho: {r} Aᵀ")
    html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(rA_T, r_AT) else '✘ No cumple'}</p><hr>"

    # 4. (AB)ᵀ = Bᵀ Aᵀ
    try:
        AB_T = obtener_transpuesta(multiplicar_matrices(A, B))
        BT_AT = multiplicar_matrices(obtener_transpuesta(B), AT)
        html += "<h3>4. Transpuesta del Producto Matricial: (AB)ᵀ = Bᵀ Aᵀ</h3>"
        html += formato_matriz_html(AB_T, "Lado Izquierdo: (AB)ᵀ")
        html += formato_matriz_html(BT_AT, "Lado Derecho: Bᵀ Aᵀ")
        html += f"<p><b>Dictamen:</b> {'✔ Cumple' if son_matrices_iguales(AB_T, BT_AT) else '✘ No cumple'}</p>"
    except Exception as e:
        html += f"<h3>4. Transpuesta del Producto Matricial: (AB)ᵀ = Bᵀ Aᵀ</h3><p style='color:red;'>No evaluable por dimensiones: {e}</p>"

    return html

# ------------------------------------------------------------------------------
# 4. PROPIEDADES DE LA INVERSA (PARA EL BOTÓN A⁻¹ y B⁻¹)
# ------------------------------------------------------------------------------

def verificar_propiedades_inversa_pasos(A, B, r=2.0):
    """
    Calcula A⁻¹ y B⁻¹ (por Gauss-Jordan y por Matriz Adjunta) y demuestra 
    las 5 Propiedades Principales de la Inversa en el mismo reporte.
    """
    html = "<h2>1. Cálculo de Inversas (Gauss-Jordan y Matriz Adjunta)</h2>"
    
    # Inversa de A y B usando la función existente
    (invA, invB), html_inversas = inversas_ambas_matrices_pasos(A, B)
    html += html_inversas
    html += "<hr style='border: 2px solid #4A90E2; margin: 20px 0;'>"
    
    html += "<h2>2. Verificación de las Propiedades Principales de la Inversa</h2>"
    
    if invA is None or invB is None:
        html += "<p style='color:#C0392B;'><b>Nota:</b> Ambas matrices deben ser cuadradas e invertibles para demostrar todas las propiedades de la inversa.</p>"
        return (invA, invB), html

    # --- Propiedad 1: (A⁻¹)⁻¹ = A ---
    inv_invA, _ = _procesar_inversa_individual(invA, "A⁻¹")
    cumple_p1 = son_matrices_iguales(inv_invA, A) if inv_invA else False
    html += "<h3>1. Inversa de la Inversa: (A⁻¹)⁻¹ = A</h3>"
    html += formato_matriz_html(inv_invA, "(A⁻¹)⁻¹") if inv_invA else ""
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if cumple_p1 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"

    # --- Propiedad 2: (AB)⁻¹ = B⁻¹ A⁻¹ ---
    try:
        AB = multiplicar_matrices(A, B)
        inv_AB, _ = _procesar_inversa_individual(AB, "AB")
        invB_invA = multiplicar_matrices(invB, invA)
        cumple_p2 = son_matrices_iguales(inv_AB, invB_invA) if inv_AB else False
        html += "<h3>2. Inversa de un Producto: (AB)⁻¹ = B⁻¹ A⁻¹</h3>"
        html += formato_matriz_html(inv_AB, "(AB)⁻¹") if inv_AB else ""
        html += formato_matriz_html(invB_invA, "B⁻¹ A⁻¹")
        html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if cumple_p2 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"
    except Exception as e:
        html += f"<h3>2. Inversa de un Producto: (AB)⁻¹ = B⁻¹ A⁻¹</h3><p style='color:#7F8C8D;'>Incompatible por dimensiones: {e}</p><hr>"

    # --- Propiedad 3: (Aᵀ)⁻¹ = (A⁻¹)ᵀ ---
    AT = obtener_transpuesta(A)
    inv_AT, _ = _procesar_inversa_individual(AT, "Aᵀ")
    invA_T = obtener_transpuesta(invA)
    cumple_p3 = son_matrices_iguales(inv_AT, invA_T) if inv_AT else False
    html += "<h3>3. Inversa de la Transpuesta: (Aᵀ)⁻¹ = (A⁻¹)ᵀ</h3>"
    html += formato_matriz_html(inv_AT, "(Aᵀ)⁻¹") if inv_AT else ""
    html += formato_matriz_html(invA_T, "(A⁻¹)ᵀ")
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if cumple_p3 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"

    # --- Propiedad 4: (kA)⁻¹ = (1/k) A⁻¹ con k = r ---
    if r != 0:
        rA = escalar_por_matriz(r, A)
        inv_rA, _ = _procesar_inversa_individual(rA, f"{r}A")
        inv_r_invA = escalar_por_matriz(1.0 / r, invA)
        cumple_p4 = son_matrices_iguales(inv_rA, inv_r_invA) if inv_rA else False
        html += f"<h3>4. Inversa de un Escalar: ({r}A)⁻¹ = (1/{r}) A⁻¹</h3>"
        html += formato_matriz_html(inv_rA, f"({r}A)⁻¹") if inv_rA else ""
        html += formato_matriz_html(inv_r_invA, f"(1/{r}) A⁻¹")
        html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if cumple_p4 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"

    # --- Propiedad 5: det(A⁻¹) = 1 / det(A) ---
    detA = determinante_cofactores(A)
    det_invA = determinante_cofactores(invA)
    inv_detA = 1.0 / detA if detA != 0 else 0
    cumple_p5 = abs(det_invA - inv_detA) < 1e-6
    html += "<h3>5. Determinante de la Inversa: det(A⁻¹) = 1 / det(A)</h3>"
    html += f"<p>&bull; det(A⁻¹) = <b>{decimal_a_fraccion(det_invA)}</b><br>"
    html += f"&bull; 1 / det(A) = 1 / ({decimal_a_fraccion(detA)}) = <b>{decimal_a_fraccion(inv_detA)}</b></p>"
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if cumple_p5 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p>"

    return (invA, invB), html

def determinante_triangular_pasos(A):
    """
    Calcula el determinante reduciendo la matriz A a forma triangular superior.
    Lleva la cuenta de los intercambios de fila para ajustar el signo final.
    """
    n = len(A)
    M = [f[:] for f in A]
    intercambios = 0

    for i in range(n):
        pivot = M[i][i]
        if abs(pivot) < 1e-9:
            swap_idx = -1
            for k in range(i + 1, n):
                if abs(M[k][i]) > 1e-9:
                    swap_idx = k
                    break
            if swap_idx == -1:
                return 0.0, "Matriz singular (det = 0)"
            
            # Intercambio de filas
            M[i], M[swap_idx] = M[swap_idx], M[i]
            intercambios += 1
            pivot = M[i][i]

        for k in range(i + 1, n):
            factor = M[k][i] / pivot
            if abs(factor) > 1e-9:
                for j in range(i, n):
                    M[k][j] -= factor * M[i][j]

    # El determinante de una matriz triangular es el producto de su diagonal
    diag_prod = 1.0
    for i in range(n):
        diag_prod *= M[i][i]

    # Ajuste por cantidad de intercambios de fila
    det_final = ((-1) ** intercambios) * diag_prod
    return det_final, "Reducción completada"

def verificar_propiedades_guia_tarea5(A, B, k_escalar=2.0):
    """
    Verifica automáticamente las 6 propiedades exigidas por la Tarea 5:
    1. (A⁻¹)⁻¹ = A
    2. (AB)⁻¹ = B⁻¹ A⁻¹
    3. (Aᵀ)⁻¹ = (A⁻¹)ᵀ
    4. det(A⁻¹) = 1 / det(A)
    5. Operaciones de fila sobre det(A) (Intercambio, Reemplazo y Escalamiento)
    6. Determinante por reducción a matriz triangular vs Cofactores
    """
    html = "<h2>VERIFICADOR DE PROPIEDADES (MÓDULO III / TAREA 5)</h2>"
    
    nA, mA = len(A), len(A[0])
    nB, mB = len(B), len(B[0])
    
    if nA != mA or nB != mB or nA != nB:
        return f"<p style='color:#C0392B;'><b>Error:</b> El Verificador requiere dos matrices cuadradas de la misma dimensión (n×n). Dimensiones ingresadas: A({nA}×{mA}) y B({nB}×{mB}).</p>"

    detA = determinante_cofactores(A)
    detB = determinante_cofactores(B)
    
    if abs(detA) < 1e-9 or abs(detB) < 1e-9:
        return "<p style='color:#C0392B;'><b>Error:</b> El Verificador requiere que ambas matrices sean invertibles (det ≠ 0).</p>"

    invA, _ = _procesar_inversa_individual(A, "A")
    invB, _ = _procesar_inversa_individual(B, "B")

    # Propiedad 1: (A⁻¹)⁻¹ = A
    inv_invA, _ = _procesar_inversa_individual(invA, "A⁻¹")
    p1 = son_matrices_iguales(inv_invA, A) if inv_invA else False
    html += f"<h3>1. Inversa de la Inversa: (A⁻¹)⁻¹ = A</h3>"
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if p1 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"

    # Propiedad 2: (AB)⁻¹ = B⁻¹ A⁻¹
    AB = multiplicar_matrices(A, B)
    inv_AB, _ = _procesar_inversa_individual(AB, "AB")
    invB_invA = multiplicar_matrices(invB, invA)
    p2 = son_matrices_iguales(inv_AB, invB_invA) if inv_AB else False
    html += f"<h3>2. Inversa de un Producto: (AB)⁻¹ = B⁻¹ A⁻¹</h3>"
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if p2 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"

    # Propiedad 3: (Aᵀ)⁻¹ = (A⁻¹)ᵀ
    AT = obtener_transpuesta(A)
    inv_AT, _ = _procesar_inversa_individual(AT, "Aᵀ")
    invA_T = obtener_transpuesta(invA)
    p3 = son_matrices_iguales(inv_AT, invA_T) if inv_AT else False
    html += f"<h3>3. Inversa de la Transpuesta: (Aᵀ)⁻¹ = (A⁻¹)ᵀ</h3>"
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if p3 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"

    # Propiedad 4: det(A⁻¹) = 1 / det(A)
    det_invA = determinante_cofactores(invA)
    inv_detA = 1.0 / detA
    p4 = abs(det_invA - inv_detA) < 1e-6
    html += f"<h3>4. Determinante de la Inversa: det(A⁻¹) = 1 / det(A)</h3>"
    html += f"<p>&bull; det(A⁻¹) = <b>{decimal_a_fraccion(det_invA)}</b> | 1 / det(A) = <b>{decimal_a_fraccion(inv_detA)}</b></p>"
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if p4 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p><hr>"

    # Propiedad 5: Operaciones de Fila sobre el Determinante
    html += "<h3>5. Efecto de Operaciones de Fila en det(A)</h3><ul>"
    if nA > 1:
        A_swap = [f[:] for f in A]
        A_swap[0], A_swap[1] = A_swap[1], A_swap[0]
        html += f"<li><b>Intercambio F1 ↔ F2:</b> det = {decimal_a_fraccion(determinante_cofactores(A_swap))} (Esperado -det(A) = {decimal_a_fraccion(-detA)})</li>"
        
        A_repl = [f[:] for f in A]
        for c in range(mA): A_repl[0][c] += k_escalar * A_repl[1][c]
        html += f"<li><b>Reemplazo F1 → F1 + ({k_escalar})F2:</b> det = {decimal_a_fraccion(determinante_cofactores(A_repl))} (Esperado det(A) = {decimal_a_fraccion(detA)})</li>"
        
    A_scale = [f[:] for f in A]
    for c in range(mA): A_scale[0][c] *= k_escalar
    html += f"<li><b>Escalamiento F1 → ({k_escalar})F1:</b> det = {decimal_a_fraccion(determinante_cofactores(A_scale))} (Esperado {k_escalar}·det(A) = {decimal_a_fraccion(k_escalar * detA)})</li>"
    html += "</ul><hr>"

    # Propiedad 6: Matriz Triangular
    det_triang, _ = determinante_triangular_pasos(A)
    p6 = abs(det_triang - detA) < 1e-6
    html += f"<h3>6. Determinante por Reducción a Matriz Triangular</h3>"
    html += f"<p>&bull; Producto Diagonal Corregido: <b>{decimal_a_fraccion(det_triang)}</b> | Resultado por Cofactores: <b>{decimal_a_fraccion(detA)}</b></p>"
    html += f"<p><b>Dictamen:</b> {'<b style=\"color:#27AE60;\">✔ SE CUMPLE</b>' if p6 else '<b style=\"color:#C0392B;\">✘ NO SE CUMPLE</b>'}</p>"

    return html