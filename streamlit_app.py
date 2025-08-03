# Import Python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# App title and instructions
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!!")

# Text input for name
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake session
session = get_active_session()

# Get fruit options from the database
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()
fruit_list = [row["FRUIT_NAME"] for row in fruit_df]

# Multiselect with max_selections=5
ingredients_list = st.multiselect(
    "Choose up to five ingredients:",
    fruit_list,
    max_selections=5
)

# Insert logic
if ingredients_list and name_on_order:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string.strip() + """', '""" + name_on_order + """')"""

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")
