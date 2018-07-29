import pandas as pd

def pandas_index():
    df = pd.read_csv('data-netflix.csv')
    return df[['title', 'rating']].to_html('templates/a.html')