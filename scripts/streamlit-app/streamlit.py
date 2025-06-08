
import pandas as pd
import plotly.express as px
from datetime import datetime
import streamlit as st

st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is a playground for you to try Streamlit and have fun. 

    **There's :rainbow[so much] you can build!**asdasdasdasd11
    
    We prepared a few examples for you to get started. Just 222
    click on the buttons above and discover what you can do 
    with Streamlit. asdasdasd
    """
)

if st.button("Send balloons!"):
    st.balloons()
