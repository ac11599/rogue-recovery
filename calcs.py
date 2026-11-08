import math

LB_TO_KG = 0.45359237  # same factors as Excel CONVERT
FT_TO_M = 0.3048
G = 9.81  # m/s^2


def polygon_area_coef(n):
    return n / 4 * math.tan(math.pi / n)


# canopy area S = k * D^2, polygon D measured across the flats (Apogee Newsletter 149, figs. 5-6)
SHAPES = {
    "Circle": math.pi / 4,
    "Square": polygon_area_coef(4),
    "Hexagon": polygon_area_coef(6),
    "Octagon": polygon_area_coef(8),
}


def parachute_diameter_ft(mass_lb, rho, cd, descent_fps, shape="Circle"):
    m = mass_lb * LB_TO_KG
    v = descent_fps * FT_TO_M
    area = 2 * m * G / (rho * cd * v**2)
    return math.sqrt(area / SHAPES[shape]) / FT_TO_M


def descent_rate_fps(mass_lb, rho, cd, diameter_ft, shape="Circle"):
    m = mass_lb * LB_TO_KG
    area = SHAPES[shape] * (diameter_ft * FT_TO_M) ** 2
    return math.sqrt(2 * m * G / (rho * cd * area)) / FT_TO_M


def shock_cord_ft(rocket_length_in):
    return 3 * rocket_length_in / 12


# Ejection charges: imperial, with the spreadsheet's 454 g/lb and 12 in/ft factors
R_BP = 22.16  # ft-lbf / (lbm R), black powder combustion gas constant
T_BP = 3307  # R, combustion temperature
PYRODEX_PER_BP = 1.3  # g Pyrodex per g black powder
MUZZLE_9MM = 350  # ft-lb, sanity check


def section_area_in2(diameter_in):
    return math.pi * (diameter_in / 2) ** 2


def pyrodex_charge(diameter_in, length_in, desired_psi, n_pins, pin_force_lb, sf):
    area = section_area_in2(diameter_in)
    volume = area * length_in
    pins_psi = n_pins * pin_force_lb / area
    total_psi = desired_psi + pins_psi
    bp_g = total_psi * volume * 454 * sf / (R_BP * 12 * T_BP)
    return {
        "volume_in3": volume,
        "pins_psi": pins_psi,
        "total_psi": total_psi,
        "bp_g": bp_g,
        "pyrodex_g": bp_g * PYRODEX_PER_BP,
        "force_lb": total_psi * area,
        "energy_ftlb": total_psi * volume / 12,
    }


def pressure_from_pyrodex(diameter_in, length_in, pyrodex_g, sf):
    volume = section_area_in2(diameter_in) * length_in
    bp_g = pyrodex_g / PYRODEX_PER_BP
    return bp_g, bp_g * R_BP * T_BP * 12 / (volume * sf * 454)


if __name__ == "__main__":
    # slide 11 + parachute spreadsheet values
    assert math.isclose(parachute_diameter_ft(67, 1.225, 2.2, 24), 7.52756095, rel_tol=1e-8)
    assert math.isclose(descent_rate_fps(67, 1.225, 2.2, 8.913), 20.26943373, rel_tol=1e-8)
    assert math.isclose(parachute_diameter_ft(40, 1.225, 1.7, 45), 3.528844185, rel_tol=1e-8)
    assert math.isclose(descent_rate_fps(40, 1.225, 1.7, 3), 52.93266277, rel_tol=1e-8)
    # Apogee fig. 6 area factors
    assert math.isclose(SHAPES["Square"], 1.0)
    assert round(SHAPES["Hexagon"], 3) == 0.866
    assert round(SHAPES["Octagon"], 3) == 0.828
    for shape in SHAPES:  # the two modes invert each other for every shape
        d = parachute_diameter_ft(67, 1.225, 2.2, 24, shape)
        assert math.isclose(descent_rate_fps(67, 1.225, 2.2, d, shape), 24)
    assert shock_cord_ft(112) == 28

    # slide 18 + Pyrodex spreadsheet values
    r = pyrodex_charge(5, 7.5, 15, 2, 40, 1.5)
    expected = {"volume_in3": 147.2621556, "pins_psi": 4.074366543, "total_psi": 19.07436654, "bp_g": 2.175220023,
                "pyrodex_g": 2.82778603, "force_lb": 374.5243113, "energy_ftlb": 234.0776945}
    for key, value in expected.items():
        assert math.isclose(r[key], value, rel_tol=1e-8), key
    assert math.isclose(r["energy_ftlb"] / MUZZLE_9MM, 0.668793413, rel_tol=1e-8)
    bp, psi = pressure_from_pyrodex(5, 7.5, 13, 1.5)
    assert math.isclose(bp, 10) and math.isclose(psi, 87.68936632, rel_tol=1e-8)
    # RV sheet: primary at SF 1.5, backup at SF 2, main (29 in) and drogue (24 in) sections
    assert math.isclose(pyrodex_charge(4.98, 29, 15, 2, 40, 1.5)["pyrodex_g"], 10.86545529, rel_tol=1e-8)
    assert math.isclose(pyrodex_charge(4.98, 29, 15, 2, 40, 2)["pyrodex_g"], 14.48727372, rel_tol=1e-8)
    assert math.isclose(pyrodex_charge(4.98, 24, 15, 2, 40, 1.5)["pyrodex_g"], 8.992100928, rel_tol=1e-8)
    assert math.isclose(pyrodex_charge(4.98, 24, 15, 2, 40, 2)["pyrodex_g"], 11.98946790, rel_tol=1e-8)
    print("ok")
