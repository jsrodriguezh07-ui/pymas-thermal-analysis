"""
Módulo de Análisis Estructural bajo Cargas Térmicas y Gradientes de Temperatura
Basado en la librería pymas (Direct Stiffness Method).

Aplicación de Ingeniería Civil:
Evaluación de esfuerzos térmicos e hiperestáticos inducidos por variaciones de 
temperatura (expansión/contracción restringida) en estructuras continuas y pórticos.
"""

from pymas import Structure

class ThermalAnalysisTool:
    def __init__(self, alpha=1.2e-5, E_pa=200e9):
        """
        Inicializa la herramienta de análisis térmico.
        
        :param alpha: Coeficiente de expansión térmica del material (1/°C).
                      Por defecto: 1.2e-5 /°C (Acero/Concreto).
        :param E_pa: Módulo de elasticidad del material en Pascales (Pa).
                     Por defecto: 200 GPa (Acero de estructural).
        """
        self.alpha = alpha
        self.E = E_pa

    def calculate_equivalent_thermal_force(self, area_m2, delta_T_celsius):
        """
        Calcula la fuerza axial equivalente restricta debida a un cambio de temperatura.
        Fuerza Térmica N_th = E * A * alpha * delta_T
        
        :param area_m2: Área de la sección transversal (m²).
        :param delta_T_celsius: Cambio de temperatura (°C). Positivo = Calentamiento, Negativo = Enfriamiento.
        :return: Fuerza axial equivalente en Newtons (N).
        """
        return self.E * area_m2 * self.alpha * delta_T_celsius

    def analyze_truss_thermal_expansion(self, length_m, section_area_m2, delta_T_celsius):
        """
        Evalúa el esfuerzo y reacción de una barra hiperestática fija en ambos extremos
        sometida a una variación de temperatura ΔT.
        """
        # Creación del modelo estático en PyMAS
        model = Structure(type='space_frame')

        # 1. Definición de sección
        section_name = "thermal_sec"
        # Asumiendo sección circular equivalente para pymas
        import math
        r = math.sqrt(section_area_m2 / math.pi)
        model.add_section(section_name, A=section_area_m2, Iy=1e-5, Iz=1e-5, J=2e-5)

        # 2. Definición de nudos (Barra restringida entre X=0 y X=length_m)
        model.add_node("N1", x=0.0, y=0.0, z=0.0)
        model.add_node("N2", x=length_m, y=0.0, z=0.0)

        # 3. Apoyos empotrados en ambos extremos para restringir la expansión libre
        model.add_support("N1", ux=True, uy=True, uz=True, rx=True, ry=True, rz=True)
        model.add_support("N2", ux=True, uy=True, uz=True, rx=True, ry=True, rz=True)

        # 4. Elemento estructural
        model.add_element("E1", node_i="N1", node_j="N2", section=section_name, E=self.E)

        # 5. Cálculo de la carga térmica equivalente en los nudos
        # La dilatación impone una fuerza axial estáticamente equivalente N = E * A * alpha * ΔT
        N_thermal = self.calculate_equivalent_thermal_force(section_area_m2, delta_T_celsius)
        
        # Se aplican cargas puntuales equivalentes en los nudos opuestas a la expansión
        # Si ΔT > 0 (Calentamiento), el elemento intenta empujar hacia afuera a los nudos
        model.add_nodal_load("N1", fx=-N_thermal)
        model.add_nodal_load("N2", fx=N_thermal)

        # 6. Resolución del sistema matricial
        model.run_analysis()

        # Esfuerzo compresión / tracción (sigma = N / A)
        stress_pa = N_thermal / section_area_m2

        return {
            "delta_T": delta_T_celsius,
            "thermal_force_N": N_thermal,
            "stress_MPa": stress_pa / 1e6,
            "free_expansion_mm": (self.alpha * delta_T_celsius * length_m) * 1000
        }


if __name__ == "__main__":
    # Ejemplo de Aplicación en Ingeniería Civil:
    # Evaluación de una viga/trabe metálica rígida de un puente de 12 metros
    # Expuesta a un incremento de temperatura estival de ΔT = +35 °C.

    print("=================================================================")
    print(" ANÁLISIS DE ESFUERZOS TÉRMICOS EN ESTRUCTURAS RESTRINGIDAS ")
    print("=================================================================\n")

    analizador = ThermalAnalysisTool(alpha=1.2e-5, E_pa=200e9) # Acero estructural

    longitud = 12.0  # metros
    area_seccion = 0.015  # 150 cm2 = 0.015 m2
    variacion_temp = 35.0  # +35 grados Celsius

    resultado = analizador.analyze_truss_thermal_expansion(
        length_m=longitud,
        section_area_m2=area_seccion,
        delta_T_celsius=variacion_temp
    )

    print(f"Parámetros de Entrada:")
    print(f" - Longitud del elemento: {longitud} m")
    print(f" - Área transversal: {area_seccion} m²")
    print(f" - Gradiente térmico (ΔT): +{variacion_temp} °C\n")

    print(f"Resultados del Análisis con PyMAS:")
    print(f" - Expansión libre (sin restricciones): {resultado['free_expansion_mm']:.2f} mm")
    print(f" - Fuerza Axial de Restricción Requerida: {resultado['thermal_force_N'] / 1000:.2f} kN")
    print(f" - Esfuerzo Térmico Inducido: {resultado['stress_MPa']:.2f} MPa")
    
    if resultado['stress_MPa'] > 0:
        print(" -> La estructura se encuentra bajo ESFUERZO DE COMPRESIÓN TÉRMICA.")
