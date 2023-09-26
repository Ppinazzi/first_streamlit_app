import streamlit
import pandas as pd
import requests
import snowflake.connector


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
selected_fruit_list = streamlit.multiselect(
  "Pick your fruits:", 
  df_fruit_list.index, 
  ['Avocado']
)
# Show the fruit list below the pick up list:
# streamlit.dataframe(df_fruit_list)
streamlit.dataframe(df_fruit_list.loc[selected_fruit_list])

streamlit.header("Suggestion of the week:")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())
streamlit.dataframe(pd.json_normalize(fruityvice_response.json()))
#
streamlit.header("Pick fruit, I'll tellhow it is good!!")
user_choice = streamlit.text_input(
  'What fruit would you like information about?',
  'Kiwi'
)
fruit_request_response = requests.get("https://fruityvice.com/api/fruit/" + user_choice)
streamlit.dataframe(pd.json_normalize(fruit_request_response.json()))

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)
