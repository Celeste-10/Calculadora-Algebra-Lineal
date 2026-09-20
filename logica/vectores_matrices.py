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