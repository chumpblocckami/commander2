import json

import streamlit as st

from src.checker import Checker

st.markdown("""# COMMANDER 2
Write a card for each line, then run submit.
    """)

checker = Checker()

cards = st.text_area(label="Insert here your deck",
                     placeholder="Yotian Soldier\nMyr Retriever\nKrark-Clan Ironworks\nTime Sieve")
manual_inserting_button = st.button(label="Check")

if manual_inserting_button:
    if not cards:
        st.error("Please enter some cards!")
    if cards:
        for card in cards.split("\n"):
            result = checker.card_check(card.strip())
            with open("recent_cards.json", "r+") as file:
                file_data = json.load(file)
                file_data.append(result)
                file.seek(0)
                json.dump(file_data, file)
            with st.expander(label=f"{result['label'].capitalize()}"):
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    for title, comment in result["data"].items():
                        st.markdown(f"**{title.capitalize()}**: {comment}")
                with col2:
                    for title, resources in result["resources"].items():
                        st.image(resources, caption=card.strip())

st.divider()
with st.expander(label="Recent searched cards"):
    with open("recent_cards.json", "r") as file:
        recent_cards = json.load(file)
    for recent_card in recent_cards[-10:]:
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            for title, comment in recent_card["data"].items():
                st.markdown(f"**{title.capitalize()}**: {comment}")
        with col2:
            for title, resources in recent_card["resources"].items():
                st.image(resources, caption=recent_card["label"].strip())

st.write("by BojukaPod")
