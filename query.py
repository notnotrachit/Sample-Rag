import streamlit as st
from app import query_images, query_ai


if "messages" not in st.session_state:
    st.session_state.messages = []

if "image" not in st.session_state:
    st.session_state.image = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        print(message)
        try:
            if message["content"][0]["type"] == "image_url":
                st.image(message["content"][0]["image_url"]["url"])
            else:
                st.markdown(message["content"][0]["content"])
        except:
            try:
                st.markdown(message["content"][0]["content"])
            except:
                st.markdown(message["content"])

if prompt := st.chat_input("Ask about any image?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": [{
        "type": "text",
        "content": [
            {
                "type": "text",
                "content": prompt
            }
        ]
    }]})
    if not st.session_state.image:
        response = query_images(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "content": [{
                "type": "image_url",
                "image_url": {
                    "url": response
                }
            }
            ]
        })
        st.session_state.image = True
        with st.chat_message("assistant"):
            st.image(response)
    response = query_ai(st.session_state.messages, prompt)
    st.session_state.messages.append({
        "role": "assistant",
        "content": [{
            "type": "text",
            "content": response
        }]
    })
    with st.chat_message("assistant"):
        st.markdown(response)




