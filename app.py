import streamlit as st
from streamlit_chat import message
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

def get_response(user_input):
    if st.session_state['conversation'] is None:
        llm = OpenAI(
            temperature = 0,
            model_name = "gpt-3.5-turbo"
        )

        st.session_state['conversation'] = ConversationChain(
            llm = llm,
            verbose = True,
            memory = ConversationBufferMemory()
        )

    response = st.session_state['conversation'].predict(input = user_input)
    print(st.session_state['conversation'].memory.buffer)
    
    return response

### Setting page title and header ###
st.set_page_config(
    page_title = "Chat GPT Clone",
    page_icon = ":robot_face:"
    )
st.markdown(
    "<h1 style='text-align: center;'>How can I assist you?</h1>",
    unsafe_allow_html=True    
)

### Setting side bar ###
st.sidebar.title("😎")
api_key = st.sidebar.text_input(
    "What's your API key?",
    type = "password"
)

summarize_button = st.sidebar.button(
    "Summarise the conversation",
    key = "summarize"
)

if summarize_button:
    summarise_placeholder = st.sidebar.write("Summary:\n\n") 
    # summarise_placeholder.write("Summary:\n\n"+ st.session_state['conversation'].memory.buffer)


### Setting container for user input ###
response_container = st.container()
container = st.container()

with container:
    with st.form(
        key="my_form", 
        clear_on_submit = True
    ):
        user_input = st.text_area(
            "Your question goes here", 
            key = 'input',
            height = 100
        )
        submit_button = st.form_submit_button(label = 'Send')
        
        if submit_button:
            answer = get_response(user_input)

            with response_container:
                st.write(answer)
    

import os
os.environ["OPENAI_API_KEY"] = "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"


