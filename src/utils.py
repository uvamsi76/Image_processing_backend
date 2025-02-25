import pandas as pd

def is_valid(df):
    df=pd.read_json(df)
    return set(df.columns)==set(['short_question', 'short_answer', 'tags', 'label'])