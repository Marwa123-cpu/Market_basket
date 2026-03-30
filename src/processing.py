import pandas as pd

def clean_grocery_data(df):
    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    # Add Time Features
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Is_Weekend'] = df['Day_of_Week'].isin(['Saturday', 'Sunday'])
    # Audit
    df = df.drop_duplicates()
    return df