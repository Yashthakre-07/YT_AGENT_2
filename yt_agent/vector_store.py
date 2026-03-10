import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []


def simple_embedding(text):
    # temporary embedding
    return np.random.rand(384).astype("float32")


def add_documents(chunks):
    global documents

    vectors = []

    for chunk in chunks:
        emb = simple_embedding(chunk)
        vectors.append(emb)
        documents.append(chunk)

    vectors = np.array(vectors)
    index.add(vectors)


def search(query, k=5):

    query_vec = np.array([simple_embedding(query)])

    distances, indices = index.search(query_vec, k)

    results = []

    for i in indices[0]:
        if i < len(documents):
            results.append(documents[i])

    return results