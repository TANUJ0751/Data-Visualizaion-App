import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title("Beautiful CSV Data Visualizer")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded file
    data = pd.read_csv(uploaded_file)
    
    # Display the first few rows of the dataset
    st.header("Dataset Overview")
    st.write(data.head())
    
    # Display basic statistics
    st.header("Statistical Summary")
    st.write(data.describe())
    
    # Visualizations
    st.header("Data Visualizations")
    
    # Column selection for visualization
    columns_to_visualize = st.multiselect("Select columns to visualize", options=data.columns)
    
    # Generate visualizations for selected columns
    for col in columns_to_visualize:
        if data[col].dtype in ["float64", "int64"]:
            # Histogram with Plotly
            st.subheader(f"Histogram for {col}")
            fig = px.histogram(data, x=col, nbins=30, title=f"Distribution of {col}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Boxplot with Plotly
            st.subheader(f"Boxplot for {col}")
            fig = px.box(data, y=col, title=f"Boxplot of {col}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif data[col].dtype == "object":
            # Bar chart for categorical data
            st.subheader(f"Bar Chart for {col}")
            fig = px.bar(data[col].value_counts().reset_index(),
                         x='index', y=col, title=f"Count of {col}")
            st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    st.header("Correlation Heatmap")
    numerical_cols = data.select_dtypes(include=["float64", "int64"]).columns
    if len(numerical_cols) > 1:
        corr = data[numerical_cols].corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis",
                        title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please upload a CSV file to proceed.")

