import joblib, faiss
import numpy as np

# load prebuilt indexes
data = joblib.load("indexes.pkl")
model = data["model"]
process_names = data["process_names"]
index_proc = data["index_proc"]

def search_process(user_input, top_k=5, threshold=0.90):
    query_emb = model.encode([user_input], convert_to_numpy=True)
    faiss.normalize_L2(query_emb)

    D, I = index_proc.search(query_emb, top_k)

    results = []
    for idx, score in zip(I[0], D[0]):
        results.append({
            "process_name": process_names[idx],
            "similarity": round(float(score) * 100, 2)
        })

    if results[0]["similarity"] < threshold * 100:
        print(f"⚠️ No strong match for '{user_input}'. Did you mean:")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['process_name']} ({r['similarity']}%)")
        choice = int(input("Select the correct process number: ")) - 1
        return results[choice]
    else:
        return results[0]
