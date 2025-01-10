## 1. Ingest PDF Files
# 2. Extract Text from PDF Files and split into small chunks
# 3. Send the chunks to the embedding model
# 4. Save the embeddings to a vector database
# 5. Perform similarity search on the vector database to find similar documents
# 6. retrieve the similar documents and present them to the user
## run pip install -r requirements.txt to install the required packages
import json
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader


## 1. Ingest PDF Files
doc_path = "../data/BOI.pdf"


# Local PDF file uploads
if doc_path:
    loader = UnstructuredPDFLoader(file_path=doc_path)
    data = loader.load()
    print("done loading....")
else:
    print("Upload a PDF file")

# Preview first page
# content = data[0].page_content
# print(content[:100])
# ==== End of PDF Ingestion ====


# ==== Extract Text from PDF Files and Split into Small Chunks ====
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 2. Extract Text from PDF Files and split into small chunks
# Split and chunk
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("done splitting....")

# print(f"Number of chunks: {len(chunks)}")
# print(f"Example chunk: {chunks[0]}")

# ===== Add to vector database ===
import ollama
import subprocess
import psutil

def is_ollama_serve_running():
    """Check if 'ollama serve' is running."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'ollama' in proc.info['cmdline'] and 'serve' in proc.info['cmdline']:
            return True
    return False

def start_ollama_serve():
    """Start 'ollama serve' if it is not running."""
    if not is_ollama_serve_running():
        print("Starting 'ollama serve'...")
        subprocess.Popen(['ollama', 'serve'])
    else:
        print("'ollama serve' is already running.")

# Check and start 'ollama serve'
start_ollama_serve()

# Load the Ollama model
ollama.pull("nomic-embed-text")


# 3. Send the chunks to the embedding model
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
# chroma db : vector database
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="simple-rag",
)
print("done adding to vector database....")


## === Retrieval ===
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever

from langchain_core.runnables      import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser



# set up our model to use
model = "llama3.2"
llm = ChatOllama(model=model)

# a simple technique to generate multiple questions from a single question
#              and then retrieve documents based on those questions,
# getting the best of both worlds.
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""
        You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}
    """,
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),
    llm,
    prompt=QUERY_PROMPT
)
# RAG prompt
template = """
    Answer the question based ONLY on the following context:
    {context}
    Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)


chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# res = chain.invoke(input=("what is the document about?",))
# res = chain.invoke(
#     input=("what are the main points as a business owner I should be aware of?",)
# )
res = chain.invoke(input=("how to report BOI?",))
print(res)
