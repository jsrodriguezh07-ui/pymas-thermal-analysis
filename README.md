Thermal Analysis Tool for Hyperstatic Structures using pymasMódulo especializado de análisis térmico e hiperestaticidad para estructuras rígidas de Ingeniería Civil, desarrollado a partir de la librería pymas (creada por el profesor rvcristiand).1. Contexto y Marco Teórico (Background)Los cambios de temperatura en el entorno ambiental inducen variaciones dimensionales en los materiales de construcción. La ley de dilatación térmica lineal establece que el cambio no restringido de longitud ($\Delta L$) viene dado por:$$\Delta L = \alpha \cdot L \cdot \Delta T$$Donde:$\alpha$: Coeficiente de expansión térmica lineal ($1/^\circ\text{C}$).$L$: Longitud inicial del elemento ($\text{m}$).$\Delta T$: Gradiente o variación de temperatura ($^\circ\text{C}$).En estructuras hiperestáticas (como puentes continuos, cerchas y pórticos con apoyos rígidos), la expansión o contracción no puede ocurrir libremente. Como resultado, la restricción de estos apoyos genera fuerzas axiales de restricción y esfuerzos térmicos internos:$$N_{\text{th}} = E \cdot A \cdot \alpha \cdot \Delta T$$$$\sigma_{\text{th}} = E \cdot \alpha \cdot \Delta T$$¿Qué calcula este script?Expansión Térmica Libre: Calcula cuánto se dilataría libremente la estructura ante un incremento o decremento de temperatura.Cargas Nodales Equivalentes: Modela y convierte la deformación térmica en cargas vectoriales equivalentes a nivel de nudos.Análisis Matricial con PyMAS: Integra las cargas térmicas dentro del solver matricial de la librería pymas.Cálculo de Esfuerzos Inducidos: Determina las fuerzas axiales y esfuerzos de compresión o tracción ($\text{MPa}$) en los elementos estructurales restringidos.2. Instalación (Installation)Para ejecutar este módulo de análisis térmico es necesario instalar previamente la librería base pymas desarrollada por el profesor.Paso 1: Instalación de pymasInstala el paquete base directamente desde su repositorio de GitHub:pip install git+https://github.com/rvcristiand/pymas.git
O bien, si prefieres clonarlo localmente:git clone https://github.com/rvcristiand/pymas.git
cd pymas
pip install .
cd ..
Paso 2: Ejecución del CódigoDescarga el archivo thermal_analysis.py y ejecútalo mediante Python:python thermal_analysis.py
3. Ejemplo de Uso (Usage Example)A continuación se presenta un ejemplo de integración para evaluar los efectos de un gradiente de temperatura estival ($\Delta T = +35^\circ\text{C}$) sobre una barra de acero de un puente con apoyos restringidos:from thermal_analysis import ThermalAnalysisTool

# 1. Inicializar la herramienta especificando las propiedades del material
# Acero: alpha = 1.2e-5 /°C, E = 200 GPa (200e9 Pa)
analizador = ThermalAnalysisTool(alpha=1.2e-5, E_pa=200e9)

# 2. Definir parámetros geométricos y térmicos del elemento
longitud_puente = 12.0      # metros
area_seccion = 0.015         # m^2
delta_temperatura = 35.0     # °C (calentamiento)

# 3. Ejecutar análisis térmico hiperestático con PyMAS
resultado = analizador.analyze_truss_thermal_expansion(
    length_m=longitud_puente,
    section_area_m2=area_seccion,
    delta_T_celsius=delta_temperatura
)

# 4. Mostrar resultados
print(f"Dilatación Libre: {resultado['free_expansion_mm']:.2f} mm")
print(f"Fuerza de Compresión Restringida: {resultado['thermal_force_N']/1000:.2f} kN")
print(f"Esfuerzo Térmico Inducido: {resultado['stress_MPa']:.2f} MPa")
4. Requisitos del SistemaPython 3.8 o superior.Paquete pymas instalado correctamente.
