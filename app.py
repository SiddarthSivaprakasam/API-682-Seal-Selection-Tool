import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="API 682 Seal Selector",
    page_icon="🔰",
    layout="wide"
)

# Constants
CATEGORY_LIMITS = {
    1: {"pressure": 20, "temp": 260, "speed": 20},
    2: {"pressure": 40, "temp": 400, "speed": 25},
    3: {"pressure": 100, "temp": 400, "speed": 25}
}

# --- API 682 Selection Logic ---
def get_seal_category(pressure, temperature, speed):
    """Determine seal category based on operating conditions (Sheet 1 & 2)"""
    for cat in [1, 2, 3]:
        if (pressure <= CATEGORY_LIMITS[cat]["pressure"] and
            temperature <= CATEGORY_LIMITS[cat]["temp"] and
            speed <= CATEGORY_LIMITS[cat]["speed"]):
            return cat
    return None

def get_fluid_type_group(fluid_type, is_flashing):
    """Categorize fluid type (Sheet 1)"""
    if fluid_type == "Hydrocarbon":
        return "Flashing Hydrocarbon" if is_flashing else "Nonflashing Hydrocarbon"
    return "Nonhydrocarbon"

def get_seal_type(fluid_group, temp, pressure, category, contaminants):
    """Determine seal type based on fluid properties (Sheets 3, 4, 5)"""
    # Nonhydrocarbon logic (Sheet 3)
    if fluid_group == "Nonhydrocarbon":
        if temp < 80:
            return "Type B" if pressure < 20 else "Engineered System"
        else:
            return "Engineered System"
    
    # Hydrocarbon logic
    elif "Hydrocarbon" in fluid_group:
        # Nonflashing (Sheet 4)
        if "Nonflashing" in fluid_group:
            if temp < 176:
                return "Type A" if pressure < 20 else "Type C"
            elif temp < 280:
                return "Type C" if pressure < 20 else "Engineered System"
            else:
                return "Engineered System"
        
        # Flashing (Sheet 5)
        else:
            if temp < 176:
                return "Type A" if pressure < 20 else "Type C"
            elif temp < 260:
                return "Type C" if pressure < 20 else "Engineered System"
            else:
                return "Engineered System"
    
    return "Type A"  # Default

def get_arrangement(fluid_group, exposure_hazard, vapor_risk, 
                   environmental_limits, solids, polymerizing, 
                   poor_lubricity, low_density, high_vapor_pressure,
                   temp, zero_leakage, mandated_arrangement=None):
    """Determine seal arrangement (Sheets 6-9)"""
    # Override with mandates
    if mandated_arrangement:
        return mandated_arrangement
    
    # Special cases
    if fluid_group == "Nonhydrocarbon" and any(contaminants.values()):
        return 3
    
    # Arrangement 3 conditions (Sheet 6)
    if (zero_leakage or 
        exposure_hazard or 
        vapor_risk or 
        environmental_limits or
        temp > 260 or
        solids or
        polymerizing or
        poor_lubricity or
        low_density or
        high_vapor_pressure):
        return 3
    
    # Arrangement 2 conditions
    if any([solids, polymerizing, poor_lubricity, low_density, high_vapor_pressure]):
        return 2
    
    return 1  # Default to Arrangement 1

def get_barrier_fluid_recommendation(fluid_type, temp_range):
    """Recommend barrier fluid (Sheet 10)"""
    if "Hydrocarbon" in fluid_type:
        if temp_range == "Low":
            return "Mineral oil (2-10 cSt at operating temp)"
        elif temp_range == "Medium":
            return "Paraffin-based high purity oil"
        else:  # High temp
            return "Synthetic-based oil"
    else:  # Nonhydrocarbon
        return "Water/ethylene glycol mixture (commercial antifreeze prohibited)"

# Streamlit App
st.title("🔰 API 682 4th Edition Seal Selector")
st.markdown("""
*Mechanical seal selection according to API 682 4th Edition (Sheets 1-10)*  
Configure parameters below to determine recommended seal configuration.
""")

# Section 1: Operating Conditions
with st.expander("📋 Operating Conditions (Sheet 1 & 2)", expanded=True):
    col1, col2, col3 = st.columns(3)
    pressure = col1.number_input("Seal Chamber Pressure (bar g)", 
                                min_value=0.0, max_value=200.0, value=15.0, step=0.5)
    temperature = col2.number_input("Temperature (°C)", 
                                   min_value=-50.0, max_value=500.0, value=100.0, step=1.0)
    speed = col3.number_input("Shaft Speed (m/s)", 
                             min_value=0.0, max_value=50.0, value=10.0, step=0.5)

# Section 2: Fluid Properties
with st.expander("🧪 Fluid Properties (Sheets 3-5)", expanded=True):
    col1, col2 = st.columns(2)
    fluid_type = col1.selectbox("Fluid Type", 
                               ["Hydrocarbon", "Nonhydrocarbon"], index=0)
    is_flashing = col2.checkbox("Flashing Fluid")
    
    st.caption("Fluid Characteristics:")
    col1, col2, col3 = st.columns(3)
    hazardous = col1.checkbox("Hazardous")
    toxic = col1.checkbox("Toxic")
    flammable = col2.checkbox("Flammable")
    abrasive = col2.checkbox("Abrasive/Solids")
    polymerizing = col3.checkbox("Polymerizing")
    poor_lubricity = col3.checkbox("Poor Lubricity")
    
    st.caption("Contaminants:")
    col1, col2 = st.columns(2)
    caustic = col1.checkbox("Caustic")
    h2s = col1.checkbox("H₂S")
    amines = col2.checkbox("Amines")
    ammonia = col2.checkbox("Ammonia")

# Section 3: Environmental & Safety
with st.expander("🌍 Environmental & Safety (Sheet 6)", expanded=True):
    col1, col2 = st.columns(2)
    exposure_hazard = col1.checkbox("Personnel Exposure Hazard")
    vapor_risk = col1.checkbox("Vapor Cloud Risk")
    environmental_limits = col2.checkbox("Environmental Emission Limits")
    monitoring_required = col2.checkbox("Leakage Monitoring Required")
    zero_leakage = st.checkbox("Zero Emission Requirement")
    
    col1, col2 = st.columns(2)
    low_density = col1.checkbox("Relative Density < 0.4")
    high_vapor_pressure = col1.checkbox("Vapor Pressure > 0.414 kPa at 38°C")
    mandated_arrangement = col2.selectbox("Mandated Arrangement", 
                                         [None, "Arrangement 1", "Arrangement 2", "Arrangement 3"], 
                                         index=0)

# Get recommendations
category = get_seal_category(pressure, temperature, speed)
fluid_group = get_fluid_type_group(fluid_type, is_flashing)
contaminants = {
    "caustic": caustic, "h2s": h2s, "amines": amines, 
    "ammonia": ammonia, "abrasive": abrasive
}
seal_type = get_seal_type(
    fluid_group, temperature, pressure, category, contaminants
)
arrangement = get_arrangement(
    fluid_group, exposure_hazard, vapor_risk, environmental_limits,
    abrasive, polymerizing, poor_lubricity, low_density, high_vapor_pressure,
    temperature, zero_leakage, mandated_arrangement
)

# Determine temperature range for barrier fluid
temp_range = "Low" if temperature < 70 else "Medium" if temperature < 150 else "High"
barrier_fluid = get_barrier_fluid_recommendation(fluid_type, temp_range) if arrangement in [2, 3] else "Not required"

# Display Results
st.divider()
st.subheader("Seal Recommendation")

if category:
    cat_desc = {
        1: "General Service Conditions",
        2: "Severe Service Conditions",
        3: "Extreme Service Conditions"
    }.get(category)
    
    arr_desc = {
        1: "Single Seal (Arrangement 1)",
        2: "Tandem Seals (Arrangement 2)",
        3: "Double Seals (Arrangement 3)"
    }.get(arrangement)
    
    st.success(f"*Category {category}*: {cat_desc}")
    st.success(f"*Seal Type*: {seal_type}")
    st.success(f"*{arr_desc}*")
    
    if arrangement in [2, 3]:
        st.info(f"*Barrier/Buffer Fluid*: {barrier_fluid}")
    
    # Additional guidance
    with st.expander("📖 Standard Requirements", expanded=True):
        st.markdown(f"""
        ### Category {category} Requirements (Sheet 2)
        - *Max Pressure*: {CATEGORY_LIMITS[category]['pressure']} bar g
        - *Max Temperature*: {CATEGORY_LIMITS[category]['temp']} °C
        - *Max Speed*: {CATEGORY_LIMITS[category]['speed']} m/s
        
        ### {seal_type} Seal Features:
        {"- Elastomer secondary seals" if seal_type == "Type A" else ""}
        {"- Bellows design" if seal_type in ["Type B", "Type C"] else ""}
        {"- Engineered solution required" if seal_type == "Engineered System" else ""}
        
        ### Arrangement {arrangement} Requirements:
        {"- No auxiliary system required" if arrangement == 1 else ""}
        {"- Buffer fluid system recommended" if arrangement == 2 else ""}
        {"- Barrier fluid system required" if arrangement == 3 else ""}
        {"- Zero process leakage to atmosphere" if arrangement == 3 else ""}
        """)
        
        if arrangement == 3:
            st.markdown("""
            *Barrier Fluid Requirements (Sheet 10):*
            - Viscosity < 500 cSt at minimum temperature
            - Initial boiling point > service temp + 28°C
            - Flash point > service temperature (if oxygen present)
            - Must not freeze at minimum ambient temperature
            """)
else:
    st.error("Operating conditions exceed API 682 scope. Consult Sheet 10 for special designs")

# Footer
st.divider()
st.caption("© API 682 4th Edition Seal Selection Tool | Refer to API Standard 682 for complete requirements")