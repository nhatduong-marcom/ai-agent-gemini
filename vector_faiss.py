import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# Khởi tạo model nhúng văn bản (Tiếng Việt + Anh)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def build_vector_store():
    """
    Tạo FAISS vector store từ file knowledge_base/faq.txt
    """
    loader = TextLoader("knowledge_base/faq.txt", encoding="utf-8")
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(docs)
    store = FAISS.from_documents(chunks, embedding_model)
    store.save_local("knowledge_base/vector_store")
    return store

def load_vector_store():
    if os.path.exists("knowledge_base/vector_store/index.faiss"):
        return FAISS.load_local("knowledge_base/vector_store", embedding_model)
    else:
        raise Exception("Vector store chưa được build! Hãy chạy build_local trước.")

def get_relevant_docs(query: str, k=3):
    """
    Truy vấn top-k tài liệu liên quan nhất từ FAISS
    """
    db = load_vector_store()
    docs = db.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
