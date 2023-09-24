ries"import streamlit
import pandas as pd

filepath = "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"

streamlit.header('Breakfast Favorites')

streamlit.text("🥣 Omega 3 & Blueberry Oatmel")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Chicken !!")
streamlit.text("🥑🍞 Avodacdo Toast")

streamlit.header("'🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")
df_fruit_list = pd.read_csv(filepath) 
df_fruit_list = df_fruit_list.set_index('Fruit')
# Let's put a pick list so they can pick the fruit they want to include 
streamlit.multiselect(
  label="Pick your fruits:",
  df_fruit_list.index,
  ['Avocqdo']
)
# Show the fruit list below the pick up list:
streamlit.dataframe(df_fruit_list)
