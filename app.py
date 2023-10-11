from io import StringIO

import streamlit as st

from src.checker import Checker
from src.logger import Logger

st.set_page_config(
    layout="wide", page_title="Commander2 - a MTG format by Bojuka Pod", page_icon="🏆"
)

if "default" not in st.session_state:
    st.session_state["default"] = ""

st.markdown("""# COMMANDER 2""")

checker = Checker()
logger = Logger()

uploaded_file = st.file_uploader(label="Upload a decklist")
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    st.session_state["default"] = string_data

cards = st.text_area(
    label="or manually insert cards here",
    value=st.session_state["default"],
    placeholder="Yotian Soldier\nMyr Retriever\nKrark-Clan Ironworks\nTime Sieve",
)

manual_inserting_button = st.button(label="Check")

if manual_inserting_button:
    if not cards:
        st.error("Please enter some cards!")
    if cards:
        parsed_cards = [
            card.strip()
            for card in cards.split("\n")
            if card.strip() is not None and len(card) > 1
        ]
        for card in parsed_cards:
            result = checker.card_check(card.strip())
            logger.log_to_db(result)
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
    recent_cards = logger.log_from_db()
    for recent_card in recent_cards[-10:]:
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            for title, comment in recent_card["data"].items():
                st.markdown(f"**{title.capitalize()}**: {comment}")
        with col2:
            for title, resources in recent_card["resources"].items():
                if resources is not None:
                    st.image(resources, caption=recent_card["label"].strip())

st.write("by BojukaPod")
