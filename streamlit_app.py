import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")       
    return pandas.json_normalize(fruityvice_response.json())
    
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()

if __name__ == "__main__":

    streamlit.header('🥣 Breakfast Menu')
    streamlit.text(' 🥗 Omega 3 & Blueberry Oatmeal')
    streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
    streamlit.text(' 🥑🍞 Hard-Boiled Free-Range Egg')

    streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
    my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
    my_fruit_list = my_fruit_list.set_index('Fruit')

    # Let's put a pick list here so they can pick the fruit they want to include 
    fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']) # 
    fruits_to_show = my_fruit_list.loc[fruits_selected]

    # Display the table on the page.
    streamlit.dataframe(fruits_to_show)

    streamlit.header("Fruityvice Fruit Advice!")

    try:
        fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
        if not fruit_choice:
            streamlit.error("select a fruit for info.")
        else:
            fruityvice_normalized = get_fruityvice_data(fruit_choice)
            streamlit.dataframe(fruityvice_normalized)

    except URLError as e:
        streamlit.error()


  

    streamlit.header("the fruit load list contains:")

    if streamlit.button("get fruit load list"):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        streamlit.dataframe(my_data_rows)


    streamlit.stop()

    fruit_to_add = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
    streamlit.write('Thanks for adding ', fruit_to_add)

    my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
