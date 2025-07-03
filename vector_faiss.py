import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def build_vector_store():
    loader = TextLoader("knowledge_base/faq.txt", encoding="utf-8")
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(docs)
    store = FAISS.from_documents(chunks, embedding_model)
    store.save_local("knowledge_base/vector_store")
    return store

def load_vector_store():
    if not os.path.exists("knowledge_base/vector_store/index.faiss"):
        return build_vector_store()
    return FAISS.load_local(
        "knowledge_base/vector_store",
        embedding_model,
        allow_dangerous_deserialization=True  # 👈 thêm dòng này
    )

def get_relevant_docs(query: str, k=3):
    db = load_vector_store()
    docs = db.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
