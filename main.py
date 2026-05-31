import streamlit as st
from sklearn.cluster import KMeans
import pandas as pd

st.title("YF Grouper")

data = st.file_uploader("Upload a E-commerce .csv file", ['.csv', '.txt'])

if data:
    df = pd.read_csv(data)

    st.write(df.head())

    input1 = st.text_input("Enter first column name")
    input2 = st.text_input("Enter second column name")

    if input1 and input2:

        # ML Model
        X = df[[input1, input2]].fillna(0)

        model = KMeans(n_clusters=2, random_state=42)
        model.fit(X)

        df['Group'] = model.labels_

        # USER CHOOSES SORT COLUMNS
        sort_columns = st.multiselect(
            "Choose columns to sort",
            df.columns.tolist(),
            default=['Group']
        )

        # USER CHOOSES ORDER
        ascending_list = []

        for col in sort_columns:
            order = st.selectbox(
                f"{col} order",
                ["Ascending", "Descending"]
            )

            ascending_list.append(order == "Ascending")

        # SORT
        ranked_df = df.sort_values(
            by=sort_columns,
            ascending=ascending_list
        )

        st.table(ranked_df.head(20))

        # DOWNLOAD
        csv_data = ranked_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Updated CSV",
            data=csv_data,
            file_name="grouped_data.csv",
            mime="text/csv"
        )