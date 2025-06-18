import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="Toronto Healthy Restaurant Assistant",
    page_icon="🍽",
    layout="wide"
)

st.title("Toronto Healthy Restaurant Assistant")
st.markdown("Ask me anything about healthy restaurants in Toronto!")

# Initialize chatbot function
@st.cache_resource
def initialize_chatbot():
    """Initialize chatbot - runs only once"""
    # Load the previously created vector database
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory="db", embedding_function=embeddings)
    
    # Set up the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
    
    # Set up conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create conversational retrieval chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True
    )
    
    return qa_chain

# Initialize chatbot
if 'qa_chain' not in st.session_state:
    with st.spinner("Initializing chatbot..."):
        st.session_state.qa_chain = initialize_chatbot()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me anything about healthy restaurants in Toronto!"}
    ]

# Display existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            try:
                # Generate answer using LangChain
                result = st.session_state.qa_chain({"question": prompt})
                response = result['answer']
                
                # Display response
                st.markdown(response)
                
                # Save response to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response
                })
                
            except Exception as e:
                error_msg = f"Sorry, an error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# Sidebar with additional information
with st.sidebar:
    st.header("Information")
    st.markdown("""
    This chatbot provides information about healthy restaurants in Toronto.
    
    **Features:**
    - Restaurant recommendations
    - Menu information  
    - Location and contact details
    - Nutrition information
    """)
    
    # Reset conversation button
    if st.button("Reset Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Ask me anything about healthy restaurants in Toronto!"}
        ]
        # Clear LangChain memory as well
        st.session_state.qa_chain.memory.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Tip**: Ask specific questions to get more accurate answers!")