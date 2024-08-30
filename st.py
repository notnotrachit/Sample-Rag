import streamlit as st

st.title("Image RAG System")




pages = [
    st.Page("query.py", title="Query"),
    st.Page("upload.py", title="Upload Image")
]

pg = st.navigation(pages)
pg.run()
