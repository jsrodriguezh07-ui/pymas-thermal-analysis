# Thermal Analysis Tool for Hyperstatic Structures using pymas

Módulo especializado de análisis térmico e hiperestaticidad para estructuras rígidas de Ingeniería Civil, desarrollado a partir de la librería **pymas** (creada por el profesor `rvcristiand`).

---

## 1. Contexto y Marco Teórico (Background)

Los cambios de temperatura en el entorno ambiental inducen variaciones dimensionales en los materiales de construcción. La ley de dilatación térmica lineal establece que el cambio no restringido de longitud ($\Delta L$) viene dado por:

$$\Delta L = \alpha \cdot L \cdot \Delta T$$

**Donde:**
* $\alpha$: Coeficiente de expansión térmica lineal ($1/^\circ\text{C}$).
* $L$: Longitud inicial del elemento ($\text{m}$).
* $\Delta T$: Gradiente o variación de temperatura ($^\circ\text{C}$).

En estructuras hiperestáticas (como puentes continuos, cerchas y pórticos con apoyos rígidos), la expansión o contracción no puede ocurrir libremente. Como resultado, la restricción de estos apoyos genera fuerzas axiales de restricción y esfuerzos térmicos internos:

$$N_{\text{th}} = E \cdot A \cdot \alpha \cdot \Delta T$$

$$\sigma_{\text{th}} = E \cdot \alpha \cdot \Delta T$$

### ¿Qué calcula este script?
* **Expansión Térmica Libre:** Calcula cuánto se dilataría libremente la estructura ante un incremento o decremento de temperatura.
* **Cargas Nodales Equivalentes:** Modela y convierte la deformación térmica en cargas vectoriales equivalentes a nivel de nudos.
* **Análisis Matricial con PyMAS:** Integra las cargas térmicas dentro del solver matricial de la librería `pymas`.
* **Cálculo de Esfuerzos Inducidos:** Determina las fuerzas axiales y esfuerzos de compresión o tracción ($\text{MPa}$) en los elementos estructurales restringidos.

---

## 2. Instalación (Installation)

Para ejecutar este módulo de análisis térmico es necesario instalar previamente la librería base **pymas** desarrollada por el profesor.

### Paso 1: Instalación de pymas
Instala el paquete base directamente desde su repositorio de GitHub:

```bash
pip install git+https://github.com/rvcristiand/pymas.git
