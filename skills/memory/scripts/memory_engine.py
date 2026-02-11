import argparse, sys, json, os
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

# Initialize DB in project workspace
DB_PATH = "./workspace/.memory_db"
COLLECTION_NAME = "nanobot_memory"

def get_client():
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
    return PersistentClient(path=DB_PATH)

def get_collection(client):
    # Use default embedding function (all-MiniLM-L6-v2) - lightweight and good
    ef = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

def add_memory(text, metadata_json="{}"):
    client = get_client()
    collection = get_collection(client)
    metadata = json.loads(metadata_json)
    
    # ID is hash of text to prevent duplicates
    import hashlib
    mem_id = hashlib.md5(text.encode()).hexdigest()
    
    collection.upsert(
        documents=[text],
        metadatas=[metadata],
        ids=[mem_id]
    )
    print(f"✅ Memory stored: {mem_id}")

def search_memory(query, n_results=5):
    client = get_client()
    collection = get_collection(client)
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    print(json.dumps(results, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Nanobot Semantic Memory Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # ADD command
    add_parser = subparsers.add_parser("add", help="Store text in memory")
    add_parser.add_argument("text", help="Text content to remember")
    add_parser.add_argument("--metadata", default="{}", help="JSON metadata (e.g. project name)")
    
    # SEARCH command
    search_parser = subparsers.add_parser("search", help="Semantic search")
    search_parser.add_argument("query", help="Question or concept to find")
    search_parser.add_argument("-n", type=int, default=3, help="Number of results")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_memory(args.text, args.metadata)
    elif args.command == "search":
        search_memory(args.query, args.n)

if __name__ == "__main__":
    main()
