# Calculadora de Álgebra Lineal - UAM

Proyecto integral desarrollado para la asignatura de **Álgebra Lineal** en la **Universidad Americana (UAM)** para la carrera de **Ingeniería de Sistemas**.

Esta suite de software ofrece una herramienta gráfica interactiva, intuitiva y de alta precisión para el estudio, resolución y demostración paso a paso de conceptos fundamentales del álgebra lineal.

---

## 🚀 Visión General del Proyecto

El objetivo principal es proporcionar un entorno didáctico que resuelva problemas complejos y verifique teoremas **sin el uso de librerías numéricas de terceros** (como NumPy o SciPy). Toda la lógica matemática, operaciones con renglones, determinantes por cofactores y algoritmos de reducción fueron construidos desde cero en **Pure Python**.

---

## 💻 Módulos y Funcionalidades

1. **Sistemas de Ecuaciones Lineales ($Ax = b$):**
   * Resolución por eliminación de **Gauss-Jordan** (RREF) paso a paso.
   * Resolución detallada mediante **Regla de Cramer** con desglose de determinantes modificados ($|A_x|, |A_y|, |A_z|$) y matriz principal.

2. **Operaciones con Vectores en $\mathbb{R}^n$:**
   * Suma, resta y producto por escalar $c \cdot u$ y $c \cdot v$.
   * Evaluación de Independencia Lineal (L.I. / L.D.) mediante matriz aumentada homogénea.

3. **Álgebra Matricial e Inversa:**
   * Operaciones básicas: Suma ($A + B$), Resta ($A - B$), Producto ($A \times B$) y Transposición ($A^T, B^T$).
   * Cálculo de Inversa ($A^{-1}, B^{-1}$) por dos métodos en paralelo: **Gauss-Jordan $[A | I]$** y **Matriz Adjunta $A^{-1} = \frac{1}{|A|} \text{Adj}(A)$**.
   * Demostración explícita de la propiedad fundamental $A \cdot A^{-1} = I$.

4. **Combinaciones Lineales y Propiedades $Ax$:**
   * Verificación de la combinación lineal de vectores con vector constante $b$.
   * Demostración gráfica y algebraica de las propiedades $A(u + v) = Au + Av$ y $A(c \cdot u) = c(Au)$.

5. **Verificador de Propiedades y Teoremas:**
   * Comprobación automatizada de los teoremas de inversión, transposición y operaciones elementales sobre el determinante.
   * Evaluación de determinantes por Expansión de Cofactores y Método de Sarrus (para matrices $3 \times 3$).
   * Módulo interactivo de Resumen de Teoremas y Fundamentos.

---

## 🛠️ Arquitectura y Tecnologías

El proyecto sigue un patrón desacoplado separando la lógica matemática de la interfaz gráfica:

* **Lenguaje:** Python 3.8+
* **Interfaz Gráfica (Frontend):** PyQt6 / PyQt5 con diseño personalizado (*Light & Soft Blues Palette* / Navy & Deep Blues).
* **Motor Matemático (Backend):** Algoritmos nativos en Python puro para la conversión a fracciones explícitas, determinantes por cofactores y reducción matricial.

---

## ⚙️ Requisitos e Instalación

### Requisitos Previos:
* Python 3.8 o superior instalado en el sistema.

### Instalación de Dependencias:
Instala la librería gráfica necesaria para ejecutar la interfaz:

```bash
pip install PyQt6
