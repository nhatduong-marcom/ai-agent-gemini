import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# Dùng mô hình nhúng đa ngôn ngữ hỗ trợ tiếng Việt, Anh, Nhật, Trung, v.v.
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

VECTOR_STORE_PATH = "knowledge_base/vector_store"
DATA_FILE = "knowledge_base/faq.txt"

def build_vector_store():
    """
    Tạo FAISS vector store từ file văn bản.
    """
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Không tìm thấy file: {DATA_FILE}")

    loader = TextLoader(DATA_FILE, encoding="utf-8")
    docs = loader.load()

    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(docs)

    store = FAISS.from_documents(chunks, embedding_model)
    store.save_local(VECTOR_STORE_PATH)

    print(f"FAISS vector store đã được lưu tại {VECTOR_STORE_PATH}")
    return store

def load_vector_store():
    """
    Tải lại FAISS vector store từ local.
    """
    index_path = os.path.join(VECTOR_STORE_PATH, "index.faiss")
    if not os.path.exists(index_path):
        raise Exception("❌ Chưa tồn tại vector store. Vui lòng gọi build_vector_store() trước.")
    
    return FAISS.load_local(VECTOR_STORE_PATH, embedding_model)

def get_relevant_docs(query: str, k=3):
    """
    Truy vấn top-k đoạn văn bản liên quan đến query.
    """
    db = load_vector_store()
    docs = db.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
