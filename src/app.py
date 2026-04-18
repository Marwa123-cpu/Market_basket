import streamlit as st
import pandas as pd
import os

# 1. Setup the dynamic path
# This gets the path to the 'src' folder
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to Market_basket/data/raw/groceries.csv
csv_path = os.path.join(current_dir, "..", "data", "raw", "groceries.csv")

st.set_page_config(page_title="Egypt Retail Insights", layout="wide")
st.title("🛒 Market Basket Recommendation System")

@st.cache_data
def load_data():
    # 2. Check if the file exists before reading
    if not os.path.exists(csv_path):
        st.error(f"❌ File not found at: {csv_path}")
        st.info("Ensure you have pushed 'data/raw/groceries.csv' to your GitHub repository.")
        return pd.DataFrame()
    
    df = pd.read_csv(csv_path)
    
    # 3. Clean string sets back into lists (as done in your notebook)
    if 'antecedents' in df.columns:
        df['antecedents'] = df['antecedents'].apply(lambda x: x.strip("{}").replace("'", "").split(", "))
        df['consequents'] = df['consequents'].apply(lambda x: x.strip("{}").replace("'", "").split(", "))
    return df

rules = load_data()

# Only show the UI if rules were loaded successfully
if not rules.empty:
    st.success("✅ Data loaded successfully from data/raw/groceries.csv")
    
    # Sidebar Filters
    min_confidence = st.sidebar.slider("Minimum Confidence", 0.1, 1.0, 0.3)
    min_lift = st.sidebar.slider("Minimum Lift", 1.0, 5.0, 1.2)

    # Item Selection
    all_items = sorted(list(set([item for sublist in rules['antecedents'] for item in sublist])))
    selected_item = st.selectbox("Select an item in the customer's basket:", all_items)

    if selected_item:
        filtered_rules = rules[
            (rules['antecedents'].apply(lambda x: selected_item in x)) & 
            (rules['confidence'] >= min_confidence) & 
            (rules['lift'] >= min_lift)
        ].sort_values('lift', ascending=False)

        if not filtered_rules.empty:
            st.table(filtered_rules[['consequents', 'confidence', 'lift']].head(5))
        else:
            st.warning("No associations found for this item.")