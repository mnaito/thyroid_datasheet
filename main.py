import streamlit as st
import data_input
import analysis

st.set_page_config(
    page_title='Datasheet for temporal thyroid monitoring',
)

tab1,tab2=st.tabs(['入力','まとめ'])

with tab1:
    date=data_input.data_form()

with tab2:
    analysis.comparison()
