# ==============================================================================
# MÓDULO DE ÁLGEBRA LINEAL (CON FRACCIONES PUERTO PYTHON)
# ==============================================================================

# Mapa de caracteres Unicode para subíndices de variables
SUBINDICES = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', 
              '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'}

def var_subind(i):
    """Retorna la variable x con subíndice Unicode (ej. x₁)"""
    num_str = str(i)
    sub_str = "".join(SUBINDICES.get(d, d) for d in num_str)
    return f"x{sub_str}"

def var_subind_html(i):
    """Retorna la variable x con formato HTML (ej. x<sub>1</sub>)"""
    return f"x<sub>{i}</sub>"

def decimal_a_fraccion(val, max_den=10000):
    """
    Convierte un número flotante a una representación en fracción exacta
    mediante fracciones continuas (sin usar la librería math ni numpy).
    """
    if abs(val) < 1e-9:
        return "0"
    
    signo = "-" if val < 0 else ""
    val = abs(val)
    
    # Manejar enteros exactos
    if abs(val - round(val)) < 1e-7:
        return f"{signo}{int(round(val))}"
    
    # Algoritmo de fracciones continuas
    p0, q0 = 0, 1
    p1, q1 = 1, 0
    num = val
    
    while True:
        a = int(num)
        p2 = a * p1 + p0
        q2 = a * q1 + q0
        
        if q2 > max_den:
            break
            
        p0, q0 = p1, q1
        p1, q1 = p2, q2
        
        diff = num - a
        if diff < 1e-9:
            break
        num = 1.0 / diff

    # Validar si el resultado aproximado es altamente preciso
    if abs(val - (p1 / q1)) < 1e-5:
        if q1 == 1:
            return f"{signo}{p1}"
        return f"{signo}{p1}/{q1}"
    
    # En caso de no converger, retorna representación decimal a 4 dígitos
    return f"{signo}{val:.4f}"

def formato_matriz_html(matriz, titulo=""):
    """
    Convierte una matriz a HTML mostrando los elementos como fracciones exactas.
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    html = f"<b>{titulo}</b><br><table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse; border-color: #BDC3C7; text-align: center; margin-top: 5px; margin-bottom: 10px;'>"
    for i in range(filas):
        html += "<tr>"
        for j in range(columnas):
            val_frac = decimal_a_fraccion(matriz[i][j])
            bg_color = "#EBF5FB" if j == columnas - 1 else "#FFFFFF"
            html += f"<td style='background-color: {bg_color}; min-width: 50px; font-weight: 500;'>{val_frac}</td>"
        html += "</tr>"
    html += "</table>"
    return html

def resolver_gauss_jordan(matriz_orig, m, n):
    """
    Aplica el algoritmo de Gauss-Jordan formateando las soluciones con
    parámetros algebraicos (t, s, r, etc.) para las variables libres.
    """
    matriz = [fila[:] for fila in matriz_orig]
    pasos_log = []
    pasos_log.append(formato_matriz_html(matriz, "Matriz Aumentada Inicial [A|b]:"))

    columnas_pivote = []
    r = 0  # Fila pivote actual

    for c in range(n):
        if r >= m:
            break

        # 1. Búsqueda de Pivote (Pivoteo Parcial)
        max_fila = r
        for i in range(r + 1, m):
            if abs(matriz[i][c]) > abs(matriz[max_fila][c]):
                max_fila = i

        if abs(matriz[max_fila][c]) < 1e-9:
            continue

        # Intercambio de filas
        if max_fila != r:
            matriz[r], matriz[max_fila] = matriz[max_fila], matriz[r]
            pasos_log.append(formato_matriz_html(matriz, f"Paso: Intercambiar F<sub>{r+1}</sub> &harr; F<sub>{max_fila+1}</sub>"))

        # 2. Normalización del Pivote
        pivote = matriz[r][c]
        if abs(pivote - 1.0) > 1e-9:
            for j in range(c, n + 1):
                matriz[r][j] /= pivote
            matriz[r][c] = 1.0
            piv_str = decimal_a_fraccion(pivote)
            pasos_log.append(formato_matriz_html(matriz, f"Paso: F<sub>{r+1}</sub> &rarr; F<sub>{r+1}</sub> / ({piv_str})"))

        columnas_pivote.append(c)

        # 3. Eliminación Arriba y Abajo del Pivote
        for i in range(m):
            if i != r:
                factor = matriz[i][c]
                if abs(factor) > 1e-9:
                    for j in range(c, n + 1):
                        matriz[i][j] -= factor * matriz[r][j]
                    
                    signo = "-" if factor > 0 else "+"
                    abs_fact_str = decimal_a_fraccion(abs(factor))
                    pasos_log.append(formato_matriz_html(matriz, f"Paso: F<sub>{i+1}</sub> &rarr; F<sub>{i+1}</sub> {signo} ({abs_fact_str}) &times; F<sub>{r+1}</sub>"))

        r += 1

    # 4. Clasificación e Identificación de Pivotes y Variables
    filas_ceros = 0
    es_inconsistente = False

    for i in range(m):
        es_cero_A = all(abs(matriz[i][j]) < 1e-9 for j in range(n))
        if es_cero_A and abs(matriz[i][n]) > 1e-9:
            es_inconsistente = True
            break
        elif es_cero_A and abs(matriz[i][n]) <= 1e-9:
            filas_ceros += 1

    # Lista de parámetros en orden para variables libres: t, s, r, p, q, u, v, w
    letras_parametros = ['t', 's', 'r', 'p', 'q', 'u', 'v', 'w']
    
    # Crear un diccionario asignando un parámetro a cada variable libre
    indices_libres = [j for j in range(n) if j not in columnas_pivote]
    mapa_parametros = {}
    for k, j in enumerate(indices_libres):
        letra = letras_parametros[k] if k < len(letras_parametros) else f"t_{k+1}"
        mapa_parametros[j] = letra

    vars_basicas = [var_subind_html(c+1) for c in columnas_pivote]
    vars_libres = [f"{var_subind_html(j+1)} = <i>{mapa_parametros[j]}</i>" for j in indices_libres]
    
    resumen_txt = ""
    if es_inconsistente:
        resumen_txt = "<b style='color:#C0392B;'>CLASIFICACIÓN: Sistema Inconsistente (Sin Solución)</b><br>"
        resumen_txt += "<b>Razón:</b> Existe al menos una fila de la forma [0 0 ... 0 | k] con k ≠ 0.<br>"
    else:
        if len(columnas_pivote) == n:
            resumen_txt = "<b style='color:#27AE60;'>CLASIFICACIÓN: Sistema Consistente Determinado (Solución Única)</b><br><br>"
            resumen_txt += "<b>Solución del Sistema:</b><br>"
            for idx, c in enumerate(columnas_pivote):
                val_frac = decimal_a_fraccion(matriz[idx][n])
                resumen_txt += f"&nbsp;&nbsp;&bull; {var_subind_html(c+1)} = <b>{val_frac}</b><br>"
        else:
            resumen_txt = "<b style='color:#D35400;'>CLASIFICACIÓN: Sistema Consistente Indeterminado (Infinitas Soluciones)</b><br><br>"
            resumen_txt += "<b>Estructura de la Solución General:</b><br>"
            
            # Imprimir ecuaciones en términos del parámetro (t, s, r, etc.)
            for idx, c in enumerate(columnas_pivote):
                val_b_frac = decimal_a_fraccion(matriz[idx][n])
                expr = f"{var_subind_html(c+1)} = {val_b_frac}"
                for j in indices_libres:
                    if abs(matriz[idx][j]) > 1e-9:
                        coef = matriz[idx][j]
                        signo = "-" if coef > 0 else "+"
                        coef_frac = decimal_a_fraccion(abs(coef))
                        param = mapa_parametros[j]
                        
                        # Omitir el 1 en el coeficiente para expresiones limpias (ej: + t en vez de + 1(t))
                        str_coef = "" if coef_frac == "1" else f"{coef_frac}"
                        expr += f" {signo} {str_coef}<i>{param}</i>"
                resumen_txt += f"&nbsp;&nbsp;&bull; {expr}<br>"

    resumen_txt += "<br><b>Columnas Pivote Identificadas:</b> " + (", ".join([str(c+1) for c in columnas_pivote]) if columnas_pivote else "Ninguna") + "<br>"
    resumen_txt += "<b>Variables Básicas:</b> " + (", ".join(vars_basicas) if vars_basicas else "Ninguna") + "<br>"
    resumen_txt += "<b>Variables Libres:</b> " + (", ".join(vars_libres) if vars_libres else "Ninguna") + "<br>"

    return matriz, pasos_log, resumen_txt