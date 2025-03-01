import streamlit as st
import pandas as pd
import math

# Add safety check for unit selection
def get_safe_unit_index(unit, units_list):
    try:
        return units_list.index(unit)
    except ValueError:
        return 0

# Set page configuration
st.set_page_config(
    page_title="Unit Converter Express",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: white;
        background-color: #2e7d32;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .category-button {
        background-color: #2e7d32;
        color: white;
        border-radius: 5px;
        padding: 0.5rem;
        text-align: center;
        cursor: pointer;
        margin: 0.25rem;
    }
    .converter-container {
        background-color: #f0f0f0;
        padding: 1.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .find-units-container {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .common-conversions {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .common-conversion-button {
        background-color: #f5f5f5;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin: 0.25rem;
        cursor: pointer;
        text-align: left;
        display: flex;
        justify-content: space-between;
    }
    .common-conversion-button:hover {
        background-color: #e0e0e0;
    }
    .arrow {
        color: #999;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="main-header">🔄 UnitConverters.net</div>', unsafe_allow_html=True)
st.markdown('<h2 style="margin-bottom: 2rem;">Unit Converter Express Version ⚡</h2>', unsafe_allow_html=True)

# Create tabs for different conversion categories
categories = [
    ("Length", "📏"), 
    ("Temp", "🌡️"), 
    ("Area", "📐"), 
    ("Volume", "🧊"), 
    ("Weight", "⚖️"), 
    ("Time", "⏰")
]
cols = st.columns(len(categories))
selected_category = st.session_state.get("selected_category", "Length")

for i, (category, emoji) in enumerate(categories):
    button_style = "background-color: #2e7d32; color: white;" if category == selected_category else "background-color: #e0e0e0; color: black;"
    if cols[i].button(f"{emoji} {category}", key=f"cat_{category}", use_container_width=True):
        selected_category = category
        st.session_state["selected_category"] = category

# Conversion dictionaries for each category
conversion_factors = {
    "Length": {
        "Meters": 1.0,
        "Kilometers": 1000.0,
        "Centimeters": 0.01,
        "Millimeters": 0.001,
        "Miles": 1609.34,
        "Yards": 0.9144,
        "Feet": 0.3048,
        "Inches": 0.0254,
    },
    "Weight": {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Metric Ton": 1000.0,
        "Pound": 0.453592,
        "Ounce": 0.0283495,
        "Stone": 6.35029,
    },
    "Volume": {
        "Cubic Meter": 1.0,
        "Cubic Centimeter": 0.000001,
        "Liter": 0.001,
        "Milliliter": 0.000001,
        "Gallon (US)": 0.00378541,
        "Quart (US)": 0.000946353,
        "Pint (US)": 0.000473176,
        "Cup (US)": 0.000236588,
        "Fluid Ounce (US)": 0.0000295735,
    },
    "Area": {
        "Square Meter": 1.0,
        "Square Kilometer": 1000000.0,
        "Square Centimeter": 0.0001,
        "Square Millimeter": 0.000001,
        "Square Mile": 2589988.11,
        "Acre": 4046.86,
        "Square Yard": 0.836127,
        "Square Foot": 0.092903,
        "Square Inch": 0.00064516,
    },
    "Time": {
        "Second": 1.0,
        "Millisecond": 0.001,
        "Microsecond": 0.000001,
        "Minute": 60.0,
        "Hour": 3600.0,
        "Day": 86400.0,
        "Week": 604800.0,
        "Month": 2592000.0,
        "Year": 31536000.0,
    },
    "Temp": {
        "Celsius": "C",
        "Fahrenheit": "F",
        "Kelvin": "K",
    }
}

# Function to convert temperatures
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    
    # Convert to Celsius first
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    
    # Convert from Celsius to target unit
    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15

# Function to convert units
def convert_unit(value, from_unit, to_unit, category):
    try:
        # Validate input for non-temperature categories
        if category != "Temp" and value < 0:
            st.error("Negative values are not allowed for this category")
            return None
            
        if category == "Temp":
            return convert_temperature(value, from_unit, to_unit)
        else:
            if from_unit == to_unit:
                return value
            # Convert to base unit first, then to target unit
            base_value = value * conversion_factors[category][from_unit]
            return base_value / conversion_factors[category][to_unit]
    except Exception as e:
        st.error(f"An error occurred during conversion: {str(e)}")
        return None

# Main conversion form
st.markdown('<div class="converter-container">', unsafe_allow_html=True)

units = list(conversion_factors[selected_category].keys())

# Initialize default values in session state if not exists
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Length"
    st.session_state.default_from_unit = units[0]
    st.session_state.default_to_unit = units[1]

# Reset default units when category changes
if "previous_category" not in st.session_state or st.session_state.previous_category != selected_category:
    st.session_state.default_from_unit = units[0]
    st.session_state.default_to_unit = units[1]
    st.session_state.previous_category = selected_category

# Create conversion form
amount = st.number_input("Amount:", value=1.0, format="%.6f", key="amount_input")

# Use safe index selection
from_unit_index = get_safe_unit_index(st.session_state.default_from_unit, units)
to_unit_index = get_safe_unit_index(st.session_state.default_to_unit, units)

from_unit = st.selectbox("From:", units, index=from_unit_index, key="from_unit")
to_unit = st.selectbox("To:", units, index=to_unit_index, key="to_unit")

# Add decimal places selection
decimal_places = st.slider("Decimal places in result:", 0, 10, 6)

# Calculate and display result
if st.button("Convert 🔄", key="convert_button"):
    result = convert_unit(amount, from_unit, to_unit, selected_category)
    if result is not None:
        st.success(f"✨ {amount} {from_unit} = {result:.{decimal_places}f} {to_unit} ✨")

st.markdown('</div>', unsafe_allow_html=True)

# Common conversions section
st.markdown('<h3>🔥 Common Conversions</h3>', unsafe_allow_html=True)
st.markdown('<div class="common-conversions">', unsafe_allow_html=True)

# Update common conversions with emojis
common_conversions = [
    # Length conversions
    ("📏 Meters to Feet", "Meters", "Feet", "Length"),
    ("📏 Feet to Meters", "Feet", "Meters", "Length"),
    ("📏 Centimeters to Inches", "Centimeters", "Inches", "Length"),
    ("📏 Inches to Centimeters", "Inches", "Centimeters", "Length"),
    ("📏 Kilometers to Miles", "Kilometers", "Miles", "Length"),
    ("📏 Miles to Kilometers", "Miles", "Kilometers", "Length"),
    
    # Weight conversions
    ("⚖️ kg to lbs", "Kilogram", "Pound", "Weight"),
    ("⚖️ lbs to kg", "Pound", "Kilogram", "Weight"),
    ("⚖️ g to oz", "Gram", "Ounce", "Weight"),
    ("⚖️ oz to g", "Ounce", "Gram", "Weight"),
    
    # Volume conversions
    ("🧊 Liters to Gallons", "Liter", "Gallon (US)", "Volume"),
    ("🧊 Gallons to Liters", "Gallon (US)", "Liter", "Volume"),
    ("🧊 ml to fl oz", "Milliliter", "Fluid Ounce (US)", "Volume"),
    ("🧊 fl oz to ml", "Fluid Ounce (US)", "Milliliter", "Volume"),
    
    # Area conversions
    ("📐 sq m to sq ft", "Square Meter", "Square Foot", "Area"),
    ("📐 sq ft to sq m", "Square Foot", "Square Meter", "Area"),
    ("📐 acres to hectares", "Acre", "Square Meter", "Area"),
    ("📐 hectares to acres", "Square Meter", "Acre", "Area"),
    
    # Temperature conversions
    ("🌡️ Celsius to Fahrenheit", "Celsius", "Fahrenheit", "Temp"),
    ("🌡️ Fahrenheit to Celsius", "Fahrenheit", "Celsius", "Temp"),
    ("🌡️ Celsius to Kelvin", "Celsius", "Kelvin", "Temp"),
    ("🌡️ Kelvin to Celsius", "Kelvin", "Celsius", "Temp"),
    
    # Time conversions
    ("⏰ Hours to Minutes", "Hour", "Minute", "Time"),
    ("⏰ Minutes to Hours", "Minute", "Hour", "Time"),
    ("⏰ Days to Hours", "Day", "Hour", "Time"),
    ("⏰ Hours to Days", "Hour", "Day", "Time")
]

# Create a grid layout for common conversions
cols_per_row = 2
rows = len(common_conversions) // cols_per_row + (len(common_conversions) % cols_per_row > 0)

for row in range(rows):
    cols = st.columns(cols_per_row)
    for col in range(cols_per_row):
        idx = row * cols_per_row + col
        if idx < len(common_conversions):
            conv = common_conversions[idx]
            with cols[col]:
                if st.button(f"{conv[0]} →", key=f"common_{idx}", use_container_width=True):
                    st.session_state.selected_category = conv[3]
                    st.session_state.default_from_unit = conv[1]
                    st.session_state.default_to_unit = conv[2]
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #666;">
    © 2025 UnitConverters.net 🚀 - A simple unit conversion tool
</div>
""", unsafe_allow_html=True)
