import streamlit as st

from calcs import G, SHAPES, descent_rate_fps, parachute_diameter_ft, shock_cord_ft

st.title("Parachutes & Shock Cords")

st.header("Parachutes")
st.subheader("Calculator")
st.markdown("**Rocket & Parachute Properties**")
c1, c2, c3, c4 = st.columns(4, vertical_alignment="bottom")
mass_lb = c1.number_input("Rocket mass (lbs)", min_value=0.01, value=67.0, step=1.0)
rho = c2.number_input("Density of air (kg/m³)", min_value=0.001, value=1.225, step=0.001, format="%.3f",
                      help="Depends on altitude")
cd = c3.number_input("Coefficient of drag (estimated)", min_value=0.01, value=2.2, step=0.1,
                     help="Takes into account parachute shape and material")
shape = c4.selectbox("Parachute shape", list(SHAPES),
                     help="Polygon diameters are measured across the flats (Apogee Newsletter 149)")
st.caption(f"Constant: gravitational acceleration g = {G} m/s² · {shape} canopy area: S = {SHAPES[shape]:.3f}·D²")

size, rate = st.columns(2, border=True)
with size:
    st.markdown("**Parachute Sizing for a Desired Descent Rate**")
    v = st.number_input("Desired descent rate (ft/s)", min_value=0.01, value=24.0, step=1.0,
                        help="Targets: ~50 ft/s drogue, ~20 ft/s main")
    d = parachute_diameter_ft(mass_lb, rho, cd, v, shape)
    m1, m2 = st.columns(2)
    m1.metric("Diameter of parachute", f"{d:.2f} ft")
    m2.metric("Diameter of parachute", f"{d * 12:.1f} in")
with rate:
    st.markdown("**Descent Rate for a Given Parachute Diameter**")
    dia = st.number_input("Diameter of parachute (ft)", min_value=0.01, value=8.913, step=0.1, format="%.3f")
    st.metric("Descent rate", f"{descent_rate_fps(mass_lb, rho, cd, dia, shape):.2f} ft/s")

st.header("Shock Cords")
st.subheader("Shock Cord Length")
with st.columns(2)[0].container(border=True):
    st.markdown("**Shock Cord Length Calculator**")
    length_in = st.number_input("Length of rocket (in)", min_value=0.0, value=112.0, step=1.0)
    st.metric("Length of shock cord", f"{shock_cord_ft(length_in):.1f} ft")
