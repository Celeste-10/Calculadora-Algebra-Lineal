<div align="center" style="margin-bottom: 0px;">
  <img src="assets/MatrixX.png" alt="MatrixX Logo" width="380" style="margin-bottom: 0px;" />
</div>

---

<p align="center">
  <b>Calculadora de Álgebra Lineal</b><br>
  <b>Universidad Americana (UAM)</b><br>
  <b>Facultad de Ingeniería y Arquitectura · Ingeniería de Sistemas</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PYQT-6%20%2F%205-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/MATPLOTLIB-3.5+-11557c?style=for-the-badge&logo=matplotlib&logoColor=white" />
  <img src="https://img.shields.io/badge/NUMPY-USADO-BLUE?style=for-the-badge&logo=numpy&logoColor=white" />
</p>

<div align="center">

| Campo | Detalle |
| :--- | :--- |
| **Universidad** | Universidad Americana (UAM) · Ingeniería de Sistemas |
| **Asignatura** | Álgebra Lineal y Métodos Numéricos |
| **Proyecto** | Suite de Software Interactivo para Álgebra Lineal y Análisis Numérico |
| **Período** | II Semestre 2026 |

</div>

---

## 🚀 Descripción del proyecto

Esta suite de software ofrece una herramienta gráfica interactiva, intuitiva y de alta precisión para el estudio, resolución y demostración paso a paso de conceptos fundamentales del **álgebra lineal** y los **métodos numéricos**.

El objetivo principal es proporcionar un entorno didáctico que resuelva problemas complejos y verifique teoremas algebraicos y analíticos de forma transparente. La aplicación integra un motor de cálculo matricial detallado, visualización gráfica interactiva de funciones y análisis numérico de raíces y propagación de errores.

---

## 💻 Módulos y funcionalidades

1. **Sistemas de Ecuaciones Lineales ($Ax = b$):**
   * Resolución por eliminación de **Gauss-Jordan** (RREF) paso a paso.
   * Resolución detallada mediante **Regla de Cramer** con desglose de determinantes modificados ($\vert{}A_x\vert{}, \vert{}A_y\vert{}, \vert{}A_z\vert{}$) y matriz principal.

2. **Operaciones con Vectores en $\mathbb{R}^n$:**
   * Suma, resta y producto por escalar $c \cdot u$ y $c \cdot v$.
   * Evaluación de Independencia Lineal (L.I. / L.D.) mediante matriz aumentada homogénea.

3. **Álgebra Matricial e Inversa:**
   * Operaciones básicas: Suma ($A + B$), Resta ($A - B$), Producto ($A \times B$) y Transposición ($A^T, B^T$).
   * Cálculo de Inversa ($A^{-1}, B^{-1}$) por dos métodos en paralelo: **Gauss-Jordan $[A \vert{} I]$** y **Matriz Adjunta $A^{-1} = \frac{1}{\vert{}A\vert{}} \text{Adj}(A)$**.
   * Demostración explícita de la propiedad fundamental $A \cdot A^{-1} = I$.

4. **Combinaciones Lineales y Propiedades $Ax$:**
   * Verificación de la combinación lineal de vectores con vector constante $b$.
   * Demostración gráfica y algebraica de las propiedades $A(u + v) = Au + Av$ y $A(c \cdot u) = c(Au)$.

5. **Factorización $LU$ ($A = LU$):**
   * Descomposición de la matriz $A$ en factores Triangular Inferior ($L$) y Triangular Superior ($U$).
   * Resolución del sistema de ecuaciones $Ax = b$ mediante sustitución hacia adelante ($Ly = b$) y hacia atrás ($Ux = y$).

6. **Métodos Numéricos (Herramienta Numérica Integral):**
   * **Método de Bisección:** Cálculo iterativo de raíces con tabla completa de iteraciones ($a$, $b$, $c$, $f(c)$, error) e integración automática con el graficador.
   * **Graficador de Funciones Interactivo:** Representación gráfica en tiempo real con Matplotlib, soporte para funciones algebraicas y trascendentes, resaltado de raíces y manejo de discontinuidades/asíntotas.
   * **Notación Posicional:** Descomposición analítica de enteros en Base 10 y representación en Base 2 (Binario).
   

7. **Verificador de Propiedades y Teoremas:**
   * Comprobación automatizada de teoremas de inversión, transposición y operaciones elementales sobre el determinante.
   * Evaluación de determinantes por Expansión de Cofactores y Método de Sarrus (para matrices $3 \times 3$).
   * Módulo interactivo de Resumen de Teoremas y Fundamentos.

---

## 🛠️ Requisitos del sistema

| Herramienta | Versión utilizada | Observación |
| :--- | :--- | :--- |
| **Python** | 3.8+ | Entorno de ejecución principal |
| **PyQt6 / PyQt5** | Última estable | Biblioteca para la interfaz gráfica (GUI) |
| **NumPy** | Última estable | Soporte para evaluación y arreglos numéricos |
| **Matplotlib** | 3.5+ | Renderizado de gráficas interactivas en la GUI |
| **SymPy** | Última estable | Parseador y evaluación segura de funciones matemáticas |
| **Git** | Cualquier versión reciente | Control de versiones |
| **IDE Recomendado** | VS Code | Entorno de desarrollo recomendado |

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone [https://github.com/Celeste-10/Calculadora-Algebra-Lineal.git](https://github.com/Celeste-10/Calculadora-Algebra-Lineal.git)
cd Calculadora-Algebra-Lineal
```
### 2️⃣ Instalar dependencias requeridas
```bash
pip install PyQt6
pip install numpy
pip install matplotlib
pip install sympy
```
### 3️⃣ Ejecutar la aplicación
```bash
python main.py
```

## 🏗️ Arquitectura del proyecto
```bash
Calculadora_Algebra_Lineal/
├── 📄 main.py                            Punto de entrada principal del sistema
├── 📁 assets/
│   └── 📄 MatrixX.png                    Logotipo y recursos gráficos de la GUI
├── 📁 gui/
│   ├── 📄 gui_window.py                  Ventana principal, contenedor de pestañas y Graficador Matplotlib
│   ├── 📄 interfaz_gui.py                Componentes gráficos auxiliares
│   └── 📄 interfaz_programa3.py           Controladores visuales del módulo 3
├── 📁 logica/
│   └── 📄 operaciones.py                 Motor Gauss-Jordan, fracciones y tablas HTML
├── 📁 modulos/
│   ├── 📄 modulo_determinantes.py        Cofactores, Sarrus y Regla de Cramer
│   ├── 📄 modulo_lu.py                   Factorización LU y solución Ax = b (Ly=b, Ux=y)
│   ├── 📄 modulo_matrices.py             Álgebra de matrices, Inversas y Verificador
│   ├── 📄 modulo_numerico.py             Bisección, Notación Posicional, Errores y Evaluador de Funciones
│   ├── 📄 modulo_sistemas.py             Solucionador de sistemas Ax = b
│   └── 📄 modulo_vectores.py             Operaciones en Rⁿ e Independencia Lineal
├── 📁 programas_iniciales/
│   ├── 📄 Programa 1_Grupo 5.py           Prototipo inicial del módulo 1
│   ├── 📄 Programa 2_Grupo5.py            Prototipo inicial del módulo 2
│   └── 📄 Programa 3_Grupo5.py            Prototipo inicial del módulo 3
└── 📁 teoremas/
    └── 📄 resumen_teoremas.py            Resumen interactivo de Teoremas y Teoría
```
