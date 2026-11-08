import streamlit as st

st.title("Rogue Aerospace Recovery")
st.caption("Presented by Dynamics Subteam (Alberto Chen, Vadim Hettena, Adithya Renjit) · 2026-2027 Academic Year")
st.markdown("[View the slides](https://docs.google.com/presentation/d/1nDDsDf0I3p07p0JZrgIZk2pAGAZvDE4uSH_vPD59ysw/edit?usp=sharing)")

st.header("Recovery Overview")

st.subheader("Recovery Stages")
st.image("assets/recovery_stages.png", width=600)

drogue, main = st.columns(2, border=True)
drogue.subheader("Drogue Deployment")
drogue.markdown(
    "- **Deploys at apogee**\n"
    "- **Target Speed:** ~50 feet/second\n"
    "- **Purpose:** Slows down rocket before main deployment and minimizes drift\n\n"
    "**Note:** Typically, smaller rockets will not use a drogue parachute"
)
main.subheader("Main Deployment")
main.markdown(
    "- **Deploys at ~1000 feet**\n"
    "- **Target Speed:** ~20 feet/second\n"
    "- **Purpose:** Slows down rocket for a safe, damage-free landing"
)

st.subheader("Recovery Method (Ejection Charges)")
st.markdown(
    "An ejection charge creates a sudden burst of gas pressure to separate rocket parts\n\n"
    "**How the Process Works:**\n"
    "1. Ejection charge is ignited\n"
    "2. The airframe is pressurized and a large volume of high-pressure hot gas is generated\n"
    "3. Pressure builds until the shear pins holding the rocket sections together break\n"
    "4. Recovery system is released"
)

st.subheader("Recovery System Diagram")
# ponytail: widths roughly match the CAD render on slide 7; no images by request
for col, label in zip(st.columns([3, 1.3, 1.6], border=True), ["Main Compartment", "Avionics Bay", "Drogue Compartment"]):
    col.markdown(f"**{label}**")

st.subheader("System Overview")
st.markdown(
    "**Bulkhead ➔ U-bolt ➔ Fire Blanket ➔ Swivel ➔ Shock Cord ➔ Swivel ➔ Parachute ➔ "
    "Shock Cord (continued) ➔ Swivel ➔ U-bolt ➔ Bulkhead**"
)

st.header("External Links")
st.markdown(
    "- https://apogeerockets.com/education/downloads/Newsletter149.pdf\n"
    "- https://www.youtube.com/watch?v=xV18hs8FwPg\n"
    "- https://www.arsabq.org/ejection.htm\n"
    "- https://www.space-rockets.com/pyrodex/"
)
