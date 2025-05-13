from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

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

# Start the conversation
def chat():
    print("Welcome to the Toronto Healthy Restaurant Assistant! Ask me anything. (Type 'q' to exit)")
    while True:
        query = input("\nQuestion: ")
        if query.lower() == 'q':
            print("Ending the conversation. Thank you!")
            break
        
        # Answer the question
        result = qa_chain({"question": query})
        print(f"\nAnswer: {result['answer']}")

if __name__ == "__main__":
    chat()
