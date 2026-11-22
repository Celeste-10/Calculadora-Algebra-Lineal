"""Módulo de Métodos Iterativos: Jacobi y Gauss-Seidel."""

import numpy as np


def preparar_sistema(A, b, x0, tolerancia, max_iter, reordenar=True):
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    x0 = np.asarray(x0, dtype=float)
    if A.ndim != 2 or A.shape[0] == 0 or A.shape[0] != A.shape[1]:
        raise ValueError('A debe ser una matriz cuadrada no vacía.')
    n = A.shape[0]
    if b.shape != (n,) or x0.shape != (n,):
        raise ValueError('Los vectores b y x⁽⁰⁾ deben tener n componentes.')
    if not all(np.all(np.isfinite(v)) for v in (A, b, x0)):
        raise ValueError('Los datos deben ser números finitos.')
    if not np.isfinite(tolerancia) or tolerancia <= 0 or int(max_iter) != max_iter or max_iter <= 0:
        raise ValueError('La tolerancia y las iteraciones máximas deben ser positivas.')

    orden = tuple(range(n))

    def domina(M):
        return bool(np.all(np.abs(np.diag(M)) > np.sum(np.abs(M), axis=1) - np.abs(np.diag(M))))

    if reordenar and (np.any(np.isclose(np.diag(A), 0, atol=1e-14)) or not domina(A)):
        opciones = [
            sorted(
                (i for i in range(n) if abs(A[i, j]) > 1e-14),
                key=lambda i: abs(A[i, j]) / (sum(abs(A[i])) + 1e-30),
                reverse=True
            )
            for j in range(n)
        ]
        mejor = None

        def buscar(j, usados, actual):
            nonlocal mejor
            if j == n:
                p = tuple(actual)
                if mejor is None or domina(A[list(p)]):
                    mejor = p
                return domina(A[list(p)])
            for i in opciones[j]:
                if i not in usados:
                    if buscar(j + 1, usados | {i}, actual + [i]):
                        return True
            return False

        buscar(0, set(), [])
        if mejor is not None:
            orden = mejor
            A, b = A[list(orden)], b[list(orden)]

    if np.any(np.abs(np.diag(A)) <= 1e-14):
        raise ValueError('Hay ceros en la diagonal y no se encontró un reordenamiento válido.')

    return A, b, x0, domina(A), orden


def iterar(A, b, x0, tolerancia, max_iter, metodo):
    if metodo not in ('Jacobi', 'Gauss-Seidel'):
        raise ValueError('Método desconocido.')
    matriz = A.tolist()
    independientes = b.tolist()
    x = x0.tolist()
    n = len(x)
    historial = []
    estado = 'Máximo de iteraciones / posible no convergencia'

    for k in range(1, max_iter + 1):
        anterior = x.copy()
        if metodo == 'Jacobi':
            nuevo = []
            for i in range(n):
                suma = sum(matriz[i][j] * anterior[j] for j in range(n) if j != i)
                nuevo.append((independientes[i] - suma) / matriz[i][i])
            x = nuevo
        else:
            for i in range(n):
                suma_antes = sum(matriz[i][j] * x[j] for j in range(i))
                suma_despues = sum(matriz[i][j] * anterior[j] for j in range(i + 1, n))
                x[i] = (independientes[i] - suma_antes - suma_despues) / matriz[i][i]

        error = max(abs(x[i] - anterior[i]) for i in range(n))
        residuo = max(abs(sum(matriz[i][j] * x[j] for j in range(n)) - independientes[i]) for i in range(n))

        if not all(np.isfinite(v) for v in x) or not np.isfinite(error) or not np.isfinite(residuo):
            x = anterior
            estado = 'Advertencia: valores no finitos / posible divergencia'
            break

        historial.append({'k': k, 'x': np.array(x), 'error': error, 'residuo': residuo})

        if error <= tolerancia:
            estado = 'Convergencia por criterio de error entre iteraciones'
            break

        if max(abs(v) for v in x) > 1e100 or (
            len(historial) >= 8 and all(historial[-j]['error'] > historial[-j - 1]['error'] * 1.5 for j in range(1, 6))
        ):
            estado = 'Advertencia: crecimiento del error / posible divergencia'
            break

    x_resultado = np.array(x)
    residuo_final = max(abs(sum(matriz[i][j] * x[j] for j in range(n)) - independientes[i]) for i in range(n))
    return {
        'metodo': metodo,
        'x': x_resultado,
        'historial': historial,
        'estado': estado,
        'iteraciones': len(historial),
        'residuo': residuo_final
    }


def comparar(A, b, x0, tolerancia=1e-6, max_iter=100, reordenar=True):
    A, b, x0, dominante, orden = preparar_sistema(A, b, x0, tolerancia, max_iter, reordenar)
    resultados = {m: iterar(A, b, x0, tolerancia, max_iter, m) for m in ('Jacobi', 'Gauss-Seidel')}
    referencia = None
    try:
        referencia = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        pass
    return {
        'A': A,
        'b': b,
        'dominante': dominante,
        'orden': orden,
        'resultados': resultados,
        'referencia': referencia,
        'diferencia_metodos': float(np.max(np.abs(resultados['Jacobi']['x'] - resultados['Gauss-Seidel']['x'])))
    }