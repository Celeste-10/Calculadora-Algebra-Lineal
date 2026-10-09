
# ==============================================================================
# UNIVERSIDAD AMERICANA - FACULTAD DE INGENIERIA Y ARQUITECTURA
# PROGRAMA 1: Solucion de Sistemas de Ecuaciones Lineales por Eliminacion por Filas
# ==============================================================================

def mostrar_matriz(matriz, mensaje="Matriz Aumentada:"):
    """
    Imprime la matriz aumentada [A|b] en pantalla con un formato legible y alineado.
    Recibe la matriz y una cadena descriptiva para contextualizar el paso actual.
    """
    print(f"\n--- {mensaje} ---")
    filas = len(matriz)
    columnas = len(matriz[0])
    
    for i in range(filas):
        fila_str = ""
        for j in range(columnas):
            if j == columnas - 1:
                # Separador visual '|' antes de la columna de términos independientes (vector b)
                fila_str += f" | {matriz[i][j]:10.4f}"
            else:
                fila_str += f"{matriz[i][j]:10.4f}"
        print(fila_str)
    print()

def pedir_entero_positivo(mensaje):
    """
    Valida que el usuario ingrese únicamente números enteros positivos mayores a cero.
    """
    while True:
        try:
            val = int(input(mensaje))
            if val <= 0:
                print(" Por favor ingrese un número entero mayor a 0.")
            else:
                return val
        except ValueError:
            print(" Entrada inválida. Ingrese un número entero válido.")

def pedir_flotante(mensaje):
    """
    Valida que el usuario ingrese un valor numérico real (float).
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print(" Entrada inválida. Ingrese un número real (ej. 5, -2.5, 0).")

def ingresar_datos():
    """
    Solicita al usuario el número de ecuaciones (m) y variables (n),
    así como la entrada término a término de la matriz A y el vector b.
    """
    print("=" * 60)
    print(" INGRESO DE DATOS DEL SISTEMA DE ECUACIONES [A|b]")
    print("=" * 60)
    
    m = pedir_entero_positivo("Ingrese el número de ecuaciones (filas, m): ")
    n = pedir_entero_positivo("Ingrese el número de variables (columnas, n): ")

    matriz = []
    print("\nIngrese los coeficientes de la matriz A y el término independiente b:")
    for i in range(m):
        fila = []
        print(f"\n-- Ecuación / Fila {i + 1} --")
        for j in range(n):
            val = pedir_flotante(f" Coeficiente A[{i+1}][{j+1}]: ")
            fila.append(val)
        b_val = pedir_flotante(f" Término independiente b[{i+1}]: ")
        fila.append(b_val)
        matriz.append(fila)
    
    return matriz, m, n

def eliminacion_gaussiana(matriz_orig, m, n):
    """
    Aplica el algoritmo de Eliminación Gaussiana con pivoteo parcial.
    Transforma la matriz a su Forma Escalonada por Filas generando ceros 
    ÚNICAMENTE DEBAJO de cada pivote.
    
    Retorna:
      - matriz: Matriz escalonada resultante.
      - pivotes: Lista de tuplas (fila, columna) identificando la posición de cada pivote.
    """
    # copia para evitar modificar la matriz original cargada
    matriz = [fila[:] for fila in matriz_orig]
    r = 0  # indice de fila actual para buscar pivote
    pivotes = []  # almacena posiciones (fila, columna) de los pivotes encontrados

    for c in range(n):
        if r >= m:
            break
            
        # 1. pivoteo parcial: busca el mayor valor absoluto en la columna c desde la fila r
        max_fila = r
        for i in range(r + 1, m):
            if abs(matriz[i][c]) > abs(matriz[max_fila][c]):
                max_fila = i
                
        # si la columna c es casi nula (todos los valores < 1e-9), no hay pivote en esta columna
        if abs(matriz[max_fila][c]) < 1e-9:
            continue
            
        # intercambio de filas si el elemento mayor está en una fila inferior
        if max_fila != r:
            matriz[r], matriz[max_fila] = matriz[max_fila], matriz[r]
            mostrar_matriz(matriz, f"Paso: Intercambio de Fila {r+1} con Fila {max_fila+1}")

        # registra la ubicación del pivote
        pivotes.append((r, c))
        pivote = matriz[r][c]

        # 2. generación de ceros ÚNICAMENTE DEBAJO del pivote actual
        for i in range(r + 1, m):
            factor = matriz[i][c] / pivote
            if abs(factor) > 1e-9:
                for j in range(c, n + 1):
                    matriz[i][j] -= factor * matriz[r][j]
                matriz[i][c] = 0.0  # asegura el cero numérico exacto para evitar errores de redondeo
                mostrar_matriz(matriz, f"Paso: Fila_{i+1} -> Fila_{i+1} - ({factor:.4f}) * Fila_{r+1}")
                
        r += 1

    return matriz, pivotes

def sustitucion_hacia_atras(matriz_escalonada, pivotes, n):
    """
    Resuelve el sistema mediante el proceso de Sustitución Hacia Atrás
    una vez que la matriz está en Forma Escalonada.
    """
    solucion = [0.0] * n
    # recorre los pivotes desde el último hacia el primero (de abajo hacia arriba)
    for r, c in reversed(pivotes):
        suma = matriz_escalonada[r][n]
        for j in range(c + 1, n):
            suma -= matriz_escalonada[r][j] * solucion[j]
        solucion[c] = suma / matriz_escalonada[r][c]
    return solucion

def clasificar_y_resolver(matriz_escalonada, pivotes, m, n):
    """
    Evalúa la matriz escalonada para determinar si el sistema es:
      1. Inconsistente (Sin Solución)
      2. Consistente Determinado (Solución Única)
      3. Consistente Indeterminado (Infinitas Soluciones e Identificación de Variables Libres)
    """
    es_inconsistente = False
    fila_inconsistente = -1

    #  verifica contradicciones: filas [0 0 ... 0 | k] con k != 0
    for i in range(m):
        todos_ceros_A = all(abs(matriz_escalonada[i][j]) < 1e-9 for j in range(n))
        if todos_ceros_A and abs(matriz_escalonada[i][n]) > 1e-9:
            es_inconsistente = True
            fila_inconsistente = i + 1
            break

    print("=" * 50)
    print("CLASIFICACIÓN DEL SISTEMA DE ECUACIONES")
    print("=" * 50)

    # CASO 1: sistema inconsistente
    if es_inconsistente:
        k_val = matriz_escalonada[fila_inconsistente - 1][n]
        print("Clasificación: Sistema Inconsistente (Sin Solución).")
        print(f"Razón: Se detectó en la Fila {fila_inconsistente} una ecuación contradictoria de tipo 0 = {k_val:.4f} (con k ≠ 0).")
        return None

    # identificación de columnas pivote y variables libres
    cols_pivotes = [c for r, c in pivotes]
    num_pivotes = len(cols_pivotes)

    # CASO 2: sistema consistente determinado
    if num_pivotes == n:
        print("Clasificación: Sistema Consistente Determinado (Solución Única).")
        solucion = sustitucion_hacia_atras(matriz_escalonada, pivotes, n)
        
        print("\nValores numéricos de las variables halladas (Sustitución Hacia Atrás):")
        for k in range(n):
            print(f"  x{k+1} = {solucion[k]:.4f}")
        return solucion

    # CASO 3: sistema consistente indeterminado
    else:
        print("Clasificación: Sistema Consistente Indeterminado (Infinitas Soluciones).")
        
        # identificar cuáles variables son básicas y cuáles son libres
        vars_basicas = [f"x{c+1}" for c in cols_pivotes]
        vars_libres = [f"x{j+1}" for j in range(n) if j not in cols_pivotes]
        
        print(f"\nDetalle de Variables:")
        print(f"  - Cantidad de variable(s) libre(s): {len(vars_libres)}")
        print(f"  - Variable(s) Libre(s) identificada(s): {', '.join(vars_libres)}")
        print(f"  - Variable(s) Básica(s) / Pivote: {', '.join(vars_basicas)}")
        return None

def verificar_solucion(matriz_orig, solucion, m, n):
    """
    Sustituye los valores numéricos obtenidos en cada una de las ecuaciones 
    del sistema original para comprobar automáticamente la igualdad (Ax = b).
    """
    if solucion is None:
        return

    print("\n" + "=" * 50)
    print("VERIFICACIÓN DE LA SOLUCIÓN EN EL SISTEMA ORIGINAL")
    print("=" * 50)

    for i in range(m):
        suma_lhs = 0.0
        expr_str = ""
        for j in range(n):
            coef = matriz_orig[i][j]
            suma_lhs += coef * solucion[j]
            signo = " + " if j < n - 1 else ""
            expr_str += f"({coef:.2f} * {solucion[j]:.4f}){signo}"
        
        rhs = matriz_orig[i][n]
        diferencia = abs(suma_lhs - rhs)
        es_valido = diferencia < 1e-6
        
        estado = " Correcto" if es_valido else " Error"
        print(f"Ecuación {i+1}: {expr_str} = {suma_lhs:.4f} | b[{i+1}] = {rhs:.4f} -> {estado}")

def main():
    print("=" * 60)
    print(" CALCULADORA DE ÁLGEBRA LINEAL - ELIMINACIÓN POR FILAS ")
    print("=" * 60)
    
    # 1. entrada de datos
    matriz_orig, m, n = ingresar_datos()
    mostrar_matriz(matriz_orig, "Matriz Aumentada Inicial [A|b]")
    
    # 2. procesamiento (eliminación gaussiana)
    matriz_escalonada, pivotes = eliminacion_gaussiana(matriz_orig, m, n)
    mostrar_matriz(matriz_escalonada, "Matriz en Forma Escalonada por Filas Final")
    
    # 3. clasificación y resolución
    solucion = clasificar_y_resolver(matriz_escalonada, pivotes, m, n)
    
    # 4. verificación
    verificar_solucion(matriz_orig, solucion, m, n)

if __name__ == "__main__":
    main()