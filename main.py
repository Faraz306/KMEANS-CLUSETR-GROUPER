import streamlit as st
from sklearn.cluster import KMeans
import pandas as pd

st.title("YF Grouper")

data = st.file_uploader("Upload a E-commerce .csv file", ['.csv', '.txt'])
if data:
    df = pd.read_csv(data)
    YES = st.button("Do you want to show data?")
    No = st.button("Do you not want to show data?")
    if YES:
        st.table(df)
    else:
        st.success('okay, not showing data')
    input = st.text_input("Enter the Age col name")
    input2 = st.text_input("Enter the money spent col name")
    if input and input2:
        model = KMeans(n_clusters=2)
        # Extract the actual data columns from your dataframe and fill missing gaps
        X = df[[input, input2]].fillna(0)

        model.fit(X)
        df['Group'] = model.labels_

        ranked_df = df.sort_values(by=['Group', input2], ascending=[True, False])
        st.table(ranked_df.head(20))

        # 1. Convert the DataFrame into a CSV text format
        csv_data = ranked_df.to_csv(index=False).encode('utf-8')

        # 2. Pass the converted text data into the download button
        st.download_button(
            label="Download the Updated Version",
            data=csv_data,
            file_name="grouped_ecommerce_data.csv",
            mime="text/csv"
        )