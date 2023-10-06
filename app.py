import streamlit as st

from src.checker import Checker

st.markdown("""# COMMANDER 2
    Write a card for each line, then run submit.
    """)

checker = Checker()

cards = st.text_area(label="Insert here your deck", placeholder="Forest\nIsland\nPlains\nWaste")
button = st.button(label="Check")
if button:
    for card in cards.split(","):
        st.markdown(f"{checker.card_check(card).strip()}")

st.write("by BojukaPod")