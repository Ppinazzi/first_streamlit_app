import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# Config 
filepath = "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"

# Helper Functions 
def get_fruit_info(user_fruit_request: str):
  fruit_request_response = requests.get("https://fruityvice.com/api/fruit/" + user_fruit_request)
  return pd.json_normalize(fruit_request_response.json())


def get_data_from_snowflake():
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    query_response = my_cur.fetchall()
  return query_response

def put_data_into_snowflake(fruit_string: str):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{fruit_string}')")
  return f"Thank you for adding {fruit_string}"


##############################################################################

# Main
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
fruit_info = get_fruit_info("watermelon")
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())
# streamlit.dataframe(pd.json_normalize(fruityvice_response.json()))
streamlit.dataframe(fruit_info)

# New section to display the fruityvice response 
streamlit.header("Pick fruit, I'll tell how it is good!!")
try:
  user_choice = streamlit.text_input('What fruit would you like information about?')
  if not user_choice:
    streamlit.error("Please select a fruit")
  else:
    fruit_request_response = get_fruit_info(user_choice)
    streamlit.dataframe(fruit_request_response)
except URLError as e:
  streamlit.error()


# Add a button to load fruit from snowflake database
if streamlit.button('Get Fruit Load List'):
  query_response = get_data_from_snowflake()
  streamlit.text("The fruit load list contains:")
  streamlit.dataframe(query_response)

# Let the user specify a fruit he wants to add to the database
fruit_to_add = streamlit.text_input(
  'What fruit would you like to add?',
  'jackfruit',
)
if streamlit.button("Add fruit to SNFK:"):
  put_data_into_snowflake(fruit_to_add)

my_data_rows = get_data_from_snowflake()
streamlit.dataframe(my_data_rows)
