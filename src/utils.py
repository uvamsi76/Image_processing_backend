import pandas as pd

def is_valid(df):
    df=pd.read_json(df)
    print(df.columns)
    return set(df.columns)==set(['S. No.', 'Product Name', 'Input Image Urls'])