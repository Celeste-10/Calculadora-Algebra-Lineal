"""
MÓDULO DE OPERACIONES CON VECTORES EN Rⁿ
Implementa suma, resta, producto por escalar, evaluación de combinaciones lineales 
y análisis de independencia o dependencia lineal mediante reducción Gauss-Jordan.

Asignatura: Álgebra Lineal 
"""
from logica.operaciones import resolver_gauss_jordan

# ------------------------------------------------------------------------------
# 1. MÓDULO DE VECTORES (Rⁿ)
# ------------------------------------------------------------------------------

# modulo_vectores.py
from logica.operaciones import decimal_a_fraccion

def sumar_vectores(v1, v2):
    """
    Suma dos vectores en Rⁿ elemento por elemento.
    Equivalente algebraico: u + v = (u₁ + v₁, u₂ + v₂, ..., uₙ + vₙ)
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return [v1[i] + v2[i] for i in range(len(v1))]

def escalar_por_vector(c, v):
    """
    Multiplica un escalar 'c' por un vector 'v'.
    Equivalente algebraico: c·v = (c·v₁, c·v₂, ..., c·vₙ)
    """
    return [c * x for x in v]

def sumar_vectores_pasos(u, v):
    if len(u) != len(v):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    
    pasos = "<h3>Procedimiento Suma (u + v):</h3>"
    pasos += f"<p><b>u</b> = {u}<br><b>v</b> = {v}</p>"
    
    operaciones = [f"{decimal_a_fraccion(u[i])} + {decimal_a_fraccion(v[i])}" for i in range(len(u))]
    res = [u[i] + v[i] for i in range(len(u))]
    
    pasos += f"<p><b>Paso a paso:</b><br>[ {', '.join(operaciones)} ]</p>"
    pasos += f"<p><b>Resultado Final:</b><br>{res}</p>"
    return res, pasos

def restar_vectores_pasos(u, v):
    if len(u) != len(v):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    
    pasos = "<h3>Procedimiento Resta (u - v):</h3>"
    pasos += f"<p><b>u</b> = {u}<br><b>v</b> = {v}</p>"
    
    operaciones = [f"{decimal_a_fraccion(u[i])} - ({decimal_a_fraccion(v[i])})" for i in range(len(u))]
    res = [u[i] - v[i] for i in range(len(u))]
    
    pasos += f"<p><b>Paso a paso:</b><br>[ {', '.join(operaciones)} ]</p>"
    pasos += f"<p><b>Resultado Final:</b><br>{res}</p>"
    return res, pasos

def escalar_por_vector_pasos(c, u):
    pasos = f"<h3>Procedimiento Producto por Escalar ({c} · u):</h3>"
    pasos += f"<p><b>c</b> = {c}<br><b>u</b> = {u}</p>"
    
    operaciones = [f"{c} × ({decimal_a_fraccion(u[i])})" for i in range(len(u))]
    res = [c * x for x in u]
    
    pasos += f"<p><b>Paso a paso:</b><br>[ {', '.join(operaciones)} ]</p>"
    pasos += f"<p><b>Resultado Final:</b><br>{res}</p>"
    return res, pasos

def es_combinacion_lineal(conjunto_vectores, b):
    """
    Evalúa si b es combinación lineal del conjunto de vectores usando Gauss-Jordan.
    Devuelve la matriz reducida, los pasos y el resumen con el dictamen en HTML.
    """
    from logica.operaciones import resolver_gauss_jordan

    n = len(b)
    k = len(conjunto_vectores)

    # Construir matriz aumentada [A|b]
    matriz_aumentada = []
    for i in range(n):
        fila = [conjunto_vectores[j][i] for j in range(k)] + [float(b[i])]
        matriz_aumentada.append(fila)

    # Resolver el sistema
    matriz_rref, pasos_log, resumen_txt = resolver_gauss_jordan(matriz_aumentada, n, k)

    # Verificar si hay filas del tipo [0 0 ... 0 | c] con c != 0
    inconsistente = False
    for i in range(n):
        coef_ceros = all(abs(matriz_rref[i][j]) < 1e-9 for j in range(k))
        if coef_ceros and abs(matriz_rref[i][k]) > 1e-9:
            inconsistente = True
            break

    # Construir dictamen explícito
    dictamen_html = "<div style='margin-bottom: 10px;'>"
    if inconsistente:
        dictamen_html += "<b style='color:#C0392B; font-size:15px;'>"
        dictamen_html += "✖ DICTAMEN: El vector b NO ES combinación lineal del conjunto.</b><br>"
        dictamen_html += "<i>El sistema es inconsistente (no existen escalares).</i>"
    else:
        dictamen_html += "<b style='color:#27AE60; font-size:15px;'>"
        dictamen_html += "✔ DICTAMEN: El vector b SÍ ES combinación lineal del conjunto.</b><br>"
        dictamen_html += "<i>El sistema es consistente.</i>"
    dictamen_html += "</div><hr>"

    resumen_final = dictamen_html + resumen_txt

    return matriz_rref, pasos_log, resumen_final

def evaluar_independencia_lineal(conjunto_vectores):
    """
    Evalúa si un conjunto de vectores en R^n es Linealmente Independiente (L.I.)
    o Linealmente Dependiente (L.D.) usando Gauss-Jordan sobre la matriz homogénea [A | 0].
    """
    from logica.operaciones import resolver_gauss_jordan, decimal_a_fraccion

    if not conjunto_vectores:
        raise ValueError("El conjunto de vectores no puede estar vacío.")

    n = len(conjunto_vectores[0])  # Dimensión de R^n
    k = len(conjunto_vectores)     # Cantidad de vectores

    # Validar que todos tengan la misma dimensión
    for v in conjunto_vectores:
        if len(v) != n:
            raise ValueError("Todos los vectores deben tener la misma dimensión.")

    # Regla de dimensión rápida: si k > n, son L.D.
    # Aún así, construimos la matriz para mostrar el procedimiento completo
    matriz_aumentada = []
    for i in range(n):
        fila = [float(conjunto_vectores[j][i]) for j in range(k)] + [0.0]
        matriz_aumentada.append(fila)

    # Resolver Gauss-Jordan
    matriz_rref, pasos_log, resumen_txt = resolver_gauss_jordan(matriz_aumentada, n, k)

    # Contar variables libres (columnas pivote < k)
    pivotes = 0
    for i in range(n):
        # Buscar primer elemento no nulo en la fila
        for j in range(k):
            if abs(matriz_rref[i][j]) > 1e-9:
                pivotes += 1
                break

    es_li = (pivotes == k)

    # Construir dictamen explícito en HTML
    dictamen_html = "<div style='margin-bottom: 12px;'>"
    if es_li:
        dictamen_html += "<b style='color:#27AE60; font-size:16px;'>"
        dictamen_html += "✔ DICTAMEN: El conjunto de vectores es LINEALMENTE INDEPENDIENTE (L.I.).</b><br>"
        dictamen_html += f"<i>Explicación: Existen {pivotes} pivotes para {k} vectores. La única solución al sistema homogéneo c₁v₁ + c₂v₂ + ... = 0 es la solución trivial (c₁ = c₂ = ... = 0).</i>"
    else:
        dictamen_html += "<b style='color:#C0392B; font-size:16px;'>"
        dictamen_html += "✖ DICTAMEN: El conjunto de vectores es LINEALMENTE DEPENDIENTE (L.D.).</b><br>"
        dictamen_html += f"<i>Explicación: Solo hay {pivotes} pivotes para {k} vectores (hay variables libres). Existen soluciones no triviales para los escalares.</i>"
    dictamen_html += "</div><hr>"

    resumen_final = dictamen_html + resumen_txt

    return matriz_rref, pasos_log, resumen_final, es_li

def evaluar_combinacion_lineal_gauss_jordan(vectores, b):
    """
    Evalúa si b es combinación lineal de {v1, v2, ..., vk} usando Gauss-Jordan.
    
    :param vectores: Lista de listas con los vectores columna [[v1_1, v1_2, ...], [v2_1, v2_2, ...]]
    :param b: Lista con el vector b [b1, b2, ...]
    :return: (bool es_combinacion, list pasos, list pesos)
    """
    m = len(b)          # Filas (dimensión en Rn)
    k = len(vectores)   # Columnas (cantidad de vectores)
    
    # 1. Construir la matriz aumentada [A | b]
    matriz = []
    for i in range(m):
        fila = [float(vectores[j][i]) for j in range(k)] + [float(b[i])]
        matriz.append(fila)
        
    pasos = ["Matriz aumentada inicial [A | b]:"]
    for f in matriz:
        pasos.append(str([round(x, 2) for x in f]))
        
    # 2. Algoritmo de Gauss-Jordan
    fila_pivote = 0
    for col in range(k):
        if fila_pivote >= m:
            break
            
        # Buscar pivote
        max_fila = fila_pivote
        for i in range(fila_pivote + 1, m):
            if abs(matriz[i][col]) > abs(matriz[max_fila][col]):
                max_fila = i
                
        if abs(matriz[max_fila][col]) < 1e-9:
            continue
            
        # Intercambiar filas
        if max_fila != fila_pivote:
            matriz[fila_pivote], matriz[max_fila] = matriz[max_fila], matriz[fila_pivote]
            pasos.append(f"\nFila {fila_pivote+1} ↔ Fila {max_fila+1}")
            
        # Hacer 1 el pivote
        val_pivote = matriz[fila_pivote][col]
        for j in range(col, k + 1):
            matriz[fila_pivote][j] /= val_pivote
        pasos.append(f"Fila {fila_pivote+1} ÷ {round(val_pivote, 2)}")
        
        # Hacer ceros arriba y abajo del pivote
        for i in range(m):
            if i != fila_pivote:
                factor = matriz[i][col]
                if abs(factor) > 1e-9:
                    for j in range(col, k + 1):
                        matriz[i][j] -= factor * matriz[fila_pivote][j]
                    pasos.append(f"Fila {i+1} = Fila {i+1} - ({round(factor, 2)}) * Fila {fila_pivote+1}")
                    
        fila_pivote += 1

    # 3. Verificar consistencia (fila [0 ... 0 | k] con k != 0)
    for i in range(m):
        coef_ceros = all(abs(matriz[i][j]) < 1e-9 for j in range(k))
        if coef_ceros and abs(matriz[i][k]) > 1e-9:
            pasos.append("\nDictamen: El sistema es INCONSISTENTE.")
            pasos.append("El vector b NO es combinación lineal del conjunto de vectores.")
            return False, pasos, None

    # 4. Extraer escalares/pesos
    pesos = [0.0] * k
    for i in range(m):
        for j in range(k):
            if abs(matriz[i][j] - 1.0) < 1e-9:
                if all(abs(matriz[i][c]) < 1e-9 for c in range(k) if c != j):
                    pesos[j] = round(matriz[i][k], 4)
                break

    pasos.append("\nDictamen: El sistema es CONSISTENTE.")
    pasos.append(f"El vector b SÍ es combinación lineal.")
    pasos.append(f"Escalares encontrados: {pesos}")
    
    return True, pasos, pesos

def multiplicar_escalar_u_y_v(u, v, c):
    c = float(c)
    cu = [round(c * x, 4) for x in u]
    cv = [round(c * x, 4) for x in v]
    
    pasos = []
    pasos.append(f"Procedimiento Producto por Escalar (c = {c}):\n")
    
    # Bloque Vector u
    pasos.append(f"u = {u}")
    pasos.append("Paso a paso (c · u):")
    pasos.append("[ " + ", ".join([f"{c} * ({x})" for x in u]) + " ]")
    pasos.append("Resultado c · u:")
    pasos.append(f"{cu}\n")
    
    # Bloque Vector v
    pasos.append(f"v = {v}")
    pasos.append("Paso a paso (c · v):")
    pasos.append("[ " + ", ".join([f"{c} * ({x})" for x in v]) + " ]")
    pasos.append("Resultado c · v:")
    pasos.append(f"{cv}")
    
    return cu, cv, "\n".join(pasos)


def evaluar_combinacion_lineal_gauss_jordan(vectores, b):
    m = len(b)          # Filas (dimensión)
    k = len(vectores)   # Columnas (vectores u, v)
    
    # 1. Matriz aumentada [A | b]
    matriz = []
    for i in range(m):
        fila = [float(vectores[j][i]) for j in range(k)] + [float(b[i])]
        matriz.append(fila)
        
    pasos = ["--- COMBINACIÓN LINEAL POR GAUSS-JORDAN ---"]
    pasos.append("Matriz aumentada inicial [A | b]:")
    for f in matriz:
        pasos.append(str([round(x, 2) for x in f]))
        
    # 2. Eliminación Gauss-Jordan
    fila_pivote = 0
    for col in range(k):
        if fila_pivote >= m:
            break
            
        max_fila = fila_pivote
        for i in range(fila_pivote + 1, m):
            if abs(matriz[i][col]) > abs(matriz[max_fila][col]):
                max_fila = i
                
        if abs(matriz[max_fila][col]) < 1e-9:
            continue
            
        if max_fila != fila_pivote:
            matriz[fila_pivote], matriz[max_fila] = matriz[max_fila], matriz[fila_pivote]
            pasos.append(f"\nIntercambiar Fila {fila_pivote+1} ↔ Fila {max_fila+1}")
            
        val_pivote = matriz[fila_pivote][col]
        for j in range(col, k + 1):
            matriz[fila_pivote][j] /= val_pivote
        pasos.append(f"Fila {fila_pivote+1} ÷ {round(val_pivote, 2)}")
        
        for i in range(m):
            if i != fila_pivote:
                factor = matriz[i][col]
                if abs(factor) > 1e-9:
                    for j in range(col, k + 1):
                        matriz[i][j] -= factor * matriz[fila_pivote][j]
                    pasos.append(f"Fila {i+1} = Fila {i+1} - ({round(factor, 2)}) * Fila {fila_pivote+1}")
                    
        fila_pivote += 1

    # 3. Comprobar consistencia del sistema
    for i in range(m):
        coef_ceros = all(abs(matriz[i][j]) < 1e-9 for j in range(k))
        if coef_ceros and abs(matriz[i][k]) > 1e-9:
            pasos.append("\nDICTAMEN: El sistema es INCONSISTENTE.")
            pasos.append("El vector b NO es combinación lineal del conjunto {u, v}.")
            return False, "\n".join(pasos), None

    # 4. Extraer escalares
    pesos = [0.0] * k
    for i in range(m):
        for j in range(k):
            if abs(matriz[i][j] - 1.0) < 1e-9:
                if all(abs(matriz[i][c]) < 1e-9 for c in range(k) if c != j):
                    pesos[j] = round(matriz[i][k], 4)
                break

    pasos.append("\nDICTAMEN: El sistema es CONSISTENTE.")
    pasos.append("El vector b SÍ es combinación lineal de {u, v}.")
    pasos.append(f"Escalares encontrados: x1 = {pesos[0]}, x2 = {pesos[1] if k > 1 else 0}")
    
    return True, "\n".join(pasos), pesos



# ------------------------------------------------------------------------------
# 4. PROPIEDADES DEL PRODUCTO MATRIZ-VECTOR Ax
# Teorema:
# a) A(u + v) = Au + Av
# b) A(c·u) = c(Au)
# ------------------------------------------------------------------------------
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
def multiplicar_matriz_vector(A, v):
    """
    Multiplica una matriz A de m x n por un vector columna v de n x 1.
    Retorna un vector de m elementos.
    """
    m = len(A)
    n = len(A[0])
    if len(v) != n:
        raise ValueError(f"Incompatibilidad de dimensiones: Matriz A ({m}x{n}) y vector v de dimensión {len(v)}.")
    
    mat_v = [[elem] for elem in v]
    res_mat = multiplicar_matrices(A, mat_v)
    return [fila[0] for fila in res_mat]

def verificar_propiedades_ax(A, u, v, c):
    """
    Verifica las propiedades del producto matriz-vector Ax demostrando paso a paso:
    a) A(u + v) = Au + Av
    b) A(c·u) = c(Au)
    """
    from logica.operaciones import decimal_a_fraccion, formato_matriz_html

    def vec_a_mat(vec):
        return [[elem] for elem in vec]

    pasos_html = []

    # ==========================================================================
    # PROPIEDAD A: A(u + v) = Au + Av
    # ==========================================================================
    
    pasos_html.append("<h4 style='color:#1B4F72;'>PROPIEDAD A: A(u + v) = Au + Av</h4>")

    # Lado Izquierdo: A(u + v)
    u_mas_v = sumar_vectores(u, v)
    A_u_mas_v = multiplicar_matriz_vector(A, u_mas_v)

    pasos_html.append("<b>1. Lado Izquierdo: A(u + v)</b><br>")
    pasos_html.append(f"&bull; Paso 1.1: Sumar vectores (u + v) = {u_mas_v}<br>")
    pasos_html.append(formato_matriz_html(vec_a_mat(u_mas_v), "Vector (u + v):"))
    pasos_html.append(formato_matriz_html(vec_a_mat(A_u_mas_v), "Resultado A(u + v):"))

    # Lado Derecho: Au + Av
    Au = multiplicar_matriz_vector(A, u)
    Av = multiplicar_matriz_vector(A, v)
    Au_mas_Av = sumar_vectores(Au, Av)

    pasos_html.append("<br><b>2. Lado Derecho: Au + Av</b><br>")
    pasos_html.append(formato_matriz_html(vec_a_mat(Au), "Resultado Au:"))
    pasos_html.append(formato_matriz_html(vec_a_mat(Av), "Resultado Av:"))
    pasos_html.append(f"&bull; Paso 2.1: Sumar resultados Au + Av = {Au_mas_Av}<br>")
    pasos_html.append(formato_matriz_html(vec_a_mat(Au_mas_Av), "Resultado Au + Av:"))

    cumple_a = all(abs(A_u_mas_v[i] - Au_mas_Av[i]) < 1e-7 for i in range(len(A_u_mas_v)))

    # ==========================================================================
    # PROPIEDAD B: A(c·u) = c(Au)
    # ==========================================================================
    pasos_html.append("<hr><h4 style='color:#1B4F72;'>PROPIEDAD B: A(c·u) = c(Au)</h4>")

    # Lado Izquierdo: A(c·u)
    cu = escalar_por_vector(c, u)
    A_cu = multiplicar_matriz_vector(A, cu)

    c_str = decimal_a_fraccion(c)
    pasos_html.append(f"<b>1. Lado Izquierdo: A({c_str} · u)</b><br>")
    pasos_html.append(f"&bull; Paso 1.1: Multiplicar escalar c · u = {cu}<br>")
    pasos_html.append(formato_matriz_html(vec_a_mat(cu), f"Vector ({c_str}·u):"))
    pasos_html.append(formato_matriz_html(vec_a_mat(A_cu), f"Resultado A({c_str}·u):"))

    # Lado Derecho: c(Au)
    c_Au = escalar_por_vector(c, Au)

    pasos_html.append(f"<br><b>2. Lado Derecho: {c_str} · (Au)</b><br>")
    pasos_html.append(f"&bull; Paso 2.1: Multiplicar escalar por el vector Au resultante:<br>")
    pasos_html.append(formato_matriz_html(vec_a_mat(c_Au), f"Resultado {c_str} · (Au):"))

    cumple_b = all(abs(A_cu[i] - c_Au[i]) < 1e-7 for i in range(len(A_cu)))

    # ==========================================================================
    # DICTAMEN FINAL
    # ==========================================================================
    resumen_html = "<h3>Dictamen de Comprobación del Teorema:</h3>"
    if cumple_a:
        resumen_html += "<b style='color:#27AE60;'>✔ Propiedad a) A(u + v) = Au + Av SE CUMPLE SATISFACTORIAMENTE.</b><br>"
    else:
        resumen_html += "<b style='color:#C0392B;'>✘ Propiedad a) NO SE CUMPLE.</b><br>"

    if cumple_b:
        resumen_html += "<b style='color:#27AE60;'>✔ Propiedad b) A(c·u) = c(Au) SE CUMPLE SATISFACTORIAMENTE.</b><br>"
    else:
        resumen_html += "<b style='color:#C0392B;'>✘ Propiedad b) NO SE CUMPLE.</b><br>"

    return "".join(pasos_html), resumen_html
