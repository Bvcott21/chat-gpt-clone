import streamlit as st
from streamlit_chat import message
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'API_KEY' not in st.session_state:
    st.session_state['API_KEY'] = ''

def get_response(user_input, api_key):
    if st.session_state['conversation'] is None:
        llm = ChatOpenAI(
            temperature = 0,
            openai_api_key = api_key,
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
st.session_state['API_KEY'] = st.sidebar.text_input(
    "What's your API key?",
    type = "password"
)

summarize_button = st.sidebar.button(
    "Summarise the conversation",
    key = "summarize"
)

if summarize_button:
    summarise_placeholder = st.sidebar.write("Summary:\n\n" + st.session_state['conversation'].memory.buffer) 
    #summarise_placeholder.write("Summary:\n\n"+ st.session_state['conversation'].memory.buffer)


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
            st.session_state['messages'].append(user_input)
            model_response = get_response(user_input, st.session_state['API_KEY'])
            st.session_state['messages'].append(model_response)

            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if(i % 2) == 0:
                        message(st.session_state['messages'][i], is_user = True, key = str(i) + '_user')
                    else:
                        message(st.session_state['messages'][i], key=str(i) + "_AI")



