"""
MÓDULO DE SISTEMAS DE ECUACIONES LINEALES (Ax = b)
Construye la matriz aumentada [A|b] y ejecuta la eliminación de Gauss-Jordan para determinar
si el sistema tiene solución única, infinitas soluciones o es inconsistente.

Asignatura: Álgebra Lineal 
"""
from logica.operaciones import resolver_gauss_jordan

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