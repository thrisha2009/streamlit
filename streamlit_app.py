import streamlit as st
from collections import deque
from Chat_Application import *

def chatbot(text):
    
    response = f"Chatbot response to: {text}"
    return response


st.markdown(
    """
    <style>
    body {
        background-image: url('coffee.jpeg');
        background-size: cover;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.image('cafe.png', width=150)
st.title("Café Coffee Day Chatbot")
st.markdown("Get answers to your Café Coffee Day questions")


user_input = st.text_input("Ask a question related to Café Coffee Day", key="user_input")

if user_input:
    
    response = chatbot(user_input)

    
    st.text("Chatbot Response:")
    with st.spinner("Thinking..."):
        st.write(response)


st.sidebar.markdown("Example Questions:")
example_questions = [
    "Hello",
    "List all the spicy items",
    "List all the milk products",
    "List all the cold coffee",
    "List some chicken items",
]

example = st.sidebar.selectbox("Select an example question", example_questions)
if st.button("Use Example"):
    user_input = example


if st.button("Clear", key="clear_button"):
    user_input = ""
    st.balloons()


if st.button("Retry"):
    response = chatbot(user_input)
    st.text("Chatbot Response:")
    st.write(response)

if st.button("Delete Previous"):
    user_input = ""
    st.balloons()


st.sidebar.markdown("Options:")
if st.checkbox("Share"):
    st.write("Share option selected")
if st.checkbox("Debug"):
    st.write("Debug option selected")
