from flask import Flask, render_template, request
import pandas as pd
import os
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

app = Flask(__name__)

# Absolute path to your data
DATA_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "market_basket", "data", "raw", "groceries.csv")

def run_analysis(search_item):
    if not os.path.exists(DATA_PATH):
        return None, "CSV File not found at the specified path."

    # 1. Load Data
    df = pd.read_csv(DATA_PATH)
    
    # 2. Transform: Group by Member and Date to create 'Baskets'
    baskets = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).values.tolist()
    
    # 3. Encode
    te = TransactionEncoder()
    te_ary = te.fit(baskets).transform(baskets)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    # 4. FP-Growth & Rules
    frequent_itemsets = fpgrowth(df_encoded, min_support=0.001, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    # 5. Filter for the searched item
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x))
    
    # Look for the item in the 'if' part of the rule
    filtered_rules = rules[rules['antecedents'].apply(lambda x: search_item.lower() in [i.lower() for i in x])]
    return filtered_rules.sort_values('lift', ascending=False).head(5), None

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error = None
    query = None
    
    if request.method == 'POST':
        query = request.form.get('product_name')
        results, error = run_analysis(query)
        
    return render_template('index.html', results=results, error=error, query=query)

if __name__ == '__main__':
    app.run(port=5000, debug=True)