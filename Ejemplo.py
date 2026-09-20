"""
Thermal Analysis Tool for Hyperstatic Structures using pymas
=============================================================
Aplicación para el cálculo de deformaciones, fuerzas nodales equivalentes 
y esfuerzos térmicos inducidos en estructuras analizadas con pymas.
"""

from pymas import Structure

class ThermalAnalysisTool:
    def __init__(self, alpha: float, E: float):
        """
        Inicializa la herramienta de análisis térmico.
        
        Parametros:
        -----------
        alpha : float
            Coeficiente de expansión térmica lineal (1/°C).
            Ejemplo: Acero = 1.2e-5, Concreto = 1.0e-5.
        E : float
            Módulo de elasticidad del material (kN/m² o Pa).
        """
        self.alpha = alpha
        self.E = E

    def calculate_free_expansion(self, L: float, delta_T: float) -> float:
        """Calcula el cambio no restringido de longitud (delta L = alpha * L * delta_T)."""
        return self.alpha * L * delta_T

    def calculate_thermal_stress(self, A: float, delta_T: float):
        """
        Calcula el esfuerzo de restricción y la fuerza axial térmica en un elemento fijo.
        
        Retorna:
        --------
        stress : float
            Esfuerzo térmico (misma unidad que E).
        axial_force : float
            Fuerza axial equivalente de restricción (N_th = E * A * alpha * delta_T).
        """
        stress = self.E * self.alpha * delta_T
        axial_force = stress * A
        return stress, axial_force


def run_thermal_simulation():
    print("=" * 60)
    print(" SIMULACIÓN DE CARGAS TÉRMICAS EN PÓRTICO RESTRINGIDO (pymas) ")
    print("=" * 60)

    # 1. Propiedades del Material y Geometría
    E_steel = 200e6      # Módulo de Young del acero (kN/m²)
    alpha_steel = 1.2e-5  # Coeficiente de dilatación térmica (1/°C)
    base = 0.3            # Ancho de la sección (m)
    height = 0.5          # Alto de la sección (m)
    Area = base * height  # Área (m²)
    L = 6.0               # Longitud de la viga (m)
    delta_T = 35.0        # Gradiente térmico (°C)

    # 2. Inicializar la herramienta de análisis térmico
    thermal_tool = ThermalAnalysisTool(alpha=alpha_steel, E=E_steel)

    # 3. Cálculo Teórico previo
    delta_L_free = thermal_tool.calculate_free_expansion(L, delta_T)
    stress_th, N_th = thermal_tool.calculate_thermal_stress(Area, delta_T)

    print(f"\n[1] PARAMETROS DE ENTRADA:")
    print(f"    - Longitud de la barra (L): {L:.2f} m")
    print(f"    - Sección transversal: {base}m x {height}m (Área = {Area:.4f} m²)")
    print(f"    - Variación de Temperatura (ΔT): +{delta_T:.1f} °C")
    print(f"    - Coeficiente α: {alpha_steel:.2e} 1/°C")

    print(f"\n[2] RESULTADOS TEÓRICOS DE RESTRICCIÓN TÉRMICA:")
    print(f"    - Dilatación térmica libre (sin apoyos): {delta_L_free * 1000:.3f} mm")
    print(f"    - Fuerza axial equivalente de compresión (N_th): {N_th:.2f} kN")
    print(f"    - Esfuerzo de compresión restringido (σ_th): {stress_th / 1000:.2f} MPa")

    # 4. Modelado con pymas (Método de Rigidez)
    model = Structure(type='plane_frame')

    # Agregar material y sección
    model.add_material('Steel', E_steel)
    model.add_rectangular_section('Rect_0.3x0.5', base=base, height=height)

    # Agregar nudos
    model.add_joint('1', x=0, y=0)
    model.add_joint('2', x=L, y=0)

    # Agregar elemento (viga)
    model.add_frame('beam1', '1', '2', 'Steel', 'Rect_0.3x0.5', axial=True, bending_z=True)

    # Agregar apoyos fijos (Restricción total para simular esfuerzo térmico)
    model.add_support('1', r_ux=True, r_uy=True, r_rz=True)
    model.add_support('2', r_ux=True, r_uy=True, r_rz=True)

    # Patron de carga térmica nodal equivalente
    model.add_load_pattern('Thermal_Load')
    # La expansión intenta empujar hacia los extremos, la restricción reacciona con empuje hacia adentro
    model.add_joint_point_load('Thermal_Load', '1', fx=+N_th, fy=0, rz=0)
    model.add_joint_point_load('Thermal_Load', '2', fx=-N_th, fy=0, rz=0)

    # Ejecutar análisis
    model.run_analysis()

    print(f"\n[3] RESULTADOS OBTENIDOS CON PYMAS:")
    print(f"    - Reacción axial en Apoyo 1 (Fx): {model.reactions['Thermal_Load']['1'].fx:+.2f} kN")
    print(f"    - Reacción axial en Apoyo 2 (Fx): {model.reactions['Thermal_Load']['2'].fx:+.2f} kN")
    print("=" * 60)


if __name__ == "__main__":
    run_thermal_simulation()
