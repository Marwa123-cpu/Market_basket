import streamlit as st
import pandas as pd
import os
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 1. Setup Path
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "data", "raw", "groceries.csv")

st.set_page_config(page_title="Egypt Retail Insights", layout="wide")
st.title("🛒 Market Basket Recommendation System")

@st.cache_data
def get_rules_from_raw():
    if not os.path.exists(csv_path):
        st.error("File not found!")
        return pd.DataFrame()

    # Load the raw data (Member_number, Date, itemDescription)
    df = pd.read_csv(csv_path)
    
    # Preprocessing: Group items by Member and Date to create a 'Basket'
    st.info("Processing raw transactions... please wait.")
    baskets = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).values.tolist()
    
    # One-Hot Encoding
    te = TransactionEncoder()
    te_ary = te.fit(baskets).transform(baskets)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Run FP-Growth
    frequent_itemsets = fpgrowth(df_encoded, min_support=0.001, use_colnames=True)
    
    # Generate Rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    # Clean up rules for display (convert frozensets to lists)
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x))
    
    return rules

# Load the logic
rules = get_rules_from_raw()

if not rules.empty:
    st.sidebar.header("Settings")
    min_conf = st.sidebar.slider("Confidence Threshold", 0.01, 1.0, 0.1)
    
    # Get unique items for dropdown
    all_items = sorted(list(set([item for sublist in rules['antecedents'] for item in sublist])))
    selected_item = st.selectbox("Select an item in the basket:", all_items)

    if selected_item:
        results = rules[
            (rules['antecedents'].apply(lambda x: selected_item in x)) & 
            (rules['confidence'] >= min_conf)
        ].sort_values('lift', ascending=False)

        if not results.empty:
            st.subheader(f"Recommendations for {selected_item}")
            # Format for table display
            display_df = results[['consequents', 'confidence', 'lift']].copy()
            display_df['consequents'] = display_df['consequents'].apply(lambda x: ", ".join(x))
            st.table(display_df.head(10))
        else:
            st.warning("No associations found. Try lowering the Confidence Threshold.")