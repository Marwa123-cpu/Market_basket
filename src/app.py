import streamlit as st
import pandas as pd
import os
import ast

# 1. Setup the dynamic path
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "data", "raw", "groceries.csv")

st.set_page_config(page_title="Egypt Retail Insights", layout="wide")
st.title("🛒 Market Basket Recommendation System")

@st.cache_data
def load_data():
    if not os.path.exists(csv_path):
        st.error(f"❌ File not found at: {csv_path}")
        return pd.DataFrame()
    
    df = pd.read_csv(csv_path)
    
    # Check if this is the RULES file or the RAW data file
    if 'antecedents' not in df.columns:
        st.error("⚠️ The CSV exists but it is not the 'Rules' file. Please re-export from your Notebook.")
        return pd.DataFrame()

    # Convert strings like "frozenset({'milk'})" or "{'milk'}" into actual Python lists
    def clean_format(x):
        try:
            # Handle frozenset strings or dictionary-like strings
            if isinstance(x, str):
                if 'frozenset' in x:
                    # Extracts the part inside the parentheses
                    return list(eval(x))
                return list(ast.literal_eval(x))
            return x
        except:
            return x

    df['antecedents'] = df['antecedents'].apply(clean_format)
    df['consequents'] = df['consequents'].apply(clean_format)
    
    return df

rules = load_data()

# 2. Main Logic
if not rules.empty:
    st.sidebar.header("Parameters")
    min_conf = st.sidebar.slider("Minimum Confidence", 0.1, 1.0, 0.2)
    
    # Flatten the antecedents to get a unique list of all items for the dropdown
    all_items = sorted(list(set([item for sublist in rules['antecedents'] for item in sublist])))
    
    selected_item = st.selectbox("What is in the customer's basket?", all_items)

    if selected_item:
        # Filter rules based on the selected item and confidence
        results = rules[
            (rules['antecedents'].apply(lambda x: selected_item in x)) & 
            (rules['confidence'] >= min_conf)
        ].sort_values('lift', ascending=False)

        if not results.empty:
            st.subheader(f"Customers who bought '{selected_item}' also bought:")
            # Clean up the display for the user
            display_df = results[['consequents', 'confidence', 'lift']].copy()
            display_df['consequents'] = display_df['consequents'].apply(lambda x: ", ".join(x))
            st.table(display_df.head(10))
        else:
            st.warning("No strong associations found for this item. Try lowering the Confidence.")