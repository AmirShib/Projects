import os
# Import OpenAI as main LLM service
from langchain.llms import OpenAI 
from langchain.embeddings import OpenAIEmbeddings

# import streamlit for UI/app interface
import streamlit as st

# Import PDF document loaders to load the pdf file
from langchain.document_loaders import PyPDFLoader
# Import chroma as the vector store 
from langchain.vectorstores import Chroma


# Import vector store toolkit 
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)

# Set APIkey for OpenAI Service
os.environ['OPENAI_API_KEY'] =  "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" #"your_openai_api_key"

# Create instance of OpenAI LLM
llm = OpenAI(
    temperature=0.1, # we use a low temperature so the model will use the pdf file and its own "creativity"
    verbose=True, # set to True to see the progress of the LLM (the chain of thought)
)
# Create instance of OpenAI Embeddings, which will be used to embed the documents
# (i.e. create a numerical representation of textual data)
embeddings = OpenAIEmbeddings()

# load the PDF Document
loader = PyPDFLoader('apple_annual_report.pdf')
# Split pages from pdf 
pages = loader.load_and_split()
# Load documents into vector database (ChromaDB)
store = Chroma.from_documents(pages, embeddings, collection_name='apple_annual_report')

# Create vectorstore info object (type of database optimized for storing documents and their embeddings)
vectorstore_info = VectorStoreInfo(
    name="annual_report",
    description="apple's annual report as a pdf",
    vectorstore=store
)
# Convert the document store into a langchain toolkit
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)


# Add the toolkit to an end-to-end LC
agent= create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    
)

st.title('GPT Annual Report Analysis')
# Create a text input box for the user
prompt = st.text_input('Input your question here')

# If the user hits enter
if prompt:
    # Then pass the prompt to the LLM
    response = agent.run(prompt)
    # return the response from the LLM
    st.write(response)

    # find the relevant pages for the query  
    with st.expander('Document Similarity Search'):
        # Find the relevant pages
        search = store.similarity_search_with_score(prompt) 
        # Write out the first result (most relevant)
        st.write(search[0][0].page_content) 