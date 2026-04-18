import streamlit as st
import pandas as pd
import os

# --- UPDATED DYNAMIC PATHING ---
# current_dir points to /Users/user/Desktop/Market_basket/src
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up to 'Market_basket', then into 'data/raw/groceries.csv'
csv_path = os.path.join(current_dir, "..", "data", "raw", "groceries.csv")

# Load the model results
@st.cache_data
def load_data():
    if not os.path.exists(csv_path):
        st.error(f"❌ File not found at: {csv_path}")
        return pd.DataFrame()

    # Load the rules (ensure you saved the 'rules' dataframe to this path earlier)
    df = pd.read_csv(csv_path)
    
    # Cleaning string sets back into lists for the recommendations
    df['antecedents'] = df['antecedents'].apply(lambda x: x.strip("{}").replace("'", "").split(", "))
    df['consequents'] = df['consequents'].apply(lambda x: x.strip("{}").replace("'", "").split(", "))
    return df