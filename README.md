<h1 align="center">Calculadora de Álgebra Lineal - UAM</h1>

<p align="center">
  <b>Universidad Americana (UAM)</b><br>
  <b>Facultad de Ingeniería y Arquitectura · Ingeniería de Sistemas</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PYQT-6%20%2F%205-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/NUMPY-NO%20USADO-RED?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PURE%20PYTHON-100%25-BLUE?style=for-the-badge" />
</p>

<div align="center">

| Campo | Detalle |
| :--- | :--- |
| **Universidad** | Universidad Americana (UAM) · Ingeniería de Sistemas |
| **Asignatura** | Álgebra Lineal |
| **Proyecto** | Suite de Software Interactivo para Álgebra Lineal |
| **Modalidad** | Pure Python (Sin librerías numéricas de terceros) |
| **Período** | II Semestre 2026 |

</div>

---

## 🚀 Descripción del proyecto

Esta suite de software ofrece una herramienta gráfica interactiva, intuitiva y de alta precisión para el estudio, resolución y demostración paso a paso de conceptos fundamentales del álgebra lineal.

El objetivo principal es proporcionar un entorno didáctico que resuelva problemas complejos y verifique teoremas **sin el uso de librerías numéricas de terceros** (como NumPy o SciPy). Toda la lógica matemática, operaciones con renglones, determinantes por cofactores y algoritmos de reducción fueron construidos desde cero en **Pure Python**.

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

5. **Verificador de Propiedades y Teoremas:**
   * Comprobación automatizada de los teoremas de inversión, transposición y operaciones elementales sobre el determinante.
   * Evaluación de determinantes por Expansión de Cofactores y Método de Sarrus (para matrices $3 \times 3$).
   * Módulo interactivo de Resumen de Teoremas y Fundamentos.

---

## 🛠️ Requisitos del sistema

| Herramienta | Versión utilizada | Observación |
| :--- | :--- | :--- |
| **Python** | 3.8+ | Entorno de ejecución principal |
| **PyQt6 / PyQt5** | Última estable | Biblioteca para la interfaz gráfica (GUI) |
| **Git** | Cualquier versión reciente | Control de versiones |
| **IDE Recomendado** | VS Code / PyCharm | Entorno de desarrollo recomendado |

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Celeste-10/Calculadora-Algebra-Lineal.git
cd Calculadora-Algebra-Lineal
```

### 2️⃣ Instalar dependencias requeridas

```bash
pip install PyQt6
```

### 3️⃣ Ejecutar la aplicación
```bash
python main.py
```

---

## 🏗️ Arquitectura del proyecto

```bash
Calculadora_Algebra_Lineal/
├── 📄 main.py                             Punto de entrada principal del sistema
├── 📁 assets/
│   └── 📄 MatrixX.png                     Logotipo y recursos gráficos de la GUI
├── 📁 gui/
│   ├── 📄 gui_window.py                   Ventana principal y contenedor de pestañas
│   ├── 📄 interfaz_gui.py                 Componentes gráficos auxiliares
│   └── 📄 interfaz_programa3.py           Controladores visuales del módulo 3
├── 📁 logica/
│   └── 📄 operaciones.py                  Motor Gauss-Jordan, fracciones y tablas HTML
├── 📁 modulos/
│   ├── 📄 modulo_determinantes.py         Cofactores, Sarrus y Regla de Cramer
│   ├── 📄 modulo_matrices.py              Álgebra de matrices, Inversas y Verificador
│   ├── 📄 modulo_sistemas.py              Solucionador de sistemas Ax = b
│   └── 📄 modulo_vectores.py              Operaciones en Rⁿ e Independencia Lineal
├── 📁 programas_iniciales/
│   ├── 📄 Programa 1_Grupo 5.py           Prototipo inicial del módulo 1
│   ├── 📄 Programa 2_Grupo5.py            Prototipo inicial del módulo 2
│   └── 📄 Programa 3_Grupo5.py            Prototipo inicial del módulo 3
└── 📁 teoremas/
    └── 📄 resumen_teoremas.py             Resumen interactivo de Teoremas y Teoría
```
