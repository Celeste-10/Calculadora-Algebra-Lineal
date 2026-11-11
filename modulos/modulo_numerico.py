"""
MÓDULO DE MÉTODOS NUMÉRICOS, GRAFICADOR, NOTACIÓN POSICIONAL Y ERRORES 
Implementa:
- Sub-módulo A: Método de Bisección (Algoritmo propio desde cero + validación SciPy)
- Sub-módulo B: Graficador de funciones interactivo con detección de discontinuidades
- Sub-módulo C: Notación Posicional (Base 10 y Base 2)
- Sub-módulo D: Errores Numéricos y Propagación de Errores

Asignatura: Álgebra Lineal 
"""

import math
import numpy as np
import sympy as sp
from scipy.optimize import bisect

# ------------------------------------------------------------------------------
# EVALUADOR SEGURO DE FUNCIONES CON SYMPY (EVITA EVAL DIRECTO)
# ------------------------------------------------------------------------------
def evaluar_funcion_segura(expr_str, x_val):
    """
    Evalúa una función matemática ingresada como string sin usar eval().
    Maneja funciones trigonométricas, exponenciales y potencias de forma segura.
    """
    try:
        expr_str = expr_str.replace('^', '**')
        x = sp.Symbol('x')
        
        # Transformaciones para interpretar multiplicación implícita y funciones estándar
        transformaciones = (
            sp.parsing.sympy_parser.standard_transformations +
            (sp.parsing.sympy_parser.implicit_multiplication_application,)
        )
        
        expr = sp.parse_expr(expr_str, transformations=transformaciones)
        
        # Convertir a función evaluable mediante numpy/math
        f_num = sp.lambdify(x, expr, modules=['numpy', 'math', {'cos': np.cos, 'sin': np.sin, 'tan': np.tan, 'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt}])
        
        res = float(f_num(x_val))
        return res
    except Exception:
        return float('nan')

# ------------------------------------------------------------------------------
# SUB-MÓDULO A: MÉTODO DE BISECCIÓN
# ------------------------------------------------------------------------------
def algoritmo_biseccion(expr_str, a, b, tol, max_iter):
    """
    Ejecuta el Método de Bisección desde cero cumpliendo todos los requerimientos:
    - Validación f(a)*f(b) < 0 y raíces en extremos.
    - Registro de k, a, b, xr, f(a), f(b), f(xr), Eb y ea.
    - Comparación con el número teórico de iteraciones: n_min = ceil(log2((b-a)/E)).
    - Comparación con scipy.optimize.bisect.
    """
    if a >= b:
        return False, "<b>ERROR:</b> El extremo inferior <i>a</i> debe ser estrictamente menor que <i>b</i> (a < b).", [], None

    if tol <= 0:
        return False, "<b>ERROR:</b> La tolerancia debe ser un valor positivo (E > 0).", [], None

    x = sp.Symbol('x')
    expr_str_clean = expr_str.replace('^', '**')
    try:
        expr = sp.parse_expr(expr_str_clean)
        f = sp.lambdify(x, expr, modules=['numpy', 'math'])
    except Exception as e:
        return False, f"<b>ERROR AL PARSEAR LA FUNCIÓN:</b> {str(e)}", [], None

    # Evaluar extremos iniciales
    try:
        fa = float(f(a))
        fb = float(f(b))
    except Exception as e:
        return False, f"<b>ERROR DE DOMINIO:</b> La función no está definida o es infinita en los extremos: {str(e)}", [], None

    if math.isnan(fa) or math.isnan(fb) or math.isinf(fa) or math.isinf(fb):
        return False, "<b>ERROR:</b> f(a) o f(b) no producen valores finitos en los extremos.", [], None

    # Raíz exacta en extremos
    if abs(fa) < 1e-14:
        return True, f"<b>RAÍZ EXACTA EN EXTREMO:</b> x = {a} es raíz exacta (f(a) = 0).", [], a
    if abs(fb) < 1e-14:
        return True, f"<b>RAÍZ EXACTA EN EXTREMO:</b> x = {b} es raíz exacta (f(b) = 0).", [], b

    # Condición de cambio de signo
    if fa * fb > 0:
        return False, (f"<b>ADVERTENCIA DE TEORÍA:</b> f(a)={fa:.5f} y f(b)={fb:.5f} tienen el mismo signo (f(a)·f(b) > 0).<br>"
                       f"El intervalo [{a}, {b}] no garantiza un cambio de signo para el Método de Bisección."), [], None

    # Iteraciones teóricas mínimas
    n_teorico = math.ceil(math.log2((b - a) / tol))

    filas_tabla = []
    xr_anterior = None
    raiz_encontrada = None
    motivo_paro = ""

    for k in range(1, max_iter + 1):
        xr = (a + b) / 2.0
        Eb = (b - a) / 2.0  # Semiancho del intervalo vigente
        
        try:
            fr = float(f(xr))
        except Exception:
            return False, f"<b>ERROR EN ITERACIÓN {k}:</b> La función falló al evaluarse en xr = {xr}.", filas_tabla, None

        # Error relativo aproximado
        if xr_anterior is not None:
            Ea = abs(xr - xr_anterior)
            if abs(xr) > 1e-14:
                ea_perc = (Ea / abs(xr)) * 100.0
                ea_str = f"{ea_perc:.6f}%"
            else:
                ea_str = "No definido (xr=0)"
        else:
            ea_str = "-"

        # Guardar estado de la iteración (antes de actualizar a o b)
        filas_tabla.append({
            'k': k,
            'a': a,
            'b': b,
            'xr': xr,
            'fa': fa,
            'fb': fb,
            'fr': fr,
            'Eb': Eb,
            'ea': ea_str
        })

        # Criterios de parada
        if abs(fr) < 1e-14:
            raiz_encontrada = xr
            motivo_paro = f"Raíz exacta alcanzada en máquina (f(xr) ≈ 0) en la iteración {k}."
            break

        if Eb <= tol:
            raiz_encontrada = xr
            motivo_paro = f"Tolerancia alcanzada (E_β = {Eb:.8e} ≤ {tol}) en la iteración {k}."
            break

        # Actualizar intervalo manteniendo el cambio de signo
        if fa * fr < 0:
            b = xr
            fb = fr
        else:
            a = xr
            fa = fr

        xr_anterior = xr

    if raiz_encontrada is None:
        raiz_encontrada = (a + b) / 2.0
        motivo_paro = f"Se alcanzó el número máximo de iteraciones ({max_iter}) sin satisfacer la tolerancia exigida E = {tol}."

    # Comparación con SciPy
    diferencia_scipy_str = "N/A"
    try:
        raiz_scipy = bisect(f, a_init := filas_tabla[0]['a'], b_init := filas_tabla[0]['b'], xtol=tol)
        diff = abs(raiz_encontrada - raiz_scipy)
        diferencia_scipy_str = f"{diff:.10e} (SciPy: {raiz_scipy:.8f})"
    except Exception:
        diferencia_scipy_str = "No contrastable por condición del intervalo"

    # Construcción del informe HTML
    html = f"<h3>RESULTADOS DEL MÉTODO DE BISECCIÓN</h3>"
    html += f"<p><b>Función:</b> f(x) = {expr_str}<br>"
    html += f"<b>Intervalo inicial:</b> [{filas_tabla[0]['a']}, {filas_tabla[0]['b']}] | <b>Tolerancia E:</b> {tol}<br>"
    html += f"<b>Iteraciones teóricas requeridas:</b> n<sub>mín</sub> = ⌈log₂((b-a)/E)⌉ = <b>{n_teorico}</b> | <b>Ejecutadas:</b> {len(filas_tabla)}<br>"
    html += f"<b>Estado:</b> {motivo_paro}</p>"

    html += f"<div style='background-color:#E8F8F5; border:2px solid #27AE60; border-radius:6px; padding:10px; margin-bottom:15px;'>"
    html += f"<h4 style='color:#1E8449; margin-top:0px;'>RAÍZ APROXIMADA ENCONTRADA:</h4>"
    html += f"<span style='font-size:18px; color:#1E8449;'><b>x<sub>r</sub> ≈ {raiz_encontrada:.8f}</b></span><br>"
    html += f"f(x<sub>r</sub>) = {filas_tabla[-1]['fr']:.8e}<br>"
    html += f"Diferencia absoluta con SciPy: <b>{diferencia_scipy_str}</b></div>"

    # Generación de la tabla HTML
    html += "<h4>Tabla Completa de Iteraciones:</h4>"
    html += "<table border='1' cellspacing='0' cellpadding='4' style='border-collapse:collapse; width:100%; text-align:center; font-size:11px;'>"
    html += "<tr style='background-color:#4A90E2; color:white;'>"
    html += "<th>k</th><th>a</th><th>b</th><th>x<sub>r</sub></th><th>f(a)</th><th>f(b)</th><th>f(x<sub>r</sub>)</th><th>E<sub>β</sub> (Semiancho)</th><th>ε<sub>a</sub> (%)</th>"
    html += "</tr>"

    for r in filas_tabla:
        html += f"<tr>"
        html += f"<td>{r['k']}</td>"
        html += f"<td>{r['a']:.6f}</td>"
        html += f"<td>{r['b']:.6f}</td>"
        html += f"<td><b>{r['xr']:.6f}</b></td>"
        html += f"<td>{r['fa']:.4f}</td>"
        html += f"<td>{r['fb']:.4f}</td>"
        html += f"<td>{r['fr']:.4e}</td>"
        html += f"<td>{r['Eb']:.6e}</td>"
        html += f"<td>{r['ea']}</td>"
        html += f"</tr>"
    html += "</table>"

    return True, html, filas_tabla, raiz_encontrada


# ------------------------------------------------------------------------------
# SUB-MÓDULO C: NOTACIÓN POSICIONAL (BASE 10 Y BASE 2)
# ------------------------------------------------------------------------------
def descomponer_notacion_posicional(numero_num):
    """
    Descompone un número entero en Notación Posicional Base 10 y Base 2.
    """
    signo = "-" if numero_num < 0 else ""
    val_abs = abs(int(numero_num))

    str_b10 = str(val_abs)
    len_b10 = len(str_b10)
    terminos_b10 = []
    suma_b10_verif = 0

    for idx, dig in enumerate(str_b10):
        d = int(dig)
        pot = len_b10 - 1 - idx
        terminos_b10.append(f"{d}·10<sup>{pot}</sup>")
        suma_b10_verif += d * (10 ** pot)

    str_b2 = bin(val_abs)[2:]
    len_b2 = len(str_b2)
    terminos_b2 = []
    terminos_eval_b2 = []
    suma_b2_verif = 0

    for idx, dig in enumerate(str_b2):
        d = int(dig)
        pot = len_b2 - 1 - idx
        val_term = d * (2 ** pot)
        terminos_b2.append(f"{d}·2<sup>{pot}</sup>")
        if val_term > 0:
            terminos_eval_b2.append(str(val_term))
        suma_b2_verif += val_term

    html = "<h3>DESCOMPOSICIÓN EN NOTACIÓN POSICIONAL</h3>"
    if signo == "-":
        html += "<p style='color:#E67E22;'><b>Nota:</b> El número es negativo. La descomposición posicional se aplica al valor absoluto y se conserva el signo al final.</p>"

    # Base 10
    html += "<div style='background-color:#F4F8FF; border:1px solid #BFD8FF; padding:10px; border-radius:6px; margin-bottom:12px;'>"
    html += f"<b>1. Descomposición en Base 10 (Decimal):</b><br>"
    html += f"({signo}{val_abs})<sub>10</sub> = {signo}[" + " + ".join(terminos_b10) + "]<br>"
    html += f"<b>Verificación de suma:</b> {signo}({suma_b10_verif})<sub>10</sub>"
    html += "</div>"

    # Base 2
    html += "<div style='background-color:#F4F8FF; border:1px solid #BFD8FF; padding:10px; border-radius:6px;'>"
    html += f"<b>2. Descomposición en Base 2 (Binario):</b><br>"
    html += f"({signo}{str_b2})<sub>2</sub> = {signo}[" + " + ".join(terminos_b2) + "]<br>"
    eval_str = " + ".join(terminos_eval_b2) if terminos_eval_b2 else "0"
    html += f"<b>Suma de potencias activas:</b> {signo}[{eval_str}] = <b>({signo}{suma_b2_verif})<sub>10</sub></b>"
    html += "</div>"

    return html


# ------------------------------------------------------------------------------
# SUB-MÓDULO D: ERRORES NUMÉRICOS Y PROPAGACIÓN DE ERRORES
# ------------------------------------------------------------------------------
def calcular_errores_y_propagacion(xv, xa, x_prop, dx):
    """
    Calcula errores absolutos/relativos/porcentuales y evalúa la propagación del error
    en f(x) = sin(x) + x² mediante la derivada f'(x) = cos(x) + 2x.
    """
    html = "<h3>1. CÁLCULO DE ERRORES NUMÉRICOS</h3>"

    E_abs = abs(xv - xa)
    if abs(xv) > 1e-15:
        E_rel = E_abs / abs(xv)
        E_porc = E_rel * 100.0
        rel_str = f"{E_rel:.8e}"
        porc_str = f"{E_porc:.6f}%"
    else:
        rel_str = "<span style='color:red;'>No definido (x_v = 0)</span>"
        porc_str = "<span style='color:red;'>No definido (x_v = 0)</span>"

    html += f"<p><b>Valor Verdadero (x<sub>v</sub>):</b> {xv} | <b>Valor Aproximado (x<sub>a</sub>):</b> {xa}</p>"
    html += "<ul>"
    html += f"<li><b>Error Absoluto (E<sub>a</sub> = |x<sub>v</sub> - x<sub>a</sub>|):</b> {E_abs:.8e}</li>"
    html += f"<li><b>Error Relativo (E<sub>r</sub> = E<sub>a</sub> / |x<sub>v</sub>|):</b> {rel_str}</li>"
    html += f"<li><b>Error Relativo Porcentual (E<sub>r%</sub>):</b> {porc_str}</li>"
    html += "</ul><hr>"

    # Propagación de Error
    html += "<h3>2. PROPAGACIÓN DEL ERROR EN f(x) = sin(x) + x²</h3>"
    
    # f(x) = sin(x) + x^2 -> f'(x) = cos(x) + 2x
    fx = math.sin(x_prop) + (x_prop ** 2)
    dfx = math.cos(x_prop) + (2.0 * x_prop)

    # Cambio real Δy = f(x + Δx) - f(x)
    fx_plus_dx = math.sin(x_prop + dx) + ((x_prop + dx) ** 2)
    dy_real = fx_plus_dx - fx

    # Aproximación por diferencial dy ≈ f'(x) · Δx
    dy_aprox = dfx * dx
    diferencia = abs(dy_real - dy_aprox)

    html += f"<p><b>Punto de evaluación x:</b> {x_prop} | <b>Perturbación Δx:</b> {dx}</p>"
    html += f"<ul>"
    html += f"<li><b>Derivada f'(x) = cos(x) + 2x:</b> {dfx:.6f}</li>"
    html += f"<li><b>Aproximación lineal (dy ≈ f'(x)·Δx):</b> {dy_aprox:.8e}</li>"
    html += f"<li><b>Cambio real (Δy = f(x+Δx) - f(x)):</b> {dy_real:.8e}</li>"
    html += f"<li><b>Diferencia absoluta (|Δy<sub>real</sub> - dy<sub>aprox</sub>|):</b> <b style='color:#2980B9;'>{diferencia:.8e}</b></li>"
    html += f"</ul>"
    html += "<p><i>La aproximación lineal basada en la derivada de primer orden es más precisa cuando la perturbación Δx es pequeña.</i></p>"

    # Explicación de 0.1 + 0.2 != 0.3 y Epsilon
    eps = np.finfo(float).eps
    val_sum = 0.1 + 0.2
    es_igual = (val_sum == 0.3)

    html += "<hr><h3>3. REPRESENTACIÓN EN PUNTO FLOTANTE Y EPSILON</h3>"
    html += f"<p><b>Prueba en Python: 0.1 + 0.2 == 0.3 &rarr; <span style='color:{'green' if es_igual else 'red'};'><b>{es_igual}</b></span></b><br>"
    html += f"<i>Valor real obtenido de (0.1 + 0.2):</i> {val_sum:.17f}<br>"
    html += f"<b>Razón:</b> 0.1 y 0.2 son fracciones periódicas en binario (Base 2) y sufren truncamiento al almacenarse en los 53 bits de mantisa del estándar IEEE 754.</p>"
    html += f"<p><b>Epsilon de máquina (numpy.finfo(float).eps):</b> <code>{eps:.10e}</code><br>"
    html += "<i>Representa la distancia relativa entre 1.0 y el número representable inmediatamente superior en doble precisión.</i></p>"

    return html