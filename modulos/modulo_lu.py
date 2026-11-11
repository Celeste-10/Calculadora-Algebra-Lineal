# ==============================================================================
# MÓDULO DE FACTORIZACIÓN LU (A = LU) Y RESOLUCIÓN DE SISTEMAS Ax = b
# Asignatura: Álgebra Lineal
# Unidad: Descomposición Matricial y Sistemas Sustitutivos
# ==============================================================================

from fractions import Fraction
from logica.operaciones import decimal_a_fraccion, formato_matriz_html

def factorizacion_lu(A):
    """
    Calcula la descomposición LU de la matriz A (A = LU) en Python puro.
    
    Parámetros:
        A (list): Matriz de entrada de dimensión m x n (lista anidada).
        
    Retorna:
        tuple: (exito: bool, L: list, U: list, mensaje: str, pasos: list)
    """
    m = len(A)
    n = len(A[0])
    
    # Se convierte U a objetos Fraction para evitar imprecisiones de coma flotante
    U = [[Fraction(val) for val in fila] for fila in A]
    
    # L se construye como la matriz identidad m x m de orden m
    L = [[Fraction(1 if i == j else 0) for j in range(m)] for i in range(m)]
    
    pasos = ["<b>Proceso de Eliminación Gaussiana para LU:</b><br>"]
    
    min_dim = min(m, n)
    for j in range(min_dim):
        pivote = U[j][j]
        
        # Si un pivote en la diagonal resulta ser cero, requiere pivoteo parcial
        if pivote == 0:
            msg = "La matriz no admite Factorización LU sin permutación (requiere pivoteo parcial PA=LU)."
            return False, None, None, msg, pasos
            
        for i in range(j + 1, m):
            elemento_a_eliminar = U[i][j]
            if elemento_a_eliminar != 0:
                # Se calcula el multiplicador l = elemento / pivote
                multiplicador_l = elemento_a_eliminar / pivote
                
                # Se registra el multiplicador de eliminación en L antes de alterar la fila en U
                L[i][j] = multiplicador_l
                
                # Operación elemental de reemplazo de fila: F_i <- F_i - l * F_j
                for k in range(j, n):
                    U[i][k] -= multiplicador_l * U[j][k]
                    
                val_l_str = decimal_a_fraccion(float(multiplicador_l))
                pasos.append(f"F<sub>{i+1}</sub> &rarr; F<sub>{i+1}</sub> - ({val_l_str}) &times; F<sub>{j+1}</sub> | Multiplicador L<sub>{i+1}{j+1}</sub> = {val_l_str}")
                
    # Convertir L y U a flotantes para el despliegue y compatibilidad del sistema
    L_float = [[float(x) for x in fila] for fila in L]
    U_float = [[float(x) for x in fila] for fila in U]
    
    return True, L_float, U_float, "Factorización LU realizada exitosamente.", pasos


def sustitucion_hacia_adelante(L, b):
    """
    Resuelve el sistema triangular inferior Ly = b para obtener el vector y.
    
    Parámetros:
        L (list): Matriz triangular inferior m x m con 1s en la diagonal.
        b (list): Vector de términos independientes de m elementos.
        
    Retorna:
        list: Vector intermedio y (lista de floats).
    """
    m = len(L)
    vector_y = [Fraction(0)] * m
    
    # Recorrido descendente (de arriba hacia abajo)
    for i in range(m):
        suma = Fraction(b[i])
        for j in range(i):
            suma -= Fraction(L[i][j]) * vector_y[j]
        # Como L[i][i] es 1 en la diagonal principal, L[i][i] no altera la división
        vector_y[i] = suma / Fraction(L[i][i])
        
    return [float(val) for val in vector_y]


def sustitucion_hacia_atras(U, y):
    """
    Resuelve el sistema triangular superior Ux = y para obtener el vector x.
    
    Parámetros:
        U (list): Matriz en forma escalonada de dimensión n x n.
        y (list): Vector de resultados intermedios de n elementos.
        
    Retorna:
        list: Vector solución final x (lista de floats).
    """
    n = len(U)
    vector_x = [Fraction(0)] * n
    
    # Recorrido ascendente (de abajo hacia arriba)
    for i in range(n - 1, -1, -1):
        pivote = Fraction(U[i][i])
        if pivote == 0:
            raise ValueError("Pivote nulo detectado en U durante la sustitución hacia atrás.")
            
        suma = Fraction(y[i])
        for j in range(i + 1, n):
            suma -= Fraction(U[i][j]) * vector_x[j]
            
        vector_x[i] = suma / pivote
        
    return [float(val) for val in vector_x]


def resolver_sistema_lu(A, b):
    """
    Resuelve el sistema Ax = b integrando Factorización LU, Ly=b y Ux=y.
    
    Parámetros:
        A (list): Matriz cuadrada n x n.
        b (list): Vector columna n x 1.
        
    Retorna:
        tuple: (exito: bool, L, U, y, x, html_reporte: str)
    """
    m = len(A)
    n = len(A[0])
    
    if m != n:
        return False, None, None, None, None, "<b style='color:red;'>La resolución de Ax=b por LU requiere una matriz cuadrada A (n x n).</b>"
        
    if len(b) != m:
        return False, None, None, None, None, f"<b style='color:red;'>El vector b debe tener dimensión {m}.</b>"
        
    # Paso 1: Obtener la Factorización LU
    exito, L, U, msg, pasos = factorizacion_lu(A)
    if not exito:
        return False, None, None, None, None, f"<b style='color:red;'>Error en Factorización LU:</b> {msg}"
        
    # Paso 2: Sustitución hacia adelante Ly = b
    vector_y = sustitucion_hacia_adelante(L, b)
    
    # Paso 3: Sustitución hacia atrás Ux = y
    try:
        vector_x = sustitucion_hacia_atras(U, y=vector_y)
    except ValueError as e:
        return False, L, U, vector_y, None, f"<b style='color:red;'>Error en Sustitución Hacia Atrás:</b> {str(e)}"
        
    # Paso 4: Verificación L · U == A
    from modulos.modulo_matrices import multiplicar_matrices, son_matrices_iguales
    LU = multiplicar_matrices(L, U)
    lu_correcta = son_matrices_iguales(LU, A)
    
    # Paso 5: Verificación A · x == b
    from modulos.modulo_vectores import multiplicar_matriz_vector
    Ax = multiplicar_matriz_vector(A, vector_x)
    ax_b_correcto = all(abs(Ax[i] - b[i]) < 1e-7 for i in range(len(b)))
    
    # Construcción del informe visual HTML
    html = "<h2>FACTORIZACIÓN LU Y RESOLUCIÓN SUSTITUTIVA DE Ax = b</h2>"
    html += f"<p><b>Estado del proceso:</b> {msg}</p>"
    html += formato_matriz_html(L, "Matriz L (Triangular Inferior con 1s en la diagonal):")
    html += formato_matriz_html(U, "Matriz U (Forma Escalonada Superior):")
    
    if lu_correcta:
        html += "<p style='color:#27AE60;'><b>✔ Verificación de la Factorización:</b> La descomposición es correcta (L &middot; U == A).</p>"
    else:
        html += "<p style='color:#C0392B;'><b>✘ Verificación de la Factorización:</b> L &middot; U != A.</p>"
        
    html += "<hr><h3>ETAPAS DE RESOLUCIÓN SUSTITUTIVA:</h3>"
    
    # Despliegue del Vector y
    vec_y_mat = [[val] for val in vector_y]
    html += "<b>1. Sustitución hacia adelante (L &middot; y = b):</b><br>"
    html += formato_matriz_html(vec_y_mat, "Vector Intermedio y:")
    
    # Despliegue del Vector x
    vec_x_mat = [[val] for val in vector_x]
    html += "<b>2. Sustitución hacia atrás (U &middot; x = y):</b><br>"
    html += formato_matriz_html(vec_x_mat, "Vector Solución x:")
    
    if ax_b_correcto:
        html += "<p style='color:#27AE60; font-size:14px;'><b>✔ Comprobación Exitosa:</b> A &middot; x == b</p>"
    else:
        html += "<p style='color:#C0392B; font-size:14px;'><b>✘ Comprobación Fallida:</b> A &middot; x != b</p>"
        
    return True, L, U, vector_y, vector_x, html