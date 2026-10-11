# 💬 Part 2, step 2.9: the chat screen. Ask Grandma's trunk anything; every answer comes with its sources.
#
#   streamlit run app.py      → opens "Grandma's Trunk 🧳" in your browser
import os

import streamlit as st

from graph import ask

PREVIEWS = os.path.join(os.path.dirname(__file__), "trunk_maker", "preview")  # page pictures, if you made them with the trunk maker

st.set_page_config(page_title="Grandma's Trunk", page_icon="🧳")
st.title("Grandma's Trunk 🧳")
st.caption("Ask about sixty years of family papers. Every answer shows where it came from.")

if "chat" not in st.session_state:
    st.session_state.chat = []


def show_sources(passages, sources):
    with st.expander(f"📄 Sources ({len(sources)})"):
        for source in sources:
            st.markdown(f"**{source}**")
            picture = os.path.join(PREVIEWS, source.replace(".pdf", ".png"))
            if os.path.exists(picture):
                st.image(picture, width=260)
            for p in passages:
                if p["source"] == source:
                    st.text(p["content"][:600])


for turn in st.session_state.chat:
    with st.chat_message(turn["role"], avatar="🧓" if turn["role"] == "user" else "🤖"):
        st.markdown(turn["text"])
        if turn.get("sources"):
            show_sources(turn["passages"], turn["sources"])

if question := st.chat_input("When did Grandpa move to Mumbai?"):
    st.session_state.chat.append({"role": "user", "text": question})
    with st.chat_message("user", avatar="🧓"):
        st.markdown(question)
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Looking through the trunk…"):
            result = ask(question)
        st.markdown(result["answer"])
        passages = result.get("relevant") or []
        if result.get("sources"):
            show_sources(passages, result["sources"])
    st.session_state.chat.append({"role": "assistant", "text": result["answer"], "sources": result.get("sources"), "passages": passages})
