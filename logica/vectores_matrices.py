# ==============================================================================
# MÓDULO DE ÁLGEBRA LINEAL - PROGRAMA 3
# Operaciones en Rⁿ, Combinación Lineal y Ecuaciones Matriciales
# ==============================================================================

from logica.algebra_lineal import resolver_gauss_jordan

# ------------------------------------------------------------------------------
# 1. MÓDULO DE VECTORES (Rⁿ)
# ------------------------------------------------------------------------------

def sumar_vectores(v1, v2):
    """
    Suma dos vectores en Rⁿ elemento por elemento.
    Equivalente algebraico: u + v = (u₁ + v₁, u₂ + v₂, ..., uₙ + vₙ)
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return [v1[i] + v2[i] for i in range(len(v1))]

def restar_vectores(v1, v2):
    """
    Resta dos vectores en Rⁿ elemento por elemento.
    Equivalente algebraico: u - v = (u₁ - v₁, u₂ - v₂, ..., uₙ - vₙ)
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return [v1[i] - v2[i] for i in range(len(v1))]

def escalar_por_vector(c, v):
    """
    Multiplica un escalar 'c' por un vector 'v'.
    Equivalente algebraico: c·v = (c·v₁, c·v₂, ..., c·vₙ)
    """
    return [c * x for x in v]

def es_combinacion_lineal(conjunto_vectores, b):
    """
    Evalúa si un vector 'b' es combinación lineal de {v₁, v₂, ..., vₖ}.
    Equivalente algebraico: Plantea c₁·v₁ + c₂·v₂ + ... + cₖ·vₖ = b,
    lo construye como la matriz aumentada [A|b] y resuelve mediante Gauss-Jordan.
    """
    n = len(b)  # Dimensión de los vectores (filas)
    k = len(conjunto_vectores)  # Cantidad de vectores (columnas)

    # Validar dimensiones de los vectores del conjunto
    for v in conjunto_vectores:
        if len(v) != n:
            raise ValueError("Todos los vectores del conjunto deben tener la misma dimensión que b.")

    # Construir la matriz aumentada [A|b]
    # Cada vector vⱼ del conjunto se convierte en la columna j de la matriz A
    matriz_aumentada = []
    for i in range(n):
        fila = [conjunto_vectores[j][i] for j in range(k)]
        fila.append(b[i])  # Se agrega el término independiente bᵢ
        matriz_aumentada.append(fila)

    # Resolver el sistema equivalente usando Gauss-Jordan
    matriz_rref, pasos_log, resumen_txt = resolver_gauss_jordan(matriz_aumentada, n, k)
    return matriz_rref, pasos_log, resumen_txt


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


# ------------------------------------------------------------------------------
# 3. ECUACIONES MATRICIALES (Ax = b)
# ------------------------------------------------------------------------------

def resolver_ecuacion_matricial(A, b):
    """
    Resuelve la ecuación matricial Ax = b representando A como sistema lineal.
    Equivalente algebraico: Construye [A|b] y reduce por Gauss-Jordan.
    """
    m = len(A)
    n = len(A[0])

    if len(b) != m:
        raise ValueError(f"Dimensiones incompatibles: Matriz A ({m}x{n}) con vector b de dimensión {len(b)}.")

    # Construir matriz aumentada [A|b]
    matriz_aumentada = []
    for i in range(m):
        fila = A[i][:] + [b[i]]
        matriz_aumentada.append(fila)

    return resolver_gauss_jordan(matriz_aumentada, m, n)

# ------------------------------------------------------------------------------
# 4. PROPIEDADES DEL PRODUCTO MATRIZ-VECTOR Ax
# Teorema:
# a) A(u + v) = Au + Av
# b) A(c·u) = c(Au)
# ------------------------------------------------------------------------------

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
    from logica.algebra_lineal import decimal_a_fraccion, formato_matriz_html

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

# ------------------------------------------------------------------------------
# 5. EVALUACIÓN DE INDEPENDENCIA LINEAL (L.I. / L.D.)
# ------------------------------------------------------------------------------

def evaluar_independencia_lineal(conjunto_vectores, n, k):
    """
    Evalúa si un conjunto de k vectores en Rⁿ es L.I. o L.D.
    Construye el sistema homogéneo [A|0] y lo reduce mediante Gauss-Jordan.
    """
    # 1. Construir la matriz aumentada del sistema homogéneo [A | 0]
    matriz_aumentada = []
    for i in range(n):
        # Tomar la componente i-ésima de cada vector y agregar el término independiente 0
        fila = [conjunto_vectores[j][i] for j in range(k)] + [0.0]
        matriz_aumentada.append(fila)

    # 2. Resolver usando Gauss-Jordan (reutilizando algebra_lineal.py)
    matriz_rref, pasos_log, resumen_txt = resolver_gauss_jordan(matriz_aumentada, n, k)

    # 3. Contar pivotes en las columnas de los vectores (0 a k-1)
    num_pivotes = 0
    for i in range(n):
        # Si la fila tiene algún elemento distinto de cero en las primeras k columnas, es una fila con pivote
        if any(abs(matriz_rref[i][j]) > 1e-9 for j in range(k)):
            num_pivotes += 1

    num_vars_libres = k - num_pivotes
    es_li = (num_vars_libres == 0)

    # 4. Generar el dictamen teórico
    dictamen_html = "<br><b>DICTAMEN TEÓRICO DE INDEPENDENCIA LINEAL:</b><br>"
    dictamen_html += f"&bull; Cantidad de vectores (k): <b>{k}</b><br>"
    dictamen_html += f"&bull; Número de pivotes encontrados: <b>{num_pivotes}</b><br>"
    dictamen_html += f"&bull; Variables libres: <b>{num_vars_libres}</b><br><br>"

    if es_li:
        dictamen_html += "<b style='color:#27AE60; font-size:14px;'>"
        dictamen_html += "✔ El conjunto de vectores es LINEALMENTE INDEPENDIENTE (L.I.).</b><br>"
        dictamen_html += "<i>Explicación: La única solución al sistema homogéneo Ax = 0 es la solución trivial (x₁ = x₂ = ... = 0).</i>"
    else:
        dictamen_html += "<b style='color:#C0392B; font-size:14px;'>"
        dictamen_html += "✖ El conjunto de vectores es LINEALMENTE DEPENDIENTE (L.D.).</b><br>"
        dictamen_html += f"<i>Explicación: Existen {num_vars_libres} variable(s) libre(s), lo que implica infinitas soluciones además de la trivial.</i>"

    # Unir el resumen de la solución con el dictamen explícito
    resumen_completo = resumen_txt + dictamen_html

    return matriz_rref, pasos_log, resumen_completo