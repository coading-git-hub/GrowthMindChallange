import streamlit as st
import pandas as pd
import os
from io import BytesIO
import json
import plotly
import plotly.express as px
import google.generativeai as genai
from streamlit_chat import message

# Page Configuration
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp{
    background-color:black;
    color:white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("🎇 Datasweeper Sterling Integrator By Kiran Ahmed")
st.write("Transform your files between CSV, Excel, and JSON formats with built-in data cleaning and visualization!")

# Gemini Setup
genai.configure(api_key="AIzaSyBrv7QpiLUyzw4k_E9kdFbY3IMEcjQv1Wc")
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize chat history and data storage
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_data" not in st.session_state:
    st.session_state.current_data = None

# Sidebar Chatbot
st.sidebar.subheader("💬 Gemini Assistant")

# Add clear all button with a unique key
if st.sidebar.button("🗑️ Clear Chat History", key="clear_chat"):
    st.session_state.messages = []
    st.session_state.current_data = None  # Also clear current data
    st.rerun()  # Force refresh the page

# Existing chat input
user_input = st.sidebar.text_input("Ask something:")

# Modify the chat message display section
def create_message_container():
    for idx, msg in enumerate(st.session_state.messages):
        message(
            msg["content"], 
            is_user=(msg["role"] == "user"),
            key=f"msg_{idx}"
        )

# Update the chat processing section
if user_input:
    try:
        # Add new user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if st.session_state.current_data is not None:
            df = st.session_state.current_data
            data_info = f"""
            You are analyzing a file with the following information:
            - File contains {len(df)} rows and {len(df.columns)} columns
            - Column names: {', '.join(df.columns.tolist())}
            - Data sample: 
            {df.head(3).to_string()}
            
            Please provide a specific answer about this data for the following question:
            {user_input}
            """
        else:
            data_info = "No file has been uploaded yet. Please upload a file first to analyze it."
        
        # Generate and add new response
        response = model.generate_content(data_info)
        bot_reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    except Exception as e:
        st.error(f"Error in chat completion: {str(e)}")

# Display messages
create_message_container()

# Main File Processing
uploaded_files = st.file_uploader(
    "Upload your files (CSV, Excel, or JSON):", 
    type=["csv", "xlsx", "json"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # File Reading
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            elif file_ext == ".json":
                df = pd.read_json(file)
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
                
            # Store the current dataframe in session state
            st.session_state.current_data = df
            
            # File Preview
            st.write("🔍 Preview the head of the Dataframe")
            st.dataframe(df.head())

            # Data Cleaning Options
            st.subheader("🛠 Data Cleaning Options")
            if st.checkbox(f"Clean data for {file.name}"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(f"Remove duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("✔ Duplicates removed!")

                with col2:
                    if st.button(f"Fill missing values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        categorical_cols = df.select_dtypes(include=['object']).columns
                        df[categorical_cols] = df[categorical_cols].fillna('Unknown')
                        st.write("✔ Missing values filled!")

                with col3:
                    if st.button(f"Rename Columns for {file.name}"):
                        new_cols = {col: st.text_input(f"Rename {col}", col) for col in df.columns}
                        df.rename(columns=new_cols, inplace=True)
                        st.write("✔ Columns renamed!")

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show visualization for {file.name}"):
                chart_type = st.selectbox("Select chart type:", ["Bar Chart", "Pie Chart", "Histogram"])
                
                # Allow selection from all columns
                if chart_type == "Bar Chart":
                    x_col = st.selectbox("Select Column for Bar Chart", df.columns)
                    try:
                        fig = px.bar(df, x=x_col, title=f"Bar Chart of {x_col}")
                        st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"Could not create bar chart: {str(e)}")
                
                elif chart_type == "Pie Chart":
                    name_col = st.selectbox("Select Column for Pie Chart", df.columns)
                    try:
                        # Count values for categorical data
                        value_counts = df[name_col].value_counts()
                        fig = px.pie(values=value_counts.values, names=value_counts.index, title=f"Pie Chart of {name_col}")
                        st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"Could not create pie chart: {str(e)}")
                
                elif chart_type == "Histogram":
                    hist_col = st.selectbox("Select Column for Histogram", df.columns)
                    try:
                        fig = px.histogram(df, x=hist_col, title=f"Histogram of {hist_col}")
                        st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"Could not create histogram: {str(e)}")

            # Conversion Options
            st.subheader("🌀 Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel", "JSON"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif conversion_type == "JSON":
                    buffer.write(df.to_json(indent=4).encode())
                    file_name = file.name.replace(file_ext, ".json")
                    mime_type = "application/json"
                
                buffer.seek(0)
                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")

    st.success("🎉 All files processed successfully!")
