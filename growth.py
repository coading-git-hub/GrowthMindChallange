import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title = "Data Sweeper",layout='wide')

#custom css

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

#title and description 
st.title("🎇 Datasweeper Sterling Integrator By Kiran Ahmed")
st.write("Transform your files between CSV and Excel formates with built-in data cleaning and visualization Creating the project for quarter 3!")

#file uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):",type=["cvs","xlsx"],accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext =os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type:{file_ext}")
            continue

        #file detail
        st.write("🔍 Preview the head of the Dataframe")
        st.dataframe(df.head())

        #data cleaning option
        st.subheader("🛠 Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✔ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numaric_cols = df.select_dtypes(include=['number']).columns
                    df[numaric_cols]= df[numaric_cols].fillna(df[numaric_cols].mean())  
                    st.write("✔ Missing values have been filled!")
        st.subheader("🎯 Select Columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualizaition for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #Conversion Options 

        st.subheader("🌀 Conversion Options")
        conversion_type =st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, "csv")
                mime_type ="text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformates-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
st.success("🎉 All fileds processed successfully!")                                                     