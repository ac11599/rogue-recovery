import streamlit as st

from calcs import (MUZZLE_9MM, PYRODEX_PER_BP, R_BP, T_BP, pressure_from_pyrodex, pyrodex_charge,
                   section_area_in2)

st.title("Ejection Charges")

st.subheader("Calculator")
st.markdown("**Setup**")
c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
dia = c1.number_input("Internal diameter (in)", min_value=0.01, value=5.0, step=0.1)
length = c2.number_input("Section length (in)", min_value=0.01, value=7.5, step=0.5)
sf = c3.number_input("Safety factor", min_value=0.01, value=1.5, step=0.1,
                     help="Charge mass is multiplied by the safety factor")
st.caption(
    f"Internal volume V = {section_area_in2(dia) * length:.2f} in³ · "
    f"Black powder constants: R = {R_BP} ft·lbf/(lbm·°R), T = {T_BP} °R · "
    f"Black powder : Pyrodex = 1 : {PYRODEX_PER_BP} by mass"
)

mass_card, pressure_card = st.columns(2, border=True)
with mass_card:
    st.markdown("**Mass of Pyrodex for a Desired Ejection Pressure**")
    a, b, c = st.columns(3, vertical_alignment="bottom")
    desired = a.number_input("Desired pressure (psi)", min_value=0.0, value=15.0, step=1.0,
                             help="Pressure required to split the rocket without any shear pins")
    pins = b.number_input("# of shear pins", min_value=0, value=2, step=1)
    pin_force = c.number_input("Single pin shear force (lbs)", min_value=0.0, value=40.0, step=1.0)
    r = pyrodex_charge(dia, length, desired, pins, pin_force, sf)
    m1, m2, m3 = st.columns(3)
    m1.metric("Mass of Pyrodex", f"{r['pyrodex_g']:.2f} g")
    m2.metric("Ejection force", f"{r['force_lb']:.1f} lbs")
    m3.metric("Charge energy", f"{r['energy_ftlb']:.1f} ft·lb")
    st.caption(
        f"Pressure to break shear pins: {r['pins_psi']:.2f} psi  \n"
        f"Total pressure required: {r['total_psi']:.2f} psi  \n"
        f"Mass of black powder: {r['bp_g']:.2f} g  \n"
        f"Sanity check: {r['energy_ftlb'] / MUZZLE_9MM:.2f}× a 9mm bullet's muzzle energy ({MUZZLE_9MM} ft·lb)"
    )
    b1, b2 = st.columns(2, vertical_alignment="bottom")
    backup_sf = b1.number_input("Backup safety factor", min_value=0.01, value=2.0, step=0.1,
                                help="Backup charge is the same calculation at a higher safety factor (RV sheet uses 2)")
    backup = pyrodex_charge(dia, length, desired, pins, pin_force, backup_sf)
    b2.metric("Backup charge Pyrodex", f"{backup['pyrodex_g']:.2f} g")
with pressure_card:
    st.markdown("**Pressure Generated for a Given Mass of Pyrodex**")
    pyro = st.number_input("Mass of Pyrodex powder (g)", min_value=0.0, value=13.0, step=0.1)
    bp, psi = pressure_from_pyrodex(dia, length, pyro, sf)
    m1, m2 = st.columns(2)
    m1.metric("Equivalent mass of black powder", f"{bp:.2f} g")
    m2.metric("Pressure generated", f"{psi:.2f} psi")
