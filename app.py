import streamlit as st

from src.checker import Checker

st.markdown("""# COMMANDER 2
Write a card for each line, then run submit.
    """)

checker = Checker()

cards = st.text_area(label="Insert here your deck",
                     placeholder="Yotian Soldier\nMyr Retriever\nKrark-Clan Ironworks\nTime Sieve")
button = st.button(label="Check")
if button:
    for card in cards.split("\n"):
        result = checker.card_check(card.strip())
        with st.expander(label=f"{result['label'].capitalize()}"):
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                for title, comment in result["data"].items():
                    st.markdown(f"**{title.capitalize()}**: {comment}")
            with col2:
                for title, resources in result["resources"].items():
                    st.image(resources, caption=card)

st.write("by BojukaPod")
