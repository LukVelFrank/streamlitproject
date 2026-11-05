import streamlit as st

st.title("¡Hola, Streamlit!")
st.write("Esta app corre dentro de mi entorno virtual.")

import pandas as pd


if __name__ == '__main__':

    # First, let's set up the multi index with 2 levels:
    # city and store. We will create an empty frame with some
    # column data (fruits) and pass in the multi index as index.
    # Index names are set for accessing later

    multi_index = pd.MultiIndex.from_product([
        ['city_1', 'city_2'],
        ['store_1', 'store_2', 'store_3'],
    ])
    df = pd.DataFrame(columns=['apples', 'oranges'], index=multi_index)
    df.index.set_names(['city', 'store'], inplace=True)

    # Now let's make some selectboxes for drilling up/down

    levels = [
        st.selectbox('Level 1', ['All'] + [i for i in df.index.get_level_values(0).unique()]),
        st.selectbox('Level 2', ['All'] + [i for i in df.index.get_level_values(1).unique()])
    ]

    # We need to use slice(None) if the user selects 'All'.
    # The specified level with 'All' will take all values in that level.

    for idx, level in enumerate(levels):
        if level == 'All':
            levels[idx] = slice(None)

    # Make a cross section with the level values and pass in the index names.

    st.dataframe(
        df.xs(
            (levels[0], levels[1]),
            level=['city', 'store']
        )
    )

@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")