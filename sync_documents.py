import json
import os

def sync_documents(static_doc_path: str, dynamic_doc_path: str, combined_doc_path: str) -> None:
    static_docs = []
    dynamic_docs = []

    # Load static documents
    if os.path.exists(static_doc_path):
        with open(static_doc_path, 'r') as file:
            static_docs = json.load(file)

    # Load dynamic documents only if the file is not empty
    if os.path.exists(dynamic_doc_path) and os.path.getsize(dynamic_doc_path) > 0:
        with open(dynamic_doc_path, 'r') as file:
            dynamic_docs = json.load(file)

    # Combine static and dynamic documents
    combined_docs = static_docs + dynamic_docs

    # Save combined documents
    with open(combined_doc_path, 'w') as file:
        json.dump(combined_docs, file)

    print(f"Documents successfully synced into {combined_doc_path}.")

# Example call
sync_documents('static_data.json', 'dynamic_data.json', 'combined_documents.json')
