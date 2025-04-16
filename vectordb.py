from helper import load_summaries_with_metadata, embed_texts, build_documents, build_faiss_index, save_faiss_index, save_documents, load_faiss_index, load_documents, clear_vector_db, bm25_search, faiss_search, brute_force_metadata_search, combine_results
from sentence_transformers import SentenceTransformer

def create_vector_db(summaries, metadata_list, faiss_path, docs_path):
    # Try to load saved DB
    index = load_faiss_index(faiss_path)
    documents = load_documents(docs_path)

    if not documents or index is None:
        # Load new summaries and metadata
        # summaries, metadata_list = load_summaries_with_metadata(jsonl_file)
        # Generate embeddings
        model, embeddings = embed_texts(summaries)
        # Build document objects
        documents = build_documents(summaries, metadata_list, embeddings)
        # Create FAISS index
        index = build_faiss_index(embeddings)

        # Save FAISS index and documents
        save_documents(documents, docs_path)
        save_faiss_index(index, faiss_path)
    else:
        print("✅ Existing vector database loaded successfully.")

def delete_vector_db(faiss_path, docs_path):
    # Delete the stored vector DB (FAISS index and documents)
    clear_vector_db(faiss_path, docs_path)

def search_vector_db(query, model, index, documents, top_k=5):
    # Perform search using BM25, FAISS, and Metadata search
    # bm25_hits = bm25_search(query, documents, top_k)
    faiss_hits = faiss_search(query, model, index, documents, top_k)
    metadata_hits = brute_force_metadata_search(query, documents, top_k)
    # Combine results and return the sorted list
    final_results = combine_results( faiss_hits, metadata_hits)
    return final_results

# if __name__ == "__main__":
#     # Paths for the JSONL file, FAISS index, and document store
#     jsonl_file = "/Users/priyaninagle/sports-chatbot/ingestion/debug_output.jsonl"
#     faiss_path = "faiss_index.index"
#     docs_path = "document_store.json"

#     # Create the vector DB (FAISS index + document store)
#     # create_vector_db(, faiss_path, docs_path)

#     # If you want to delete the vector DB, uncomment the following line:
#     # delete_vector_db(faiss_path, docs_path)

#     # Example of how to use the search function:
#     query = "Which team has the highest goal difference in Bundesliga?"
#     # Load the FAISS index and documents to perform search
#     index = load_faiss_index(faiss_path)
#     documents = load_documents(docs_path)
#     model = SentenceTransformer("all-MiniLM-L6-v2")

#     # Perform search
#     search_results = search_vector_db(query, model, index, documents)
    
#     # Print top results
#     for hit in search_results[:15]:
#         print(f"[Source: {hit['source']} | Distance: {hit.get('distance', '')} | Score: {hit.get('score', '')} | Relevance: {hit.get('relevance', '')}]")
#         print(f"Summary: {hit['summary']}")
#         print(f"Metadata: {hit['metadata']}")
#         print("------")
